from datetime import timedelta

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