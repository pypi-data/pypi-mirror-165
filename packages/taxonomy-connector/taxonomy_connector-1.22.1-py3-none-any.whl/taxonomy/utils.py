"""
Utils for taxonomy.
"""
import logging
import time
import boto3

from bs4 import BeautifulSoup
from edx_django_utils.cache import get_cache_key, TieredCache

from taxonomy.constants import (
    AMAZON_TRANSLATION_ALLOWED_SIZE,
    AUTO,
    ENGLISH,
    REGION,
    TRANSLATE_SERVICE,
    EMSI_API_RATE_LIMIT_PER_SEC
)
from taxonomy.emsi.client import EMSISkillsApiClient
from taxonomy.exceptions import TaxonomyAPIError
from taxonomy.models import CourseSkills, ProgramSkill, JobSkills, Skill, Translation
from taxonomy.serializers import SkillSerializer

LOGGER = logging.getLogger(__name__)
CACHE_TIMEOUT_COURSE_SKILLS_SECONDS = 60 * 60


def get_whitelisted_serialized_skills(course_key):
    """
    Get a list of serialized course skills.

    Arguments:
        course_key (str): Key of the course whose course skills need to be returned.

    Returns:
        (dict): A dictionary containing the following key-value pairs
            1.  name: 'Skill name'
            2. description: "Skill Description"
    """
    cache_key = get_cache_key(domain='taxonomy', subdomain='course_skills', course_key=course_key)
    cached_response = TieredCache.get_cached_response(cache_key)
    if cached_response.is_found:
        return cached_response.value

    course_skills = get_whitelisted_course_skills(course_key)
    skills = [course_skill.skill for course_skill in course_skills]
    skills_data = SkillSerializer(skills, many=True).data
    TieredCache.set_all_tiers(
        cache_key,
        skills_data,
        django_cache_timeout=CACHE_TIMEOUT_COURSE_SKILLS_SECONDS,
    )
    return skills_data


def get_product_identifier(product_type):
    """
    Return the identifier of a Product Model from Discovery.
    """
    identifier = None
    if product_type == 'Program':
        identifier = 'uuid'
    elif product_type == 'Course':
        identifier = 'key'

    return identifier


def get_product_skill_model_and_identifier(product_type):
    """
    Return the Skill Model along with its identifier based on product type.
    """
    return (ProgramSkill, 'program_uuid') if product_type == 'Program' else (CourseSkills, 'course_key')


def update_skills_data(key_or_uuid, skill_external_id, confidence, skill_data, product_type):
    """
    Persist the skills data in the database either for Program or Course.
    """
    skill, __ = Skill.objects.update_or_create(external_id=skill_external_id, defaults=skill_data)
    skill_model, identifier = get_product_skill_model_and_identifier(product_type)
    kwargs = {
        identifier: key_or_uuid,
        'skill': skill,
        'confidence': confidence
    }
    if not is_skill_blacklisted(key_or_uuid, skill.id, product_type):
        _, created = skill_model.objects.update_or_create(**kwargs)
        action = 'created' if created else 'updated'
        LOGGER.error(f'{skill_model} {action} for key {key_or_uuid}')


def process_skills_data(product, skills, should_commit_to_db, product_type):
    """
    Process skills data returned by the EMSI service and update databased.

    Arguments:
        product (dict): Dictionary containing course or program data whose skills are being processed.
        skills (dict): Course or Program skills data returned by the EMSI API.
        should_commit_to_db (bool): Boolean indicating whether data should be committed to database.
        product_type (str): String indicating about the product type.
    """
    failures = []
    key_or_uuid = get_product_identifier(product_type)
    for record in skills['data']:
        try:
            confidence = float(record['confidence'])
            skill = record['skill']
            skill_external_id = skill['id']
            skill_data = {
                'name': skill['name'],
                'info_url': skill['infoUrl'],
                'type_id': skill['type']['id'],
                'type_name': skill['type']['name'],
                'description': skill['description']
            }
            if should_commit_to_db:
                update_skills_data(
                    product[key_or_uuid], skill_external_id, confidence, skill_data, product_type
                )
        except KeyError:
            message = f'[TAXONOMY] Missing keys in skills data for key: {product[key_or_uuid]}'
            LOGGER.error(message)
            failures.append((product['uuid'], message))
        except (ValueError, TypeError):
            message = f'[TAXONOMY] Invalid type for `confidence` in skills for key: {product[key_or_uuid]}'
            LOGGER.error(message)
            failures.append((product[key_or_uuid], message))
    return failures


