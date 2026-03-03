# -*- coding: utf-8 -*-
# VAPT Security Platform


import uuid

from vaptapi.models import OrgAPIKey
try:
    from compliance.models import DockleScanDb, DockleScanResultsDb
    COMPLIANCE_AVAILABLE = True
except ImportError:
    DockleScanDb = None
    InspecScanDb = None
    DockleScanResultsDb = None
    InspecScanResultsDb = None
    COMPLIANCE_AVAILABLE = False
from utility.email_notify import email_sch_notify

status = None
controls_results_message = None
vuln_col = ""


def dockle_report_json(data, project_id, scan_id, request):
    """

    :param data:
    :param project_id:
    :param scan_id:
    :return:
    """
    global vul_col

    api_key = request.META.get("HTTP_X_API_KEY")
    key_object = OrgAPIKey.objects.filter(api_key=api_key).first()
    if str(request.user) == 'AnonymousUser':
        organization = key_object.organization
    else:
        organization = request.user.organization

    for vuln in data["details"]:
        code = vuln["code"]
        title = vuln["title"]
        level = vuln["level"]
        alerts = vuln["alerts"][0]

        if level == "FATAL":
            vul_col = "danger"

        elif level == "PASS":
            vul_col = "warning"

        elif level == "WARN":
            vul_col = "warning"

        elif level == "INFO":
            vul_col = "info"

        vul_id = uuid.uuid4()

        save_all = DockleScanResultsDb(
            scan_id=scan_id,
            project_id=project_id,
            vul_col=vul_col,
            vuln_id=vul_id,
            code=code,
            title=title,
            alerts=alerts,
            level=level,
        )
        save_all.save()

    all_dockle_data = DockleScanResultsDb.objects.filter(
        scan_id=scan_id, organization=organization
    )

    total_vul = len(all_dockle_data)
    dockle_failed = len(all_dockle_data.filter(level="FATAL"))
    dockle_passed = len(all_dockle_data.filter(level="PASS"))
    dockle_warn = len(all_dockle_data.filter(level="WARN"))
    dockle_info = len(all_dockle_data.filter(level="INFO"))
    total_duplicate = len(all_dockle_data.filter(level="Yes"))

    DockleScanDb.objects.filter(
        scan_id=scan_id, organization=organization
    ).update(
        total_vuln=total_vul,
        dockle_fatal=dockle_failed,
        dockle_warn=dockle_warn,
        dockle_info=dockle_info,
        dockle_pass=dockle_passed,
        total_dup=total_duplicate,
        organization=organization,
    )
    subject = "Archery Tool Scan Status - dockle Report Uploaded"
    message = (
        "dockle Scanner has completed the scan "
        "  %s <br> Total: %s <br>Failed: %s <br>"
        "failed: %s <br>Skipped %s"
        % (scan_id, total_vul, dockle_failed, dockle_warn, dockle_passed)
    )

    email_sch_notify(subject=subject, message=message)


parser_header_dict = {
    "dockle_scan": {
        "displayName": "Dockle Scanner",
        "dbtype": "DockleScan",
        "type": "JSON",
        "parserFunction": dockle_report_json,
        "icon": "/static/tools/dockle.png",
    }
}
