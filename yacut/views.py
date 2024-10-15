from flask import flash, render_template, redirect, request

from . import app, db

from settings import SHORT_ID_BY_FUNCTION_MAX_LENGTH
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id, is_short_id_present


SHORT_ID_IS_EXISTING = (
    'Предложенный вариант короткой ссылки уже существует.'
)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if short_id and is_short_id_present(short_id):
            flash(SHORT_ID_IS_EXISTING)
            return render_template('index.html', form=form)
        short_id = short_id or get_unique_short_id(
            SHORT_ID_BY_FUNCTION_MAX_LENGTH
        )
        urlmap = URLMap(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(urlmap)
        db.session.commit()
        return render_template('index.html', **{
            'form': form,
            'short_url': f'{request.root_url}{short_id}'
        })
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def short_url_redirect_view(short_id):
    return redirect(
        URLMap.query.filter_by(short=short_id).first_or_404().original
    )