def get_translation_attr(product_type):
    """
    Return properties based on product type.
    """
    return 'overview' if product_type == 'Program' else 'full_description'


def refresh_product_skills(products, should_commit_to_db, product_type):
    """
    Refresh the skills associated with the provided products.
    """
    all_failures = []
    success_count = 0
    skipped_count = 0
    skill_extraction_attr, key_or_uuid = get_translation_attr(product_type), get_product_identifier(product_type)

    client = EMSISkillsApiClient()

    for index, product in enumerate(products, start=1):
        skill_attr_val = product[skill_extraction_attr]
        if skill_attr_val:
            translated_skill_attr = get_translated_skill_attribute_val(
                product[key_or_uuid], skill_attr_val, product_type
            )
            try:
                # EMSI only allows 5 requests/sec
                # We need to add one sec delay after every 5 requests to prevent 429 errors
                if index % EMSI_API_RATE_LIMIT_PER_SEC == 0:
                    time.sleep(1)  # sleep for 1 second
                skills = client.get_product_skills(translated_skill_attr)
            except TaxonomyAPIError:
                message = f'[TAXONOMY] API Error for key: {product[key_or_uuid]}'
                LOGGER.error(message)
                all_failures.append((product['uuid'], message))
                continue

            try:
                failures = process_skills_data(product, skills, should_commit_to_db, product_type)
                if failures:
                    LOGGER.info('[TAXONOMY] Skills data received from EMSI. Skills: [%s]', skills)
                    all_failures += failures
                else:
                    success_count += 1
            except Exception as ex:  # pylint: disable=broad-except
                LOGGER.info('[TAXONOMY] Skills data received from EMSI. Skills: [%s]', skills)
                message = f'[TAXONOMY] Exception for key: {product[key_or_uuid]} Error: {ex}'
                LOGGER.error(message)
                all_failures.append((product[key_or_uuid], message))
        else:
            skipped_count += 1

    LOGGER.info(
        '[TAXONOMY] Refresh %s skills process completed. \n'
        'Failures: %s \n'
        'Total %s Updated Successfully: %s \n'
        'Total %s Skipped: %s \n'
        'Total Failures: %s \n',
        product_type,
        all_failures,
        product_type,
        success_count,
        product_type,
        skipped_count,
        len(all_failures),
    )


def blacklist_course_skill(course_key, skill_id):
    """
    Blacklist a course skill.

    Arguments:
        course_key (CourseKey): CourseKey object pointing to the course whose skill need to be black-listed.
        skill_id (int): Primary key identifier of the skill that need to be blacklisted.
    """
    CourseSkills.objects.filter(
        course_key=course_key,
        skill_id=skill_id,
    ).update(is_blacklisted=True)


def remove_course_skill_from_blacklist(course_key, skill_id):
    """
    Remove a course skill from the blacklist.

    Arguments:
        course_key (CourseKey): CourseKey object pointing to the course whose skill need to be black-listed.
        skill_id (int): Primary key identifier of the skill that need to be blacklisted.
    """
    CourseSkills.objects.filter(
        course_key=course_key,
        skill_id=skill_id,
    ).update(is_blacklisted=False)


