# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.contrib import admin

from authentication import models

admin.site.register(models.UserLoginHistory)
