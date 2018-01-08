# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta


def list_day_from_monday_till_friday():
    """
        Список дат текущей недели с пондельника до пятницы.
        Если день субботний или воскресный, то список будет
        для следующей недели.
    """
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    WEEK_LEN = 0

    day_off_week = {
        MONDAY: u'MONDAY',
        TUESDAY: u'TUESDAY',
        WEDNESDAY: u'WEDNESDAY',
        THURSDAY: u'THURSDAY',
        FRIDAY: u'FRIDAY',
    }
    now_time = datetime.now()
    current_day_off_week = datetime.weekday(now_time)
    list_day = []
    if current_day_off_week > FRIDAY:
        WEEK_LEN = 7
    for day_num in day_off_week:
        diff_day = timedelta(days=day_num - current_day_off_week + WEEK_LEN)
        day_string_result = u'{} {}'.format(
            day_off_week[day_num][0:2],
            (now_time + diff_day).strftime(u'%Y-%m-%d'))
        simple_day = u'{}'.format(
            (now_time + diff_day).strftime(u'%Y-%m-%d'))
        list_day.append([day_string_result, simple_day])
    return list_day
