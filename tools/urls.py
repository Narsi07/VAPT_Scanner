# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import path
from tools import views

app_name = "tools"

urlpatterns = [
    # SSL scanning
    path("sslscan/", views.SslScanList.as_view(), name="sslscanlist"),
    path("sslscanlaunch/", views.SslScanLaunch.as_view(), name="sslscanlaunch"),
    path("sslscanresult/", views.SslScanResult.as_view(), name="sslscanresult"),
    path("sslscan_delete/", views.SslScanDelete.as_view(), name="sslscan_delete"),
    # Nikto scanning
    path("nikto/", views.NiktoScanList.as_view(), name="niktolist"),
    path("niktolaunch/", views.NiktoScanLaunch.as_view(), name="niktolaunch"),
    path("niktoresult/", views.NiktoScanResult.as_view(), name="niktoresult"),
    path("nikto_vuln/", views.NiktoResultVuln.as_view(), name="nikto_vuln"),
    path("nikto_vuln_delete/", views.NiktoVulnDelete.as_view(), name="nikto_vuln_delete"),
    path("nikto_scan_delete/", views.NiktoScanDelete.as_view(), name="nikto_scan_delete"),
    # Nmap
    path("nmap/", views.Nmap.as_view(), name="nmap"),
    path("nmap_scan/", views.NmapScan.as_view(), name="nmap_scan"),
    path("nmap_result/", views.NmapResult.as_view(), name="nmap_result"),
    path("nmap_scan_delete/", views.NmapScanDelete.as_view(), name="nmap_scan_delete"),
    # Nmap Vulners
    path("nmap_vulners/", views.nmap_vulners, name="nmap_vulners"),
    path("nmap_vulners_port_list/", views.nmap_vulners_port, name="nmap_vulners_port_list"),
    path("nmap_vulners_scan/", views.nmap_vulners_scan, name="nmap_vulners_scan"),
]
