# -*- coding: utf-8 -*-
# VAPT Security Platform

"""vapt URL Configuration

"""
import notifications.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("webscanners/", include("webscanners.urls")),
    path("zapscanner/", include("webscanners.zapscanner.urls")),
    # Projects
    path("projects/", include("projects.urls")),
    # Network / Infrastructure Scanners (OpenVAS, Nmap)
    path("networkscanners/", include("networkscanners.urls")),
    # Static Analysis Scanners (Bandit, Semgrep)
    path("staticscanners/", include("staticscanners.urls")),
    # Tools (Nikto, SSLScan, Nmap, Nmap+Vulners)
    path("tools/", include("tools.urls")),
    # Pentest manual activity (disabled)
    # path("pentest/", include("pentest.urls")),
    # Reports (CSV/Excel export)
    path("reports/", include("reports.urls")),
    # Settings
    path("settings/", include("vaptsettings.urls")),
    # API v1 (VAPT REST API)
    path("archerysec/api/", include("vaptapi.urls")),
    # Auth
    path("archerysec/api/v1/auth/", include("authentication.urls")),
    path("auth/", include("authentication.urls")),
    # User management
    path("users/", include("user_management.urls")),
    # Report upload (fallback manual import)
    path("report-upload/", include("report_upload.urls")),
    # JIRA ticketing integration
    path("jira/", include("jiraticketing.urls")),
    # Notifications
    path(
        "inbox/notifications/", include(notifications.urls, namespace="notifications")
    ),
    # Default url (dashboard)
    path(r"", include("dashboard.urls")),
]

urlpatterns = urlpatterns + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

urlpatterns = urlpatterns + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
