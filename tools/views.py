# -*- coding: utf-8 -*-
# VAPT Security Platform

from __future__ import unicode_literals

import codecs
import hashlib
import os
import subprocess
import threading
import uuid
from datetime import datetime

import defusedxml.ElementTree as ET
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from notifications.signals import notify
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from scanners.scanner_parser.network_scanner import nmap_parser
from tools.models import (NmapResultDb, NmapScanDb, SslscanResultDb)
# NOTE[gmedian]: in order to be more portable we just import everything rather than add anything in this very script
from tools.nmap_vulners.nmap_vulners_view import (nmap_vulners,
                                                  nmap_vulners_port,
                                                  nmap_vulners_scan)
from user_management import permissions

sslscan_output = None

scan_result = ""
all_nmap = ""


# ─────────────────────────────────────────────────────────────────────────────
# BACKGROUND RUNNER HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _run_sslscan(scan_url, scan_id, project, user, organization):
    """Run sslscan in a background thread and save the output."""
    from tools.models import SslscanResultDb
    try:
        raw = subprocess.check_output(
            ["sslscan", "--no-colour", scan_url],
            timeout=120,
            stderr=subprocess.STDOUT,
        )
        # Decode bytes → readable text
        output = raw.decode("utf-8", errors="replace")
        SslscanResultDb.objects.filter(scan_id=scan_id).update(
            sslscan_output=output
        )
        notify.send(user, recipient=user, verb="SSLScan Completed: %s" % scan_url)
    except FileNotFoundError:
        SslscanResultDb.objects.filter(scan_id=scan_id).update(
            sslscan_output="[ERROR] sslscan is not installed. Run: sudo apt install sslscan"
        )
    except subprocess.TimeoutExpired:
        SslscanResultDb.objects.filter(scan_id=scan_id).update(
            sslscan_output="[ERROR] sslscan timed out after 120 seconds"
        )
    except Exception as e:
        SslscanResultDb.objects.filter(scan_id=scan_id).update(
            sslscan_output="[ERROR] " + str(e)
        )
        print("[VAPT] SSLScan error:", e)





def _run_nmap(ip_address, scan_id, project_id, user, organization):
    """Run nmap in a background thread, parse XML results and save."""
    from tools.models import NmapScanDb
    try:
        print("[VAPT] Starting Nmap scan on", ip_address)
        subprocess.check_output(
            [
                "nmap", "-v", "-sV", "-Pn",
                "-T4",                  # Aggressive timing (4x faster than default)
                "--max-retries", "1",   # Only retry each port once instead of 3x
                "--host-timeout", "300s",  # Give up on host after 5 minutes total
                "-p", "1-65535",
                ip_address,
                "-oX", "output.xml",
            ],
            timeout=3600,               # 1 hour outer safety net
            stderr=subprocess.STDOUT,
        )
        print("[VAPT] Nmap scan completed for", ip_address)
    except FileNotFoundError:
        print("[VAPT] nmap not found. Run: sudo apt install nmap")
        return
    except subprocess.TimeoutExpired:
        print("[VAPT] Nmap scan timed out for", ip_address)
    except Exception as e:
        print("[VAPT] Nmap error:", e)

    try:
        import defusedxml.ElementTree as ET2
        tree = ET2.parse("output.xml")
        root_xml = tree.getroot()
        nmap_parser.xml_parser(root=root_xml, scan_id=scan_id, project_id=project_id, organization=organization)
        notify.send(user, recipient=user, verb="Nmap scan completed: %s" % ip_address)
    except Exception as e:
        print("[VAPT] Nmap XML parse error:", e)


class SslScanList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tools/sslscan_list.html"

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_sslscan = SslscanResultDb.objects.filter(
            organization=request.user.organization
        )

        return render(request, "tools/sslscan_list.html", {"all_sslscan": all_sslscan})


