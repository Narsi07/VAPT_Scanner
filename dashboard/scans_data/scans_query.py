# -*- coding: utf-8 -*-
# VAPT Security Platform




from __future__ import unicode_literals

from itertools import chain

from django.db.models import Sum

try:
    from cloudscanners.models import CloudScansDb, CloudScansResultsDb
    CLOUD_AVAILABLE = True
except ImportError:
    CloudScansDb = None
    CloudScansResultsDb = None
    CLOUD_AVAILABLE = False
try:
    from compliance.models import (DockleScanDb, DockleScanResultsDb, InspecScanDb,
                                   InspecScanResultsDb)
    COMPLIANCE_AVAILABLE = True
except ImportError:
    DockleScanDb = None
    DockleScanResultsDb = None
    InspecScanDb = None
    InspecScanResultsDb = None
    COMPLIANCE_AVAILABLE = False

from networkscanners.models import NetworkScanDb, NetworkScanResultsDb
from staticscanners.models import StaticScanResultsDb, StaticScansDb
from webscanners.models import WebScanResultsDb, WebScansDb

# Create your views here.
chart = []
all_high_stat = ""
data = ""


def all_manual_scan(project_id, query):
    return 0


def all_pentest_web(project_id, query):
    return 0


def all_pentest_net(project_id, query):
    return 0


def all_vuln(project_id, query):
    all_vuln = 0

    if query == "total":
        try:
            all_sast_scan = int(
                StaticScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("total_vul")
                )["total_vul__sum"]
            )
        except Exception as e:
            #
            all_sast_scan = 0

        try:
            all_cloud_scan = int(
                CloudScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("total_vul")
                )["total_vul__sum"]
            )
        except Exception as e:
            #
            all_cloud_scan = 0

        try:
            all_dast_scan = int(
                WebScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("total_vul")
                )["total_vul__sum"]
            )
        except Exception as e:
            #
            all_dast_scan = 0

        try:
            all_net_scan = int(
                NetworkScanDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("total_vul")
                )["total_vul__sum"]
            )
        except Exception as e:
            #
            all_net_scan = 0

        all_vuln = (
            int(all_sast_scan)
            + int(all_dast_scan)
            + int(all_cloud_scan)
            + int(all_net_scan)
            + int(all_manual_scan(project_id=project_id, query=query))
        )
    elif query == "critical":
        try:
            all_sast_scan = int(
                StaticScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("critical_vul")
                )["critical_vul__sum"]
            )
        except Exception as e:
            #
            all_sast_scan = 0

        try:
            all_cloud_scan = int(
                CloudScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("critical_vul")
                )["critical_vul__sum"]
            )
        except Exception as e:
            #
            all_cloud_scan = 0

        try:
            all_dast_scan = int(
                WebScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("critical_vul")
                )["critical_vul__sum"]
            )
        except Exception as e:
            all_dast_scan = 0

        try:
            all_net_scan = int(
                NetworkScanDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("critical_vul")
                )["critical_vul__sum"]
            )
        except Exception as e:
            all_net_scan = 0

        all_vuln = (
            int(all_sast_scan)
            + int(all_dast_scan)
            + int(all_cloud_scan)
            + int(all_net_scan)
            + int(all_manual_scan(project_id=project_id, query=query))
        )
    elif query == "high":
        try:
            all_sast_scan = int(
                StaticScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("high_vul")
                )["high_vul__sum"]
            )
        except Exception as e:
            #
            all_sast_scan = 0

        try:
            all_cloud_scan = int(
                CloudScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("high_vul")
                )["high_vul__sum"]
            )
        except Exception as e:
            #
            all_cloud_scan = 0

        try:
            all_dast_scan = int(
                WebScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("high_vul")
                )["high_vul__sum"]
            )
        except Exception as e:
            all_dast_scan = 0

        try:
            all_net_scan = int(
                NetworkScanDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("high_vul")
                )["high_vul__sum"]
            )
        except Exception as e:
            all_net_scan = 0

        all_vuln = (
            int(all_sast_scan)
            + int(all_cloud_scan)
            + int(all_dast_scan)
            + int(all_net_scan)
            + int(all_manual_scan(project_id=project_id, query=query))
        )
    elif query == "medium":
        try:
            all_sast_scan = int(
                StaticScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("medium_vul")
                )["medium_vul__sum"]
            )
        except Exception as e:
            #
            all_sast_scan = 0

        try:
            all_cloud_scan = int(
                CloudScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("medium_vul")
                )["medium_vul__sum"]
            )
        except Exception as e:
            #
            all_cloud_scan = 0

        try:
            all_dast_scan = int(
                WebScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("medium_vul")
                )["medium_vul__sum"]
            )
        except Exception as e:
            all_dast_scan = 0

        try:
            all_net_scan = int(
                NetworkScanDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("medium_vul")
                )["medium_vul__sum"]
            )

        except Exception as e:
            #
            all_net_scan = 0

        all_vuln = (
            int(all_sast_scan)
            + int(all_dast_scan)
            + int(all_cloud_scan)
            + int(all_net_scan)
            + int(all_manual_scan(project_id=project_id, query=query))
        )
    elif query == "low":
        try:
            all_sast_scan = int(
                StaticScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("low_vul")
                )["low_vul__sum"]
            )
        except Exception as e:
            #
            all_sast_scan = 0

        try:
            all_cloud_scan = int(
                CloudScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("low_vul")
                )["low_vul__sum"]
            )
        except Exception as e:
            #
            all_cloud_scan = 0

        try:
            all_dast_scan = int(
                WebScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("low_vul")
                )["low_vul__sum"]
            )
        except Exception as e:
            #
            all_dast_scan = 0

        try:
            all_net_scan = int(
                NetworkScanDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("low_vul")
                )["low_vul__sum"]
            )
        except Exception as e:
            #
            all_net_scan = 0

        all_vuln = (
            int(all_sast_scan)
            + int(all_dast_scan)
            + int(all_cloud_scan)
            + int(all_net_scan)
            + int(all_manual_scan(project_id=project_id, query=query))
        )
    return all_vuln


