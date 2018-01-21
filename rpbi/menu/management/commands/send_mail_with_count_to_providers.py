# -*- coding: utf-8 -*-
"""
Пакет для отправки сообщений провайдерам
"""

from django.core.management import BaseCommand

from core.tasks import send_email
from menu.models import Order
from datetime import datetime, timedelta
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from menu.models import DisableDateOrder


class Command(BaseCommand):
    text = _(
        u"Уважаеммая компания {office__place__username}, \n"
        u"Просим Вас принять заказ на {date} в {office__name} \n\n."
        u"В количесве \n"
        u"\t Первое: {first_course},\n"
        u"\t Второе: {second_course},\n"
        u"\t Салат: {salad}\n")

    def handle(self, *args, **options):
        DAY = 1
        day_order = datetime.now()+timedelta(days=DAY)

        is_day_order_exist_in_disabled_date = (
            DisableDateOrder.objects.filter(disabled_date=day_order).exists())

        if is_day_order_exist_in_disabled_date:
            #  Если завтрашнее число, в списке выключенных дат, то
            #  Заказ, за это число не отрпавляется, даже если он существует
            return

        orders = Order.objects.filter(
            order_date=day_order
        ).values(
            'office__place__username',
            'office__name',
            'office__place__email',
        ).annotate(
            first_course=Sum('first_course'),
            second_course=Sum('second_course'),
            salad=Sum('salad')
        )
        # todo: Order by для верности
        for order in orders:
            order = dict(order)
            order['date'] = day_order.strftime(u'%Y-%m-%d')
            send_email.delay(
                order['office__place__email'],
                self.text.format(**order),
                u'Примите заказ'
            )

        # Дважды отправить заказ не получится
        DisableDateOrder(disabled_date=day_order).save()
