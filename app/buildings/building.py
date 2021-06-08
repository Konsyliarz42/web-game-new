from datetime import datetime, timedelta

def number_to_time(number):
    """This function changes number in int type to timedelta.\n
    Example:\t
    int(1125) = str(000001125) = timedelta(0:1:12.500000)"""

    text = str(int(number)).rjust(9, '0')
    time = {
        'days': int(text[:2]),
        'hours': int(text[2:4]),
        'minutes': int(text[4:6]),
        'seconds': int(text[6:8]),
        'milliseconds': int(text[8:])*100
    }

    return timedelta(
        days=time['days'],
        hours=time['hours'],
        minutes=time['minutes'],
        seconds=time['seconds'],
        milliseconds=time['milliseconds']
    )


def timedelta_dict(td):
    """Return dict with days, hours,\t
    minutes, seconds and milliseconds."""

    hours = td.seconds//3600
    minutes = td.seconds//60 - hours*60
    seconds = td.seconds - minutes*60 - hours*3600
    milliseconds = td.microseconds//1000

    return {
        'days': td.days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds,
        'milliseconds': milliseconds
    }


class Building():

    def __init__(self, level, start_build=None):

        self.level = level
        self.name = None
        self.production = dict()
        self.required_materials = dict()
        self.required_buildings = dict()
        self.start_build = start_build
        self.special_data = None


    @property
    def time_build(self):
        total_materials = sum(self.required_materials.values())

        return number_to_time(total_materials)

    
    @property
    def end_build(self):
        if self.start_build:
            return self.start_build + self.time_build
        else:
            return datetime.today() + self.time_build


    def __str__(self):
        return f"{self.name} ({self.level} lvl)"


    def __eq__(self, other):
        return self.name == other.name and self.level == other.level

    #----------------------------------------------------------------

    def remove_trash(self):
        """Remove resource from production which are not produced,\t
        remove required building below first level and\t
        remove materials which are not used to build."""

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

    
    def get_json(self):
        """Return data of the object in dictionary."""

        return {
            'level': self.level,
            'name': self.name,
            'production': self.production,
            'required_materials': self.required_materials,
            'required_buildings': self.required_buildings,
            'start_build': self.start_build,
            'time_build': timedelta_dict(self.time_build),
            'end_build': self.end_build.__str__()
        }