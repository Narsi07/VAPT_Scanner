# -*- coding: utf-8 -*-
# VAPT Security Platform
# Network Vulnerability Scanners

from django.urls import path
from networkscanners import views
from networkscanners.scanner_consolidated import (
    NmapNetworkScannerView,
    OpenVASScannerView,
    NmapVulnersScannerView
)

app_name = "networkscanners"

urlpatterns = [
    # Consolidated Nmap Scanner - Port scanning + Results
    path("nmap/", NmapNetworkScannerView.as_view(), name="nmap_scan"),
    
    # Consolidated OpenVAS Scanner - Full vulnerability assessment
    path("openvas/", OpenVASScannerView.as_view(), name="openvas_scan"),
    
    # Consolidated Nmap-Vulners Scanner - Enhanced vulnerability detection
    path("nmap_vulners/", NmapVulnersScannerView.as_view(), name="nmap_vulners_scan"),
    
    # Legacy endpoints for compatibility
    path("launch_scan/", views.OpenvasLaunchScan.as_view(), name="launch_scan"),
    path("ip_scan/", views.NetworkScan.as_view(), name="ip_scan"),
    
    # Scan management
    path("list_scans/", views.NetworkScanList.as_view(), name="list_scans"),
    path("list_vuln_info/", views.NetworkScanVulnInfo.as_view(), name="list_vuln_info"),
    path("scan_details/", views.NetworkScanDetails.as_view(), name="scan_details"),
    path("scan_delete/", views.NetworkScanDelete.as_view(), name="scan_delete"),
    path("vuln_delete/", views.NetworkScanVulnDelete.as_view(), name="vuln_delete"),
    path("vuln_mark/", views.NetworkScanVulnMark.as_view(), name="vuln_mark"),
    
    # Settings
    path("openvas_setting/", views.OpenvasSetting.as_view(), name="openvas_setting"),
    path("openvas_details/", views.OpenvasDetails.as_view(), name="openvas_details"),
]
