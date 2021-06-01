from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from .buildings import buildings as b

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


class Resources(db.Model):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    colony_id = db.Column(db.Integer(), db.ForeignKey('colony.id'))

    wood = db.Column(db.Float(), default=1000.0)
    wood_production = db.Column(db.Float(), default=0.0)

    stone = db.Column(db.Float(), default=1000.0)
    stone_production = db.Column(db.Float(), default=0.0)

    food = db.Column(db.Float(), default=1000.0)
    food_production = db.Column(db.Float(), default=0.0)

    def __repr__(self):
        return f"Resources for {self.colony_id} colony"

    #----------------------------------------------------------------

    def get_resources(self):

        return {
            'wood': (round(self.wood), self.wood_production),
            'stone': (round(self.stone), self.stone_production),
            'food': (round(self.food), self.food_production)
        }


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
            'houses': b.Houses(self.houses, self.houses_start_build),
            'sawmill': b.Sawmill(self.sawmill, self.sawmill_start_build),
            'quarry': b.Quarry(self.quarry, self.quarry_start_build),
            'farm': b.Farm(self.farm, self.farm_start_build)
        }

    
    def get_next_buildings(self):

        current_buildings = self.get_buildings()
        current_materials = self.colony.resources.get_resources()
        buildings = {
            'houses': b.Houses(self.houses + 1),
            'sawmill': b.Sawmill(self.sawmill + 1),
            'quarry': b.Quarry(self.quarry + 1),
            'farm': b.Farm(self.farm + 1)
        }

        for key, building in buildings.items():
            errors = list()

            # Require building error
            for name, required_level in building.required_buildings.items():
                if current_buildings[name].level < required_level:
                    errors.append(('required_building', name))

            # Require material error
            for name, required_value in building.required_materials.items():
                if current_materials[name][0] < required_value:
                    errors.append(('required_material', name))

            #print(key, errors)
            buildings[key] = (building, errors)
        
        return buildings


class Colony(db.Model):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    name = db.Column(db.String(128), nullable=False, unique=True)
    create_date = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    
    construction_list = db.Column(db.PickleType(), default=list())

    buildings = db.relationship('Buildings', backref='colony', uselist=False)
    resources = db.relationship('Resources', backref='colony', uselist=False)

    def __str__(self):
        return self.name


    def __repr__(self):
        return f"<Colony: {self.name} | ID: {self.id}>"
    
    #----------------------------------------------------------------
