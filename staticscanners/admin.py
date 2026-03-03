# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.contrib import admin

from staticscanners import models

admin.site.register(models.StaticScansDb)
admin.site.register(models.StaticScanResultsDb)
