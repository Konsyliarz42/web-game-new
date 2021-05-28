from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required

from ..models import db, User, Colony
from ..forms import RegisterForm, LoginForm
from ..routes_functions import response, get_user, page_not_found, unauthorized

bp = Blueprint('app', __name__)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/home', methods=['GET', 'POST'])
def home():

    # Logout user
    if request.method == 'POST':
        logout_user()
    
    return response('home.html')


@bp.route('/auth', methods=['GET', 'POST'])
def auth():

    r_form = RegisterForm()
    l_form = LoginForm()
    code = 200

    if request.method == 'POST':
        form_name = request.form['form']

        if form_name == 'register' and r_form.validate_on_submit(): # Register new user
            code = 201
            user = User(
                username=r_form.username.data,
                email=r_form.email.data
            )
            user.set_password(r_form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
        elif form_name == 'login' and l_form.validate_on_submit(): # Login user
            user = User.query.filter_by(
                email=l_form.email.data
            ).first()
            login_user(user)
        else:
            code = 400

    return response('auth.html', code,
        r_form=r_form,
        l_form=l_form
    )