# -*- coding: utf-8 -*-
# VAPT Security Platform

from __future__ import unicode_literals

from django.contrib import admin

from tools import models


admin.site.register(models.NmapResultDb)
admin.site.register(models.NmapScanDb)
admin.site.register(models.NmapVulnersPortResultDb)
admin.site.register(models.SslscanResultDb)
