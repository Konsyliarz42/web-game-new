from .building import Building

class Warehouse(Building):

    def __init__(self, level, start_build=None):
        super().__init__(level, start_build)

        self.name = 'Warehouse'
        self.special_data = {
            # Limits
            'wood': 4000*self.level,
            'stone': 4000*self.level,
            'food': 4000*self.level,
            'iron': 100*self.level
        }
        self.required_materials = {
            'wood': 500 + 250*self.level,
            'stone': 250 + 125*self.level
        }
        self.required_buildings = {
            'warehouse': self.level - 1,
            'sawmill': self.level - 1,
            'quarry': self.level - 2
        }
        self.remove_trash()


#----------------------------------------------------------------
class Sawmill(Building):

    def __init__(self, level, start_build=None):
        super().__init__(level, start_build)

        self.name = 'Sawmill'
        self.production = {
            'wood': 100*self.level,
            'food': -50*self.level
        }
        self.required_materials = {
            'wood': 100 + 50*self.level,
            'stone': 50 + 25*self.level
        }
        self.required_buildings = {
            'warehouse': self.level
        }
        self.remove_trash()


#----------------------------------------------------------------
class Quarry(Building):

    def __init__(self, level, start_build=None):
        super().__init__(level, start_build)

        self.name = 'Quarry'
        self.production = {
            'stone': 50*self.level,
            'food': -50*self.level
        }
        self.required_materials = {
            'wood': 100 + 50*self.level,
            'stone': 100 + 50*self.level
        }
        self.required_buildings = {
            'warehouse': self.level,
            'sawmill': 1 - self.level
        }
        self.remove_trash()


#----------------------------------------------------------------
class Farm(Building):

    def __init__(self, level, start_build=None):
        super().__init__(level, start_build)

        self.name = 'Farm'
        self.production = {
            'food': 200*self.level
        }
        self.required_materials = {
            'wood': 200 + 100*self.level,
            'stone': 200 + 100*self.level
        }
        self.required_buildings = {
            'warehouse': self.level,
            'sawmill': self.level - 2,
            'quarry': self.level - 3,
        }
        self.remove_trash()


#----------------------------------------------------------------
class Mine(Building):

    def __init__(self, level, start_build=None):
        super().__init__(level, start_build)

        self.name = 'Mine'
        self.production = {
            'iron': 15*self.level,
            'food': -75*self.level
        }
        self.required_materials = {
            'wood': 100 + 100*self.level,
            'stone': 100 + 100*self.level
        }
        self.required_buildings = {
            'warehouse': self.level + 5
        }
        self.remove_trash()


#----------------------------------------------------------------
class Forge(Building):

    def __init__(self, level, start_build=None):
        super().__init__(level, start_build)

        self.name = 'Forge'
        self.special_data = {
            # Craftable weapons
            'sword': self.level > 0,
            'bow': self.level - 3 >= 0, # Above 3 level
            'battle_axe': self.level - 8 >= 0, # Above 8 level
            # Craftable tools
            'saw': self.level > 0,
            'scythe': self.level - 3 >= 0, # Above 3 level
            'pickaxe': self.level - 5 >= 0 # Above 5 level
        }
        self.production = {
            'food': -50*self.level
        }
        self.required_materials = {
            'wood': 100 + 100*self.level,
            'stone': 250 + 250*self.level
        }
        self.required_buildings = {
            'warehouse': self.level + 7,
            'mine': self.level - 1
        }
        self.remove_trash()


#----------------------------------------------------------------
class Barracks(Building):

    def __init__(self, level, start_build=None):
        super().__init__(level, start_build)

        self.name = 'Barracks'
        self.special_data = {
            'swordman': self.level > 0,
            'bowman': self.level - 3 >= 0,
            'axeman': self.level - 5 >= 0
        }
        self.production = {
            'food': -100*self.level
        }
        self.required_materials = {
            'wood': 200 + 200*self.level,
            'stone': 250 + 250*self.level
        }
        self.required_buildings = {
            'warehouse': self.level + 8,
            'forge': self.level - 1
        }
        self.remove_trash()