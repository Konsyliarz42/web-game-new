from datetime import timedelta
from .tool import Tool

# ================ Weapons ================

class Sword(Tool):

    def __init__(self, start_build=None):
        super().__init__(start_build)

        self.name = 'Sword'
        self.time_active = timedelta(hours=1)
        self.required_materials = {
            'wood': 10,
            'iron': 30
        }


class Bow(Tool):

    def __init__(self, start_build=None):
        super().__init__(start_build)

        self.name = 'Bow'
        self.time_active = timedelta(hours=2)
        self.required_materials = {
            'wood': 50,
            'iron': 10
        }


class BattleAxe(Tool):

    def __init__(self, start_build=None):
        super().__init__(start_build)

        self.name = 'Battle axe'
        self.time_active = timedelta(hours=3)
        self.required_materials = {
            'wood': 40,
            'iron': 50
        }

# ================ Common Tools ================

class Saw(Tool):

    def __init__(self, start_build=None):
        super().__init__(start_build)

        self.name = 'Saw'
        self.time_active = timedelta(minutes=45)
        self.required_materials = {
            'wood': 10,
            'iron': 20
        }
        self.benefits = {
            'wood': 20
        }


class Scythe(Tool):

    def __init__(self, start_build=None):
        super().__init__(start_build)

        self.name = 'Scythe'
        self.time_active = timedelta(minutes=30)
        self.required_materials = {
            'wood': 50,
            'iron': 20
        }
        self.benefits = {
            'food': 20
        }


class Pickaxe(Tool):

    def __init__(self, start_build=None):
        super().__init__(start_build)

        self.name = 'Pickaxe'
        self.time_active = timedelta(minutes=50)
        self.required_materials = {
            'wood': 40,
            'iron': 30
        }
        self.benefits = {
            'stone': 20,
            'iron': 10
        }