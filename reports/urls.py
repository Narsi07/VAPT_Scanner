# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("", views.ReportIndex.as_view(), name="index"),
    path("export/csv/", views.ExportCSV.as_view(), name="export_csv"),
    path("export/excel/", views.ExportExcel.as_view(), name="export_excel"),
]
