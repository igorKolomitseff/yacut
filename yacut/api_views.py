from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap

REQUEST_BODY_IS_MISSING = 'Отсутствует тело запроса'
URL_FIELD_IS_MISSING = '"url" является обязательным полем!'
SHORT_DOES_NOT_EXIST = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_short():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(REQUEST_BODY_IS_MISSING)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_FIELD_IS_MISSING)
    try:
        return jsonify(URLMap.create(
            original=data['url'],
            short=data.get('custom_id')
        ).to_dict()), HTTPStatus.CREATED
    except (URLMap.ValidationError, URLMap.ShortGenerateError) as error:
        raise InvalidAPIUsage(str(error))


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original(short):
    url_map = URLMap.get(short)
    if url_map is None:
        raise InvalidAPIUsage(SHORT_DOES_NOT_EXIST, HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK
