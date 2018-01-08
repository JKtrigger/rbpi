# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Permission
from django.utils.translation import ugettext_lazy as _


class BaseHistoryModel(models.Model):
    """
    Базовый Историческая модель,
    определяет поля в моделях потмках
    """
    ON_ACTIVE, ON_DELETED, ON_MODIFY, ON_REPAIR = xrange(0, 4)
    STATUSES = (
        (ON_ACTIVE, "ON_ACTIVE"),
        (ON_DELETED, "ON_DELETED"),
        (ON_MODIFY, "ON_MODIFY"),
        (ON_REPAIR, "ON_REPAIR"),
    )

    created = models.DateTimeField(verbose_name='created', auto_now=True)
    modified = models.DateTimeField(verbose_name='modified', auto_now_add=True)
    user_modifier = models.ForeignKey(
        'core.BaseRBPIUser', verbose_name="modifier user",
        blank=True, null=True
    )
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


class LaunchProvider(BaseUser):
    """
    Класс Поставщиков обедов
    """
    def __unicode__(self):
        return u"{}".format(self.username)


class ActiveUserManager(models.Manager):
    """Менеджер активных пользователей"""
    def get_queryset(self):
        return super(ActiveUserManager, self).get_queryset().filter(
            is_active=True
        )


class ActiveLegalEntityManager(models.Manager):
    """Менеджер активных Юр., лиц """
    def get_queryset(self):
        return super(ActiveLegalEntityManager, self).get_queryset().filter(
            status_name=BaseHistoryModel.ON_ACTIVE
        )


class ActiveOffices(ActiveLegalEntityManager):
    """Менеджер активных офисов"""


class Office(BaseHistoryModel):
    """
    Класс офисов
    """

    name = models.CharField(verbose_name="office", max_length=40)
    place = models.ForeignKey(
        'LaunchProvider', verbose_name="provider",
        related_name="provider", blank=True, null=True
    )
    objects_active_offices = ActiveOffices()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.name


class LegalEntity(BaseHistoryModel):
    """
    Класс Юридических лиц
    """
    name_of_legal = models.CharField(verbose_name="Legal Name", max_length=40)
    offices = models.ManyToManyField(
        'Office', verbose_name="Offices", related_name="offices", blank=True)

    objects_active_legal = ActiveLegalEntityManager()

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        WORD_ENDING_OV = 0, 5, 6, 7, 8, 9
        WORD_ENDING_ = 1,
        WORD_ENDING_A = 2, 3, 4

        count_offices = self.offices.count()
        word = u"офис{}"
        if count_offices % 10 in WORD_ENDING_OV:
            word = word.format("ов")
        if count_offices % 10 in WORD_ENDING_:
            word = word.format('')
        if count_offices % 10 in WORD_ENDING_A:
            word = word.format("а")
        return u"{} = > {} {}".format(
            self.name_of_legal, count_offices, word)


class BaseRBPIUser(BaseUser):
    """
    Базовывй пользователь RBPI

    Разделяет HR и остальных пользователей
    """
    objects_active_users = ActiveUserManager()
    is_admin = models.BooleanField(
        verbose_name='is admin',
        default=False,
        help_text=_(u"Это отдел кадров ?")
    )
    is_group = models.BooleanField(
        verbose_name='is group',
        default=False,
        help_text=_(u"Это группа лиц ?")
    )
    legal_entity = models.ForeignKey('LegalEntity', blank=True, null=True)

    def add_perm(self, *args, **kwargs):
        self.user_permissions = [
            # Значения по умолчанию
            Permission.objects.get(codename='add_order'),
            Permission.objects.get(codename='change_order'),
            # Permission.objects.get(codename='delete_order')
        ]

        if self.is_admin:
            self.is_staff = True
            self.is_active = True
            self.user_permissions.add(
                # todo : Переписать
                Permission.objects.get(codename='add_launchprovider'),
                Permission.objects.get(codename='change_launchprovider'),
                # Permission.objects.get(codename='delete_launchprovider'),

                Permission.objects.get(codename='add_office'),
                # Permission.objects.get(codename='delete_office'),
                Permission.objects.get(codename='change_office'),

                Permission.objects.get(codename='add_legalentity'),
                # Permission.objects.get(codename='delete_legalentity'),
                Permission.objects.get(codename='change_legalentity'),

                Permission.objects.get(codename='add_messageshistory'),
                # Permission.objects.get(codename='delete_messageshistory'),
                Permission.objects.get(codename='change_messageshistory'),

                Permission.objects.get(codename='add_baserbpiuser'),
                # Permission.objects.get(codename='delete_baserbpiuser'),
                Permission.objects.get(codename='change_baserbpiuser'),
            )

        super(BaseRBPIUser, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(BaseRBPIUser, self).save(*args, **kwargs)
        self.add_perm()

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
