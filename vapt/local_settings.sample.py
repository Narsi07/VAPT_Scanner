# -*- coding: utf-8 -*-
# VAPT Security Platform - Local Settings Example
# Copy this file to local_settings.py and configure for your environment

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Security Settings
DEBUG = False  # Set to False in production
INTERNAL_IPS = ["127.0.0.1", "::1", "172.26.0.1"]
ADMINS = [("Admin", "admin@example.com")]

# ============================================================================
# SECURITY SCANNERS CONFIGURATION
# ============================================================================

# OWASP ZAP Configuration
ZAP_CONFIG = {
    'enabled': True,
    'proxy_address': '127.0.0.1',
    'proxy_port': 8090,
    'api_key': 'changeme',
    'api_port': 8090,
    'timeout': 300,  # 5 minutes
    'max_connections': 10,
}

# Nmap Configuration
NMAP_CONFIG = {
    'enabled': True,
    'path': '/usr/bin/nmap',
    'timeout': 900,  # 15 minutes
    'max_parallel_scans': 5,
    'common_arguments': ['-sV', '-sC', '--version-intensity=9'],
    'aggressive_arguments': ['-A', '-T4'],
    'stealth_arguments': ['-sS', '-T1'],
}

# Nmap Vulners Plugin Configuration
NMAP_VULNERS_CONFIG = {
    'enabled': True,
    'script_path': '~/.nmap/scripts/vulners.nse',
    'database': 'vulners',
    'min_cvss': 4.0,  # Minimum CVSS score to report
}

# OpenVAS Configuration
OPENVAS_CONFIG = {
    'enabled': True,
    'host': '127.0.0.1',  # Change to remote host if needed
    'port': 9392,
    'username': 'admin',
    'password': 'admin',  # Change in production!
    'timeout': 1800,  # 30 minutes
    'verify_ssl': False,
    'scan_target': 'GCM Scan Config',  # Default scan profile
}

# Bandit (Python Security)
BANDIT_CONFIG = {
    'enabled': True,
    'path': '/usr/bin/bandit',
    'timeout': 300,  # 5 minutes
    'severity_level': 'medium',  # 'all', 'high', 'medium', 'low'
    'confidence_level': 'medium',
    'exclude_dirs': ['.venv', 'venv', '.git', '__pycache__'],
}

# Semgrep Configuration
SEMGREP_CONFIG = {
    'enabled': True,
    'path': '/usr/bin/semgrep',
    'timeout': 600,  # 10 minutes
    'config': 'auto',  # 'auto' for auto-detection
    'include_tests': False,
    'languages': ['python', 'javascript', 'typescript', 'java', 'go', 'ruby'],
}

# Checkov Configuration
CHECKOV_CONFIG = {
    'enabled': True,
    'path': '/usr/bin/checkov',
    'timeout': 600,  # 10 minutes
    'framework': ['terraform', 'cloudformation', 'kubernetes', 'docker'],
    'check_ids': [],  # Empty = all checks
    'skip_check_ids': [],
}

# Nikto Configuration
NIKTO_CONFIG = {
    'enabled': True,
    'path': '/usr/bin/nikto',
    'timeout': 300,  # 5 minutes
    'plugins': 'all',
    'evasion_techniques': [1, 2],  # See nikto docs
}

# SSL/TLS Scanner Configuration
SSL_SCANNER_CONFIG = {
    'enabled': True,
    'path': '/usr/bin/sslscan',
    'timeout': 120,  # 2 minutes
    'check_heartbleed': True,
    'check_ccs_vuln': True,
}

# DNS Enumeration Configuration
DNS_ENUM_CONFIG = {
    'enabled': True,
    'timeout': 60,  # 1 minute
    'dns_servers': ['8.8.8.8', '8.8.4.4'],  # Google DNS
    'wordlist_path': '/usr/share/wordlists/dnsmap.txt',
}

# ============================================================================
# JIRA INTEGRATION
# ============================================================================

