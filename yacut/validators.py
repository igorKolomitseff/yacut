from re import fullmatch
from urllib.parse import urlparse

from settings import (
    ORIGINAL_URL_MAX_LENGTH,
    SHORT_ID_BY_USER_MAX_LENGTH,
    STRING_MIN_LENGTH
)
from .error_handlers import InvalidAPIUsage
from .utils import is_short_id_present

REQUEST_BODY_IS_MISSING = 'Отсутствует тело запроса'
URL_FIELD_IS_MISSING = '"url" является обязательным полем!'
INVALID_ORIGINAL_URL_LENGTH = (
    'Недопустимая длина оригинальной ссылки. '
    f'Значение должно быть в пределах от {STRING_MIN_LENGTH} до '
    f'{ORIGINAL_URL_MAX_LENGTH} символов'
)
INVALID_ORIGINAL_LINK = 'Указана недопустимая оригинальная ссылка'
SHORT_ID_IS_EXISTING = (
    'Предложенный вариант короткой ссылки уже существует.'
)
INVALID_SHORT_ID = 'Указано недопустимое имя для короткой ссылки'


def validate_data_for_add_short_id(data):
    if data is None:
        raise InvalidAPIUsage(REQUEST_BODY_IS_MISSING)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_FIELD_IS_MISSING)

    original_url = data['url']
    if (
        len(original_url) < STRING_MIN_LENGTH
        or len(original_url) > ORIGINAL_URL_MAX_LENGTH
    ):
        raise InvalidAPIUsage(INVALID_ORIGINAL_URL_LENGTH)
    original_url_parsed = urlparse(original_url)
    if not original_url_parsed.scheme and not original_url_parsed.netloc:
        raise InvalidAPIUsage(INVALID_ORIGINAL_LINK)

    if not data.get('custom_id'):
        return data
    custom_id = data['custom_id']
    if is_short_id_present(custom_id):
        raise InvalidAPIUsage(SHORT_ID_IS_EXISTING)
    if (
        len(custom_id) > SHORT_ID_BY_USER_MAX_LENGTH
        or not fullmatch('^[A-Za-z0-9]+$', custom_id)
    ):
        raise InvalidAPIUsage(INVALID_SHORT_ID)
    return data