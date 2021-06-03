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

    colonies = db.relationship('Colony', backref='owner', lazy='dynamic')

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
        return f"<Resources for {self.colony_id} colony>"

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
    sawmill = db.Column(db.Integer(), default=0)
    quarry = db.Column(db.Integer(), default=0)
    farm = db.Column(db.Integer(), default=0)

    def __repr__(self):
        return f"<Buildings for {self.colony_id} colony>"

    #----------------------------------------------------------------

    def get_buildings(self):

        return {
            'houses': b.Houses(self.houses),
            'sawmill': b.Sawmill(self.sawmill),
            'quarry': b.Quarry(self.quarry),
            'farm': b.Farm(self.farm)
        }

    
    def get_next_buildings(self):

        current_buildings = self.get_buildings()
        current_materials = self.colony.resources.get_resources()
        construction_list = self.colony.construction_list
        construction_limit = 3
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

            if building in construction_list:
                errors.append(('already_construct', None))

            if len(construction_list) >= construction_limit:
                errors.append(('construction_limit', None))

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

    def start_construction(self, construction):

        if self.construction_list:
            construction.start_build = self.construction_list[-1].end_build
        else:
            construction.start_build = datetime.today()

        for material, value in construction.required_materials.items():
            value = getattr(self.resources, material) - value
            setattr(self.resources, material, value)

        self.construction_list = self.construction_list + [construction]
        db.session.add(self.resources)


    def update(self):

        _construction_list = self.construction_list.copy()

        while _construction_list and datetime.today() >= _construction_list[0].end_build:
            key = _construction_list[0].__class__.__name__.lower()
            setattr(self.buildings, key, _construction_list[0].level)
            _construction_list.pop(0)
        
        self.construction_list = _construction_list
        db.session.add(self)
        db.session.commit()
