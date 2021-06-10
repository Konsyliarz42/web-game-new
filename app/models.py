from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from .buildings import buildings as b
from .tools import tools as t

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

    # Materials
    wood = db.Column(db.Float(), default=1000.0)
    wood_production = db.Column(db.Float(), default=0.0)
    wood_limit = db.Column(db.Float(), default=4000.0)

    stone = db.Column(db.Float(), default=1000.0)
    stone_production = db.Column(db.Float(), default=0.0)
    stone_limit = db.Column(db.Float(), default=4000.0)

    food = db.Column(db.Float(), default=1000.0)
    food_production = db.Column(db.Float(), default=0.0)
    food_limit = db.Column(db.Float(), default=4000.0)

    iron = db.Column(db.Float(), default=0.0)
    iron_production = db.Column(db.Float(), default=0.0)
    iron_limit = db.Column(db.Float(), default=0.0)

    # Tools
    saw = db.Column(db.Integer(), default=0)
    saw_limit = db.Column(db.Integer(), default=1)

    scythe = db.Column(db.Integer(), default=0)
    scythe_limit = db.Column(db.Integer(), default=1)

    pickaxe = db.Column(db.Integer(), default=0)
    pickaxe_limit = db.Column(db.Integer(), default=1)

    # Weapons
    sword = db.Column(db.Integer(), default=0)
    sword_limit = db.Column(db.Integer(), default=4)

    bow = db.Column(db.Integer(), default=0)
    bow_limit = db.Column(db.Integer(), default=4)

    battle_axe = db.Column(db.Integer(), default=0)
    battle_axe_limit = db.Column(db.Integer(), default=4)


    def __repr__(self):
        return f"<Resources for {self.colony_id} colony>"

    #----------------------------------------------------------------

    def get_resources(self):
        """Redturn dictionary with tuples of resources.\n
        First position in tuple is rounded current amount,\t
        second position is current production of resource and\t
        third position is limit the resource in warehouse."""

        return {
            'wood': (self.wood, self.wood_production, self.wood_limit),
            'stone': (self.stone, self.stone_production, self.stone_limit),
            'food': (self.food, self.food_production, self.food_limit),
            'iron': (self.iron, self.iron_production, self.iron_limit)
        }


    def get_tools(self):
        """Redturn dictionary with tuples of tools.\n
        First position in tuple is current amount of tool in database,\t
        second position is limit of tool and\t
        third position is the object of tool."""

        return {
            'sword': (self.sword, self.sword_limit, t.Sword()),
            'bow': (self.bow, self.bow_limit, t.Bow()),
            'battle_axe': (self.battle_axe, self.battle_axe_limit, t.BattleAxe()),
            'saw': (self.saw, self.saw_limit, t.Saw()),
            'scythe': (self.scythe, self.scythe_limit, t.Scythe()),
            'pickaxe': (self.pickaxe, self.pickaxe_limit, t.Pickaxe())
        }


