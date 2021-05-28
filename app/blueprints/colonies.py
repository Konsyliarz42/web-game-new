from flask import Blueprint, request, redirect, url_for
from flask_login import login_required

from ..models import db, Colony, Buildings
from ..forms import CreateColonyForm
from ..routes_functions import response, get_user, page_not_found, unauthorized, get_colony

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
            buildings = Buildings(colony=colony)
            
            db.session.add(colony)
            db.session.add(buildings)
            db.session.commit()
    
            return redirect(url_for('users.profile', user_id=user.id))
        else:
            code = 400

    return response('colony/colony_create.html', code, form=form)


@login_required
@bp.route('/<int:colony_id>/status', methods=['GET'])
def status(colony_id):

    user = get_user()
    colony = get_colony(colony_id)

    if not user or not colony:
        return page_not_found() # User not found or colony not found

    buildings = colony.buildings.get_buildings()

    return response('colony/colony.html', current_colony=colony, buildings=buildings)