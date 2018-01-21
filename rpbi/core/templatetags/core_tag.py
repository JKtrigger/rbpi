# -*- coding: utf-8 -*-

from django import template
from datetime import datetime

register = template.Library()


@register.filter(name='split_and_get_second')
def split_and_get_second(value, separator):
    """
    Разделить значение на части по separator
    и вернуть второе значение
    """
    return value.split(separator)[1]


# TODO: DRY IT

@register.filter(name='get_by_day')
def get_by_day(value, args):
    args = args.split('_')
    if isinstance(value, dict):
        selected = value.get(args[0], {}).get(args[1], None)
        return u'selected' if selected else u''


@register.filter(name='get_by_day_checked')
def get_by_day_checked(value, args):
    args = args.split('_')
    if isinstance(value, dict):
        checked = value.get(args[0], {}).get(args[1], None)
        return u'checked' if checked else u''


@register.filter(name='if_option_checked_return_one')
def if_option_checked_return_one(value, args):
    args = args.split('_')
    if isinstance(value, dict):
        one = value.get(args[0], {}).get(args[1], None)
        return 1 if one is not None else 0


@register.filter(name='return_offices')
def return_offices(value_dict):
    res = {}
    for day in value_dict:
        office = value_dict.get(day, {}).get(u'office', None)
        res[day] = office
    return res


@register.filter(name='in_list_disabled')
def in_list_disabled(value, list_):
    u"""
    Проверить значение из списка и вернуть disabled, если в списке
    """
    return 'disabled' if value in list_ else ''
