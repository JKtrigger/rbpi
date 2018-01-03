# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from core.models import BaseRBPIUser
from django.contrib.auth import login, authenticate


class CustomerView(TemplateView):
    """
    View - Для отображения заказов и их оформления на рабочую неделю
    """

    template_name = "menu/menu.html"
    top_text = "Dinners for the whole week!"
    top_text_under_text = "Everyone needs lunch or dinner"
    hello_text = "Hi {}"

    def get_context_data(self, **kwargs):
        """

        Изменяем содержание контекста. Автоматически авторизуем пользователей,
        не из числа администраторов, без пароля. Администратором буду выводить
        список пользователей по Юр лицу. Планирую отдельные учетные записи.

        :param kwargs: - словурь контеста
        :return: HTML страницу
        """
        context = super(CustomerView, self).get_context_data(**kwargs)
        context['topText'] = self.top_text
        context['topTextUnderText'] = self.top_text_under_text
        username = context.get('username', None)
        if not username or username == 'None':
            context['username'] = _(
                '<i><abbr title="Most likely you are not logged in.'
                '">Anonymous</abbr> User?</i>'
            )
        else:
            user = BaseRBPIUser.objects.filter(
                username=username)

            if not user.exists():
                context['username'] = u'{} is non existent user'.format(
                    username
                )
            else:
                if not user[0].is_admin:
                    login(self.request, user[0])

        context['helloText'] = self.hello_text.format(context['username'])
        return context
