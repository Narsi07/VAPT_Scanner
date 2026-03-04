# -*- coding: utf-8 -*-
# VAPT Security Platform
# Consolidated Web Scanners (ZAP, Arachni, Burp)

import json
import threading
import uuid
from datetime import datetime

from django.db import models
from django.http import JsonResponse
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import Notification
from notifications.signals import notify
from projects.models import ProjectDb
from user_management import permissions
from webscanners.models import WebScansDb


class ZapScannerView(APIView):
    """
    OWASP ZAP Web Application Scanner
    Handles: Scan launch, execution, and result display
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "webscanners/zapscanner/zap_scan_consolidated.html"
    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        """Display ZAP scans list and launch interface"""
        scans = WebScansDb.objects.filter(
            scanner="ZAP",
            organization=request.user.organization
        ).order_by('-date_time')
        
        projects = ProjectDb.objects.filter(
            organization=request.user.organization
        )
        
        notifications = Notification.objects.unread()
        
        return render(request, self.template_name, {
            'scans': scans,
            'projects': projects,
            'scanner': 'ZAP',
            'notifications': notifications
        })

    def post(self, request):
        """Launch ZAP scan and execute in background"""
        try:
            project_id = request.POST.get('project_id')
            scan_url = request.POST.get('scan_url')
            project_name = request.POST.get('project_name', 'Unknown')
            
            if not scan_url:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Target URL is required'
                }, status=400)
            
            scan_id = uuid.uuid4()
            scan = WebScansDb(
                scan_id=scan_id,
                project_id=project_id,
                scan_url=scan_url,
                scan_name=f"ZAP Scan - {project_name}",
                scanner='ZAP',
                scan_status='Running',
                date_time=datetime.now(),
                organization=request.user.organization
            )
            scan.save()
            
            # Execute scan in background thread
            thread = threading.Thread(
                target=self._execute_zap_scan,
                args=(scan_id, scan_url, request.user)
            )
            thread.daemon = True
            thread.start()
            
            notify.send(
                request.user,
                recipient=request.user,
                verb=f"ZAP scan started on {scan_url}"
            )
            
            return JsonResponse({
                'status': 'success',
                'scan_id': str(scan_id),
                'message': 'Scan started successfully'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    def _execute_zap_scan(self, scan_id, target_url, user):
        """Background task to execute ZAP scan"""
        try:
            # Import here to avoid circular dependency
            from scanners.scanner_plugin.web_scanner import zap_plugin
            
            scan = WebScansDb.objects.get(scan_id=scan_id)
            scan.scan_status = 'In Progress'
            scan.save()
            
            # Execute ZAP scan
            results = zap_plugin(target_url)
            
            # Process and save results
            if results:
                scan.scan_status = 'Completed'
            else:
                scan.scan_status = 'Failed'
                
            scan.save()
            
            # Send notification
            notify.send(
                user,
                recipient=user,
                verb=f"ZAP scan completed for {target_url}"
            )
            
        except Exception as e:
            scan = WebScansDb.objects.get(scan_id=scan_id)
            scan.scan_status = 'Error'
            scan.save()
            notify.send(
                user,
                recipient=user,
                verb=f"ZAP scan failed: {str(e)}"
            )

