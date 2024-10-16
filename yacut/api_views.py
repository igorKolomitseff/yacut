from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage, ShortGenerateError
from .models import URLMap

REQUEST_BODY_IS_MISSING = 'Отсутствует тело запроса'
URL_FIELD_IS_MISSING = '"url" является обязательным полем!'
SHORT_IS_NOT_EXISTING = 'Указанный id не найден'


@app.route('/api/id/', methods=['POST'])
def add_short():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage(REQUEST_BODY_IS_MISSING)
    if 'url' not in data:
        raise InvalidAPIUsage(URL_FIELD_IS_MISSING)
    original = data['url']
    short = data.get('custom_id')
    if URLMap.is_original_valid(original) and URLMap.is_short_valid(short):
        try:
            urlmap = URLMap.create(original=original, short=short)
            return (
                jsonify(urlmap.to_dict('redirect_from_short_view')),
                HTTPStatus.CREATED
            )
        except ShortGenerateError as error:
            raise InvalidAPIUsage(str(error))


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_original(short):
    urlmap = URLMap.get_by_short(short)
    if urlmap is None:
        raise InvalidAPIUsage(
            SHORT_IS_NOT_EXISTING,
            HTTPStatus.NOT_FOUND
        )
    return jsonify({'url': urlmap.original}), HTTPStatus.OK
