from datetime import datetime
from random import choices
from re import fullmatch

from flask import url_for

from settings import (
    ORIGINAL_MAX_LENGTH,
    REDIRECT_VIEW_FUNCTION_NAME,
    SHORT_BY_FUNCTION_MAX_LENGTH,
    SHORT_BY_USER_MAX_LENGTH,
    SHORT_GENERATIONS_LIMIT,
    VALID_CHARACTERS_FOR_SHORT,
    VALID_CHARACTERS_FOR_SHORT_REGEXP
)
from . import db

SHORT_NOT_CREATED = (
    'Короткая ссылка не была создана. '
    f'Количество попыток: {SHORT_GENERATIONS_LIMIT}'
)
SHORT_EXISTS = (
    'Предложенный вариант короткой ссылки уже существует.'
)
INVALID_ORIGINAL_LENGTH = (
    'Указана оригинальная ссылка, превышающая допустимую длину: '
    f'{ORIGINAL_MAX_LENGTH}'
)
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

    class ShortGenerateError(Exception):
        pass

    class ValidationError(Exception):
        pass

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
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def get_unique_short():
        for _ in range(SHORT_GENERATIONS_LIMIT):
            short = ''.join(choices(
                VALID_CHARACTERS_FOR_SHORT,
                k=SHORT_BY_FUNCTION_MAX_LENGTH
            ))
            if URLMap.get(short) is None:
                return short
        raise URLMap.ShortGenerateError(SHORT_NOT_CREATED)

    @staticmethod
    def create(original, short, from_form=False):
        if not from_form:
            if len(original) > ORIGINAL_MAX_LENGTH:
                raise URLMap.ValidationError(INVALID_ORIGINAL_LENGTH)
            if (short and (
                len(short) > SHORT_BY_USER_MAX_LENGTH
                or not fullmatch(VALID_CHARACTERS_FOR_SHORT_REGEXP, short)
            )):
                raise URLMap.ValidationError(INVALID_SHORT)
            if short and URLMap.get(short) is not None:
                raise URLMap.ValidationError(SHORT_EXISTS)
        short = short or URLMap.get_unique_short()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
