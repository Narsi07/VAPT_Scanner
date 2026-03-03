# -*- coding: utf-8 -*-
# VAPT Security Platform

from import_export import resources

from webscanners.models import WebScanResultsDb


class ZapResource(resources.ModelResource):
    class Meta:
        model = WebScanResultsDb


class BurpResource(resources.ModelResource):
    class Meta:
        model = WebScanResultsDb


class ArachniResource(resources.ModelResource):
    class Meta:
        model = WebScanResultsDb


class NetsparkerResource(resources.ModelResource):
    class Meta:
        model = WebScanResultsDb


class AcunetixResource(resources.ModelResource):
    class Meta:
        model = WebScanResultsDb


class WebinspectResource(resources.ModelResource):
    class Meta:
        model = WebScanResultsDb


# class DependencyResource(resources.ModelResource):
#     class Meta:
#         model = dependencycheck_scan_results_db
#
#
# class FindbugResource(resources.ModelResource):
#     class Meta:
#         model = findbugs_scan_results_db


class AllResource(
    ZapResource,
    BurpResource,
    ArachniResource,
    NetsparkerResource,
    AcunetixResource,
    WebinspectResource,
    # DependencyResource,
    # FindbugResource,
):
    pass
