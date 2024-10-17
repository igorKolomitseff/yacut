from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app

from .error_handlers import ShortGenerateError
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        try:
            urlmap = URLMap.create(
                original=form.original_link.data,
                short=form.custom_id.data
            )
            return render_template('index.html', **{
                'form': form,
                'short_url': urlmap.get_short_link()
            })
        except ShortGenerateError as error:
            flash(str(error))
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def redirect_from_short_view(short):
    urlmap = URLMap.get_by_short(short)
    if not urlmap:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(urlmap.original)