def all_web(project_id, query):
    all_web = 0

    if query == "total":
        try:
            all_web = int(
                WebScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("total_vul")
                )["total_vul__sum"]
            )

        except Exception as e:
            #
            all_web = 0

    elif query == "critical":
        try:
            all_web = int(
                WebScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("critical_vul")
                )["critical_vul__sum"]
            )
        except Exception as e:
            #
            all_web = 0

    elif query == "high":
        try:
            all_web = int(
                WebScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("high_vul")
                )["high_vul__sum"]
            )
        except Exception as e:
            #
            all_web = 0

    elif query == "medium":
        try:
            all_web = int(
                WebScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("medium_vul")
                )["medium_vul__sum"]
            )
        except Exception as e:
            #
            all_web = 0

    elif query == "low":
        try:
            all_web = int(
                WebScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("low_vul")
                )["low_vul__sum"]
            )
        except Exception as e:
            #
            all_web = 0

    return all_web


def all_net(project_id, query):
    all_net = 0

    if query == "total":
        try:
            all_net = int(
                NetworkScanDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("total_vul")
                )["total_vul__sum"]
            )
        except Exception as e:
            #
            all_net = 0

    elif query == "critical":
        try:
            all_net = int(
                NetworkScanDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("critical_vul")
                )["critical_vul__sum"]
            )
        except Exception as e:
            #
            all_net = 0

    elif query == "high":
        try:
            all_net = int(
                NetworkScanDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("high_vul")
                )["high_vul__sum"]
            )
        except Exception as e:
            #
            all_net = 0
    elif query == "medium":
        try:
            all_net = int(
                NetworkScanDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("medium_vul")
                )["medium_vul__sum"]
            )
        except Exception as e:
            all_net = 0

    elif query == "low":
        try:
            all_net = int(
                NetworkScanDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("low_vul")
                )["low_vul__sum"]
            )
        except Exception as e:
            all_net = 0

    return all_net


