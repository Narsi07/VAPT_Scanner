# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.conf import settings
from django.db import models

from user_management.models import UserProfile


class UserLoginHistory(models.Model):
    """Class for User Login History"""

    class Meta:
        db_table = "user_login_history"
        verbose_name_plural = "User Login Histories"

    user = models.ForeignKey(
        UserProfile, related_name="login_user", on_delete=models.CASCADE
    )
    logintime = models.DateTimeField(auto_now=True)
    logouttime = models.DateTimeField(null=True)
    IP = models.CharField(max_length=20)

    def __str__(self):
        return self.user.email + " " + str(self.logintime)
