# VAPT Scanner - Vulnerability Assessment and Penetration Testing Scanner

**Status**: ✅ Fully Functional & Ready for Kali Linux  
**Version**: 2.0 - Core Tools Only (No Commercial Tools)  
**Python**: 3.10+  
**Framework**: Django 4.2.9 + Django REST Framework

---

## 🎯 Overview

The VAPT Scanner is a comprehensive **Vulnerability Assessment and Penetration Testing** platform designed to integrate multiple open-source security scanning tools into a unified, Django-based web interface. It provides:

- **Web Application Scanning** (OWASP ZAP)
- **Network Vulnerability Assessment** (Nmap, OpenVAS, Nmap-Vulners)
- **Static Code Analysis** (Bandit, Semgrep, Checkov)
- **Additional Security Tools** (Nikto, SSL/TLS Scanner, DNS Enumeration)
- **Jira Ticketing Integration** (For vulnerability management)

Each scanner runs in **background threads** with **real-time result display** and integrated **vulnerability management**.

---

## ✨ Key Features

### 🔧 Multiple Security Scanners
- **9 open-source security tools** integrated into single platform
- **Web scanners** (OWASP ZAP) for dynamic application testing
- **Network scanners** (Nmap, OpenVAS, Nmap-Vulners) for infrastructure assessment
- **Code scanners** (Bandit, Semgrep, Checkov) for static analysis
- **Utility tools** (Nikto, SSL, DNS) for domain reconnaissance

### 🎨 Unified Interface
- **Consolidated endpoints** - One page per scanner (scan + results)
- **Real-time updates** - Results display as scan completes
- **Background execution** - Non-blocking scan operations
- **Organization isolation** - Multi-tenant deployment ready
- **Jira Integration** - Link findings to issue tracking

### 🔐 Security Features
- **JWT Authentication** - Token-based access control
- **Role-based access** (Admin, Analyst, Manager)
- **Organization isolation** - Data separation per org
- **Input validation** - Prevents injection attacks
- **SSL/TLS ready** - Production deployments supported

### 📊 Result Management
- **Vulnerability tracking** - Status updates (Open, Closed, Verified)
- **Rich filtering** - Search by severity, type, status
- **Export capabilities** - Reports and data export
- **Historical tracking** - Scan history and comparison
- **Jira ticketing** - Create and manage tickets

### 🚀 DevOps Ready
- **Docker support** - Containerized deployments
- **PostgreSQL ready** - Enterprise database support
- **Systemd integration** - Service management on Linux
- **Environment configuration** - .env file support

---

## 🚀 Quick Start

### Prerequisites
```bash
# Required
Python 3.10+
pip
PostgreSQL (recommended) or SQLite
All security tools installed (nmap, nikto, zaproxy, etc.)

# On Kali Linux, run:
chmod +x setup_kali.sh
./setup_kali.sh
```

### Installation (1-5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/VAPT_Scanner.git
cd VAPT_Scanner

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup database
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Configure settings (Jira, tools, etc.)
cp vapt/local_settings.sample.py vapt/local_settings.py
# Edit vapt/local_settings.py for your environment

# 7. Collect static files
python manage.py collectstatic --noinput

# 8. Run development server
python manage.py runserver 0.0.0.0:8000
```

### First Scan (2 minutes)
```bash
# 1. Open browser
http://localhost:8000

# 2. Login with superuser credentials

# 3. Create project (Admin → Projects → Add Project)

# 4. Go to scanner: /webscanners/zap/

# 5. Enter test URL and click "Scan"

