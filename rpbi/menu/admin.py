# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from menu.models import Order


class AdminOrders(admin.ModelAdmin):
    fields = ('customer', 'order_date', 'office',
              'first_course', 'second_course', 'salad', 'status_name'
              )


# Register your models here.

admin.site.register(Order, AdminOrders)
