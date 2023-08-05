import datetime


def yesterday() -> datetime.date:
    return datetime.date.today() - datetime.timedelta(days=1)
