# Import packages
import datetime as dt

def date_list():
    '''
    Returns:
        date_list: list of dates in format 210101,
        from 970106 (first BIS speech) to today.
    '''

    today = dt.date.today()
    start = dt.date(1997, 1, 6)

    delta = today - start
    date_list = []

    for i in range(delta.days + 1):
        day = start + dt.timedelta(days=i)
        day = day.strftime('%y%m%d')
        date_list.append(day)

    return date_list
