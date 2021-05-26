from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from email_validator import validate_email, EmailNotValidError

from . import models

class AuthMixin(object):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin


    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for("app.home"))


class AdminModel(AuthMixin, ModelView):
    pass


class AdminIndex(AuthMixin, AdminIndexView):
    pass

#--------------------------------

def create_first_admin():
    """Add first admin to the application.\n
    You have enter username (3-128 marks) and password (8-256 marks)."""

    username, email, password = None, None, None
    print("Application does not have administrators!\nCreate new Admin:")

    # Input and validation of username
    while not username:
        username = input("Username: ")

        if len(username) > 128 or len(username) < 3:
            username = None
            print("Wrong username!\n")

    # Input and validation of e-mail
    while not email:
        email = input("Address e-mail: ")

        try:
            validate_email(email)
        except EmailNotValidError:
            email = None
            print("Wrong e-mail!\n")

    # Input and validation of password
    while not password:
        password = input("Password: ")
        confirm_password = input("Confirm password: ")

        if len(password) > 256 or len(password) < 8 or password != confirm_password:
            password = None
            print("Wrong password!\n")

    # Create admin in database
    admin = models.User(
        admin=True,
        username=username,
        email=email
    )
    admin.set_password(password)
    models.db.session.add(admin)
    models.db.session.commit()
    print("\nAdmin has successful added!\n")

#--------------------------------

def admin_views(admin):
    admin.add_view(AdminModel(models.User, models.db.session))
    admin.add_view(AdminModel(models.Colony, models.db.session))
    admin.add_view(AdminModel(models.Buildings, models.db.session))