JIRA_CONFIG = {
    'enabled': True,
    'server_url': 'https://jira.example.com',
    'username': 'jira_user',
    'password': 'jira_password',  # Consider using API tokens instead
    'project_key': 'VULN',
    'issue_type': 'Bug',
    'auto_create_tickets': False,  # Create tickets automatically
    'verify_ssl': True,
}

# Auto-create ticket for vulnerabilities with severity >= this level
JIRA_AUTO_TICKET_SEVERITY = 'HIGH'  # 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'

# ============================================================================
# SCAN EXECUTION SETTINGS
# ============================================================================

# Maximum concurrent scans per user
MAX_CONCURRENT_SCANS = 5

# Default scan timeout (seconds)
DEFAULT_SCAN_TIMEOUT = 600

# Queue settings for background scan execution
SCAN_QUEUE = {
    'max_queue_size': 100,
    'worker_threads': 4,
}

# ============================================================================
# ORGANIZATION & USER SETTINGS
# ============================================================================

# Default organization name
DEFAULT_ORG_NAME = 'Default Organization'

# User roles (configured via admin interface)
USER_ROLES = {
    'admin': ['all'],
    'analyst': ['scan', 'view_reports'],
    'manager': ['view_reports', 'manage_projects'],
    'viewer': ['view_reports'],
}

# ============================================================================
# EMAIL SETTINGS
# ============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Use your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use app-specific password for Gmail
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ============================================================================
# LOGGING SETTINGS
# ============================================================================

# Log file location
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Scan results storage
SCAN_RESULTS_DIR = os.path.join(BASE_DIR, 'scan_results')
if not os.path.exists(SCAN_RESULTS_DIR):
    os.makedirs(SCAN_RESULTS_DIR)

# ============================================================================
# SECURITY SETTINGS (Production)
# ============================================================================

# SSL/HTTPS Settings
SECURE_SSL_REDIRECT = False  # Set to True in production
SESSION_COOKIE_SECURE = False  # Set to True in production
CSRF_COOKIE_SECURE = False  # Set to True in production
SECURE_HSTS_SECONDS = 0  # Set to 31536000 in production
SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # Set to True in production
SECURE_HSTS_PRELOAD = False  # Set to True in production

# Content Security Policy
SECURE_CONTENT_SECURITY_POLICY = {}

# ============================================================================
# API SETTINGS
# ============================================================================

# JWT Token expiration times (seconds)
JWT_CONFIG = {
    'ACCESS_TOKEN_LIFETIME': 3600,  # 1 hour
    'REFRESH_TOKEN_LIFETIME': 86400,  # 24 hours
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'your-secret-key-change-in-production',
}

# Rate limiting
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    }
}

# ============================================================================
# CACHING
# ============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'vapt',
        'TIMEOUT': 300,
    }
}

# Use simple in-memory cache if Redis is not available
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'vapt-cache',
#     }
# }

# ============================================================================
# CELERY CONFIGURATION (Optional - for task queue)
# ============================================================================

# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'UTC'

# ============================================================================
# OTHER SETTINGS
# ============================================================================

# Media files (uploads)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Database backup settings
DATABASE_BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
if not os.path.exists(DATABASE_BACKUP_DIR):
    os.makedirs(DATABASE_BACKUP_DIR)

# Auto-backup interval (hours)
AUTO_BACKUP_INTERVAL = 24

# Retention period for old scans (days)
SCAN_RETENTION_DAYS = 90

# Delete old scans automatically
AUTO_DELETE_OLD_SCANS = True

# Dashboard settings
DASHBOARD_REFRESH_INTERVAL = 5  # seconds

# Report generation format
REPORT_FORMATS = ['pdf', 'html', 'csv', 'json']
DEFAULT_REPORT_FORMAT = 'pdf'

# Notification settings
SEND_NOTIFICATIONS = True
NOTIFICATION_EMAIL = True
NOTIFICATION_DASHBOARD = True

# ============================================================================
# CUSTOM SETTINGS FOR ADVANCED CONFIGURATIONS
# ============================================================================

# Add any additional custom settings below
# Example:
# CUSTOM_SETTING = 'value'
