# -*- coding: utf-8 -*-
# VAPT Security Platform

import threading
from itertools import starmap

from django.shortcuts import HttpResponseRedirect, render
from notifications.signals import notify

from tools.models import NmapResultDb, NmapScanDb, NmapVulnersPortResultDb
from tools.nmap_vulners.nmap_vulners_scan import run_nmap_vulners


def nmap_vulners_scan(request):
    """List all Nmap+Vulners scans."""
    all_nmap = NmapScanDb.objects.filter(organization=request.user.organization)
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
            return HttpResponseRedirect("/tools/nmap_scan/")

        print("[VAPT] Starting Nmap+Vulners scan on", ip_address)

        # Launch in background thread so browser doesn't block
        t = threading.Thread(
            target=_run_nmap_vulners_background,
            args=(ip_address, project, organization, user),
            daemon=True,
        )
        t.start()

        notify.send(user, recipient=user, verb="Nmap+Vulners scan started for: %s" % ip_address)
        return HttpResponseRedirect("/tools/nmap_scan/")

    elif request.method == "GET":
        ip_address = request.GET.get("ip")
        all_nmap = NmapVulnersPortResultDb.objects.filter(
            ip_address=ip_address,
        ) if ip_address else []

    return render(request, "tools/nmap_vulners_list.html", {"all_nmap": all_nmap})


def _run_nmap_vulners_background(ip_address, project, organization, user):
    """Background thread runner for Nmap+Vulners scan."""
    try:
        run_nmap_vulners(
            ip_addr=ip_address,
            project=project,
            organization=organization,
        )
        notify.send(user, recipient=user, verb="Nmap+Vulners scan completed: %s" % ip_address)
        print("[VAPT] Nmap+Vulners scan completed for", ip_address)
    except Exception as e:
        print("[VAPT] Nmap+Vulners error:", e)
        notify.send(user, recipient=user, verb="Nmap+Vulners scan failed: %s — %s" % (ip_address, str(e)))


def nmap_vulners_port(request):
    ip_address = request.GET.get("ip")
    port = request.GET.get("port")
    if not (ip_address and port):
        raise ValueError("Nmap Vulners Port info: both IP and port must be present.")

    port_info = NmapVulnersPortResultDb.objects.filter(ip_address=ip_address, port=port)

    cve_info = list()
    first = port_info.first()
    if first and first.vulners_extrainfo:
        info = first.vulners_extrainfo.split("\n\t")[1:]
        info_gen = starmap(lambda x: x.split("\t\t"), info)

        names = ("cve", "cvss", "link")
        cve_info = (dict(zip(names, info)) for info in info_gen)

    return render(
        request,
        "tools/nmap_vulners_port_list.html",
        {"ip": ip_address, "port": port, "cve_info": cve_info},
    )
