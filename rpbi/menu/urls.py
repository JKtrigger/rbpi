# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.CustomerView.as_view(), name='index'),
    url(r'^submit_order$', views.submit_order),
    url(
        r'^(?P<username>[a-zA-Z]+\.[a-zA-Z]+)',
        views.CustomerView.as_view()
    ),
    # url(r'^200', views.CustomerView.message(), name='message'),
]
