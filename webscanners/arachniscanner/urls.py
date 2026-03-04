# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import path
from webscanners.arachniscanner import views

app_name = "arachniscanner"

urlpatterns = [
    path("arachni_scan/", views.ArachniScan.as_view(), name="arachni_scan_launch"),
    path("arachni_settings/", views.ArachniSetting.as_view(), name="arachni_settings"),
    path("arachni_setting_update/", views.ArachniSettingUpdate.as_view(), name="arachni_setting_update"),
    path("del_arachni_scan/", views.ArachniScan.as_view(), name="del_arachni_scan"),
    path("export/", views.ArachniScan.as_view(), name="export"),
    path("arachni_list_vuln/", views.ArachniScan.as_view(), name="arachni_list_vuln"),
]
