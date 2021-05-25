from flask import Blueprint, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

from .models import db, User, Colony
from .routes_functions import response, get_user, page_not_found, unauthorized

bp = Blueprint('users', __name__,  url_prefix='/user/<int:user_id>')

@login_required
@bp.route('/profile', methods=['GET', 'POST'])
def profile(user_id):

    user = get_user(user_id)
    code = 200

    if not user:
        return page_not_found() # User not found
    elif user != get_user():
        return unauthorized()

    if request.method == 'POST':
        form_name = request.form['form']

        if form_name == 'delete_colony':
            colony = Colony.query.filter_by(id=request.form['id']).all()

            if colony:
                db.session.delete(colony[0])
                db.session.commit()
            else:
                code = 400

        if form_name == 'delete_user':
            for colony in user.colonies:
                db.session.delete(colony)

            logout_user()
            db.session.delete(user)
            db.session.commit()

            return redirect(url_for('app.home'))

    return response('profile.html', code)