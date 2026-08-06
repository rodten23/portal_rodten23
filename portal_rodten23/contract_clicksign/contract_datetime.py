import datetime as dt


def create_deadline():
    current_date = dt.date.today()
    zero_hour = dt.time(0, 0, 0, 0)
    future_date = current_date + dt.timedelta(days=30)
    deadline = f'{future_date}T{zero_hour}.000-03:00'

    return {'current_date': current_date, 'deadline': deadline}
