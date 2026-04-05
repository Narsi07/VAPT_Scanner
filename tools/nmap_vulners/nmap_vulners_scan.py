# -*- coding: utf-8 -*-
# VAPT Security Platform

import hashlib
import os
import re
import uuid
from datetime import datetime

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


# ─────────────────────────────────────────────────────────────────────────────
# SEVERITY HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _cvss_to_severity(cvss_score):
    """Map a CVSS score string to Critical/High/Medium/Low."""
    try:
        score = float(cvss_score)
    except (ValueError, TypeError):
        return "Low"
    if score >= 9.0:
        return "Critical"
    elif score >= 7.0:
        return "High"
    elif score >= 4.0:
        return "Medium"
    return "Low"


def _severity_color(severity):
    return {
        "Critical": "critical",
        "High": "danger",
        "Medium": "warning",
        "Low": "info",
    }.get(severity, "info")


# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD FIX: write CVE records → NetworkScanResultsDb & NetworkScanDb
# ─────────────────────────────────────────────────────────────────────────────

def _write_network_vuln_records(scan_id, ip_addr, project, organization):
    """
    Parse vulners_extrainfo CVE lines, create NetworkScanResultsDb records,
    then update NetworkScanDb with aggregated severity counts so that the
    dashboard 'Network Issues' card and pie chart are populated correctly.
    """
    from networkscanners.models import NetworkScanDb, NetworkScanResultsDb

    port_results = NmapVulnersPortResultDb.objects.filter(
        ip_address=ip_addr, scan_id=scan_id
    )

    total_critical = total_high = total_medium = total_low = 0

    for port_obj in port_results:
        if not port_obj.vulners_extrainfo:
            continue

        for line in port_obj.vulners_extrainfo.split("\n"):
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split("\t") if p.strip()]
            if len(parts) < 2:
                continue

            cve_id = parts[0]
            cvss_raw = parts[1]
            severity = _cvss_to_severity(cvss_raw)
            sev_color = _severity_color(severity)

            title = "{} on port {}/{}".format(
                cve_id, port_obj.port, port_obj.protocol or "tcp"
            )
            description = (
                "CVE {} detected on {} port {}/{} "
                "(service: {}, version: {}). CVSS Score: {}".format(
                    cve_id,
                    ip_addr,
                    port_obj.port,
                    port_obj.protocol or "tcp",
                    port_obj.name or "unknown",
                    port_obj.version or "unknown",
                    cvss_raw,
                )
            )

            dup_data = str(cve_id) + str(ip_addr) + str(port_obj.port)
            dup_hash = hashlib.sha256(dup_data.encode("utf-8")).hexdigest()

            # Skip duplicates within this scan
            if NetworkScanResultsDb.objects.filter(
                scan_id=scan_id, dup_hash=dup_hash
            ).exists():
                continue

            record_kwargs = dict(
                vuln_id=uuid.uuid4(),
                scan_id=scan_id,
                title=title,
                severity=severity,
                severity_color=sev_color,
                description=description,
                port=str(port_obj.port),
                ip=ip_addr,
                scanner="Nmap-Vulners",
                dup_hash=dup_hash,
                vuln_duplicate="No",
                vuln_status="Open",
                false_positive="No",
                date_time=datetime.now(),
            )
            if project:
                record_kwargs["project"] = project
            if organization:
                record_kwargs["organization"] = organization

            NetworkScanResultsDb(**record_kwargs).save()

            if severity == "Critical":
                total_critical += 1
            elif severity == "High":
                total_high += 1
            elif severity == "Medium":
                total_medium += 1
            else:
                total_low += 1

    total_vul = total_critical + total_high + total_medium + total_low

    # Update or create the NetworkScanDb row the dashboard reads
    net_qs = NetworkScanDb.objects.filter(scan_id=scan_id)
    if net_qs.exists():
        net_qs.update(
            total_vul=total_vul,
            critical_vul=total_critical,
            high_vul=total_high,
            medium_vul=total_medium,
            low_vul=total_low,
            scan_status="Completed",
        )
    else:
        net_obj = NetworkScanDb(
            scan_id=scan_id,
            ip=ip_addr,
            scan_date=str(datetime.now().date()),
            scan_status="Completed",
            total_vul=total_vul,
            critical_vul=total_critical,
            high_vul=total_high,
            medium_vul=total_medium,
            low_vul=total_low,
        )
        if project:
            net_obj.project = project
        if organization:
            net_obj.organization = organization
        net_obj.save()

    print(
        "[VAPT] Nmap+Vulners → dashboard: Critical=%d High=%d Medium=%d Low=%d Total=%d"
        % (total_critical, total_high, total_medium, total_low, total_vul)
    )


# ─────────────────────────────────────────────────────────────────────────────
# MAIN SCAN RUNNER
# ─────────────────────────────────────────────────────────────────────────────

def run_nmap_vulners(ip_addr="", project=None, organization=None, scan_id=None):
    if not ip_addr:
        raise ValueError("[NMAP_VULNERS] ip_addr must be specified")

    try:
        import nmap
    except ImportError:
        raise RuntimeError(
            "[NMAP_VULNERS] python-nmap not installed. Run: pip install python-nmap"
        )

    if scan_id is None:
        scan_id = uuid.uuid4()

    nmap_vulners_path = os.path.join(
        settings.BASE_DIR, "tools/nmap_vulners/vulners.nse"
    )

    # Build nmap arguments from settings (with safe defaults)
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

    # Clear old port results for this IP before saving fresh ones
    NmapVulnersPortResultDb.objects.filter(ip_address=ip_addr).delete()

    for host, host_data in scan.items():
        print("[VAPT] Nmap+Vulners parsing host:", host)
        parse_port("tcp", host, host_data, scan_id, project, organization)
        parse_port("udp", host, host_data, scan_id, project, organization)

        # Count open/closed ports
        all_data = NmapVulnersPortResultDb.objects.filter(ip_address=host)
        total_ports = all_data.count()
        total_open_p = all_data.filter(state="open").count()
        total_close_p = all_data.filter(state="closed").count()

        print("[VAPT] Nmap+Vulners: %s — %d open / %d closed ports" % (
            host, total_open_p, total_close_p))

        # Update the placeholder NmapScanDb record
        updated = NmapScanDb.objects.filter(scan_id=scan_id).update(
            scan_ip=host,
            project=project,
            total_ports=total_ports,
            total_open_ports=total_open_p,
            total_close_ports=total_close_p,
        )
        if not updated:
            NmapScanDb(
                scan_id=scan_id,
                project=project,
                scan_ip=host,
                total_ports=total_ports,
                total_open_ports=total_open_p,
                total_close_ports=total_close_p,
                organization=organization,
                is_vulners=True,
            ).save()

        # ── Write CVE records to NetworkScanResultsDb and update NetworkScanDb ──
        _write_network_vuln_records(
            scan_id=scan_id,
            ip_addr=host,
            project=project,
            organization=organization,
        )
