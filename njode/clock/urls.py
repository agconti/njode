# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url

from . import views 

urlpatterns = patterns('',
    url(r'^current-time/', views.NodeServer.as_view(), name="node-server"),
)
