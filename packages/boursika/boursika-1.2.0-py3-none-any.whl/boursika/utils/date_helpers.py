from typing import Iterable, Optional

from dateutil import tz
from jdatetime import date as jdate, datetime as jdatetime, timedelta as jtimedelta, time as jtime

_TIMEZONE = tz.gettz('Asia/Tehran')


def get_tehran_timezone():
    return _TIMEZONE


def get_tehran_next_active_day(today: Optional[jdate] = None) -> jdate:
    if not today:
        today = jdatetime.today().date()

    next_day_interval = 1
    current_weekday = today.weekday()
    if current_weekday == 4:
        next_day_interval = 3
    elif current_weekday == 5:
        next_day_interval = 2

    return (get_tehran_end_of_day(today) + jtimedelta(days=next_day_interval)).date()


def get_tehran_prev_active_day(today: Optional[jdate] = None) -> jdate:
    if not today:
        today = jdatetime.today().date()

    prev_day_interval = 1
    current_weekday = today.weekday()
    if current_weekday == 5:
        prev_day_interval = 1
    elif current_weekday == 6:
        prev_day_interval = 2
    elif current_weekday == 0:
        prev_day_interval = 3

    return (get_tehran_end_of_day(today) - jtimedelta(days=prev_day_interval)).date()


def get_tehran_end_of_day(d: jdate) -> jdatetime:
    return jdatetime.combine(d, jtime(23, 59, 59, tzinfo=get_tehran_timezone()))


def jalali_date_range(start_date: jdate, end_date: jdate) -> Iterable[jdate]:
    start_time = get_tehran_end_of_day(start_date)
    end_time = get_tehran_end_of_day(end_date)

    for n in range(int((end_time - start_time).days)):
        yield (start_time + jtimedelta(n)).date()
