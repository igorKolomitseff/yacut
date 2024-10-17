from datetime import datetime
from random import choices
from re import fullmatch
from urllib.parse import urlparse

from flask import url_for

from settings import (
    VALID_CHARACTERS_FOR_SHORT,
    VALID_CHARACTERS_FOR_SHORT_REGEXP,
    ORIGINAL_MAX_LENGTH,
    REDIRECT_VIEW_FUNCTION_NAME,
    SHORT_BY_FUNCTION_MAX_LENGTH,
    SHORT_BY_USER_MAX_LENGTH,
    SHORT_GENERATIONS_LIMIT
)
from . import db
from .error_handlers import InvalidAPIUsage, ShortGenerateError

SHORT_NOT_CREATED = 'Короткая ссылка не была создана'
SHORT_EXISTS = (
    'Предложенный вариант короткой ссылки уже существует.'
)
INVALID_ORIGINAL_LENGTH = (
    'Указана оригинальная ссылка, превышающая допустимую длину'
)
INVALID_ORIGINAL = 'Указана недопустимая оригинальная ссылка'
INVALID_SHORT = 'Указано недопустимое имя для короткой ссылки'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_MAX_LENGTH), nullable=False)
    short = db.Column(
        db.String(SHORT_BY_USER_MAX_LENGTH),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.get_short_link()
        )

    def get_short_link(self):
        return url_for(
            REDIRECT_VIEW_FUNCTION_NAME,
            short=self.short,
            _external=True
        )

    @staticmethod
    def get_by_short(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def is_short_exist(short):
        return URLMap.get_by_short(short) is not None

    @staticmethod
    def get_unique_short():
        for _ in range(SHORT_GENERATIONS_LIMIT):
            short = ''.join(choices(
                VALID_CHARACTERS_FOR_SHORT,
                k=SHORT_BY_FUNCTION_MAX_LENGTH
            ))
            if not URLMap.is_short_exist(short):
                return short
        raise ShortGenerateError(SHORT_NOT_CREATED)

    @staticmethod
    def create(original, short):
        short = short or URLMap.get_unique_short()
        urlmap = URLMap(original=original, short=short)
        db.session.add(urlmap)
        db.session.commit()
        return urlmap

    @staticmethod
    def is_original_valid(original):
        if len(original) > ORIGINAL_MAX_LENGTH:
            raise InvalidAPIUsage(INVALID_ORIGINAL_LENGTH)
        original_url_parsed = urlparse(original)
        if not original_url_parsed.scheme and not original_url_parsed.netloc:
            raise InvalidAPIUsage(INVALID_ORIGINAL)
        return True

    @staticmethod
    def is_short_valid(short):
        if not short:
            return True
        if URLMap.is_short_exist(short):
            raise InvalidAPIUsage(SHORT_EXISTS)
        if (
            len(short) > SHORT_BY_USER_MAX_LENGTH
            or not fullmatch(VALID_CHARACTERS_FOR_SHORT_REGEXP, short)
        ):
            raise InvalidAPIUsage(INVALID_SHORT)
        return True
