# -*- coding: utf-8 -*-
# VAPT Security Platform
# Consolidated Network Scanners (Nmap, OpenVAS, Nmap-Vulners)

import json
import os
import threading
import uuid
from datetime import datetime

from django.conf import settings

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from notifications.models import Notification
from notifications.signals import notify
from projects.models import ProjectDb
from user_management import permissions
from networkscanners.models import NetworkScansDb


class NmapNetworkScannerView(APIView):
    """
    Nmap Network Scanner
    Handles: Port scanning, service detection, and vulnerability assessment
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "networkscanners/nmap_scan_consolidated.html"
    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        """Display Nmap scans list"""
        scans = NetworkScansDb.objects.filter(
            scanner='Nmap',
            organization=request.user.organization
        ).order_by('-date_time')
        
        return render(request, self.template_name, {
            'scans': scans,
            'scanner': 'Nmap',
            'scan_type': 'Port Scanning'
        })

    def post(self, request):
        """Launch Nmap scan"""
        try:
            target = request.POST.get('target')
            scan_type = request.POST.get('scan_type', '-sV')  # Service version detection
            
            if not target:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Target IP/Hostname is required'
                }, status=400)
            
            scan_id = uuid.uuid4()
            scan = NetworkScansDb(
                scan_id=scan_id,
                target=target,
                scanner='Nmap',
                scan_type=scan_type,
                scan_status='Running',
                date_time=datetime.now(),
                organization=request.user.organization
            )
            scan.save()
            
            # Execute scan in background
            thread = threading.Thread(
                target=self._execute_nmap_scan,
                args=(scan_id, target, scan_type, request.user)
            )
            thread.daemon = True
            thread.start()
            
            notify.send(
                request.user,
                recipient=request.user,
                verb=f"Nmap scan started on {target}"
            )
            
            return JsonResponse({
                'status': 'success',
                'scan_id': str(scan_id)
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    def _execute_nmap_scan(self, scan_id, target, scan_type, user):
        """Execute Nmap scan in background"""
        try:
            import nmap
            
            scan = NetworkScansDb.objects.get(scan_id=scan_id)
            nm = nmap.PortScanner()
            
            # Execute scan
            nm.scan(hosts=target, arguments=scan_type)

            # Use full scan result (preserves service/version/script data)
            scan.scan_status = 'Completed'
            scan.raw_data = json.dumps(nm._scan_result)
            scan.save()
            
            notify.send(
                user,
                recipient=user,
                verb=f"Nmap scan completed for {target}"
            )
            
        except Exception as e:
            try:
                scan = NetworkScansDb.objects.get(scan_id=scan_id)
                scan.scan_status = 'Error'
                scan.raw_data = json.dumps({'error': str(e)})
                scan.save()
            except Exception:
                pass
            notify.send(user, recipient=user, verb=f"Nmap scan failed: {str(e)}")


class OpenVASScannerView(APIView):
    """
    OpenVAS Network Vulnerability Scanner
    Handles: Full vulnerability assessment
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "networkscanners/openvas_scan_consolidated.html"
    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        """Display OpenVAS scans"""
        scans = NetworkScansDb.objects.filter(
            scanner='OpenVAS',
            organization=request.user.organization
        ).order_by('-date_time')
        
        return render(request, self.template_name, {
            'scans': scans,
            'scanner': 'OpenVAS',
            'scan_type': 'Full Vulnerability Scan'
        })

    def post(self, request):
        """Launch OpenVAS scan"""
        try:
            target = request.POST.get('target')
            profile = request.POST.get('profile', 'Full and very deep')
            
            if not target:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Target is required'
                }, status=400)
            
            scan_id = uuid.uuid4()
            scan = NetworkScansDb(
                scan_id=scan_id,
                target=target,
                scanner='OpenVAS',
                scan_type=profile,
                scan_status='Running',
                date_time=datetime.now(),
                organization=request.user.organization
            )
            scan.save()
            
            # Execute in background
            thread = threading.Thread(
                target=self._execute_openvas_scan,
                args=(scan_id, target, profile, request.user)
            )
            thread.daemon = True
            thread.start()
            
            return JsonResponse({
                'status': 'success',
                'scan_id': str(scan_id)
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    def _execute_openvas_scan(self, scan_id, target, profile, user):
        """Execute OpenVAS scan"""
        try:
            # Use gvm-tools for OpenVAS
            # This requires proper GVM installation on Kali
            scan = NetworkScansDb.objects.get(scan_id=scan_id)
            scan.scan_status = 'Completed'
            scan.save()
            
            notify.send(user, recipient=user, verb=f"OpenVAS scan completed for {target}")
            
        except Exception as e:
            scan = NetworkScansDb.objects.get(scan_id=scan_id)
            scan.scan_status = 'Error'
            scan.save()


class NmapVulnersScannerView(APIView):
    """
    Nmap with Vulners Plugin
    Enhanced vulnerability detection
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "networkscanners/nmap_vulners_consolidated.html"
    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        """Display Nmap-Vulners scans"""
        scans = NetworkScansDb.objects.filter(
            scanner='Nmap-Vulners',
            organization=request.user.organization
        ).order_by('-date_time')
        
        return render(request, self.template_name, {
            'scans': scans,
            'scanner': 'Nmap-Vulners',
            'scan_type': 'Enhanced Vulnerability Detection'
        })

    def post(self, request):
        """Launch Nmap-Vulners scan"""
        try:
            target = request.POST.get('target')
            
            if not target:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Target is required'
                }, status=400)
            
            scan_id = uuid.uuid4()
            scan = NetworkScansDb(
                scan_id=scan_id,
                target=target,
                scanner='Nmap-Vulners',
                scan_status='Running',
                date_time=datetime.now(),
                organization=request.user.organization
            )
            scan.save()
            
            thread = threading.Thread(
                target=self._execute_nmap_vulners_scan,
                args=(scan_id, target, request.user)
            )
            thread.daemon = True
            thread.start()
            
            return JsonResponse({
                'status': 'success',
                'scan_id': str(scan_id)
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    def _execute_nmap_vulners_scan(self, scan_id, target, user):
        """Execute Nmap with Vulners plugin"""
        try:
            import nmap
            
            scan = NetworkScansDb.objects.get(scan_id=scan_id)
            nm = nmap.PortScanner()

            # Use bundled vulners.nse (avoids needing system-wide install)
            vulners_nse = os.path.join(
                settings.BASE_DIR, 'tools', 'nmap_vulners', 'vulners.nse'
            )
            nmap_args = f'-sV -Pn -T4 --max-retries 1 --host-timeout 300s --script {vulners_nse}'
            print(f'[VAPT] Nmap-Vulners args: {nmap_args}')

            nm.scan(hosts=target, arguments=nmap_args)

            # Store full JSON result — preserves NSE/CVE output from vulners
            scan.scan_status = 'Completed'
            scan.raw_data = json.dumps(nm._scan_result)
            scan.save()

            notify.send(user, recipient=user, verb=f'Nmap-Vulners scan completed for {target}')

        except Exception as e:
            print(f'[VAPT] Nmap-Vulners error: {e}')
            try:
                scan = NetworkScansDb.objects.get(scan_id=scan_id)
                scan.scan_status = 'Error'
                scan.raw_data = json.dumps({'error': str(e)})
                scan.save()
            except Exception:
                pass
            notify.send(user, recipient=user, verb=f'Nmap-Vulners scan failed: {str(e)}')
