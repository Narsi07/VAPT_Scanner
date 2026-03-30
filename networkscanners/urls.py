# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import path
from networkscanners import views

app_name = "networkscanners"

urlpatterns = [
    # Unified launch hub page
    path("launch/", views.launch_hub, name="launch_hub"),
    # Unified results hub page
    path("results/", views.results_hub, name="results_hub"),
]
