from datetime import datetime

from . import db
from settings import ORIGINAL_URL_MAX_LENGTH, SHORT_ID_BY_USER_MAX_LENGTH


class URLMap(db.Model):
    REQUIRED_FIELDS = ('original', 'short')

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_URL_MAX_LENGTH), nullable=False)
    short = db.Column(
        db.String(SHORT_ID_BY_USER_MAX_LENGTH),
        unique=True,
        nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())

    def to_dict(self, root_url):
        return dict(
            url=self.original,
            short_link=f'{root_url}{self.short}'
        )

    def from_dict(self, data, data_fields):
        for model_field, data_field in zip(self.REQUIRED_FIELDS, data_fields):
            setattr(self, model_field, data[data_field])
