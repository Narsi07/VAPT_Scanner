# -*- coding: utf-8 -*-
# VAPT Security Platform
# OWASP ZAP Web Application Scanner

from django.urls import path
from webscanners.zapscanner import views

app_name = "zapscanner"

urlpatterns = [
    # ZAP scan launch
    path("zap_scan/", views.ZapScan.as_view(), name="zap_scan"),
    # ZAP settings
    path("zap_settings/", views.ZapSetting.as_view(), name="zap_settings"),
    path("zap_setting_update/", views.ZapSettingUpdate.as_view(), name="zap_setting_update"),
    # Legacy URL names referenced in templates — alias to nearest available view
    path("zap_list_vuln/", views.ZapSetting.as_view(), name="zap_list_vuln"),
    path("del_zap_scan/", views.ZapScan.as_view(), name="del_zap_scan"),
    path("zap_scan_pdf_gen/", views.ZapSetting.as_view(), name="zap_scan_pdf_gen"),
    path("export/", views.ZapSetting.as_view(), name="export"),
]
