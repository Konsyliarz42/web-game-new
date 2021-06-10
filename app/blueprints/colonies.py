from flask import Blueprint, request, redirect, url_for, abort
from flask_login import login_required
from datetime import datetime

from ..models import db, Colony, Buildings, Resources
from ..forms import CreateColonyForm
from ..routes_functions import response, get_user, get_colony
from ..tools import tools

bp = Blueprint('colonies', __name__,  url_prefix='/colony')

def check_request(colony_id):
    """Check if user or colony exist.\n
    Return three objects: user, colony and result.\t
    Result is abort function when some not exist or user is not authorized.\t
    If colony exist run update method.\t
    After call add condition: if result: return result!"""

    user = get_user()
    colony = get_colony(colony_id)
    result = None

    if not user or not colony:
        result = abort(404)
    elif colony not in user.colonies:
        result = abort(401)
    else:
        colony.update()

    return user, colony, result


@login_required
@bp.route('/create', methods=['GET', 'POST'])
def create():

    user = get_user()
    code = 200

    if not user:
        return abort(404) # User not found

    form = CreateColonyForm()

    # Create colony
    if request.method == 'POST':
        if form.validate_on_submit():
            colony = Colony(
                name=form.name.data,
                owner_id=user.id
            )
            db.session.add(colony)
            db.session.commit()
    
            return redirect(url_for('users.profile', user_id=user.id))
        else:
            code = 400

    return response('colony/create.html', code, form=form)


@login_required
@bp.route('/<int:colony_id>/status', methods=['GET', 'POST'])
def status(colony_id):

    user, colony, result = check_request(colony_id)
    code = 200

    if result:
        return result

    buildings = colony.buildings.get_buildings()
    resources = colony.resources.get_resources()

    # Abort build
    if request.method == 'POST':
        _buildings = colony.buildings.get_next_buildings()
        construction = _buildings[request.form['abort']][0]

        if construction in colony.construction_list:
            colony.abort_construction(construction)
            db.session.add(colony)
            db.session.commit()
        else:
            code = 400

    return response('colony/status.html', code, buildings=buildings, resources=resources)


@login_required
@bp.route('/<int:colony_id>/constructions', methods=['GET', 'POST'])
def constructions(colony_id):

    user, colony, result = check_request(colony_id)
    code = 200

    if result:
        return result

    buildings = colony.buildings.get_next_buildings()

    # Start build
    if request.method == 'POST':
        construction, errors = buildings[request.form['construction']]
        
        if not errors:
            colony.start_construction(construction)
            db.session.add(colony)
            db.session.commit()

            buildings = colony.buildings.get_next_buildings()
            code = 201
        else:
            code = 400

    return response('colony/constructions.html', code, buildings=buildings)


@login_required
@bp.route('/<int:colony_id>/<string:building_name>', methods=['GET', 'POST'])
def building(colony_id, building_name):

    user, colony, result = check_request(colony_id)
    buildings = colony.buildings.get_buildings()
    code = 200

    if result:
        return result
    elif building_name not in buildings.keys():
        return abort(404)

    building = buildings[building_name]        
    building_next, building_errors = colony.buildings.get_next_buildings()[building_name]
    tools = colony.resources.get_tools()

    if request.method == 'POST':
        if building_name == 'warehouse' and not colony.active_tool:
            tool_name = request.form['tool']

            if tools[tool_name][0] > 0:
                colony.activate_tool(tools[tool_name][2])
                db.session.add(colony)
                db.session.commit()
                tools = colony.resources.get_tools()
                code = 201

        if building_name == 'forge' and not colony.craft:
            tool_name = request.form['tool']
            colony.craft = tools[tool_name][2]
            db.session.add(colony)
            db.session.commit()

        code = 400

    return response('colony/building.html', code,
        building=building,
        building_next=building_next,
        building_errors=building_errors,
        special_content=building_name,
        tools=tools
    )