from flask import render_template
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
    - current_user"""

    default_context = {
        'current_user': get_user()
    }
    variables = {**default_context, **context}

    return render_template(template, **variables), http_code
