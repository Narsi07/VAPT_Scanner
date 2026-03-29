# -*- coding: utf-8 -*-
# VAPT Security Platform

from __future__ import print_function

from vaptapi.models import OrgAPIKey
from tools.models import NmapResultDb, NmapScanDb


def xml_parser(root, project_id, scan_id, request=None, organization=None):
    """
    Parse nmap XML output and save results to the database.

    :param root: ElementTree root of the nmap XML
    :param project_id: project UUID string (unused, kept for API compat)
    :param scan_id: UUID for this scan
    :param request: HTTP request (optional — not needed from background thread)
    :param organization: Organization object (required when request is None)
    """
    # Resolve organization from request if not passed directly
    if organization is None:
        api_key = request.META.get("HTTP_X_API_KEY")
        key_object = OrgAPIKey.objects.filter(api_key=api_key).first()
        if str(request.user) == 'AnonymousUser':
            organization = key_object.organization
        else:
            organization = request.user.organization

    ip_address = None
    used_state = used_portid = used_proto = None

    # ── Pass 1: save one NmapResultDb row per actual port ──────────────────
    for nmap in root:
        for scaninfo in nmap:

            # Extract IPv4 address
            if scaninfo.tag == "address":
                ip = scaninfo.attrib
                if ip.get("addrtype") == "ipv4":
                    ip_address = ip.get("addr")

            # Extract portused (OS detection used port)
            if scaninfo.tag == "portused":
                for key, value in scaninfo.attrib.items():
                    if key == "state":
                        used_state = value
                    elif key == "portid":
                        used_portid = value
                    elif key == "proto":
                        used_proto = value

            # Only iterate ports container
            if scaninfo.tag != "ports":
                continue

            for s in scaninfo:
                if s.tag != "port":
                    continue

                # Reset all per-port variables for each port entry
                port = protocol = state = reason = reason_ttl = None
                version = extrainfo = name = conf = method = None
                type_p = osfamily = vendor = osgen = accuracy = cpe = None

                # Port number and protocol from attributes
                port = s.attrib.get("portid")
                protocol = s.attrib.get("protocol")

                print(f"[nmap_parser] port={port} proto={protocol}")

                # Parse child elements: state, service, script, cpe
                for ss in s:
                    if ss.tag == "state":
                        state = ss.attrib.get("state")
                        reason = ss.attrib.get("reason")
                        reason_ttl = ss.attrib.get("reason_ttl")

                    elif ss.tag == "service":
                        name = ss.attrib.get("name")
                        version = ss.attrib.get("version")
                        extrainfo = ss.attrib.get("extrainfo")
                        conf = ss.attrib.get("conf")
                        method = ss.attrib.get("method")
                        type_p = ss.attrib.get("type")
                        osfamily = ss.attrib.get("osfamily")
                        vendor = ss.attrib.get("vendor")
                        osgen = ss.attrib.get("osgen")
                        accuracy = ss.attrib.get("accuracy")
                        # CPE is a child of service
                        for cpe_el in ss:
                            if cpe_el.tag == "cpe":
                                cpe = cpe_el.text

                # Only save if we have a real port number
                if port:
                    NmapResultDb(
                        scan_id=scan_id,
                        ip_address=ip_address,
                        port=port,
                        protocol=protocol,
                        state=state,
                        reason=reason,
                        reason_ttl=reason_ttl,
                        version=version,
                        extrainfo=extrainfo,
                        name=name,
                        conf=conf,
                        method=method,
                        type_p=type_p,
                        osfamily=osfamily,
                        vendor=vendor,
                        osgen=osgen,
                        accuracy=accuracy,
                        cpe=cpe,
                        used_state=used_state,
                        used_portid=used_portid,
                        used_proto=used_proto,
                        organization=organization,
                    ).save()

    # ── Pass 2: update NmapScanDb with port counts ──────────────────────────
    for nmap in root:
        for scaninfo in nmap:
            if scaninfo.tag == "address":
                ip = scaninfo.attrib
                if ip.get("addrtype") == "ipv4":
                    ip_address = ip.get("addr")
                    if ip_address:
                        total_ports = NmapResultDb.objects.filter(
                            ip_address=ip_address, organization=organization
                        ).count()
                        total_open_p = NmapResultDb.objects.filter(
                            ip_address=ip_address, organization=organization, state="open"
                        ).count()
                        total_close_p = NmapResultDb.objects.filter(
                            ip_address=ip_address, organization=organization, state="closed"
                        ).count()

                        NmapScanDb.objects.filter(
                            scan_id=scan_id, organization=organization
                        ).update(
                            scan_ip=ip_address,
                            total_ports=total_ports,
                            total_open_ports=total_open_p,
                            total_close_ports=total_close_p,
                        )


parser_header_dict = {}
