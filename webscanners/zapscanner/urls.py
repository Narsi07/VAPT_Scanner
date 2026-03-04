# -*- coding: utf-8 -*-
# VAPT Security Platform
# OWASP ZAP Web Application Scanner

from django.urls import path
from webscanners.zapscanner import views

app_name = "zapscanner"

urlpatterns = [
    # Legacy endpoints - now consolidated in parent webscanners/urls.py
    path("zap_scan/", views.ZapScan.as_view(), name="zap_scan"),
    path("zap_settings/", views.ZapSetting.as_view(), name="zap_settings"),
    path("zap_setting_update/", views.ZapSettingUpdate.as_view(), name="zap_setting_update"),
]
