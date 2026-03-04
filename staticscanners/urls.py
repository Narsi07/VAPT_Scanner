# -*- coding: utf-8 -*-
# VAPT Security Platform
# Static Code Analysis & Infrastructure as Code Scanners

from django.urls import path
from staticscanners import views
from staticscanners.scanner_consolidated import (
    BanditScannerView,
    SemgrepScannerView,
    CheckovScannerView
)

app_name = "staticscanners"

urlpatterns = [
    # Consolidated Bandit Scanner - Scan launch + Result display
    path("bandit/", BanditScannerView.as_view(), name="bandit_scan"),
    
    # Consolidated Semgrep Scanner - Scan launch + Result display
    path("semgrep/", SemgrepScannerView.as_view(), name="semgrep_scan"),
    
    # Consolidated Checkov Scanner - Infrastructure as Code
    path("checkov/", CheckovScannerView.as_view(), name="checkov_scan"),
    
    # Scan management endpoints
    path("list_scans/", views.SastScanList.as_view(), name="list_scans"),
    path("list_vuln_info/", views.SastScanVulnInfo.as_view(), name="list_vuln_info"),
    path("scan_details/", views.SastScanDetails.as_view(), name="scan_details"),
    path("scan_delete/", views.SastScanDelete.as_view(), name="scan_delete"),
    path("vuln_delete/", views.SastScanVulnDelete.as_view(), name="vuln_delete"),
    path("vuln_mark/", views.SastScanVulnMark.as_view(), name="vuln_mark"),
]
