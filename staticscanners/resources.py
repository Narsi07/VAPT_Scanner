# -*- coding: utf-8 -*-
# VAPT Security Platform

from import_export import resources

try:
    from compliance.models import DockleScanResultsDb, InspecScanResultsDb
    COMPLIANCE_AVAILABLE = True
except ImportError:
    DockleScanDb = None
    InspecScanDb = None
    DockleScanResultsDb = None
    InspecScanResultsDb = None
    COMPLIANCE_AVAILABLE = False


class InspecResource(resources.ModelResource):
    class Meta:
        model = InspecScanResultsDb


class dockleResource(resources.ModelResource):
    class Meta:
        model = DockleScanResultsDb
