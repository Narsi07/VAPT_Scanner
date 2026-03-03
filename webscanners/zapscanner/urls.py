# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import include, path

from webscanners.zapscanner import views

app_name = "zapscanner"

urlpatterns = [
    path("zap_scan/", views.ZapScan.as_view(), name="zap_scan"),
    path("zap_settings/", views.ZapSetting.as_view(), name="zap_settings"),
    path(
        "zap_setting_update/",
        views.ZapSettingUpdate.as_view(),
        name="zap_setting_update",
    ),
]
