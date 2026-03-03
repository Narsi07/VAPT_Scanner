# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import include, path

from projects import views

app_name = "projects"

urlpatterns = [
    path("project_edit/", views.project_edit, name="project_edit"),
    path("project_create/", views.ProjectCreate.as_view(), name="project_create"),
    path("project_delete/", views.ProjectDelete.as_view(), name="project_delete"),
]