def all_compliance(project_id, query):
    all_compliance = 0

    if query == "total":
        all_compliance = int(all_inspec(project_id=project_id, query=query)) + int(
            all_dockle(project_id=project_id, query=query)
        )
    elif query == "failed":
        all_compliance = int(all_inspec(project_id=project_id, query=query)) + int(
            all_dockle(project_id=project_id, query="fatal")
        )
    elif query == "passed":
        all_compliance = int(all_inspec(project_id=project_id, query=query)) + int(
            all_dockle(project_id=project_id, query="info")
        )
    elif query == "skipped":
        all_compliance = int(all_inspec(project_id=project_id, query=query))

    return all_compliance


def all_static(project_id, query):
    all_static = 0

    if query == "total":
        try:
            all_static = int(
                StaticScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("total_vul")
                )["total_vul__sum"]
            )
        except Exception as e:
            all_static = 0

    elif query == "critical":
        try:
            all_static = int(
                StaticScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("critical_vul")
                )["critical_vul__sum"]
            )
        except Exception as e:
            all_static = 0
    elif query == "high":
        try:
            all_static = int(
                StaticScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("high_vul")
                )["high_vul__sum"]
            )
        except Exception as e:
            all_static = 0
    elif query == "medium":
        try:
            all_static = int(
                StaticScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("medium_vul")
                )["medium_vul__sum"]
            )
        except Exception as e:
            all_static = 0

    elif query == "low":
        try:
            all_static = int(
                StaticScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("low_vul")
                )["low_vul__sum"]
            )
        except Exception as e:
            all_static = 0

    return all_static


def all_cloud(project_id, query):
    all_cloud = 0

    if query == "total":
        try:
            all_cloud = int(
                CloudScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("total_vul")
                )["total_vul__sum"]
            )
        except Exception as e:
            all_cloud = 0

    elif query == "critical":
        try:
            all_cloud = int(
                CloudScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("critical_vul")
                )["critical_vul__sum"]
            )
        except Exception as e:
            all_cloud = 0
    elif query == "high":
        try:
            all_cloud = int(
                CloudScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("high_vul")
                )["high_vul__sum"]
            )
        except Exception as e:
            all_cloud = 0
    elif query == "medium":
        try:
            all_cloud = int(
                CloudScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("medium_vul")
                )["medium_vul__sum"]
            )
        except Exception as e:
            all_cloud = 0

    elif query == "low":
        try:
            all_cloud = int(
                CloudScansDb.objects.filter(project__uu_id=project_id).aggregate(
                    Sum("low_vul")
                )["low_vul__sum"]
            )
        except Exception as e:
            all_cloud = 0

    return all_cloud


def all_inspec(project_id, query):
    if not COMPLIANCE_AVAILABLE or InspecScanDb is None:
        return "0"
    all_inspec = None
    if query == "total":
        all_inspec_scan = InspecScanDb.objects.filter(
            project__uu_id=project_id
        ).aggregate(Sum("total_vuln"))
        for key, value in all_inspec_scan.items():
            all_inspec = "0" if value is None else value
    elif query == "failed":
        all_inspec_high = InspecScanDb.objects.filter(
            project__uu_id=project_id
        ).aggregate(Sum("inspec_failed"))
        for key, value in all_inspec_high.items():
            all_inspec = "0" if value is None else value
    elif query == "passed":
        all_inspec_medium = InspecScanDb.objects.filter(
            project__uu_id=project_id
        ).aggregate(Sum("inspec_passed"))
        for key, value in all_inspec_medium.items():
            all_inspec = "0" if value is None else value
    elif query == "skipped":
        all_inspec_low = InspecScanDb.objects.filter(
            project__uu_id=project_id
        ).aggregate(Sum("inspec_skipped"))
        for key, value in all_inspec_low.items():
            all_inspec = "0" if value is None else value
    return all_inspec


def all_dockle(project_id, query):
    if not COMPLIANCE_AVAILABLE or DockleScanDb is None:
        return "0"
    all_dockle = None
    if query == "total":
        all_dockle_scan = DockleScanDb.objects.filter(
            project__uu_id=project_id
        ).aggregate(Sum("total_vuln"))
        for key, value in all_dockle_scan.items():
            all_dockle = "0" if value is None else value
    elif query == "fatal":
        all_dockle_high = DockleScanDb.objects.filter(
            project__uu_id=project_id
        ).aggregate(Sum("dockle_fatal"))
        for key, value in all_dockle_high.items():
            all_dockle = "0" if value is None else value
    elif query == "info":
        all_dockle_medium = DockleScanDb.objects.filter(
            project__uu_id=project_id
        ).aggregate(Sum("dockle_info"))
        for key, value in all_dockle_medium.items():
            all_dockle = "0" if value is None else value
    return all_dockle


