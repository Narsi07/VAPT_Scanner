# -*- coding: utf-8 -*-
# VAPT Security Platform
# Additional Security Tools (SSL Scan, Nikto, DNS Enumeration)

from django.urls import path
from tools import views
from tools.scanner_consolidated import (
    NiktoScannerView,
    SSLScannerView,
    DnsEnumerationView
)

app_name = "tools"

urlpatterns = [
    # Consolidated Nikto Web Server Scanner
    path("nikto/", NiktoScannerView.as_view(), name="nikto"),
    
    # Consolidated SSL/TLS Certificate Scanner
    path("sslscan/", SSLScannerView.as_view(), name="sslscan"),
    
    # Consolidated DNS Enumeration Tool
    path("dns_enum/", DnsEnumerationView.as_view(), name="dns_enum"),
    
    # Legacy endpoints for compatibility
    path("nmap/", views.Nmap.as_view(), name="nmap"),
    path("nmap_scan/", views.NmapScan.as_view(), name="nmap_scan"),
    path("nmap_vulners/", views.nmap_vulners, name="nmap_vulners"),
]
