# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView


class BaseReportView(TemplateView):
    """
        View - Для отображения заказов и их оформления на рабочую неделю
    """

    template_name = "reports/lunch_reports.html"
    top_text = 'topText'
    top_text_under_text = 'topTextUnderText'
    hello_text = 'helloText'

    def get_context_data(self, **kwargs):
        context = super(BaseReportView, self).get_context_data(**kwargs)
        context['topText'] = self.top_text
        context['helloText'] = self.hello_text
        context['topTextUnderText'] = self.top_text_under_text

        return context


class ReportView(BaseReportView):
    """
        View - Для отображения заказов и их оформления на рабочую неделю
    """

    template_name = "reports/lunch_reports.html"
    top_text = ''
    top_text_under_text = ''
    hello_text = 'Reports'

    def get_context_data(self, **kwargs):

        context = super(ReportView, self).get_context_data(**kwargs)
        return context
