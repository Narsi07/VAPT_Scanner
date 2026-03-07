# -*- coding: utf-8 -*-
# VAPT Security Platform

import os
import uuid

from django.conf import settings

from vaptsettings.models import NmapVulnersSettingDb
from tools.models import NmapScanDb, NmapVulnersPortResultDb


def parse_port(proto, ip_addr, host_data, scan_id, project, organization):
    ports = host_data.get(proto)
    if not ports:
        return

    for port, portData in dict(ports).items():
        nmap_obj, _ = NmapVulnersPortResultDb.objects.get_or_create(
            ip_address=ip_addr, port=port
        )

        nmap_obj.protocol = proto
        nmap_obj.state = portData.get("state")
        nmap_obj.scan_id = scan_id
        nmap_obj.project = project
        nmap_obj.reason = portData.get("reason")
        nmap_obj.reason_ttl = portData.get("reason_ttl")
        nmap_obj.version = portData.get("version")
        nmap_obj.extrainfo = portData.get("extrainfo")
        nmap_obj.name = portData.get("name")
        nmap_obj.conf = portData.get("conf")
        nmap_obj.method = portData.get("method")
        nmap_obj.type_p = portData.get("type_p")
        nmap_obj.osfamily = portData.get("osfamily")
        nmap_obj.vendor = portData.get("vendor")
        nmap_obj.osgen = portData.get("osgen")
        nmap_obj.accuracy = portData.get("accuracy")
        nmap_obj.cpe = portData.get("cpe")
        nmap_obj.used_state = portData.get("used_state")
        nmap_obj.used_portid = portData.get("used_portid")
        nmap_obj.used_proto = portData.get("used_proto")
        if organization:
            nmap_obj.organization = organization
        if "script" in portData and "vulners" in portData.get("script", {}):
            nmap_obj.vulners_extrainfo = (
                portData.get("script").get("vulners").strip("\n\t ")
            )

        nmap_obj.save()


def run_nmap_vulners(ip_addr="", project=None, organization=None):
    if not ip_addr:
        raise ValueError("[NMAP_VULNERS] ip_addr must be specified")

    try:
        import nmap
    except ImportError:
        raise RuntimeError("[NMAP_VULNERS] python-nmap not installed. Run: pip install python-nmap")

    scan_id = uuid.uuid4()

    nmap_vulners_path = os.path.join(
        settings.BASE_DIR, "tools/nmap_vulners/vulners.nse"
    )

    # Build nmap arguments from settings (with safe defaults if no settings row exists)
    nv_version = True   # -sV default
    nv_online = True    # -Pn default
    nv_timing = 4       # -T4 default

    all_nv = NmapVulnersSettingDb.objects.all()
    if all_nv.exists():
        for nv in all_nv:
            nv_version = bool(nv.version)
            nv_online = bool(nv.online)
            nv_timing = int(nv.timing)

    args = ""
    if nv_version:
        args += " -sV"
    if nv_online:
        args += " -Pn"
    if nv_timing:
        args += " -T" + str(nv_timing)
    args += " --max-retries 1 --host-timeout 300s"
    args += " --script " + nmap_vulners_path

    print("[VAPT] Nmap+Vulners args:", args)

    nm = nmap.PortScanner()
    result = nm.scan(hosts=ip_addr, arguments=args)
    scan = result.get("scan", {})

    if not scan:
        print("[VAPT] Nmap+Vulners: no hosts found in scan result for", ip_addr)
        return

    # Clear old results for this IP before saving new ones
    NmapVulnersPortResultDb.objects.filter(ip_address=ip_addr).delete()

    for host, host_data in scan.items():
        print("[VAPT] Nmap+Vulners parsing host:", host)
        parse_port("tcp", host, host_data, scan_id, project, organization)
        parse_port("udp", host, host_data, scan_id, project, organization)

        # Count ports
        all_data = NmapVulnersPortResultDb.objects.filter(ip_address=host)
        total_ports = all_data.count()
        total_open_p = NmapVulnersPortResultDb.objects.filter(
            ip_address=host, state="open"
        ).count()
        total_close_p = NmapVulnersPortResultDb.objects.filter(
            ip_address=host, state="closed"
        ).count()

        print("[VAPT] Nmap+Vulners: %s — %d open / %d closed ports" % (
            host, total_open_p, total_close_p))

        NmapScanDb(
            scan_id=scan_id,
            project=project,
            scan_ip=host,
            total_ports=total_ports,
            total_open_ports=total_open_p,
            total_close_ports=total_close_p,
            organization=organization,
        ).save()
