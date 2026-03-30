# -*- coding: utf-8 -*-
# VAPT Security Platform

import threading
import uuid

from django.shortcuts import HttpResponseRedirect, render
from notifications.signals import notify

from tools.models import NmapResultDb, NmapScanDb, NmapVulnersPortResultDb
from tools.nmap_vulners.nmap_vulners_scan import run_nmap_vulners


def nmap_vulners_scan(request):
    """List all Nmap+Vulners scans."""
    all_nmap = NmapScanDb.objects.filter(
        organization=request.user.organization,
        is_vulners=True,
    ).order_by('-created_time')
    return render(
        request, "tools/nmap_scan.html", {"all_nmap": all_nmap, "is_vulners": True}
    )


def nmap_vulners(request):
    """Launch a Nmap+Vulners scan in a background thread."""
    user = request.user

    if request.method == "POST":
        ip_address = request.POST.get("ip")
        project_id = request.POST.get("project_id")
        organization = request.user.organization

        # Resolve project UUID → ProjectDb object
        project = None
        if project_id:
            try:
                from projects.models import ProjectDb
                project = ProjectDb.objects.get(uu_id=project_id)
            except Exception:
                project = None

        if not ip_address:
            notify.send(user, recipient=user, verb="Nmap+Vulners: IP address is required")
            return HttpResponseRedirect("/tools/nmap_vulners_scan/")

        # Create placeholder record BEFORE thread starts so user sees scan immediately
        scan_id = uuid.uuid4()
        NmapScanDb.objects.create(
            scan_id=scan_id,
            scan_ip=ip_address,
            project=project,
            organization=organization,
            is_vulners=True,
        )

        print("[VAPT] Starting Nmap+Vulners scan on", ip_address)

        # Launch in background thread
        t = threading.Thread(
            target=_run_nmap_vulners_background,
            args=(scan_id, ip_address, project, organization, user),
            daemon=True,
        )
        t.start()

        notify.send(user, recipient=user, verb="Nmap+Vulners scan started for: %s" % ip_address)
        return HttpResponseRedirect("/tools/nmap_vulners_scan/")

    elif request.method == "GET":
        ip_address = request.GET.get("ip")
        all_nmap = NmapVulnersPortResultDb.objects.filter(
            ip_address=ip_address,
        ) if ip_address else []

    return render(request, "tools/nmap_vulners_list.html", {"all_nmap": all_nmap})


def _run_nmap_vulners_background(scan_id, ip_address, project, organization, user):
    """Background thread runner for Nmap+Vulners scan."""
    try:
        run_nmap_vulners(
            scan_id=scan_id,
            ip_addr=ip_address,
            project=project,
            organization=organization,
        )
        notify.send(user, recipient=user, verb="Nmap+Vulners scan completed: %s" % ip_address)
        print("[VAPT] Nmap+Vulners scan completed for", ip_address)
    except Exception as e:
        print("[VAPT] Nmap+Vulners error:", e)
        # Mark the placeholder as failed
        NmapScanDb.objects.filter(scan_id=scan_id).update(total_ports='0')
        notify.send(user, recipient=user, verb="Nmap+Vulners scan failed: %s — %s" % (ip_address, str(e)))


def nmap_vulners_port(request):
    ip_address = request.GET.get("ip")
    port = request.GET.get("port")
    if not (ip_address and port):
        raise ValueError("Nmap Vulners Port info: both IP and port must be present.")

    port_info = NmapVulnersPortResultDb.objects.filter(ip_address=ip_address, port=port)

    cve_info = []
    first = port_info.first()
    if first and first.vulners_extrainfo:
        for line in first.vulners_extrainfo.split("\n"):
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split("\t") if p.strip()]
            if len(parts) >= 2:
                cve_info.append({
                    "cve": parts[0],
                    "cvss": parts[1] if len(parts) > 1 else "—",
                    "link": parts[2] if len(parts) > 2 else "",
                })

    return render(
        request,
        "tools/nmap_vulners_port_list.html",
        {"ip": ip_address, "port": port, "cve_info": cve_info},
    )
