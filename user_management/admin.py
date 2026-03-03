# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.contrib import admin

from user_management import models

admin.site.register(models.UserProfile)
admin.site.register(models.UserRoles)
admin.site.register(models.Organization)