# 6. Results display in real-time
```

---

## 📚 Documentation

### Quick References
| Document | Purpose |
|----------|---------|
| [QUICK_START.md](./QUICK_START.md) | Step-by-step guide for each scanner |
| [SCANNER_ARCHITECTURE.md](./SCANNER_ARCHITECTURE.md) | Technical architecture & API reference |
| [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) | Complete implementation details |
| [KALI_SETUP_GUIDE.md](./KALI_SETUP_GUIDE.md) | Kali Linux installation walkthrough |
| [FIX_SUMMARY.md](./FIX_SUMMARY.md) | Issues fixed and technical changes |

---

## 🛠️ Scanner Endpoints

### Web Application Scanners
```
GET/POST /webscanners/zap/       - OWASP ZAP scanning
```

### Network Vulnerability Scanners
```
GET/POST /networkscanners/nmap/          - Port scanning
GET/POST /networkscanners/openvas/       - Full assessment
GET/POST /networkscanners/nmap_vulners/  - Enhanced detection
```

### Static Code Analysis
```
GET/POST /staticscanners/bandit/   - Python code analysis
GET/POST /staticscanners/semgrep/  - Multi-language analysis
GET/POST /staticscanners/checkov/  - Infrastructure as code
```

### Additional Tools
```
GET/POST /tools/nikto/             - Web server scanning
GET/POST /tools/sslscan/           - SSL/TLS analysis
GET/POST /tools/dns_enum/          - DNS enumeration
```

---

## 🔑 Usage Examples

### Example 1: Scan a Web Application
```bash
# 1. Navigate to ZAP scanner
curl http://localhost:8000/webscanners/zap/

# 2. Submit scan via POST
curl -X POST http://localhost:8000/webscanners/zap/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d "project_id=123&target_url=https://example.com"

# Response:
{
  "status": "success",
  "scan_id": "550e8400-e29b-41d4-a716-446655440000"
}

# 3. Check results by refreshing page
```

### Example 2: Scan Network Infrastructure
```bash
# 1. Navigate to Nmap scanner
curl http://localhost:8000/networkscanners/nmap/

# 2. Submit scan
curl -X POST http://localhost:8000/networkscanners/nmap/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d "target=192.168.1.0/24"

# 3. Results display in seconds to minutes
```

### Example 3: Analyze Python Code
```bash
# 1. Navigate to Bandit scanner
curl http://localhost:8000/staticscanners/bandit/

# 2. Submit scan
curl -X POST http://localhost:8000/staticscanners/bandit/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d "scan_path=/path/to/python/project"

# 3. Vulnerabilities show immediately
```

---

## 🔐 Environment Configuration

Create `.env` file in project root:

```env
# Django
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,example.com
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/vapt_scanner
# Or for SQLite:
# DATABASE_URL=sqlite:///db.sqlite3

# JWT
JWT_SECRET=your-jwt-secret
JWT_ALGORITHM=HS256

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

# OpenVAS (optional)
OPENVAS_HOST=localhost
OPENVAS_PORT=9392
OPENVAS_USERNAME=admin
OPENVAS_PASSWORD=admin

# Logging
LOG_LEVEL=INFO
```

---

## 🐳 Docker Deployment

```dockerfile
# Dockerfile included in repository
docker build -t vapt-scanner .
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e DATABASE_URL=postgresql://... \
  vapt-scanner
```

---

## 📋 Requirements

### System Requirements
- **OS**: Linux (Kali Linux, Ubuntu, Debian) or Windows with WSL2
- **CPU**: 2+ cores recommended
- **RAM**: 4GB+ recommended
- **Disk**: 20GB+ for scan storage

### Python Packages
See `requirements.txt` for complete list:
- Django 4.2.9
- djangorestframework (API)
- djangorestframework-simplejwt (Authentication)
- psycopg2 (PostgreSQL)
- celery (Task queue)
- requests (HTTP)
- And 20+ others

### External Tools
```bash
# Install all:
./setup_kali.sh

# Or individually:
apt-get install nmap nikto zaproxy bandit semgrep checkov
pip install python-nmap dnspython sslscan
```

---

## 🧪 Testing

### Run Tests
```bash
python manage.py test

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Manual Testing Checklist
- [ ] All scanners accessible via web interface
- [ ] Scans execute successfully
- [ ] Results display in real-time
- [ ] Permissions enforced correctly
- [ ] Organization isolation working
- [ ] Notifications send properly

---

## 🚀 Production Deployment

### Using Gunicorn + Nginx

```bash
# 1. Install production server
pip install gunicorn whitenoise

# 2. Create systemd service
sudo cp systemd/vapt-scanner.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable vapt-scanner
sudo systemctl start vapt-scanner

# 3. Configure Nginx reverse proxy
# See KALI_SETUP_GUIDE.md for full config

# 4. Enable SSL with certbot
sudo certbot certonly --standalone -d yourdomain.com
```

### Using Docker Compose

