from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, ValidationError
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from settings import (
    VALID_CHARACTERS_FOR_SHORT_REGEXP,
    ORIGINAL_MAX_LENGTH,
    SHORT_BY_USER_MAX_LENGTH
)
from .models import URLMap

ORIGINAL_LABEL = 'Длинная ссылка'
SHORT_LABEL = 'Ваш вариант короткой ссылки'
SUBMIT_LABEL = 'Создать'


REQUIRED_FIELD = 'Обязательное поле.'
INVALID_ORIGINAL = 'Указана недопустимая оригинальная ссылка'
INVALID_SHORT = (
    'Некорректная короткая ссылка. Допустимы только латинские буквы '
    '(верхнего и нижнего регистра) и цифры (0 - 9).'
)
SHORT_EXISTS = (
    'Предложенный вариант короткой ссылки уже существует.'
)


class URLMapForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LABEL,
        validators=(
            DataRequired(message=REQUIRED_FIELD),
            Length(max=ORIGINAL_MAX_LENGTH),
            URL(message=INVALID_ORIGINAL)
        )
    )
    custom_id = StringField(
        SHORT_LABEL,
        validators=(
            Length(max=SHORT_BY_USER_MAX_LENGTH),
            Regexp(
                VALID_CHARACTERS_FOR_SHORT_REGEXP,
                message=INVALID_SHORT
            ),
            Optional(),
        )
    )
    submit = SubmitField(SUBMIT_LABEL)

    def validate_custom_id(form, field):
        if field.data and URLMap.get(field.data) is not None:
            raise ValidationError(SHORT_EXISTS)
