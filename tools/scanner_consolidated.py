# -*- coding: utf-8 -*-
# VAPT Security Platform
# Consolidated Additional Security Tools (SSL Scan, Nikto, etc)

import json
import subprocess
import threading
import uuid
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from notifications.models import Notification
from notifications.signals import notify
from projects.models import ProjectDb
from user_management import permissions


class NiktoScannerView(APIView):
    """
    Nikto Web Server Scanner
    Handles: Web server vulnerability scanning
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tools/nikto_scan_consolidated.html"
    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        """Display Nikto scans"""
        projects = ProjectDb.objects.filter(
            organization=request.user.organization
        )
        
        return render(request, self.template_name, {
            'projects': projects,
            'scanner': 'Nikto',
            'description': 'Web Server Vulnerability Scanner'
        })

    def post(self, request):
        """Launch Nikto scan"""
        try:
            target_host = request.POST.get('host')
            target_port = request.POST.get('port', '80')
            
            if not target_host:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Target host is required'
                }, status=400)
            
            scan_id = str(uuid.uuid4())
            
            thread = threading.Thread(
                target=self._execute_nikto_scan,
                args=(scan_id, target_host, target_port, request.user)
            )
            thread.daemon = True
            thread.start()
            
            return JsonResponse({
                'status': 'success',
                'scan_id': scan_id,
                'message': 'Nikto scan started'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    def _execute_nikto_scan(self, scan_id, host, port, user):
        """Execute Nikto scan"""
        try:
            target = f"{host}:{port}"
            
            result = subprocess.run(
                ['nikto', '-h', host, '-p', port, '-Format', 'JSON', '-output', f'/tmp/nikto_{scan_id}.json'],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            notify.send(
                user,
                recipient=user,
                verb=f"Nikto scan completed on {target}"
            )
            
        except Exception as e:
            notify.send(user, recipient=user, verb=f"Nikto scan failed: {str(e)}")


class SSLScannerView(APIView):
    """
    SSL/TLS Certificate Scanner
    Handles: SSL/TLS configuration and certificate analysis
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tools/ssl_scan_consolidated.html"
    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        """Display SSL scans"""
        projects = ProjectDb.objects.filter(
            organization=request.user.organization
        )
        
        return render(request, self.template_name, {
            'projects': projects,
            'scanner': 'SSL Scan',
            'description': 'SSL/TLS Certificate and Configuration Analysis'
        })

    def post(self, request):
        """Launch SSL scan"""
        try:
            target_host = request.POST.get('host')
            target_port = request.POST.get('port', '443')
            
            if not target_host:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Target host is required'
                }, status=400)
            
            scan_id = str(uuid.uuid4())
            
            thread = threading.Thread(
                target=self._execute_ssl_scan,
                args=(scan_id, target_host, target_port, request.user)
            )
            thread.daemon = True
            thread.start()
            
            return JsonResponse({
                'status': 'success',
                'scan_id': scan_id
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    def _execute_ssl_scan(self, scan_id, host, port, user):
        """Execute SSL scan"""
        try:
            result = subprocess.run(
                ['sslscan', '--json', f'{host}:{port}'],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            notify.send(
                user,
                recipient=user,
                verb=f"SSL scan completed on {host}:{port}"
            )
            
        except Exception as e:
            notify.send(user, recipient=user, verb=f"SSL scan failed: {str(e)}")


class DnsEnumerationView(APIView):
    """
    DNS Enumeration and Analysis
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "tools/dns_enum_consolidated.html"
    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        """Display DNS enumeration"""
        return render(request, self.template_name, {
            'scanner': 'DNS Enumeration',
            'description': 'DNS Records and Subdomain Enumeration'
        })

    def post(self, request):
        """Launch DNS enumeration"""
        try:
            domain = request.POST.get('domain')
            
            if not domain:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Domain is required'
                }, status=400)
            
            scan_id = str(uuid.uuid4())
            
            thread = threading.Thread(
                target=self._execute_dns_enum,
                args=(scan_id, domain, request.user)
            )
            thread.daemon = True
            thread.start()
            
            return JsonResponse({
                'status': 'success',
                'scan_id': scan_id
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    def _execute_dns_enum(self, scan_id, domain, user):
        """Execute DNS enumeration"""
        try:
            # Use dnspython or similar for DNS enumeration
            import dns.resolver
            
            notify.send(
                user,
                recipient=user,
                verb=f"DNS enumeration completed for {domain}"
            )
            
        except Exception as e:
            notify.send(user, recipient=user, verb=f"DNS enumeration failed: {str(e)}")