class SslScanLaunch(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tools/sslscan_list.html"

    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def post(self, request):
        user = request.user
        scan_url = request.POST.get("scan_url")
        project_id = request.POST.get("project_id")

        if not project_id:
            project_id = None
            project = None
        else:
            try:
                from projects.models import ProjectDb
                project = ProjectDb.objects.get(uu_id=project_id)
            except Exception:
                project = None

        scan_item = str(scan_url)
        value = scan_item.replace(" ", "")
        value_split = value.split(",")
        for scans_url in value_split:
            scan_id = uuid.uuid4()
            # Save the record immediately with empty output — background will fill it in
            SslscanResultDb(
                scan_url=scans_url,
                scan_id=scan_id,
                project=project,
                sslscan_output=b"[Scanning...]",
                organization=request.user.organization,
            ).save()
            # Launch background thread
            t = threading.Thread(
                target=_run_sslscan,
                args=(scans_url, scan_id, project, user, request.user.organization),
                daemon=True
            )
            t.start()

        notify.send(user, recipient=user, verb="SSLScan started for: %s" % scan_url)
        return HttpResponseRedirect(reverse("tools:sslscan"))


class SslScanResult(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tools/sslscan_result.html"

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        scan_id = request.GET.get("scan_id")
        if not scan_id:
            # No scan_id — redirect to the SSL scan list page
            return HttpResponseRedirect(reverse("tools:sslscan"))
        scan_result = SslscanResultDb.objects.filter(
            scan_id=scan_id, organization=request.user.organization
        )
        return render(
            request, "tools/sslscan_result.html", {"scan_result": scan_result}
        )


class SslScanDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tools/sslscan_list.html"

    permission_classes = (IsAuthenticated, permissions.IsAdmin)

    def post(self, request):
        scan_id = request.POST.get("scan_id")

        scan_item = str(scan_id)
        value = scan_item.replace(" ", "")
        value_split = value.split(",")
        split_length = value_split.__len__()
        print("split_length"), split_length
        for i in range(0, split_length):
            vuln_id = value_split.__getitem__(i)

            del_scan = SslscanResultDb.objects.filter(
                scan_id=vuln_id, organization=request.user.organization
            )
            del_scan.delete()

        return HttpResponseRedirect(reverse("tools:sslscan"))





class NmapScan(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tools/nmap_scan.html"

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_nmap = NmapScanDb.objects.filter(
            organization=request.user.organization,
            is_vulners=False,
        )
        return render(request, "tools/nmap_scan.html", {"all_nmap": all_nmap})


class Nmap(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tools/nmap_list.html"

    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        ip_address = request.GET["ip"]

        all_nmap = NmapResultDb.objects.filter(
            ip_address=ip_address, organization=request.user.organization
        )

        return render(request, "tools/nmap_list.html", {"all_nmap": all_nmap})

    def post(self, request):
        ip_address = request.POST.get("ip")
        project_id = request.POST.get("project_id")

        if not project_id:
            project_id = None

        scan_id = uuid.uuid4()
        user = request.user

        # Save an initial scan record immediately
        NmapScanDb(
            scan_id=scan_id,
            scan_ip=ip_address,
            organization=request.user.organization,
        ).save()

        # Launch in background so browser doesn't block
        t = threading.Thread(
            target=_run_nmap,
            args=(ip_address, scan_id, project_id, user, request.user.organization),
            daemon=True,
        )
        t.start()

        notify.send(user, recipient=user, verb="Nmap scan started for: %s" % ip_address)
        return HttpResponseRedirect("/tools/nmap_scan/")


class NmapResult(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tools/nmap_result.html"

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        scan_id = request.GET.get("scan_id")
        if not scan_id:
            return HttpResponseRedirect(reverse("tools:nmap_scan"))
            
        scan_result = NmapResultDb.objects.filter(
            scan_id=scan_id, organization=request.user.organization
        )

        return render(request, "tools/nmap_result.html", {"scan_result": scan_result})


class NmapScanDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tools/nmap_result.html"

    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def post(self, request):
        scan_id = request.POST.get("scan_id")
        if scan_id:
            NmapResultDb.objects.filter(
                scan_id=scan_id, organization=request.user.organization
            ).delete()
            NmapScanDb.objects.filter(
                scan_id=scan_id, organization=request.user.organization
            ).delete()
        return HttpResponseRedirect(reverse("tools:nmap_scan"))
