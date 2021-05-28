from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from .buildings import buildings

db = SQLAlchemy()

class User(db.Model, UserMixin):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    username = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    admin = db.Column(db.Boolean(), nullable=False, default=False)
    register_date = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    colonies = db.relationship('Colony', backref='user', lazy='dynamic')

    def __str__(self):
        return self.username


    def __repr__(self):
        return f"<User: {self.username} | ID: {self.id}>"

    #----------------------------------------------------------------

    def set_password(self, password):
        """Set the password to the user.\n
        This function does not have a validation!\t
        Use after form validation."""

        self.password = generate_password_hash(password, 'sha256')


    def check_password(self, password):
        """Check if password is the same like user password."""

        return check_password_hash(self.password, password)


class Buildings(db.Model):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    colony_id = db.Column(db.Integer(), db.ForeignKey('colony.id'))

    houses = db.Column(db.Integer(), default=1)
    houses_start_build = db.Column(db.DateTime())

    sawmill = db.Column(db.Integer(), default=0)
    sawmill_start_build = db.Column(db.DateTime())

    quarry = db.Column(db.Integer(), default=0)
    quarry_start_build = db.Column(db.DateTime())

    farm = db.Column(db.Integer(), default=0)
    farm_start_build = db.Column(db.DateTime())

    def __repr__(self):
        return f"Buildings for {self.colony_id} colony"

    #----------------------------------------------------------------

    def get_buildings(self):

        return {
            'houses': buildings.Houses(self.houses, self.houses_start_build),
            'sawmill': buildings.Sawmill(self.sawmill, self.sawmill_start_build),
            'quarry': buildings.Quarry(self.quarry, self.quarry_start_build),
            'farm': buildings.Farm(self.farm, self.farm_start_build)
        }


class Colony(db.Model):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    name = db.Column(db.String(128), nullable=False, unique=True)
    create_date = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    buildings = db.relationship('Buildings', backref='colony', uselist=False)

    def __str__(self):
        return self.name


    def __repr__(self):
        return f"<Colony: {self.name} | ID: {self.id}>"
    
    #----------------------------------------------------------------