# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import path
from staticscanners import views

app_name = "staticscanners"

urlpatterns = [
    # Unified launch hub page
    path("launch/", views.launch_hub, name="launch_hub"),
    # Bandit SAST scan launch
    path("bandit_scan/", views.BanditScanLaunch.as_view(), name="bandit_scan"),
    # Semgrep SAST scan launch
    path("semgrep_scan/", views.SemgrepScanLaunch.as_view(), name="semgrep_scan"),
    # Scan management
    path("list_scans/", views.SastScanList.as_view(), name="list_scans"),
    path("list_vuln_info/", views.SastScanVulnInfo.as_view(), name="list_vuln_info"),
    path("scan_details/", views.SastScanDetails.as_view(), name="scan_details"),
    path("scan_delete/", views.SastScanDelete.as_view(), name="scan_delete"),
    path("vuln_delete/", views.SastScanVulnDelete.as_view(), name="vuln_delete"),
    path("vuln_mark/", views.SastScanVulnMark.as_view(), name="vuln_mark"),
]
