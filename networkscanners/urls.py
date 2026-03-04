# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import path
from networkscanners import views

app_name = "networkscanners"

urlpatterns = [
    # OpenVAS scanning
    path("launch_scan/", views.OpenvasLaunchScan.as_view(), name="launch_scan"),
    path("openvas_setting/", views.OpenvasSetting.as_view(), name="openvas_setting"),
    path("openvas_details/", views.OpenvasDetails.as_view(), name="openvas_details"),
    path("openvas_setting_enable/", views.OpenvasSettingEnable.as_view(), name="openvas_setting_enable"),
    path("openvas_setting_enable_details/", views.OpenvasSettingEnableDetails.as_view(), name="openvas_setting_enable_details"),
    # Network scan (Nmap)
    path("ip_scan/", views.NetworkScan.as_view(), name="ip_scan"),
    path("network_scan_schedule/", views.NetworkScanSchedule.as_view(), name="network_scan_schedule"),
    path("del_network_scan_schedule/", views.NetworkScanScheduleDelete.as_view(), name="del_network_scan_schedule"),
    # Nmap Vulners redirect — handled via nv_setting
    path("nv_setting/", views.OpenvasSettingEnable.as_view(), name="nv_setting"),
    # Scan management
    path("list_scans/", views.NetworkScanList.as_view(), name="list_scans"),
    path("list_vuln_info/", views.NetworkScanVulnInfo.as_view(), name="list_vuln_info"),
    path("scan_details/", views.NetworkScanDetails.as_view(), name="scan_details"),
    path("scan_delete/", views.NetworkScanDelete.as_view(), name="scan_delete"),
    path("vuln_delete/", views.NetworkScanVulnDelete.as_view(), name="vuln_delete"),
    path("vuln_mark/", views.NetworkScanVulnMark.as_view(), name="vuln_mark"),
]
