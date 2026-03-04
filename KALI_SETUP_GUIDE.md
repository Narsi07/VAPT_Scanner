# VAPT Scanner - Kali Linux Setup Guide

## Overview

VAPT Scanner (Vulnerable Application Penetration Testing Scanner) is a comprehensive vulnerability assessment and penetration testing platform built with Django. It integrates multiple open-source security tools for comprehensive application scanning.

## System Requirements

- **OS**: Kali Linux 2023+ or any Debian-based Linux distribution
- **Python**: 3.10+
- **Database**: PostgreSQL 12+
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: Minimum 10GB
- **Network**: Internet access for updates and tool downloads

## Prerequisites Installation

### 1. Update System
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. Install Core Dependencies
```bash
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    postgresql-client \
    libpq-dev \
    libmagic1
```

### 3. Install Security Tools
```bash
# Network scanning
sudo apt-get install -y nmap

# Web vulnerability scanning
sudo apt-get install -y zaproxy

# Static code analysis
sudo apt-get install -y bandit
pip install semgrep

# Web server testing
sudo apt-get install -y nikto

# Docker (optional for containerized scanning)
sudo apt-get install -y docker.io
```

## Installation Steps

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd VAPT_Scanner
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Database Setup

#### Option A: SQLite (Development/Testing)
No additional setup needed. Django will create the database automatically.

#### Option B: PostgreSQL (Recommended for Production)

1. Install PostgreSQL:
```bash
sudo apt-get install -y postgresql postgresql-contrib
sudo systemctl start postgresql
```

2. Create database:
```bash
sudo -u postgres psql
```

3. Execute SQL:
```sql
CREATE DATABASE vapt_db;
CREATE USER vapt_user WITH PASSWORD 'secure_password';
ALTER ROLE vapt_user SET client_encoding TO 'utf8';
ALTER ROLE vapt_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE vapt_user SET default_transaction_deferrable TO on;
ALTER ROLE vapt_user SET default_transaction_level TO 'read committed';
ALTER ROLE vapt_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE vapt_db TO vapt_user;
\q
```

### Step 5: Configure Django

Create a `.env` file in the project root:

```bash
cat > .env << EOF
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DATABASE_URL=postgresql://vapt_user:secure_password@localhost:5432/vapt_db
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,yourdomain.com
EOF
```

### Step 6: Initialize Database

```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### Step 7: Verify Installation

```bash
python manage.py check
```

## Running the Application

### Development Server
```bash
source venv/bin/activate
export $(cat .env | xargs)
python manage.py runserver 0.0.0.0:8000
```

Access: http://localhost:8000

### Production Server (Gunicorn)
```bash
source venv/bin/activate
export $(cat .env | xargs)
gunicorn -w 4 -b 0.0.0.0:8000 vapt.wsgi --timeout 300
```

### Automated Setup Script
```bash
chmod +x setup_kali.sh
./setup_kali.sh
```

## Available Scanning Tools

### Web Application Scanners
- **OWASP ZAP**: Dynamic web application scanning
- **Nikto**: Web server scanning
- **Arachni**: Web application spider (deprecated, stub provided)

### Network Scanners
- **Nmap**: Network mapping and port scanning
- **Nmap-Vulners**: Vulnerability detection for Nmap
- **OpenVAS**: Comprehensive network vulnerability assessment

### Static Code Analysis
- **Bandit**: Python security issue detection
- **Semgrep**: Pattern-based static analysis
- **SAST scanning**: Source code vulnerability detection

### Additional Tools
- **SSL/TLS Analysis**
- **DNS Enumeration**
- **WHOIS Lookup**
- **HTTP Header Analysis**

## Key Features

✅ Multi-user authentication with role-based access
✅ Organization-based resource isolation
✅ Scan scheduling and automation
✅ Vulnerability tracking and management
✅ JIRA integration for issue tracking
✅ Report generation (PDF, HTML, JSON)
✅ RESTful API for integration
✅ Notification system
✅ API key management
✅ Scan history and trending

## API Endpoints

Base URL: `http://localhost:8000/archerysec/api/`

### Authentication
- `POST /v1/auth/login/` - User login
- `POST /v1/auth/logout/` - User logout
- `POST /v1/auth/refresh-token/` - Refresh JWT token
- `POST /v1/auth/forgot-pass/` - Request password reset

