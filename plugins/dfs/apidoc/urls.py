# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<url_name>|.+)$', views.APIDocView.as_view(), name='api_doc'),
]