# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
import json
from django.core.serializers.json import DjangoJSONEncoder

from core.models import BaseRBPIUser, Office
from menu.models import Order
from datetime import datetime

from core.helpers import list_day_from_monday_till_friday
import re


def submit_order(request):
    post = request.POST
    orders = {}
    for key in post.keys():
        value = post.get(key)
        option = re.compile(
            '((?P<option_menu>[a-z]{5,6})_)?(?P<date>\d{4}-\d{2}-\d{2})'
        )
        result = option.match(key)
        # собираем данные перед сабминитом

        if result:
            option_menu = result.group('option_menu') or 'place'
            date = result.group('date')

            if orders.get(date, None):
                orders[date].update({option_menu: value or 0})
            else:
                orders[date] = {option_menu: value or 0}

    Order.objects.filter(customer=request.user).filter(
        order_date__in=orders.keys()
        ).delete()

    list_to_save_orders = []
    for order in orders:
        if orders.get(order, {}).get('place', None):
            options_to_save = {
                'customer': request.user,
                'user_modifier': request.user,
                'order_date': order,
                'office': Office.objects_active_offices.get(
                    name=orders.get(order, {}).get('place')
                ),
                'first_course': orders.get(order, {}).get('first'),
                'second_course': orders.get(order, {}).get('second'),
                'salad': orders.get(order, {}).get('salad'),
            }
            list_to_save_orders.append(Order(**options_to_save))

    message = {'success': u'lunches successfully ordered'}

    try:
        Order.objects.bulk_create(list_to_save_orders)
    except Exception as err:
        message = {'error': 'unsuccessfully', 'details': err}
    return HttpResponse(
        json.dumps(message),
        content_type="application/json"
    )


class CustomerView(TemplateView):
    """
    View - Для отображения заказов и их оформления на рабочую неделю
    """

    template_name = "menu/menu.html"
    top_text = "Dinners for the whole week!"
    top_text_under_text = "Everyone needs lunch or dinner"
    hello_text = "Hi {}"
    now_day = datetime.now()
    all_locations = Office.objects_active_offices.all()

    def get_context_data(self, **kwargs):
        """

        Изменяем содержание контекста. Автоматически авторизуем пользователей,
        не из числа администраторов, без пароля. Администратором буду выводить
        список пользователей по Юр лицу. Планирую отдельные учетные записи.

        :param kwargs: - словурь контеста
        :return: HTML страницу
        """
        context = super(CustomerView, self).get_context_data(**kwargs)
        context['all_locations'] = self.all_locations
        context['option'] = {}
        context['topText'] = self.top_text
        context['topTextUnderText'] = self.top_text_under_text
        username = context.get('username', None)
        is_group = False
        context['disabled'] = {'disabled': 'disabled'}
        context['date_list'] = list_day_from_monday_till_friday()
        if not username or username == 'None':
            context['username'] = _(
                '<i><abbr title="Most likely you are not logged in.'
                '">Anonymous</abbr> User?</i>'
            )
        else:
            user = BaseRBPIUser.objects_active_users.filter(
                username=username)

            order_week = Order.objects.filter(
                order_date__in=[
                    context['date_list'][0][1],
                    context['date_list'][1][1],
                    context['date_list'][2][1],
                    context['date_list'][3][1],
                    context['date_list'][4][1],
                ]
            ).filter(customer=user).values(
                'first_course',
                'second_course',
                'salad',
                'order_date',
                'office__name'
            )

            for order in order_week:

                context['option'].update({
                    order['order_date'].isoformat(): {
                        'first': order['first_course'],
                        'second': order['second_course'],
                        'salad': order['salad'],
                        'office': json.dumps(
                            order['office__name'], cls=DjangoJSONEncoder
                        )
                    }
                })

            if not user.exists():
                context['username'] = u'{} is non existent user'.format(
                    username
                )
            else:
                context['disabled'] = {'disabled': 'enabled'}
                try:
                    user = user.get()
                except user.multipleobjectsreturned:
                    # TODO : Сделалать обработку сообщений
                    raise_message = _(
                        u'Существуют два имени: {}, ' 
                        u'напишите в службу тех., поддержки ').format(username)
                else:
                    context['is_group'] = user.is_group or is_group
                    context['user'] = username
                if not user.is_admin:
                    login(self.request, user)

        context['helloText'] = self.hello_text.format(context['username'])
        return context
