# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.urls import path
from webscanners import views, web_views

app_name = "webscanners"

urlpatterns = [
    # Unified launch hub page
    path("launch/", web_views.launch_hub, name="launch_hub"),
    # Unified results hub page
    path("results/", web_views.results_hub, name="results_hub"),
    # Main web scanner index / ZAP launch — template uses 'webscanners:index'
    path("", web_views.Index.as_view(), name="index"),
    # Cookie management — template uses 'webscanners:cookie_add', 'webscanners:cookies_del'
    path("cookie_add/", web_views.AddCookies.as_view(), name="cookie_add"),
    path("cookies_del/", web_views.AddCookies.as_view(), name="cookies_del"),  # alias
    # Task/scan launch
    path("web_task_launch/", web_views.WebTaskLaunch.as_view(), name="web_task_launch"),
    # Schedule management — template uses 'webscanners:web_scan_schedule', 'webscanners:del_web_scan_schedule'
    path("web_scan_schedule/", web_views.WebScanSchedule.as_view(), name="web_scan_schedule"),
    path("del_web_scan_schedule/", web_views.WebScanScheduleDelete.as_view(), name="del_web_scan_schedule"),
    # Notifications
    path("del_notify/", web_views.DeleteNotify.as_view(), name="del_notify"),
    path("del_all_notify/", web_views.DeleteAllNotify.as_view(), name="del_all_notify"),
    # Scan management — templates use 'webscanners:list_scans', 'webscanners:list_vuln', 'webscanners:list_vuln_info'
    path("list_vuln/", views.WebScanVulnList.as_view(), name="list_vuln"),
    path("list_scans/", views.WebScanList.as_view(), name="list_scans"),
    path("list_vuln_info/", views.WebScanVulnInfo.as_view(), name="list_vuln_info"),
    path("scan_details/", views.WebScanDetails.as_view(), name="scan_details"),
    path("scan_delete/", views.WebScanDelete.as_view(), name="scan_delete"),
    path("vuln_delete/", views.WebScanVulnDelete.as_view(), name="vuln_delete"),
    path("vuln_mark/", views.WebScanVulnMark.as_view(), name="vuln_mark"),
    # Legacy aliases used in older templates
    path("excluded_url_list/", views.WebScanList.as_view(), name="excluded_url_list"),
    path("xml_upload/", views.WebScanList.as_view(), name="xml_upload"),
    path("export/", views.WebScanList.as_view(), name="export"),
    path("login/", web_views.Index.as_view(), name="login"),   # redirect to main
    path("signup/", web_views.Index.as_view(), name="signup"), # redirect to main
]
