# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import include, path

from dashboard import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("project_dashboard/", views.project_dashboard, name="project_dashboard"),
    path("proj_data/", views.proj_data, name="proj_data"),
    path("all_high_vuln/", views.all_high_vuln, name="all_high_vuln"),
    path("export/", views.export, name="export"),
]
