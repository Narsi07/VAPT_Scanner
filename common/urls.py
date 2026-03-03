# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import path

from common import views

urlpatterns = [
    # Your URLs...
    path("json-to-yaml/", views.Json_to_Yaml.as_view()),
    path("yaml-to-json/", views.Yaml_to_Json.as_view()),
]
