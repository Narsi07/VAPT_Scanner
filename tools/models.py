# -*- coding: utf-8 -*-
# VAPT Security Platform

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from user_management.models import Organization, UserProfile


# SSLScan Model.
class SslscanResultDb(models.Model):
    scan_id = models.TextField(blank=True, null=True)
    project = models.ForeignKey(
        "projects.ProjectDb", on_delete=models.CASCADE, null=True
    )
    scan_url = models.TextField(blank=True, null=True)
    sslscan_output = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(
        auto_now=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sslscan_result_db_created",
    )
    updated_by = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sslscan_result_db_updated",
    )
    is_active = models.BooleanField(default=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=1)



# Nmap tool models
class NmapScanDb(models.Model):
    scan_id = models.TextField(blank=True, null=True)
    project = models.ForeignKey(
        "projects.ProjectDb", on_delete=models.CASCADE, null=True
    )
    scan_ip = models.TextField(blank=True, null=True)
    total_ports = models.TextField(blank=True, null=True)
    total_open_ports = models.TextField(blank=True, null=True)
    total_close_ports = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(
        auto_now=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="nmap_result_db_created",
    )
    updated_by = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="nmap_result_db_updated",
    )
    is_active = models.BooleanField(default=True)
    is_vulners = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=1)


class NmapResultDb(models.Model):
    scan_id = models.TextField(blank=True, null=True)
    project = models.ForeignKey(
        "projects.ProjectDb", on_delete=models.CASCADE, null=True
    )
    ip_address = models.TextField(blank=True, null=True)
    protocol = models.TextField(blank=True, null=True)
    port = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    reason_ttl = models.TextField(blank=True, null=True)
    version = models.TextField(blank=True, null=True)
    extrainfo = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    conf = models.TextField(blank=True, null=True)
    method = models.TextField(blank=True, null=True)
    type_p = models.TextField(blank=True, null=True)
    osfamily = models.TextField(blank=True, null=True)
    vendor = models.TextField(blank=True, null=True)
    osgen = models.TextField(blank=True, null=True)
    accuracy = models.TextField(blank=True, null=True)
    cpe = models.TextField(blank=True, null=True)
    used_state = models.TextField(blank=True, null=True)
    used_portid = models.TextField(blank=True, null=True)
    used_proto = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(
        auto_now=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="nmap_sca_result_db_created",
    )
    updated_by = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        related_name="nmap_sca_result_db_updated",
    )
    is_active = models.BooleanField(default=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=1)


# NOTE[gmedian]: just base on the previous existing table in order not to make anything non-working
class NmapVulnersPortResultDb(NmapResultDb):
    vulners_extrainfo = models.TextField(blank=True, null=True)
