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


def response(template, http_code=200, **context):
    """Return render template with the default and additional context.\n
    Default context:
    - current_user"""

    default_context = {
        'current_user': get_user()
    }
    variables = {**default_context, **context}

    return render_template(template, **variables), http_code


def page_not_found(e=None):
    """Return render '404.html' template with 404 code."""

    return render_template('errors/404.html'), 404


def unauthorized(e=None):
    """Return render '401.html' template with 401 code."""

    return render_template('errors/401.html'), 401