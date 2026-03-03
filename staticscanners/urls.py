# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import include, path

from staticscanners import views

app_name = "staticscanners"

urlpatterns = [
    # Static scans
    path("list_vuln/", views.SastScanVulnList.as_view(), name="list_vuln"),
    path("list_scans/", views.SastScanList.as_view(), name="list_scans"),
    path("list_vuln_info/", views.SastScanVulnInfo.as_view(), name="list_vuln_info"),
    path("scan_details/", views.SastScanDetails.as_view(), name="scan_details"),
    path("scan_delete/", views.SastScanDelete.as_view(), name="scan_delete"),
    path("vuln_delete/", views.SastScanVulnDelete.as_view(), name="vuln_delete"),
    path("vuln_mark/", views.SastScanVulnMark.as_view(), name="vuln_mark"),
]
