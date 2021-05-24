from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required

from .models import db, User, Colony
from .forms import RegisterForm, LoginForm
from .routes_functions import response, get_user, page_not_found, unauthorized

bp = Blueprint('app', __name__)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/home', methods=['GET', 'POST'])
def home():
    """Home page of the game.\n
    You can register and login here.\t
    Every else check information about game.\n
    Return code 200 and 201."""

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
    
    return response('home.html', code,
        users=User.query.all(),
        r_form=r_form,
        l_form=l_form
    )


@login_required
@bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):

    user = get_user(user_id)

    if not user:
        return page_not_found() # User not found
    elif user != get_user():
        return unauthorized()

    return response('profile.html')