def is_skill_blacklisted(key_or_uuid, skill_id, product_type):
    """
    Return the black listed status of a course or program skill.

    Arguments:
        key_or_uuid: CourseKey or ProgramUUID object pointing to the course or program whose skill need to be checked.
        skill_id (int): Primary key identifier of the skill that need to be checked.
        is_programs(bool): Boolean indicating which Skill Model would be selected.

    Returns:
        (bool): True if skill (identified by the arguments) is black-listed, False otherwise.
    """
    skill_model, identifier = get_product_skill_model_and_identifier(product_type)
    kwargs = {
        identifier: key_or_uuid,
        'skill_id': skill_id,
        'is_blacklisted': True
    }
    return skill_model.objects.filter(**kwargs).exists()


def get_whitelisted_course_skills(course_key, prefetch_skills=True):
    """
    Get all the course skills that are not blacklisted.

    Arguments:
        course_key (str): Key of the course whose course skills need to be returned.
        prefetch_skills (bool): If True, Prefetch related skills in a single query using Django's select_related.

    Returns:
        (list<CourseSkills>): A list of all the course skills that are not blacklisted.
    """
    qs = CourseSkills.objects.filter(course_key=course_key, is_blacklisted=False)
    if prefetch_skills:
        qs = qs.select_related('skill')
    return qs.all()


def get_blacklisted_course_skills(course_key, prefetch_skills=True):
    """
    Get all the blacklisted course skills.

    Arguments:
        course_key (str): Key of the course whose course skills need to be returned.
        prefetch_skills (bool): If True, Prefetch related skills in a single query using Django's select_related.

    Returns:
        (list<CourseSkills>): A list of all the course skills that are blacklisted.
    """
    qs = CourseSkills.objects.filter(course_key=course_key, is_blacklisted=True)
    if prefetch_skills:
        qs = qs.select_related('skill')
    return qs.all()


def get_course_jobs(course_key):
    """
    Get data for all course jobs.

    Arguments:
        course_key (str): Key of the course whose course skills need to be returned.

    Returns:
        list: A list of dicts where each dict contain information about a particular job.
    """
    course_skills = get_whitelisted_course_skills(course_key)
    job_skills = JobSkills.objects.select_related(
        'skill',
        'job',
        'job__jobpostings',
    ).filter(
        skill__in=[course_skill.skill for course_skill in course_skills]
    )
    data = []
    for job_skill in job_skills:
        job_posting = job_skill.job.jobpostings_set.first()
        data.append(
            {
                'name': job_skill.job.name,
                'median_salary': job_posting.median_salary,
                'unique_postings': job_posting.unique_postings,
            }
        )
    return data


def get_translated_skill_attribute_val(key_or_uuid, skill_attr_val, product_type):
    """
    Return translated skill attribute value either for a course or a program.

    Create translation for provided skill attribute if translation object doesn't already exist.
     OR update translation if skill attribute changed from previous description in translation and
      return the translated skill attribute.

    Arguments:
        key_or_uuid (str): Key or uuid of the course or program needs to be translated.
        skill_attr_val (str): Value of the skill attribute that needs to be translated.
        product_type (str):

    Returns:
        str: Translated skill attribute value.
    """
    source_model_name, source_model_field = product_type, get_translation_attr(product_type)

    translation = Translation.objects.filter(
        source_model_name=source_model_name,
        source_model_field=source_model_field,
        source_record_identifier=key_or_uuid
    ).first()
    if translation:
        if translation.source_text != skill_attr_val:
            if (len(skill_attr_val.encode('utf-8'))) < AMAZON_TRANSLATION_ALLOWED_SIZE:
                result = translate_text(key_or_uuid, skill_attr_val, AUTO, ENGLISH)
            else:
                result = apply_batching_to_translate_large_text(key_or_uuid, skill_attr_val)
            if not result['TranslatedText']:
                return skill_attr_val
            if result['SourceLanguageCode'] == ENGLISH:
                translation.translated_text = skill_attr_val
            else:
                translation.translated_text = result['TranslatedText']
            LOGGER.info(f'[TAXONOMY] Translate {product_type} updated for key: {key_or_uuid}')
            translation.source_text = skill_attr_val
            translation.source_language = result['SourceLanguageCode']
            translation.save()
        return translation.translated_text
    if (len(skill_attr_val.encode('utf-8'))) < AMAZON_TRANSLATION_ALLOWED_SIZE:
        result = translate_text(key_or_uuid, skill_attr_val, AUTO, ENGLISH)
    else:
        result = apply_batching_to_translate_large_text(key_or_uuid, skill_attr_val)
    if not result['TranslatedText']:
        return skill_attr_val
    if result['SourceLanguageCode'] == ENGLISH:
        translated_text = skill_attr_val
    else:
        translated_text = result['TranslatedText']

    translation = Translation.objects.create(
        source_model_name=source_model_name,
        source_model_field=source_model_field,
        source_record_identifier=key_or_uuid,
        source_text=skill_attr_val,
        translated_text=translated_text,
        translated_text_language=ENGLISH,
        source_language=result['SourceLanguageCode'],
    )
    LOGGER.info(f'[TAXONOMY] Translate {product_type} created for key: {key_or_uuid}')
    return translation.translated_text


