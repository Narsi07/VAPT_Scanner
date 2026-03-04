# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import path
from django.views.generic import TemplateView
from networkscanners import views

app_name = "networkscanners"

urlpatterns = [
    # Unified launch hub page
    path("launch/", TemplateView.as_view(template_name="launch/network_scan.html"), name="launch_hub"),
    # OpenVAS scanning
    path("launch_scan/", views.OpenvasLaunchScan.as_view(), name="launch_scan"),
    path("openvas_setting/", views.OpenvasSetting.as_view(), name="openvas_setting"),
    path("openvas_details/", views.OpenvasDetails.as_view(), name="openvas_details"),
    # OpenVAS / Nmap Vulners settings enable
    path("openvas_setting_enable/", views.OpenvasSettingEnable.as_view(), name="openvas_setting_enable"),
    path("nv_setting/", views.OpenvasSettingEnable.as_view(), name="nv_setting"),
    path("openvas_setting_enable_details/", views.OpenvasSettingEnableDetails.as_view(), name="openvas_setting_enable_details"),
    path("nv_details/", views.OpenvasSettingEnableDetails.as_view(), name="nv_details"),
    # Network scan (Nmap / IP scan)
    path("ip_scan/", views.NetworkScan.as_view(), name="ip_scan"),
    path("net_scan_schedule/", views.NetworkScanSchedule.as_view(), name="net_scan_schedule"),
    path("del_net_scan_schedule/", views.NetworkScanScheduleDelete.as_view(), name="del_net_scan_schedule"),
    # Scan management
    path("list_scans/", views.NetworkScanList.as_view(), name="list_scans"),
    path("list_vuln_info/", views.NetworkScanVulnInfo.as_view(), name="list_vuln_info"),
    path("scan_details/", views.NetworkScanDetails.as_view(), name="scan_details"),
    path("scan_delete/", views.NetworkScanDelete.as_view(), name="scan_delete"),
    path("scan_del/", views.NetworkScanDelete.as_view(), name="scan_del"),  # alias
    path("vuln_delete/", views.NetworkScanVulnDelete.as_view(), name="vuln_delete"),
    path("del_vuln/", views.NetworkScanVulnDelete.as_view(), name="del_vuln"),  # alias
    path("vuln_mark/", views.NetworkScanVulnMark.as_view(), name="vuln_mark"),
    path("vuln_check/", views.NetworkScanVulnMark.as_view(), name="vuln_check"),  # alias
    # XML upload  — handled by report_upload but some templates link here
    path("xml_upload/", views.OpenvasLaunchScan.as_view(), name="xml_upload"),
    # Vuln details alias
    path("vul_details/", views.NetworkScanVulnInfo.as_view(), name="vul_details"),
]
