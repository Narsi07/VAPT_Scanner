# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import include, path

from vaptsettings import views

app_name = "vaptsettings"

urlpatterns = [
    path("settings/", views.Settings.as_view(), name="settings"),
    path("del_setting/", views.DeleteSettings.as_view(), name="del_setting"),
    path("email_setting/", views.EmailSetting.as_view(), name="email_setting"),
]
