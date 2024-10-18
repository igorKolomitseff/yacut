from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=URLMap.create(
                original=form.original_link.data,
                short=form.custom_id.data,
                from_form=True
            ).get_short_link()
        )
    except URLMap.ShortGenerateError as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_from_short_view(short):
    url_map = URLMap.get(short)
    if not url_map:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
