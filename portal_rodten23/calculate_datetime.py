from datetime import date, time, timedelta


def calculate_age(current_date, year_birth, month_birth, day_birth):
    count_in_days = current_date - date(
        int(year_birth), int(month_birth), int(day_birth)
    )
    division_into_years = int(count_in_days.days / 365)
    leap_years = int(division_into_years / 4)
    difference = count_in_days.days - leap_years
    age = int(difference / 365)

    return age


def create_deadline():
    current_date = date.today()
    zero_hour = time(0, 0, 0, 0)
    future_date = current_date + timedelta(days=30)
    deadline = f'{future_date}T{zero_hour}.000-03:00'

    return {'current_date': current_date, 'deadline': deadline}
