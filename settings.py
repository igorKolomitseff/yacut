import os
from string import ascii_letters, digits

ORIGINAL_MAX_LENGTH = 2048
SHORT_BY_USER_MAX_LENGTH = 16
SHORT_BY_FUNCTION_MAX_LENGTH = 6
VALID_CHARACTERS_FOR_SHORT = ascii_letters + digits
VALID_CHARACTERS_FOR_SHORT_REGEXP = f'^[{VALID_CHARACTERS_FOR_SHORT}]+$'
SHORT_GENERATIONS_LIMIT = 1000
REDIRECT_VIEW_FUNCTION_NAME = 'redirect_from_short_view'


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')