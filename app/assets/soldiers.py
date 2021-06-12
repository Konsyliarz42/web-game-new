from .soldier import Soldier

class Swordman(Soldier):

    def __init__(self, start_build=None):
        super().__init__(start_build)

        self.name = "Swordman"
        self.required_resources = {
            'sword': 1,
            'food': 50
        }
        self.attack = 5
        self.defend = 10


class Bowman(Soldier):

    def __init__(self, start_build=None):
        super().__init__(start_build)

        self.name = "Bowman"
        self.required_resources = {
            'bow': 1,
            'food': 50
        }
        self.attack = 10
        self.defend = 5


class Axeman(Soldier):

    def __init__(self, start_build=None):
        super().__init__(start_build)

        self.name = "Axeman"
        self.required_resources = {
            'battle_axe': 1,
            'food': 50
        }
        self.attack = 20
        self.defend = 5