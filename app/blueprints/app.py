from flask import Blueprint, request, abort
from flask_login import login_user, logout_user, login_required

from ..models import db, User, Colony
from ..forms import RegisterForm, LoginForm
from ..routes_functions import response

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


@login_required
@bp.route('/map')
def game_map():

    regions = [len(Colony.query.filter_by(region=x).all()) for x in range(10)]

    return response('map.html', regions=regions)


@login_required
@bp.route('/map/<int:region>')
def game_map_region(region):

    colonies = Colony.query.filter_by(region=region).all()
    _colonies = [None]*10

    for colony in colonies:
        _colonies[colony.position] = colony

    return response('map_region.html', colonies=_colonies, nr=region)


@login_required
@bp.route('/map/<int:region>/<int:position>')
def game_map_position(region, position):

    colony = Colony.query.filter_by(region=region, position=position).first()

    return response('map_position.html', colony=colony, nr=[region, position])