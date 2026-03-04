# -*- coding: utf-8 -*-
# VAPT Security Platform

from __future__ import unicode_literals


def launch_hub(request):
    from django.shortcuts import render as _render
    from projects.models import ProjectDb
    all_projects = ProjectDb.objects.filter(
        organization=request.user.organization
    ) if request.user.is_authenticated else []
    return _render(request, 'launch/static_scan.html', {'all_projects': all_projects})


import hashlib
import json
import os
import subprocess
import threading
import uuid
from datetime import datetime

from django.core import signing
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
try:
    from jira import JIRA
except ImportError:
    JIRA = None
from notifications.models import Notification
from notifications.signals import notify
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

try:
    from jiraticketing.models import jirasetting
except ImportError:
    jirasetting = None
from staticscanners.models import StaticScanResultsDb, StaticScansDb
from staticscanners.serializers import (StaticScanDbSerializer,
                                        StaticScanResultsDbSerializer)
from user_management import permissions


class SastScanList(APIView):
    permission_classes = [IsAuthenticated | permissions.VerifyAPIKey]

    def get(self, request):
        scan_list = StaticScansDb.objects.filter(organization=request.user.organization)
        all_notify = Notification.objects.unread()

        if request.path[:4] == "/api":
            serialized_data = StaticScanDbSerializer(scan_list, many=True)
            return Response(serialized_data.data)
        else:
            return render(
                request,
                "staticscanners/scans/list_scans.html",
                {"all_scans": scan_list, "message": all_notify},
            )


