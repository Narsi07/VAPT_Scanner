# -*- coding: utf-8 -*-
# VAPT Security Platform
# Consolidated Static Code Analysis Scanners (Bandit, Semgrep, Checkov)

import json
import os
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
from staticscanners.models import StaticScansDb


class BanditScannerView(APIView):
    """
    Bandit - Python Security Issue Detection
    Handles: Scanning and result display
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "staticscanners/bandit_scan_consolidated.html"
    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        """Display Bandit scans list"""
        scans = StaticScansDb.objects.filter(
            scanner='Bandit',
            organization=request.user.organization
        ).order_by('-date_time')
        
        projects = ProjectDb.objects.filter(
            organization=request.user.organization
        )
        
        return render(request, self.template_name, {
            'scans': scans,
            'projects': projects,
            'scanner': 'Bandit',
            'description': 'Python Security Issue Detection',
            'file_filter': '.py'
        })

    def post(self, request):
        """Launch Bandit scan"""
        try:
            scan_path = request.POST.get('scan_path', '').strip()
            project_id = request.POST.get('project_id')
            project_name = request.POST.get('project_name', 'Unknown')
            
            if not scan_path:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Scan path is required'
                }, status=400)
            
            if not os.path.exists(scan_path):
                return JsonResponse({
                    'status': 'error',
                    'message': f'Path does not exist: {scan_path}'
                }, status=400)
            
            scan_id = uuid.uuid4()
            scan = StaticScansDb(
                scan_id=scan_id,
                project_id=project_id,
                scan_url=scan_path,
                scan_name=f'Bandit - {project_name}',
                scanner='Bandit',
                scan_status='Running',
                date_time=datetime.now(),
                organization=request.user.organization
            )
            scan.save()
            
            thread = threading.Thread(
                target=self._execute_bandit_scan,
                args=(scan_id, scan_path, request.user)
            )
            thread.daemon = True
            thread.start()
            
            notify.send(
                request.user,
                recipient=request.user,
                verb=f"Bandit scan started on {scan_path}"
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

    def _execute_bandit_scan(self, scan_id, scan_path, user):
        """Execute Bandit scan in background"""
        try:
            scan = StaticScansDb.objects.get(scan_id=scan_id)
            
            # Execute Bandit
            result = subprocess.run(
                ['bandit', '-r', scan_path, '-f', 'json'],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            # Parse results
            if result.stdout:
                data = json.loads(result.stdout)
                issues = data.get('results', [])
                
                scan.scan_status = 'Completed'
                scan.raw_data = json.dumps(issues)
                
                # Save individual issues
                # Process issues here to save to database
            else:
                scan.scan_status = 'Completed'
            
            scan.save()
            
            notify.send(
                user,
                recipient=user,
                verb=f"Bandit scan completed on {scan_path}"
            )
            
        except subprocess.TimeoutExpired:
            scan = StaticScansDb.objects.get(scan_id=scan_id)
            scan.scan_status = 'Timeout'
            scan.save()
            notify.send(user, recipient=user, verb="Bandit scan timeout")
        except Exception as e:
            scan = StaticScansDb.objects.get(scan_id=scan_id)
            scan.scan_status = 'Error'
            scan.save()
            notify.send(user, recipient=user, verb=f"Bandit scan failed: {str(e)}")


class SemgrepScannerView(APIView):
    """
    Semgrep - Pattern-Based Static Analysis
    Handles: Scanning and result display
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "staticscanners/semgrep_scan_consolidated.html"
    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        """Display Semgrep scans list"""
        scans = StaticScansDb.objects.filter(
            scanner='Semgrep',
            organization=request.user.organization
        ).order_by('-date_time')
        
        projects = ProjectDb.objects.filter(
            organization=request.user.organization
        )
        
        return render(request, self.template_name, {
            'scans': scans,
            'projects': projects,
            'scanner': 'Semgrep',
            'description': 'Pattern-Based Static Analysis',
            'file_filter': 'all'
        })

    def post(self, request):
        """Launch Semgrep scan"""
        try:
            scan_path = request.POST.get('scan_path', '').strip()
            project_id = request.POST.get('project_id')
            project_name = request.POST.get('project_name', 'Unknown')
            
            if not scan_path:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Scan path is required'
                }, status=400)
            
            if not os.path.exists(scan_path):
                return JsonResponse({
                    'status': 'error',
                    'message': f'Path does not exist: {scan_path}'
                }, status=400)
            
            scan_id = uuid.uuid4()
            scan = StaticScansDb(
                scan_id=scan_id,
                project_id=project_id,
                scan_url=scan_path,
                scan_name=f'Semgrep - {project_name}',
                scanner='Semgrep',
                scan_status='Running',
                date_time=datetime.now(),
                organization=request.user.organization
            )
            scan.save()
            
            thread = threading.Thread(
                target=self._execute_semgrep_scan,
                args=(scan_id, scan_path, request.user)
            )
            thread.daemon = True
            thread.start()
            
            notify.send(
                request.user,
                recipient=request.user,
                verb=f"Semgrep scan started on {scan_path}"
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

    def _execute_semgrep_scan(self, scan_id, scan_path, user):
        """Execute Semgrep scan"""
        try:
            scan = StaticScansDb.objects.get(scan_id=scan_id)
            
            result = subprocess.run(
                ['semgrep', '--config', 'auto', scan_path, '--json', '--quiet'],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.stdout:
                data = json.loads(result.stdout)
                results = data.get('results', [])
                
                scan.scan_status = 'Completed'
                scan.raw_data = json.dumps(results)
            else:
                scan.scan_status = 'Completed'
            
            scan.save()
            
            notify.send(user, recipient=user, verb=f"Semgrep scan completed on {scan_path}")
            
        except subprocess.TimeoutExpired:
            scan = StaticScansDb.objects.get(scan_id=scan_id)
            scan.scan_status = 'Timeout'
            scan.save()
        except Exception as e:
            scan = StaticScansDb.objects.get(scan_id=scan_id)
            scan.scan_status = 'Error'
            scan.save()
            notify.send(user, recipient=user, verb=f"Semgrep scan failed: {str(e)}")


class CheckovScannerView(APIView):
    """
    Checkov - Infrastructure as Code Security
    Handles: IaC scanning and result display
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "staticscanners/checkov_scan_consolidated.html"
    permission_classes = (IsAuthenticated, permissions.IsAnalyst)

    def get(self, request):
        """Display Checkov scans"""
        scans = StaticScansDb.objects.filter(
            scanner='Checkov',
            organization=request.user.organization
        ).order_by('-date_time')
        
        projects = ProjectDb.objects.filter(
            organization=request.user.organization
        )
        
        return render(request, self.template_name, {
            'scans': scans,
            'projects': projects,
            'scanner': 'Checkov',
            'description': 'Infrastructure as Code Security',
            'file_filter': 'tf,yml,yaml,json'
        })

    def post(self, request):
        """Launch Checkov scan"""
        try:
            scan_path = request.POST.get('scan_path', '').strip()
            project_id = request.POST.get('project_id')
            
            if not scan_path or not os.path.exists(scan_path):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid scan path'
                }, status=400)
            
            scan_id = uuid.uuid4()
            scan = StaticScansDb(
                scan_id=scan_id,
                project_id=project_id,
                scan_url=scan_path,
                scanner='Checkov',
                scan_status='Running',
                date_time=datetime.now(),
                organization=request.user.organization
            )
            scan.save()
            
            thread = threading.Thread(
                target=self._execute_checkov_scan,
                args=(scan_id, scan_path, request.user)
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

    def _execute_checkov_scan(self, scan_id, scan_path, user):
        """Execute Checkov scan"""
        try:
            scan = StaticScansDb.objects.get(scan_id=scan_id)
            
            result = subprocess.run(
                ['checkov', '-d', scan_path, '-o', 'json'],
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.stdout:
                data = json.loads(result.stdout)
                scan.scan_status = 'Completed'
                scan.raw_data = json.dumps(data)
            else:
                scan.scan_status = 'Completed'
            
            scan.save()
            
            notify.send(user, recipient=user, verb=f"Checkov scan completed")
            
        except Exception as e:
            scan = StaticScansDb.objects.get(scan_id=scan_id)
            scan.scan_status = 'Error'
            scan.save()
