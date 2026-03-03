# -*- coding: utf-8 -*-
# VAPT Security Platform

from __future__ import unicode_literals

from django.contrib import admin

from webscanners import models

admin.site.register(models.WebScansDb)
admin.site.register(models.WebScanResultsDb)
