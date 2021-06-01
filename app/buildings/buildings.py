from .building import Building

class Houses(Building):

    def __init__(self, level, start_build=None):
        super().__init__(level, start_build)

        self.name = 'Houses'
        self.production['food'] = 10*self.level
        self.required_materials = {
            'wood': 500 + 250*self.level,
            'stone': 250 + 125*self.level
        }
        self.required_buildings = {
            'houses': self.level - 1,
            'sawmill': self.level
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
            'houses': self.level
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
            'houses': self.level,
            'sawmill': 1 - self.level
        }
        self.remove_trash()


#----------------------------------------------------------------
class Farm(Building):

    def __init__(self, level, start_build=None):
        super().__init__(level, start_build)

        self.name = 'Farm'
        self.production = {
            'food': 500*self.level
        }
        self.required_materials = {
            'wood': 200 + 100*self.level,
            'stone': 200 + 100*self.level
        }
        self.required_buildings = {
            'houses': self.level,
            'sawmill': self.level - 2,
            'quarry': self.level - 3,
        }
        self.remove_trash()