def _cloud_filter(query_kwargs):
    """Return CloudScansResultsDb queryset or empty list if unavailable."""
    if not CLOUD_AVAILABLE or CloudScansResultsDb is None:
        return []
    return CloudScansResultsDb.objects.filter(**query_kwargs)


def all_vuln_count(project_id, query):
    all_data = 0
    if query == "Critical":
        web_all_critical = WebScanResultsDb.objects.filter(
            project__uu_id=project_id,
            severity="Critical",
        )

        sast_all_critical = StaticScanResultsDb.objects.filter(
            project__uu_id=project_id, severity="Critical"
        )

        cloud_all_critical = _cloud_filter({"project__uu_id": project_id, "severity": "Critical"})

        net_all_critical = NetworkScanResultsDb.objects.filter(
            severity="Critical", project__uu_id=project_id
        )
        all_data = chain(
            web_all_critical,
            sast_all_critical,
            cloud_all_critical,
            net_all_critical,
        )
    elif query == "High":
        web_all_high = WebScanResultsDb.objects.filter(
            project__uu_id=project_id,
            severity="High",
        )

        sast_all_high = StaticScanResultsDb.objects.filter(
            project__uu_id=project_id, severity="High"
        )

        cloud_all_high = _cloud_filter({"project__uu_id": project_id, "severity": "High"})

        net_all_high = NetworkScanResultsDb.objects.filter(
            severity="High", project__uu_id=project_id
        )
        all_data = chain(
            web_all_high,
            sast_all_high,
            cloud_all_high,
            net_all_high,
        )

    elif query == "Medium":
        web_all_medium = WebScanResultsDb.objects.filter(
            project__uu_id=project_id,
            severity="Medium",
        )

        sast_all_medium = StaticScanResultsDb.objects.filter(
            project__uu_id=project_id, severity="Medium"
        )

        cloud_all_medium = _cloud_filter({"project__uu_id": project_id, "severity": "Medium"})

        net_all_medium = NetworkScanResultsDb.objects.filter(
            severity="Medium", project__uu_id=project_id
        )

        all_data = chain(
            web_all_medium,
            sast_all_medium,
            cloud_all_medium,
            net_all_medium,
        )

    elif query == "Low":
        web_all_low = WebScanResultsDb.objects.filter(
            project__uu_id=project_id,
            severity="Low",
        )

        sast_all_low = StaticScanResultsDb.objects.filter(
            project__uu_id=project_id, severity="Low"
        )

        cloud_all_low = _cloud_filter({"project__uu_id": project_id, "severity": "Low"})

        net_all_low = NetworkScanResultsDb.objects.filter(
            severity="Low", project__uu_id=project_id
        )

        all_data = chain(
            web_all_low,
            sast_all_low,
            cloud_all_low,
            net_all_low,
        )

    elif query == "Total":
        web_all = WebScanResultsDb.objects.filter(
            project__uu_id=project_id,
        )

        sast_all = StaticScanResultsDb.objects.filter(
            project__uu_id=project_id,
        )

        cloud_all = _cloud_filter({"project__uu_id": project_id})

        net_all = NetworkScanResultsDb.objects.filter(project__uu_id=project_id)

        pentest_all = PentestScanResultsDb.objects.filter(project__uu_id=project_id)

        all_data = chain(
            web_all,
            sast_all,
            cloud_all,
            net_all,
            pentest_all,
        )

    elif query == "False":
        web_all_false = WebScanResultsDb.objects.filter(
            project__uu_id=project_id, false_positive="Yes"
        )

        sast_all_false = StaticScanResultsDb.objects.filter(
            project__uu_id=project_id, false_positive="Yes"
        )

        cloud_all_false = _cloud_filter({"project__uu_id": project_id, "false_positive": "Yes"})

        net_all_false = NetworkScanResultsDb.objects.filter(
            project__uu_id=project_id, false_positive="Yes"
        )
        all_data = chain(
            web_all_false,
            sast_all_false,
            cloud_all_false,
            net_all_false,
        )

    elif query == "Close":
        web_all_close = WebScanResultsDb.objects.filter(
            project__uu_id=project_id, vuln_status="Closed"
        )

        sast_all_close = StaticScanResultsDb.objects.filter(
            project__uu_id=project_id, vuln_status="Closed"
        )

        cloud_all_close = _cloud_filter({"project__uu_id": project_id, "vuln_status": "Closed"})

        net_all_close = NetworkScanResultsDb.objects.filter(
            project__uu_id=project_id, vuln_status="Closed"
        )
        all_data = chain(
            web_all_close,
            sast_all_close,
            cloud_all_close,
            net_all_close,
        )

    elif query == "Open":
        web_all_open = WebScanResultsDb.objects.filter(
            project__uu_id=project_id, vuln_status="Open"
        )

        sast_all_open = StaticScanResultsDb.objects.filter(
            project__uu_id=project_id, vuln_status="Open"
        )

        cloud_all_open = _cloud_filter({"project__uu_id": project_id, "vuln_status": "Open"})

        net_all_open = NetworkScanResultsDb.objects.filter(
            project__uu_id=project_id, vuln_status="Open"
        )
        all_data = chain(
            web_all_open,
            sast_all_open,
            cloud_all_open,
            net_all_open,
        )

    return all_data


