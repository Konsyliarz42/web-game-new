from flask import Blueprint, render_template, request
from flask_login import login_user, logout_user

from .models import db, User
from .forms import RegisterForm, LoginForm
from .routes_functions import get_user

bp = Blueprint('app', __name__)

@bp.route('/', methods=['GET', 'POST'])
def home():

    r_form = RegisterForm()
    l_form = LoginForm()
    code = 200

    if request.method == 'POST':
        form_name = request.form['form']

        # Register new user
        if form_name == 'register' and r_form.validate_on_submit():
            code = 201
            user = User(
                username=r_form.username.data,
                email=r_form.email.data
            )
            user.set_password(r_form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)

        # Login user
        if form_name == 'login' and l_form.validate_on_submit():
            user = User.query.filter_by(
                email=l_form.email.data
            ).first()
            login_user(user)

        # Logout user
        if form_name == 'logout':
            logout_user()
    
    return render_template('index.html',
        current_user=get_user(),
        users=User.query.all(),
        r_form=r_form,
        l_form=l_form
    ), code