import os
from string import ascii_letters, digits

ORIGINAL_URL_MAX_LENGTH = 2048
SHORT_ID_BY_USER_MAX_LENGTH = 16
SHORT_ID_BY_FUNC_MAX_LENGTH = 6
STRING_MIN_LENGTH = 1
VALID_CHARACTERS_FOR_SHORT_ID = ascii_letters + digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')