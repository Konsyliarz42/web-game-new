from flask_wtf import FlaskForm
from wtforms import fields, validators

from .forms_validators import UniqueUsername, UniqueEmail, CheckPasswordFromEmail

NAMES = {
    'username': "Nazwa użytkownika",
    'password': "Hasło",
    'confirm-password': "Potwierdź hasło",
    'email': "Adres e-mail"
}

MESSAGES = {
    'required': "To pole jest wymagane.",
    'length': "Zawartość musi posiadać minimum {} i nie przekraczać {} znaków.",
    #'length-min': "Zawartość musi posiadać minimum {} znaków.",
    #'length-max': "Zawartość nie może przekraczać {} znaków.",
    'equal': "Zawartość musi być taka sam jak w {}.",
    'unique-username': "Nazwa jest już zajęta.",
    'unique-email': "Email jest już zajęty.",
    'email': "Niepoprawny adres e-mail."
}

# ----------------------------------------------------------------

class RegisterForm(FlaskForm):

    username = fields.StringField(
        label=NAMES['username'],
        validators=[
            validators.DataRequired(MESSAGES['required']),
            validators.Length(3, 128, MESSAGES['length'].format(3, 128)),
            UniqueUsername(MESSAGES['unique-username'])
        ]
    )
    password = fields.PasswordField(
        label=NAMES['password'],
        validators=[
            validators.DataRequired(MESSAGES['required']),
            validators.length(8, 256, MESSAGES['length'].format(8, 256))
        ]
    )
    confirm_password = fields.PasswordField(
        label=NAMES['confirm-password'],
        validators=[
            validators.DataRequired(MESSAGES['required']),
            validators.EqualTo('password', MESSAGES['equal'].format(NAMES['password']))
        ]
    )
    email = fields.StringField(
        label=NAMES['email'],
        validators=[
            validators.DataRequired(MESSAGES['required']),
            validators.Email(MESSAGES['email']),
            UniqueEmail(MESSAGES['unique-email'])
        ]
    )


class LoginForm(FlaskForm):

    email = fields.StringField(
        label=NAMES['email'],
        validators=[
            validators.DataRequired(MESSAGES['required']),
            validators.Email(MESSAGES['email'])
        ]
    )
    password = fields.PasswordField(
        label=NAMES['password'],
        validators=[
            validators.DataRequired(MESSAGES['required']),
            CheckPasswordFromEmail()
        ]
    )