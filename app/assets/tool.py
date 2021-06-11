from datetime import datetime

from .classes_functions import number_to_time

class Tool():

    def __init__(self, start_build=None):

        self.name = None
        self.required_materials = dict()
        self.start_build = start_build
        self.start_active = None
        self.time_active = None
        self.benefits = dict()


    @property
    def time_build(self):
        total_materials = sum(self.required_materials.values())*1000

        return number_to_time(total_materials)

    
    @property
    def end_build(self):
        if self.start_build:
            return self.start_build + self.time_build
        else:
            return datetime.today() + self.time_build


    @property
    def end_active(self):
        if self.start_active and self.time_active:
            return self.start_active + self.time_active

        return None

    
    def __str__(self):
        return self.name
    
    #----------------------------------------------------------------
