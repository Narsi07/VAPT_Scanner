from django.urls import path
from webscanners.burpscanner import views

app_name = "burpscanner"

urlpatterns = [
    path("burp_scan/", views.BurpScanLaunch.as_view(), name="burp_scan"),
    path("burp_settings/", views.BurpSetting.as_view(), name="burp_settings"),
]
