# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class BaseHistoryModel(models.Model):
    """
    Базовый Историческая модель,
    определяет поля в моделях потмках
    """
    ON_ACTIVE, ON_DELETED, ON_MODIFY, ON_REPAIR = xrange(0, 4)
    STATUSES = (
        (ON_ACTIVE, "ON_ACTIVE"),
        (ON_DELETED, "ON_DELETED,"),
        (ON_MODIFY, "ON_MODIFY"),
        (ON_REPAIR, "ON_REPAIR"),
    )

    created = models.DateTimeField(verbose_name='created', auto_now=True)
    modified = models.DateTimeField(verbose_name='modified', auto_now_add=True)
    user_modifier = models.ForeignKey(
        'core.BaseRBPIUser', verbose_name="modifier user")
    status_name = models.PositiveSmallIntegerField(
        choices=STATUSES, verbose_name='status', default=ON_ACTIVE)

    class Meta:
        abstract = True


class BaseUser(User):
    receive_message = models.BooleanField(
        verbose_name='receive messages',
        default=True)

    class Meta:
        abstract = True


class Office(BaseHistoryModel):
    """
    Класс офисов
    """
    name = models.CharField(verbose_name="Office", max_length=40)


class LegalEntity(BaseHistoryModel):
    """
    Класс Юридических лиц
    """
    name_of_legal = models.CharField(verbose_name="Legal Name", max_length=40)
    offices = models.ForeignKey('Office', verbose_name="Offices")


class BaseRBPIUser(BaseUser):
    """
    Базовывй пользователь RBPI
    """
    is_admin = models.BooleanField(
        verbose_name='is admin',
        default=False)
    is_group = models.BooleanField(
        verbose_name='is group',
        default=False)
    legal_entity = models.ForeignKey('LegalEntity')

    class Meta:
        permissions = (
            ("can_control_RBPI_users", "To HR department"),
        )


class MessagesHistory(BaseHistoryModel):
    """
    История сообщений
    """
    from_user = models.ForeignKey(
        'BaseRBPIUser', verbose_name='from user', related_name='sender')
    to_user = models.ForeignKey('auth.User', related_name='receiver')

    class Meta:
        permissions = (
            ("can_create_messages", "To HR department"),
        )
