from flask import render_template, request
from flask_login import current_user
from .models import User, Colony

def get_user(user_id=None):
    """Return current user object or None.\t
    If user_id exist in database return the user object."""

    user = current_user or None

    if user_id:
        user = User.query.filter_by(id=user_id).all() or None

        if user:
            return user[0]

    return user


def get_colony(colony_id=None):
    """Return the current user's first colony object or None.\t
    If colony_id exist in colonies of the user return colony."""
     
    user = current_user or None

    if not user:
        return None

    colonies = user.colonies

    if colony_id:
        colonies = [c for c in colonies if c.id == colony_id]

    if not colonies:
        return None
            
    return colonies[0]


def response(template, http_code=200, **context):
    """Return render template with the default and additional context.\n
    Default context:
    - current_user
    - current_colony (for colonies blueprint)"""

    default_context = {
        'current_user': get_user()
    }

    # Add current colony to the default context
    if 'colony/<int:colony_id>' in str(request.url_rule):
        colony_id = request.view_args['colony_id']
        default_context['current_colony'] = get_colony(colony_id)

    variables = {**default_context, **context}

    return render_template(template, **variables), http_code


def check_tools_permission(colony, forge):
    """Function checks permit on craft all tools."""

    craft = bool(colony.craft)
    tools = colony.resources.get_tools()
    resources = colony.resources.get_resources()
    
    for tool_name, permission in forge.special_data.items():
        if craft:
            forge.special_data.update({tool_name: False})
        elif permission:
            for material, amount in tools[tool_name][2].required_materials.items():
                if resources[material][0] < amount:
                    forge.special_data.update({tool_name: False})
                    break

    return forge.special_data


def check_army_permission(colony, barracks):

    training = bool(colony.training)
    army = colony.army.get_army()
    resources = {**colony.resources.get_resources(), **colony.resources.get_tools()}

    for soldier, permission in barracks.special_data.items():
        if training:
            barracks.special_data.update({soldier: False})
        elif permission:
            for resource, amount in army[soldier][1].required_resources.items():
                if resources[resource][0] < amount:
                    barracks.special_data.update({soldier: False})
                    break

    return barracks.special_data