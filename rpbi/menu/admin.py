# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from menu.models import Order, DisableDateOrder


class AdminOrders(admin.ModelAdmin):
    fields = ('customer', 'order_date', 'office',
              'first_course', 'second_course', 'salad', 'status_name',
              )
    list_display = (
        'order_date', 'customer',
        'office',
        'first_course', 'second_course', 'salad')

    list_filter = (
        'office__name',
        'customer__legal_entity',
        # 'office__offices__name_of_legal',
        'customer'
    )
    date_hierarchy = 'order_date'
    ordering = ('customer', 'office')


# Register your models here.
admin.site.register(Order, AdminOrders)
admin.site.register(DisableDateOrder)
