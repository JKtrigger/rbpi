# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from core.models import (
    BaseRBPIUser, MessagesHistory, LegalEntity, Office)
from menu.models import Order, LaunchProvider

# Register your models here.
admin.site.register(BaseRBPIUser)
admin.site.register(MessagesHistory)
admin.site.register(LegalEntity)
admin.site.register(Office)
admin.site.register(Order)
admin.site.register(LaunchProvider)
