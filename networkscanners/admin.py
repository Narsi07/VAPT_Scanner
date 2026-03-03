# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.contrib import admin

from networkscanners import models

admin.site.register(models.NetworkScanDb)
admin.site.register(models.NetworkScanResultsDb)