### Scans
- `GET /v1/web-scans/` - List web scans
- `GET /v1/network-scans/` - List network scans
- `GET /v1/sast-scans/` - List static scans
- `POST /v1/zap-scan/` - Trigger ZAP scan
- `POST /v1/bandit_scan/` - Trigger Bandit scan
- `POST /v1/semgrep_scan/` - Trigger Semgrep scan

### Management
- `GET /v1/project-list/` - List projects
- `POST /v1/project-create/` - Create project
- `GET /v1/users/user/` - List users
- `POST /v1/users/user/` - Create user

## Troubleshooting

### Issue: "No module named 'arachniscanner'"
**Solution**: This is now fixed with stub modules. Arachni is deprecated.

### Issue: "NoReverseMatch: 'arachniscanner' is not a registered namespace"
**Solution**: All namespaces are now properly registered in URLs.

### Issue: "Method Not Allowed" on /staticscanners/semgrep_scan/
**Solution**: Added GET methods to support form rendering.

### Issue: Cannot connect to database
```bash
# Check PostgreSQL status
systemctl status postgresql

# Verify connection
psql -U vapt_user -d vapt_db -h localhost
```

### Issue: Permission denied on setup_kali.sh
```bash
chmod +x setup_kali.sh
```

### Issue: Port 8000 already in use
```bash
# Find and kill process using port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
python manage.py runserver 0.0.0.0:8080
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DJANGO_DEBUG | Debug mode | 0 (Production) |
| DJANGO_SECRET_KEY | Django secret key | Generated |
| DATABASE_URL | Database connection string | sqlite:///db.sqlite3 |
| ALLOWED_HOSTS | Allowed hostnames | localhost,127.0.0.1 |
| DJANGO_SUPERUSER_USERNAME | Admin username | admin |
| DJANGO_SUPERUSER_PASSWORD | Admin password | admin123 |
| DJANGO_SUPERUSER_EMAIL | Admin email | admin@example.com |

## Security Recommendations

⚠️ **IMPORTANT FOR PRODUCTION:**

1. Change default admin credentials
2. Set `DJANGO_DEBUG=0`
3. Generate strong `DJANGO_SECRET_KEY`
4. Use HTTPS/TLS
5. Implement proper authentication
6. Restrict database access
7. Use environment variables for sensitive data
8. Implement regular backups
9. Keep dependencies updated
10. Run behind a reverse proxy (Nginx)

## Nginx Configuration Example

```nginx
upstream vapt {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name _;
    client_max_body_size 100M;

    location /static/ {
        alias /path/to/VAPT_Scanner/static/;
    }

    location / {
        proxy_pass http://vapt;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Systemd Service File

Create `/etc/systemd/system/vapt.service`:

```ini
[Unit]
Description=VAPT Scanner Service
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/VAPT_Scanner
Environment="PATH=/path/to/VAPT_Scanner/venv/bin"
EnvironmentFile=/path/to/VAPT_Scanner/.env
ExecStart=/path/to/VAPT_Scanner/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    --timeout 300 \
    vapt.wsgi

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable vapt
sudo systemctl start vapt
sudo systemctl status vapt
```

## Maintenance Tasks

### Backup Database
```bash
pg_dump -U vapt_user -d vapt_db > backup_$(date +%Y%m%d).sql
```

### Restore Database
```bash
psql -U vapt_user -d vapt_db < backup_file.sql
```

### Update Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

### Clean Up Old Scans
```bash
python manage.py shell
```
```python
from django.utils import timezone
from datetime import timedelta
from webscanners.models import WebScansDb

# Delete scans older than 90 days
cutoff = timezone.now() - timedelta(days=90)
WebScansDb.objects.filter(date_time__lt=cutoff).delete()
```

## References

- **Repository**: https://github.com/archerysec/archerysec
- **Django Documentation**: https://docs.djangoproject.com/
- **OWASP ZAP**: https://www.zaproxy.org/
- **Nmap**: https://nmap.org/
- **Bandit**: https://bandit.readthedocs.io/

## Support & Contribution

For issues, questions, or contributions, please refer to the GitHub repository.

## License

Please check the LICENSE file in the repository for license information.

---

**Last Updated**: March 3, 2026
**Kali Linux Tested**: Version 2023.4+
