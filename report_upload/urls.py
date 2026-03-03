# -*- coding: utf-8 -*-
# VAPT Security Platform
from django.urls import include, path

from report_upload import views

app_name = "report_upload"

urlpatterns = [
    path("upload/", views.Upload.as_view(), name="upload"),
]
