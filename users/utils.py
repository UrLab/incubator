from datetime import datetime


def current_year():
    """ returns """

    now = datetime.today()
    if now.month < 9:
        return now.year - 1
    elif now.month == 9:
        return now.year - 1 if now.day < 15 else now.year
    else:
        return now.year