class Buildings(db.Model):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    colony_id = db.Column(db.Integer(), db.ForeignKey('colony.id'))

    warehouse = db.Column(db.Integer(), default=1)
    sawmill = db.Column(db.Integer(), default=0)
    quarry = db.Column(db.Integer(), default=0)
    farm = db.Column(db.Integer(), default=0)

    mine = db.Column(db.Integer(), default=0)
    forge = db.Column(db.Integer(), default=0)
    barracks = db.Column(db.Integer(), default=0)

    def __repr__(self):
        return f"<Buildings for {self.colony_id} colony>"

    #----------------------------------------------------------------

    def get_buildings(self):
        """Return dictionary with object of all buildings."""

        return {
            'warehouse': b.Warehouse(self.warehouse),
            'sawmill': b.Sawmill(self.sawmill),
            'quarry': b.Quarry(self.quarry),
            'farm': b.Farm(self.farm),
            'mine': b.Mine(self.mine),
            'forge': b.Forge(self.forge),
            'barracks': b.Barracks(self.barracks)
        }

    
    def get_next_buildings(self):
        """Return dictionary with tuples of next level buildings.\n
        First position of the tuple is object of buildings and\t
        second position are errors in building.\n
        Errors are tuple with key and optional argument why building can't build.\n
        Errors:
        - required_building - (key, name of required building)
        - required_material - (key, name of required material)
        - already_construct - (key, None)
        - construction_limit - (key, None)"""

        current_buildings = self.get_buildings()
        current_materials = self.colony.resources.get_resources()
        construction_list = self.colony.construction_list
        construction_limit = 3
        buildings = {
            'warehouse': b.Warehouse(self.warehouse + 1),
            'sawmill': b.Sawmill(self.sawmill + 1),
            'quarry': b.Quarry(self.quarry + 1),
            'farm': b.Farm(self.farm + 1),
            'mine': b.Mine(self.mine + 1),
            'forge': b.Forge(self.forge + 1),
            'barracks': b.Barracks(self.barracks + 1)
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
    last_update = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    
    construction_list = db.Column(db.PickleType(), default=list())

    craft = db.Column(db.PickleType(), default=None)
    active_tool = db.Column(db.PickleType(), default=None)

    buildings = db.relationship('Buildings', backref='colony', uselist=False)
    resources = db.relationship('Resources', backref='colony', uselist=False)

    def __str__(self):
        return self.name


    def __repr__(self):
        return f"<Colony: {self.name} | ID: {self.id}>"

    
    def __init__(self, name, owner_id):

        self.name = name
        self.owner_id = owner_id

        buildings = Buildings(colony=self)
        resources = Resources(colony=self)

        db.session.add(buildings)
        db.session.add(resources)
    
    #----------------------------------------------------------------

    def start_construction(self, construction):
        """Add building to construction list."""

        if self.construction_list:
            construction.start_build = self.construction_list[-1].end_build
        else:
            construction.start_build = datetime.today()

        for material, value in construction.required_materials.items():
            value = getattr(self.resources, material) - value
            setattr(self.resources, material, value)

        self.construction_list = self.construction_list + [construction]
        db.session.add(self.resources)

    
    def abort_construction(self, construction):
        """Remove building from construction list and return some materials."""

        _construction_list = self.construction_list.copy()
        build_status = 100

        # Calculate build status
        if construction == _construction_list[0]:
            _construction = _construction_list[0]
            build_status = 100*((datetime.today() - _construction.start_build)/_construction.time_build)
            build_status /= len(construction.required_materials)

        # Return materials
        for material, amount in construction.required_materials.items():
            amount /= build_status
            amount += getattr(self.resources, material)
            setattr(self.resources, material, amount)

        _construction_list.remove(construction)

        # Set new times for other constructions
        for index in range(len(_construction_list)):
            if index == 0:
                _construction_list[index].start_build = datetime.today()
            else:
                _construction_list[index].start_build = _construction_list[index - 1].end_build

        self.construction_list = _construction_list

    
    def activate_tool(self, tool):
        """Make tool active form now."""

        name = tool.name.lower()
        amount = getattr(self.resources, name) - 1
        setattr(self.resources, name, amount)

        tool.start_active = datetime.today()
        self.active_tool = tool


    def update(self):
        """Update status of colony.\n
        This function ends of build from construction list,\t
        increase production and adds resources.\n
        This function is used in check request functions!"""

        # End of build
        _construction_list = self.construction_list.copy()

        while _construction_list and datetime.today() >= _construction_list[0].end_build:
            construction = _construction_list[0]
            key = construction.__class__.__name__.lower()
            setattr(self.buildings, key, construction.level)

            # Change limit of resources
            if construction.name == "Warehouse":
                for resource, amount in construction.special_data.items():
                    key = resource + '_limit'
                    setattr(self.resources, key, amount)

            _construction_list.pop(0)
        
        self.construction_list = _construction_list

        # End of craft
        if self.craft and datetime.today() >= self.craft.end_build:
            tool_name = self.craft.name.lower()
            amount = getattr(self.resources, tool_name) + 1
            setattr(self.resources, tool_name, amount)
            self.craft = None

        # End of active tool
        if self.active_tool and datetime.today() > self.active_tool.end_active:
            self.active_tool = None

        # Update current production
        production = dict()

        for building in self.buildings.get_buildings().values():
            for resource, value in building.production.items():
                resource += '_production'
                
                if resource in production:
                    production[resource] += value
                else:
                    production[resource] = value

                # Include tools
                if self.active_tool:
                    _resource = resource[:resource.rfind('_')]

                    if _resource in self.active_tool.benefits:
                        production[resource] += (self.active_tool.benefits[_resource]/100)*production[resource]

                    
        for resource, value in production.items():
            setattr(self.resources, resource, value)

        # Add resources
        if self.last_update + timedelta(minutes=10) <= datetime.today():
            times = (datetime.today() - self.last_update)/timedelta(hours=1)

            for resource in self.resources.get_resources().keys():
                limit = getattr(self.resources, resource + '_limit')
                production = getattr(self.resources, resource + '_production')
                amount = getattr(self.resources, resource) + times*production
                
                if amount < limit:
                    setattr(self.resources, resource, amount)
                else:
                    setattr(self.resources, resource, limit)

            self.last_update = datetime.today()

        # Save update
        db.session.add(self)
        db.session.commit()
