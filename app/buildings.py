class Building():

    def __init__(self, level):

        self.level = level
        self.name = None
        self.production = dict()
        self.required_materials = dict()
        self.required_buildings = dict()

    
    def remove_trash(self):

        # Remove from production all products that are not produced
        for key, value in self.production.copy().items():
            if value == 0:
                self.production.pop(key)

        # Remove all building below level 1 form required buildings
        for key, value in self.required_buildings.copy().items():
            if value <= 0:
                self.required_buildings.pop(key)

        # Remove all materials that are not used to build
        for key, value in self.required_materials.copy().items():
            if value <= 0:
                self.required_materials.pop(key)

#----------------------------------------------------------------

class Houses(Building):

    def __init__(self, level):
        super().__init__(level)

        self.name = 'Houses'
        self.production['food'] = 10*self.level
        self.required_materials = {
            'wood': 500 + 250*self.level,
            'stone': 250 + 125*self.level
        }
        self.required_buildings = {
            'houses': self.level,
            'sawmill': self.level
        }
        self.remove_trash()


class Sawmill(Building):

    def __init__(self, level):
        super().__init__(level)

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
            'houses': 1 - self.level
        }
        self.remove_trash()


class Quarry(Building):

    def __init__(self, level):
        super().__init__(level)

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
            'houses': 1 - self.level,
            'sawmill': 1 - self.level
        }
        self.remove_trash()


class Farm(Building):

    def __init__(self, level):
        super().__init__(level)

        self.name = 'Farm'
        self.production = {
            'food': 500*self.level
        }
        self.required_materials = {
            'wood': 200 + 100*self.level,
            'stone': 200 + 100*self.level
        }
        self.required_buildings = {
            'houses': 1 - self.level,
            'sawmill': self.level - 2,
            'quarry': self.level - 3,
        }
        self.remove_trash()