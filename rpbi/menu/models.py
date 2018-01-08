# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from core.models import BaseHistoryModel, BaseRBPIUser, Office
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Order(BaseHistoryModel):
    """
    Класс заказов
    """
    ZERO = 0
    customer = models.ForeignKey(
        BaseRBPIUser, verbose_name='user', related_name='customer',
        blank=True, null=True
    )
    order_date = models.DateField()
    office = models.ForeignKey(Office, verbose_name='Office')
    first_course = models.PositiveSmallIntegerField(
        verbose_name='first_course', default=ZERO)
    second_course = models.PositiveSmallIntegerField(
        verbose_name='second_course', default=ZERO)
    salad = models.PositiveSmallIntegerField(
        verbose_name='salad', default=ZERO)

    class Meta:
        permissions = (
            ("can_control_order", "To HR control order"),
        )

    def __unicode__(self):
        return _(u"Заказ от {}. Первое :{} Втотое:{} Салат:{}. "
                 u"На офис {}").format(
            self.customer.username,
            self.first_course,
            self.second_course,
            self.salad,
            self.office.name
        )

