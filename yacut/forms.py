from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp, URL

from settings import (
    ORIGINAL_URL_MAX_LENGTH,
    SHORT_ID_BY_USER_MAX_LENGTH,
    STRING_MIN_LENGTH
)

REQUIRED_FIELD = 'Обязательное поле'
INVALID_ORIGINAL_LINK = 'Некорректная оригинальная ссылка'
INVALID_SHORT_LINK = (
    'Некорректная короткая ссылка. Допустимы только латинские буквы '
    '(верхнего и нижнего регистра) и цифры (0 - 9).'
)


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=(
            DataRequired(message=REQUIRED_FIELD),
            Length(
                min=STRING_MIN_LENGTH,
                max=ORIGINAL_URL_MAX_LENGTH,
            ),
            URL(message=INVALID_ORIGINAL_LINK)
        )
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(
            Length(
                min=STRING_MIN_LENGTH,
                max=SHORT_ID_BY_USER_MAX_LENGTH
            ),
            Regexp(
                '^[A-Za-z0-9]+$',
                message=INVALID_SHORT_LINK
            ),
            Optional()
        )
    )
    submit = SubmitField('Создать')
