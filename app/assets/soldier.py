from datetime import datetime

from .classes_functions import number_to_time, timedelta_dict

class Soldier():

    def __init__(self, start_training=None):

        self.name = None
        self.required_resources = dict()
        self.start_training = start_training
        self.special_data = None
        self.attack = 0
        self.defend = 0


    @property
    def time_training(self):
        total_materials = sum(self.required_resources.values())

        return number_to_time(total_materials)

    
    @property
    def end_training(self):
        if self.start_training:
            return self.start_training + self.time_training
        else:
            return datetime.today() + self.time_training


    def __str__(self):
        return self.name

    #----------------------------------------------------------------
