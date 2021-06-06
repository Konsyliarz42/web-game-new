from flask import Blueprint, request, redirect, url_for, abort
from flask_login import login_required, logout_user

from ..models import db, User, Colony
from ..routes_functions import response, get_user

bp = Blueprint('users', __name__,  url_prefix='/user/<int:user_id>')

@login_required
@bp.route('/profile', methods=['GET', 'POST'])
def profile(user_id):

    user = get_user(user_id)
    code = 200

    if not user:
        return abort(404) # User not found
    elif user != get_user():
        return abort(401)

    if request.method == 'POST':
        form_name = request.form['form']

        # Delete Resources, Buildings and Colony Recods
        if form_name == 'delete_colony':
            colony = Colony.query.filter_by(id=request.form['id']).all()

            if colony:
                colony = colony[0]
                db.session.delete(colony.resources)
                db.session.delete(colony.buildings)
                db.session.delete(colony)
                db.session.commit()
            else:
                code = 400

        # Delete all user data
        if form_name == 'delete_user':
            for colony in user.colonies:
                db.session.delete(colony.resources)
                db.session.delete(colony.buildings)
                db.session.delete(colony)

            logout_user()
            db.session.delete(user)
            db.session.commit()

            return redirect(url_for('app.home'))

    return response('profile.html', code)