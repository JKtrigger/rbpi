# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission

from core.models import (
    BaseRBPIUser, MessagesHistory, LegalEntity, Office, LaunchProvider)


class RBPIAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'password', 'is_admin', 'is_group',
              'legal_entity')


class AdminLaunchProvider(admin.ModelAdmin):
    fields = ('username', 'email', 'password')


# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(BaseRBPIUser, RBPIAdmin)
admin.site.register(MessagesHistory)
admin.site.register(LegalEntity)
admin.site.register(Office)
admin.site.register(LaunchProvider, AdminLaunchProvider)
