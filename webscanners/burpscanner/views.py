# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render
from notifications.models import Notification


class BurpScanLaunch(APIView):
    """
    Burp Suite Scanner - Requires commercial Burp Suite integration
    """
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return HttpResponse("Burp Suite scanning requires commercial setup and integration")

    def get(self, request):
        all_notify = Notification.objects.unread()
        return render(
            request,
            "webscanners/burpscanner/burp_setting_form.html",
            {"message": all_notify},
        )


class BurpSetting(APIView):
    """
    Burp Suite Configuration
    """
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return render(
            request,
            "webscanners/burpscanner/burp_setting_form.html",
            {"settings": None},
        )

    def post(self, request):
        return HttpResponse("Burp Suite settings update not available")
