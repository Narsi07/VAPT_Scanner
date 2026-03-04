# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render
from notifications.models import Notification


class ArachniScan(APIView):
    """
    Arachni Web Application Scanner
    Note: Arachni is deprecated. This is a stub for template compatibility.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "webscanners/arachniscanner/arachni_scan_list.html"
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_notify = Notification.objects.unread()
        return render(
            request,
            "webscanners/arachniscanner/arachni_scan_list.html",
            {"message": all_notify, "scans": []},
        )

    def post(self, request):
        return HttpResponse("Arachni scanning is not configured in this installation")

    def delete(self, request):
        return HttpResponse("Method not supported")


class ArachniSetting(APIView):
    """
    Arachni Scanner Configuration
    Note: Arachni is deprecated. This is a stub for template compatibility.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "webscanners/arachniscanner/arachni_settings_form.html"
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return render(
            request,
            "webscanners/arachniscanner/arachni_settings_form.html",
            {"settings": None},
        )

    def post(self, request):
        return HttpResponse("Arachni settings not available")


class ArachniSettingUpdate(APIView):
    """
    Update Arachni Scanner Configuration
    Note: Arachni is deprecated. This is a stub for template compatibility.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return HttpResponse("Arachni settings update not available")