def all_vuln_count_data(project_id, query):
    all_data = 0

    if query == "false":
        web_false_positive = WebScanResultsDb.objects.filter(
            false_positive="Yes", project__uu_id=project_id
        )

        sast_false_positive = StaticScanResultsDb.objects.filter(
            false_positive="Yes", project__uu_id=project_id
        )

        cloud_false_positive = _cloud_filter({"false_positive": "Yes", "project__uu_id": project_id})

        net_false_positive = NetworkScanResultsDb.objects.filter(
            false_positive="Yes", project__uu_id=project_id
        )

        all_data = (
            int(len(web_false_positive))
            + int(len(sast_false_positive))
            + int(len(cloud_false_positive))
            + int(len(net_false_positive))
        )

    elif query == "Closed":
        web_closed_vuln = WebScanResultsDb.objects.filter(
            vuln_status="Closed", project__uu_id=project_id
        )

        net_closed_vuln = NetworkScanResultsDb.objects.filter(
            vuln_status="Closed", project__uu_id=project_id
        )

        sast_closed_vuln = StaticScanResultsDb.objects.filter(
            vuln_status="Closed", project__uu_id=project_id
        )

        cloud_closed_vuln = _cloud_filter({"vuln_status": "Closed", "project__uu_id": project_id})

        pentest_closed_vuln = PentestScanResultsDb.objects.filter(
            vuln_status="Closed", project__uu_id=project_id
        )
        all_data = (
            int(len(web_closed_vuln))
            + int(len(net_closed_vuln))
            + int(len(sast_closed_vuln))
            + int(len(cloud_closed_vuln))
            + int(len(pentest_closed_vuln))
        )

    elif query == "Open":
        web_open_vuln = WebScanResultsDb.objects.filter(
            vuln_status="Open", project__uu_id=project_id
        )
        net_open_vuln = NetworkScanResultsDb.objects.filter(
            vuln_status="Open", project__uu_id=project_id
        )
        sast_open_vuln = StaticScanResultsDb.objects.filter(
            vuln_status="Open", project__uu_id=project_id
        )

        cloud_open_vuln = _cloud_filter({"vuln_status": "Open", "project__uu_id": project_id})

        pentest_open_vuln = PentestScanResultsDb.objects.filter(
            vuln_status="Open", project__uu_id=project_id
        )
        # add your scanner name here <scannername>
        all_data = (
            int(len(web_open_vuln))
            + int(len(net_open_vuln))
            + int(len(sast_open_vuln))
            + int(len(cloud_open_vuln))
            + int(len(pentest_open_vuln))
        )

    return all_data
