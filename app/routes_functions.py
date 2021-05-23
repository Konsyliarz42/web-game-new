from flask_login import current_user
from .models import User

def get_user(user_id=None):
    """Return current user object or None.\t
    If user_id exist in database return the user object."""

    user = current_user or None

    if user_id:
        user = User.query.filter_by(id=user_id).all() or None

        if user:
            return user[0]

    return user