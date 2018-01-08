# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import User, Group

from core.models import (
    BaseRBPIUser, MessagesHistory, LegalEntity, Office, LaunchProvider)

# TODO нужны предзаполненые поля для объекта history


class RBPIAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'password', 'is_admin', 'is_group',
              'legal_entity', 'is_active')


class AdminLaunchProvider(admin.ModelAdmin):
    fields = ('username', 'email', 'password')


class AdminLegalEntity(admin.ModelAdmin):
    fields = ('name_of_legal', 'offices', 'status_name')


class AdminOffice(admin.ModelAdmin):
    fields = ('name', 'place', 'status_name')


# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(BaseRBPIUser, RBPIAdmin)
admin.site.register(MessagesHistory)
admin.site.register(LegalEntity, AdminLegalEntity)
admin.site.register(Office, AdminOffice)
admin.site.register(LaunchProvider, AdminLaunchProvider)
