from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required

from .models import db, User, Colony
from .forms import CreateColonyForm
from .routes_functions import response, get_user, page_not_found, unauthorized

bp = Blueprint('colonies', __name__,  url_prefix='/colony')

@login_required
@bp.route('/create', methods=['GET', 'POST'])
def create():

    user = get_user()
    code = 200

    if not user:
        return page_not_found() # User not found

    form = CreateColonyForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            colony = Colony(
                name=form.name.data,
                owner_id=user.id
            )

            db.session.add(colony)
            db.session.commit()
            code = 201
        else:
            code = 400

    return response('colony/colony_create.html', code, form=form)