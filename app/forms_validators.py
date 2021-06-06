from wtforms.validators import ValidationError

from .models import User, Colony

class UniqueUsername():

    def __init__(self, message=None):
        self.message = message or "This name is already in our database."

    
    def __call__(self, form, field):
        if field.data in [u.username for u in User.query.all()]:
            raise ValidationError(self.message)


class UniqueEmail():

    def __init__(self, message=None):
        self.message = message or "This e-mail is already in our database."


    def __call__(self, form, field):
        if field.data in [u.email for u in User.query.all()]:
            raise ValidationError(self.message)


class CheckPasswordFromEmail():

    def __init__(self, message=None):
        self.message = message or "Wrong password."


    def __call__(self, form, field):
        user = User.query.filter_by(email=form['email'].data).first()

        if not user or not user.check_password(field.data):
            raise ValidationError(self.message)


class UniqueColony():

    def __init__(self, message=None):
        self.message = message or "This name is already in our database."

    
    def __call__(self, form, field):
        if field.data in [c.name for c in Colony.query.all()]:
            raise ValidationError(self.message)