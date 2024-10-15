from http import HTTPStatus

from flask import jsonify, request

from settings import SHORT_ID_BY_FUNCTION_MAX_LENGTH
from . import app, db
from .validators import validate_data_for_add_short_id
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id

DATA_FIELDS_FOR_ADD_SHORT_ID = ('url', 'custom_id')
SHORT_ID_IS_NOT_EXISTING = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_short_id():
    data = validate_data_for_add_short_id(request.get_json(silent=True))
    data['custom_id'] = (
        data.get('custom_id')
        or get_unique_short_id(SHORT_ID_BY_FUNCTION_MAX_LENGTH)
    )
    urlmap = URLMap()
    urlmap.from_dict(data, DATA_FIELDS_FOR_ADD_SHORT_ID)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict(request.root_url)), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_link(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage(
            SHORT_ID_IS_NOT_EXISTING,
            HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': urlmap.original}), HTTPStatus.OK
