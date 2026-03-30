# -*- coding: utf-8 -*-
# VAPT Security Platform

from django.shortcuts import render
from tools.models import NmapScanDb
from projects.models import ProjectDb


def launch_hub(request):
    try:
        all_projects = ProjectDb.objects.filter(organization=request.user.organization)
    except Exception:
        all_projects = []
    return render(request, 'launch/network_scan.html', {'all_projects': all_projects})


def results_hub(request):
    try:
        nmap_scans = NmapScanDb.objects.filter(
            organization=request.user.organization, 
            is_vulners=False
        ).order_by('-created_time')
        
        vulners_scans = NmapScanDb.objects.filter(
            organization=request.user.organization, 
            is_vulners=True
        ).order_by('-created_time')
    except Exception:
        nmap_scans = []
        vulners_scans = []
        
    return render(request, 'results/network_results.html', {
        'nmap_scans': nmap_scans,
        'vulners_scans': vulners_scans,
    })