class SastScanVulnInfo(APIView):
    permission_classes = [IsAuthenticated | permissions.VerifyAPIKey]

    def get(self, request, uu_id=None):
        jira_url = None
        jira = jirasetting.objects.filter(organization=request.user.organization)
        for d in jira:
            jira_url = d.jira_server

        # all_notify =
        Notification.objects.unread()
        if uu_id is None:
            scan_id = request.GET["scan_id"]
            scan_name = request.GET["scan_name"]
            vuln_data = StaticScanResultsDb.objects.filter(
                scan_id=scan_id, title=scan_name, organization=request.user.organization
            )
        else:
            try:
                vuln_data = StaticScanResultsDb.objects.filter(
                    scan_id=uu_id, organization=request.user.organization
                )
            except Exception:
                return Response(
                    {"message": "Scan Id Doesn't Exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        if request.path[:4] == "/api":
            serialized_data = StaticScanResultsDbSerializer(vuln_data, many=True)
            return Response(serialized_data.data)
        else:
            return render(
                request,
                "staticscanners/scans/list_vuln_info.html",
                {"vuln_data": vuln_data, "jira_url": jira_url},
            )


class SastScanVulnMark(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "staticscanners/scans/list_vuln_info.html"

    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def post(self, request):
        false_positive = request.POST.get("false")
        status = request.POST.get("status")
        vuln_id = request.POST.get("vuln_id")
        scan_id = request.POST.get("scan_id")
        vuln_name = request.POST.get("vuln_name")
        notes = request.POST.get("note")
        StaticScanResultsDb.objects.filter(
            vuln_id=vuln_id, scan_id=scan_id, organization=request.user.organization
        ).update(false_positive=false_positive, vuln_status=status, note=notes)

        if false_positive == "Yes":
            vuln_info = StaticScanResultsDb.objects.filter(
                scan_id=scan_id, vuln_id=vuln_id, organization=request.user.organization
            )
            for vi in vuln_info:
                name = vi.title
                url = vi.fileName
                severity = vi.severity
                dup_data = str(name) + str(url) + str(severity)
                false_positive_hash = hashlib.sha256(
                    dup_data.encode("utf-8")
                ).hexdigest()
                StaticScanResultsDb.objects.filter(
                    vuln_id=vuln_id,
                    scan_id=scan_id,
                    organization=request.user.organization,
                ).update(
                    false_positive=false_positive,
                    vuln_status="Closed",
                    false_positive_hash=false_positive_hash,
                    note=notes,
                )

        all_vuln = StaticScanResultsDb.objects.filter(
            scan_id=scan_id,
            false_positive="No",
            vuln_status="Open",
            organization=request.user.organization,
        )

        total_high = len(all_vuln.filter(severity="High"))
        total_medium = len(all_vuln.filter(severity="Medium"))
        total_low = len(all_vuln.filter(severity="Low"))
        total_info = len(all_vuln.filter(severity="Informational"))
        total_dup = len(all_vuln.filter(vuln_duplicate="Yes"))
        total_vul = total_high + total_medium + total_low + total_info

        StaticScansDb.objects.filter(
            scan_id=scan_id, organization=request.user.organization
        ).update(
            total_vul=total_vul,
            high_vul=total_high,
            medium_vul=total_medium,
            low_vul=total_low,
            info_vul=total_info,
            total_dup=total_dup,
        )
        return HttpResponseRedirect(
            reverse("staticscanners:list_vuln_info")
            + "?scan_id=%s&scan_name=%s" % (scan_id, vuln_name)
        )


class SastScanDetails(APIView):
    enderer_classes = [TemplateHTMLRenderer]
    template_name = "staticscanners/scans/vuln_details.html"

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        jira_server = None
        jira_username = None
        jira_password = None
        jira_projects = None
        vuln_id = request.GET["vuln_id"]
        jira_setting = jirasetting.objects.filter(
            organization=request.user.organization
        )
        # user = request.user

        for jira in jira_setting:
            jira_server = jira.jira_server
            jira_username = jira.jira_username
            jira_password = jira.jira_password

        if jira_username is not None:
            jira_username = signing.loads(jira_username)

        if jira_password is not None:
            jira_password = signing.loads(jira_password)

        options = {"server": jira_server}
        try:
            if jira_username is not None and jira_username != "":
                jira_ser = JIRA(
                    options,
                    basic_auth=(jira_username, jira_password),
                    max_retries=0,
                    timeout=30,
                )
            else:
                jira_ser = JIRA(
                    options, token_auth=jira_password, max_retries=0, timeout=30
                )
            jira_projects = jira_ser.projects()
        except Exception as e:
            print(e)
            jira_projects = None
            # notify.send(user, recipient=user, verb="Jira settings not found")

        vul_dat = StaticScanResultsDb.objects.filter(
            vuln_id=vuln_id, organization=request.user.organization
        ).order_by("vuln_id")

        return render(
            request,
            "staticscanners/scans/vuln_details.html",
            {"vul_dat": vul_dat, "jira_projects": jira_projects},
        )


class SastScanDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "staticscanners/scans/list_scans.html"

    permission_classes = (
        IsAuthenticated,
        permissions.IsAnalyst,
    )

    def post(self, request):
        scan_id = request.POST.get("scan_id")

        scan_item = str(scan_id)
        value = scan_item.replace(" ", "")
        value_split = value.split(",")
        split_length = value_split.__len__()
        # print "split_length", split_length
        for i in range(0, split_length):
            scan_id = value_split.__getitem__(i)

            item = StaticScansDb.objects.filter(
                scan_id=scan_id, organization=request.user.organization
            )
            item.delete()
            item_results = StaticScanResultsDb.objects.filter(
                scan_id=scan_id, organization=request.user.organization
            )
            item_results.delete()
        return HttpResponseRedirect(reverse("staticscanners:list_scans"))


class SastScanVulnDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "staticscanners/scans/list_vuln_info.html"

    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def post(self, request):
        vuln_id = request.POST.get("vuln_id")
        scan_id = request.POST.get("scan_id")

        scan_item = str(vuln_id)
        value = scan_item.replace(" ", "")
        value_split = value.split(",")
        split_length = value_split.__len__()
        # print "split_length", split_length
        for i in range(0, split_length):
            vuln_id = value_split.__getitem__(i)
            delete_vuln = StaticScanResultsDb.objects.filter(
                vuln_id=vuln_id, organization=request.user.organization
            )
            delete_vuln.delete()
        all_vuln = StaticScanResultsDb.objects.filter(
            scan_id=scan_id, organization=request.user.organization
        )

        total_vul = len(all_vuln)
        total_critical = len(all_vuln.filter(severity="Critical"))
        total_high = len(all_vuln.filter(severity="High"))
        total_medium = len(all_vuln.filter(severity="Medium"))
        total_low = len(all_vuln.filter(severity="Low"))
        total_info = len(all_vuln.filter(severity="Information"))

        StaticScansDb.objects.filter(
            scan_id=scan_id, organization=request.user.organization
        ).update(
            total_vul=total_vul,
            critical_vul=total_critical,
            high_vul=total_high,
            medium_vul=total_medium,
            low_vul=total_low,
            info_vul=total_info,
        )
        return HttpResponseRedirect(
            reverse("staticscanners:list_vuln") + "?scan_id=%s" % (scan_id)
        )


class SastScanVulnList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "staticscanners/scans/list_vuln.html"

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        scan_id = request.GET["scan_id"]
        all_vuln = (
            StaticScanResultsDb.objects.filter(
                scan_id=scan_id, organization=request.user.organization
            )
            .distinct()
            .values(
                "title",
                "severity",
                "vuln_status",
                "severity_color",
                "scanner",
                "note",
                "scan_id",
            )
            .exclude(vuln_status="Duplicate")
        )

        return render(
            request,
            "staticscanners/scans/list_vuln.html",
            {
                "all_vuln": all_vuln,
                "scan_id": scan_id,
            },
        )


# ─────────────────────────────────────────────────────────────────────────────
# BANDIT SCANNER
# ─────────────────────────────────────────────────────────────────────────────

def _bandit_severity(sev):
    mapping = {"HIGH": "High", "MEDIUM": "Medium", "LOW": "Low"}
    return mapping.get(sev.upper(), "Informational")

def _bandit_color(sev):
    mapping = {"High": "danger", "Medium": "warning", "Low": "info"}
    return mapping.get(sev, "info")


def _run_bandit_scan(scan_path, project, scan_id, user, organization):
    """Run bandit in a background thread and save results."""
    date_time = datetime.now()
    try:
        result = subprocess.run(
            ["bandit", "-r", scan_path, "-f", "json", "-q"],
            capture_output=True, text=True, timeout=300
        )
        output = result.stdout or result.stderr
        data = json.loads(output)
        results = data.get("results", [])

        total_high = total_medium = total_low = total_info = 0

        for item in results:
            sev = _bandit_severity(item.get("issue_severity", "LOW"))
            sev_color = _bandit_color(sev)
            title = item.get("issue_text", "Unknown Issue")
            filename = item.get("filename", "")
            line = str(item.get("line_number", ""))
            cwe = item.get("issue_cwe", {}).get("id", "")
            ref = item.get("more_info", "")

            dup_data = title + filename + str(line)
            dup_hash = hashlib.sha256(dup_data.encode()).hexdigest()

            StaticScanResultsDb(
                vuln_id=uuid.uuid4(),
                scan_id=scan_id,
                project=project,
                title=title,
                severity=sev,
                severity_color=sev_color,
                fileName=filename + ":" + line,
                description="CWE-" + str(cwe) if cwe else title,
                reference=ref,
                false_positive="No",
                vuln_status="Open",
                vuln_duplicate="No",
                scanner="Bandit",
                organization=organization,
            ).save()

            if sev == "High": total_high += 1
            elif sev == "Medium": total_medium += 1
            elif sev == "Low": total_low += 1
            else: total_info += 1

        total_vul = total_high + total_medium + total_low + total_info
        StaticScansDb.objects.filter(scan_id=scan_id).update(
            scan_status="100",
            total_vul=total_vul,
            high_vul=total_high,
            medium_vul=total_medium,
            low_vul=total_low,
            info_vul=total_info,
        )
        notify.send(user, recipient=user, verb="Bandit scan completed: %d issues" % total_vul)
    except FileNotFoundError:
        StaticScansDb.objects.filter(scan_id=scan_id).update(scan_status="Failed: bandit not installed")
        print("[VAPT] bandit not found. Install: pip install bandit")
    except Exception as e:
        StaticScansDb.objects.filter(scan_id=scan_id).update(scan_status="Failed")
        print("[VAPT] Bandit error:", e)


class BanditScanLaunch(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "staticscanners/scans/list_scans.html"
    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        """Render the Bandit scan list + launch form"""
        from projects.models import ProjectDb
        all_scans = StaticScansDb.objects.filter(organization=request.user.organization, scanner="Bandit")
        all_projects = ProjectDb.objects.filter(organization=request.user.organization)
        all_notify = Notification.objects.unread()
        return render(
            request,
            "staticscanners/scans/list_scans.html",
            {"all_scans": all_scans, "all_projects": all_projects, "message": all_notify, "scanner": "Bandit"},
        )

    def post(self, request):
        user = request.user
        scan_path = request.POST.get("scan_path", "").strip()
        project_id = request.POST.get("project_id", None)

        # Resolve UUID → ProjectDb object to avoid FK int/UUID mismatch
        project = None
        if project_id:
            try:
                from projects.models import ProjectDb
                project = ProjectDb.objects.get(uu_id=project_id)
            except Exception:
                project = None

        if not scan_path or not os.path.exists(scan_path):
            notify.send(user, recipient=user, verb="Bandit: invalid or missing scan path")
            return HttpResponseRedirect(reverse("staticscanners:list_scans"))

        scan_id = uuid.uuid4()
        date_time = datetime.now()

        StaticScansDb(
            scan_id=scan_id,
            project=project,
            project_name=scan_path,
            date_time=date_time,
            scanner="Bandit",
            scan_status="Scanning",
            scan_date=date_time.strftime("%Y-%m-%d"),
            organization=request.user.organization,
        ).save()

        thread = threading.Thread(
            target=_run_bandit_scan,
            args=(scan_path, project, scan_id, user, request.user.organization)
        )
        thread.daemon = True
        thread.start()

        notify.send(user, recipient=user, verb="Bandit scan started on %s" % scan_path)
        return HttpResponseRedirect(reverse("staticscanners:list_scans"))


# ─────────────────────────────────────────────────────────────────────────────
# SEMGREP SCANNER
# ─────────────────────────────────────────────────────────────────────────────

def _semgrep_severity(sev):
    mapping = {"ERROR": "High", "WARNING": "Medium", "INFO": "Low"}
    return mapping.get(sev.upper(), "Informational")

def _semgrep_color(sev):
    mapping = {"High": "danger", "Medium": "warning", "Low": "info"}
    return mapping.get(sev, "info")


def _run_semgrep_scan(scan_path, project, scan_id, user, organization):
    """Run semgrep in a background thread and save results."""
    date_time = datetime.now()
    try:
        result = subprocess.run(
            ["semgrep", "--config", "auto", scan_path, "--json", "--quiet"],
            capture_output=True, text=True, timeout=600
        )
        output = result.stdout
        data = json.loads(output)
        results = data.get("results", [])

        total_high = total_medium = total_low = total_info = 0

        for item in results:
            raw_sev = item.get("extra", {}).get("severity", "INFO")
            sev = _semgrep_severity(raw_sev)
            sev_color = _semgrep_color(sev)
            title = item.get("check_id", "Unknown Rule")
            filename = item.get("path", "")
            line = str(item.get("start", {}).get("line", ""))
            description = item.get("extra", {}).get("message", title)
            ref = item.get("extra", {}).get("references", [""])
            ref = ref[0] if ref else ""

            dup_data = title + filename + line
            dup_hash = hashlib.sha256(dup_data.encode()).hexdigest()

            StaticScanResultsDb(
                vuln_id=uuid.uuid4(),
                scan_id=scan_id,
                project=project,
                title=title,
                severity=sev,
                severity_color=sev_color,
                fileName=filename + ":" + line,
                description=description,
                reference=ref,
                false_positive="No",
                vuln_status="Open",
                vuln_duplicate="No",
                scanner="Semgrep",
                organization=organization,
            ).save()

            if sev == "High": total_high += 1
            elif sev == "Medium": total_medium += 1
            elif sev == "Low": total_low += 1
            else: total_info += 1

        total_vul = total_high + total_medium + total_low + total_info
        StaticScansDb.objects.filter(scan_id=scan_id).update(
            scan_status="100",
            total_vul=total_vul,
            high_vul=total_high,
            medium_vul=total_medium,
            low_vul=total_low,
            info_vul=total_info,
        )
        notify.send(user, recipient=user, verb="Semgrep scan completed: %d issues" % total_vul)
    except FileNotFoundError:
        StaticScansDb.objects.filter(scan_id=scan_id).update(scan_status="Failed: semgrep not installed")
        print("[VAPT] semgrep not found. Install: pip install semgrep")
    except Exception as e:
        StaticScansDb.objects.filter(scan_id=scan_id).update(scan_status="Failed")
        print("[VAPT] Semgrep error:", e)


class SemgrepScanLaunch(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "staticscanners/scans/list_scans.html"
    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        """Render the Semgrep scan list + launch form"""
        from projects.models import ProjectDb
        all_scans = StaticScansDb.objects.filter(organization=request.user.organization, scanner="Semgrep")
        all_projects = ProjectDb.objects.filter(organization=request.user.organization)
        all_notify = Notification.objects.unread()
        return render(
            request,
            "staticscanners/scans/list_scans.html",
            {"all_scans": all_scans, "all_projects": all_projects, "message": all_notify, "scanner": "Semgrep"},
        )

    def post(self, request):
        user = request.user
        scan_path = request.POST.get("scan_path", "").strip()
        project_id = request.POST.get("project_id", None)

        # Resolve UUID → ProjectDb object to avoid FK int/UUID mismatch
        project = None
        if project_id:
            try:
                from projects.models import ProjectDb
                project = ProjectDb.objects.get(uu_id=project_id)
            except Exception:
                project = None

        if not scan_path or not os.path.exists(scan_path):
            notify.send(user, recipient=user, verb="Semgrep: invalid or missing scan path")
            return HttpResponseRedirect(reverse("staticscanners:list_scans"))

        scan_id = uuid.uuid4()
        date_time = datetime.now()

        StaticScansDb(
            scan_id=scan_id,
            project=project,
            project_name=scan_path,
            date_time=date_time,
            scanner="Semgrep",
            scan_status="Scanning",
            scan_date=date_time.strftime("%Y-%m-%d"),
            organization=request.user.organization,
        ).save()

        thread = threading.Thread(
            target=_run_semgrep_scan,
            args=(scan_path, project, scan_id, user, request.user.organization)
        )
        thread.daemon = True
        thread.start()

        notify.send(user, recipient=user, verb="Semgrep scan started on %s" % scan_path)
        return HttpResponseRedirect(reverse("staticscanners:list_scans"))