def translate_text(key, text, source_language, target_language):
    """
    Translate text into the target language.

    Arguments:
        key (str): Key or id of the object to uniquely identify.
        text (str): Text which needs to be translated.
        source_language (str): Source Language of text if known otherwise provide auto.
        target_language (str): Desired language in which text needs to be converted.

    Returns:
        dict: Translated object which contains TranslatedText, SourceLanguageCode and TargetLanguageCode.
    """
    translate = boto3.client(service_name=TRANSLATE_SERVICE, region_name=REGION)

    result = {'SourceLanguageCode': '', 'TranslatedText': ''}
    try:
        result = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language,
        )
    except Exception as ex:  # pylint: disable=broad-except
        message = f'[TAXONOMY] Translate (course description or program overview) exception for key: {key} Error: {ex}'
        LOGGER.exception(message)

    return result


def apply_batching_to_translate_large_text(key, source_text):
    """
    Apply batching if text to translate is large and then combine it again.

    Arguments:
        key (str): Key or id of the object to uniquely identify.
        source_text (str): Text which needs to be translated.

    Returns:
        dict: Translated object which contains TranslatedText and SourceLanguageCode.
    """
    soup = BeautifulSoup(source_text, 'html.parser')
    # Split input text into a list of sentences on the basis of html tags
    sentences = soup.findAll()
    translated_text = ''
    source_text_chunk = ''
    result = {}
    source_language_code = ''
    LOGGER.info(f'[TAXONOMY] Translate (course description or program overview) applying batching for key: {key}')

    for sentence in sentences:
        # Translate expects utf-8 encoded input to be no more than
        # 5000 bytes, so we’ll split on the 5000th byte.

        if len(sentence.encode('utf-8')) + len(source_text_chunk.encode('utf-8')) < AMAZON_TRANSLATION_ALLOWED_SIZE:
            source_text_chunk = '%s%s' % (source_text_chunk, sentence)
        else:
            translation_chunk = translate_text(key, source_text_chunk, AUTO, ENGLISH)
            translated_text = translated_text + translation_chunk['TranslatedText']
            source_text_chunk = sentence
            source_language_code = translation_chunk['SourceLanguageCode']

    # Translate the final chunk of input text
    if source_text_chunk:
        translation_chunk = translate_text(key, source_text_chunk, AUTO, ENGLISH)
        translated_text = translated_text + translation_chunk['TranslatedText']
        source_language_code = translation_chunk['SourceLanguageCode']
    # bs4 adds /r/n which needs to be removed for consistency.
    translated_text = translated_text.replace('\r', '').replace('\n', '')
    result['TranslatedText'] = translated_text
    result['SourceLanguageCode'] = source_language_code
    return result
