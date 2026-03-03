# -*- coding: utf-8 -*-
# VAPT Security Platform

from import_export import resources

from networkscanners.models import nessus_scan_results_db, ov_scan_result_db


class OpenvasResource(resources.ModelResource):
    class Meta:
        model = ov_scan_result_db


class NessusResource(resources.ModelResource):
    class Meta:
        model = nessus_scan_results_db
