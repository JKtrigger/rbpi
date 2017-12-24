# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from core.models import BaseHistoryModel, BaseUser, BaseRBPIUser, Office
# Create your models here.


class Order(BaseHistoryModel):
    """
    Класс заказов
    """
    ZERO = 0
    is_active = models.BooleanField(
        verbose_name="is active order", default=True
    )
    office = models.ForeignKey(Office, verbose_name='Office')
    first_course = models.PositiveSmallIntegerField(
        verbose_name='first_course', default=ZERO)
    second_course = models.PositiveSmallIntegerField(
        verbose_name='second_course', default=ZERO)
    salad = models.PositiveSmallIntegerField(
        verbose_name='salad', default=ZERO)

    class Meta:
        permissions = (
            ("can control order", "To HR control order"),
        )


class LaunchProvider(BaseUser):
    """
    Класс Поставщиков обедов
    """
    office = models.ForeignKey(Office, verbose_name='name')
    count_first_course = models.PositiveSmallIntegerField()
    count_second_course = models.PositiveSmallIntegerField()
    count_salad = models.PositiveSmallIntegerField()