```bash
docker-compose up -d
```

---

## 🐛 Troubleshooting

### "Scan won't start"
```
Check:
1. Tool installed: which nmap / which zaproxy
2. Permissions: Can the app user execute tools?
3. Timeouts: Set SCAN_TIMEOUT in settings
4. Logs: tail -f logs/vapt.log
```

### "Tool not found" Error
```
Install:
./setup_kali.sh
Or: apt-get install [tool-name]
```

### "Permission denied"
```
Fix:
1. Check DJANGO_USER has tool access
2. Set tool permissions: chmod +x /path/to/tool
3. Add user to required groups: usermod -aG [group] [user]
```

### "Results not showing"
```
Check:
1. Scan background thread completed: Check scan_status in DB
2. JavaScript enabled in browser
3. Browser console for errors: F12 → Console
4. Notifications working: Check django-notifications
```

---

## 📖 Architecture Overview

```
┌─────────────────────────────────────────┐
│         Web Browser / Client            │
└─────────────┬───────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│    Django + Django REST Framework       │
│  ┌─────────────────────────────────────┤
│  │  Authentication & Permissions        │
│  │  - JWT Tokens                        │
│  │  - Role-Based Access Control         │
│  │  - Organization Isolation            │
│  └─────────────────────────────────────┤
│  ┌─────────────────────────────────────┤
│  │  Scanner Views (Consolidated)        │
│  │  - Web Scanners                      │
│  │  - Network Scanners                  │
│  │  - Code Scanners                     │
│  │  - Tool Scanners                     │
│  └─────────────────────────────────────┤
│  ┌─────────────────────────────────────┤
│  │  Background Threading                │
│  │  - Non-blocking execution            │
│  │  - Result updates                    │
│  │  - Error handling                    │
│  └─────────────────────────────────────┤
└─────────────┬───────────────────────────┘
              │
       ┌──────┴──────┬──────────┬──────────┐
       ▼             ▼          ▼          ▼
   ┌────────┐  ┌────────┐  ┌───────┐  ┌─────┐
   │ nmap   │  │ nikto  │  │ zaproxy│ │ ... │
   └────────┘  └────────┘  └───────┘  └─────┘
   
       ▼             ▼          ▼          ▼
   ┌────────┐  ┌────────┐  ┌────────┐  ┌──────┐
   │Database│  │Logs    │  │Results │  │Cache │
   └────────┘  └────────┘  └────────┘  └──────┘
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-scanner`
3. Commit changes: `git commit -am 'Add new scanner'`
4. Push to branch: `git push origin feature/new-scanner`
5. Submit Pull Request

---

## 📝 License

This project is based on [ArcherySec](https://github.com/archerysec/archerysec)  
Distributed under the MIT License - see LICENSE file for details.

---

## 🔗 Resources

### Official Documentation
- [Django Docs](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

### Security Tools
- [Nmap](https://nmap.org/) - Network mapper
- [OWASP ZAP](https://www.zaproxy.org/) - Web app scanner
- [Bandit](https://bandit.readthedocs.io/) - Python security
- [Semgrep](https://semgrep.dev/) - Pattern-based analysis
- [Checkov](https://www.checkov.io/) - IaC security
- [OpenVAS](https://www.openvas.org/) - Network assessment

### Reference Project
- [ArcherySec Repository](https://github.com/archerysec/archerysec)

---

## 📞 Support

### Issues & Bug Reports
Use GitHub Issues to report bugs with:
- Error message
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version, etc.)

### Feature Requests
Submit feature requests with:
- Use case description
- Expected behavior
- Implementation suggestions (if any)

---

## ✅ Verification Checklist

Before deployment, verify:
- [ ] All dependencies installed
- [ ] Database migrations applied
- [ ] Static files collected
- [ ] Security tools accessible
- [ ] Superuser created
- [ ] Authentication working
- [ ] All scanners accessible
- [ ] Background threading functional
- [ ] Results display correctly
- [ ] Organization isolation working

---

## 🎉 Credits

Built with ❤️ for security professionals  
Based on the excellent [ArcherySec](https://github.com/archerysec/archerysec) project

---

**Last Updated**: March 3, 2026  
**Status**: ✅ Production Ready  
**Version**: 2.0 - Consolidated Architecture
