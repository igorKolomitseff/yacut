from random import choices

from .models import URLMap
from settings import (
    SHORT_ID_BY_FUNC_MAX_LENGTH,
    VALID_CHARACTERS_FOR_SHORT_ID
)


def is_short_id_present(short_id):
    return URLMap.query.filter_by(short=short_id).first() is not None


def get_unique_short_id():
    while True:
        short_id = ''.join(choices(
            VALID_CHARACTERS_FOR_SHORT_ID,
            k=SHORT_ID_BY_FUNC_MAX_LENGTH
        ))
        if not is_short_id_present(short_id):
            return short_id
