# 🚀 Master Deployment Checklist

**Project**: VAPT Scanner - Consolidated Architecture  
**Status**: Ready for Deployment  
**Date**: March 3, 2026  

---

## Phase 1: Pre-Deployment Verification (Local)

### 1.1 Code Verification
- [ ] Clone/have latest code locally
- [ ] No uncommitted changes: `git status`
- [ ] All modified files listed in FIX_SUMMARY.md match actual changes
- [ ] No debug statements in code: `grep -r "print(" . --include="*.py" | wc -l` = 0
- [ ] No hardcoded credentials: `grep -r "password\|key\|secret" . --include="*.py" --exclude-dir=venv | wc -l` = 0

### 1.2 Virtual Environment
- [ ] Virtual environment created: `ls venv/bin/python*`
- [ ] Virtual environment activated: `which python` shows venv path
- [ ] Dependencies installed: `pip list | grep -i django` shows Django 4.2.9
- [ ] No missing dependencies: `pip check` = "No broken requirements"

### 1.3 Database (Development)
- [ ] Database initialized: `ls db.sqlite3` (or PostgreSQL configured)
- [ ] Migrations applied: `python manage.py migrate --plan` shows "all applied"
- [ ] No pending migrations: `python manage.py makemigrations --check` exits 0
- [ ] Superuser created: `python manage.py shell` → `User.objects.filter(is_superuser=True).exists()` = True

### 1.4 URL Routing
- [ ] Main URLs configured: `grep "vaptapi" vapt/urls.py`
- [ ] Web scanner URLs configured: `grep "webscanners" vapt/urls.py`
- [ ] Namespace registration verified: Check all apps in each urls.py include namespace=
  - [ ] webscanners/urls.py has namespace="webscanners"
  - [ ] networkscanners/urls.py has namespace="networkscanners"
  - [ ] staticscanners/urls.py has namespace="staticscanners"
  - [ ] tools/urls.py has namespace="tools"
  - [ ] vaptapi/urls.py has namespace="vaptapi"

### 1.5 Scanner Modules Verification
- [ ] Consolidated modules exist:
  - [ ] `webscanners/scanner_consolidated.py`
  - [ ] `networkscanners/scanner_consolidated.py`
  - [ ] `staticscanners/scanner_consolidated.py`
  - [ ] `tools/scanner_consolidated.py`
- [ ] Stub modules exist:
  - [ ] `webscanners/arachniscanner/`
  - [ ] `webscanners/burpscanner/`

### 1.6 Documentation Completeness
- [ ] README_GITHUB.md exists and is comprehensive
- [ ] QUICK_START.md exists with all 9 scanners documented
- [ ] SCANNER_ARCHITECTURE.md exists with technical details
- [ ] IMPLEMENTATION_SUMMARY.md exists with changes documented
- [ ] KALI_SETUP_GUIDE.md exists with setup steps
- [ ] FIX_SUMMARY.md exists documenting all fixes
- [ ] GIT_PUSH_GUIDE.md exists with push instructions
- [ ] This checklist exists

### 1.7 Static Files
- [ ] Static files collected: `python manage.py collectstatic --dry-run`
- [ ] No collection errors
- [ ] Static directory exists: `ls static/`

### 1.8 Permission Checks
- [ ] Check execute permissions on scripts:
  - [ ] `ls -l setup_kali.sh` shows x permission
  - [ ] `ls -l run.sh` shows x permission
  - [ ] `ls -l manage.py` shows x permission

---

## Phase 2: Local Testing (Development Server)

### 2.1 Server Startup
- [ ] Development server starts: `python manage.py runserver 0.0.0.0:8000`
- [ ] No startup errors in console
- [ ] Server accessible: `curl http://localhost:8000` returns 200/404

### 2.2 Admin Interface
- [ ] Admin page loads: Visit http://localhost:8000/admin/
- [ ] Login works with superuser credentials
- [ ] Projects visible in admin: Admin → Projects → List shows projects
- [ ] Users visible in admin: Admin → Users → List shows users
- [ ] Organizations visible in admin: Admin → Organizations → List

### 2.3 Scanner Accessibility (Web Test)
```bash
# Test each endpoint by visiting in browser
# Expected: Form loads (200 OK) with no errors
```
- [ ] /webscanners/zap/ loads successfully
- [ ] /webscanners/arachni/ loads successfully
- [ ] /webscanners/burp/ loads successfully
- [ ] /networkscanners/nmap/ loads successfully
- [ ] /networkscanners/openvas/ loads successfully
- [ ] /networkscanners/nmap_vulners/ loads successfully
- [ ] /staticscanners/bandit/ loads successfully
- [ ] /staticscanners/semgrep/ loads successfully
- [ ] /staticscanners/checkov/ loads successfully
- [ ] /tools/nikto/ loads successfully
- [ ] /tools/sslscan/ loads successfully
- [ ] /tools/dns_enum/ loads successfully

### 2.4 API Endpoints
```bash
# Test API namespace
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/archerysec/api/
```
- [ ] API endpoint accessible and returns valid response
- [ ] JWT authentication works
- [ ] Namespace resolution working: No reverse errors

### 2.5 Scanner Tool Installation Verification
```bash
# Verify all required tools are available
which nmap
which nikto
which zaproxy (or owasp-zap)
which bandit
which semgrep
which checkov
```
- [ ] Nmap installed: `nmap --version`
- [ ] Nikto installed: `nikto --version`
- [ ] ZAP installed: `~/ZAP_2.X.X/zap.sh --version` OR `zaproxy --version`
- [ ] Bandit installed: `bandit --version`
- [ ] Semgrep installed: `semgrep --version`
- [ ] Checkov installed: `checkov --version`
- [ ] nmap-vulners plugin installed: `ls ~/.nmap/scripts/ | grep vulners`
- [ ] SSL Scanner installed: `sslscan --version` OR available via apt

### 2.6 Quick Functionality Test (Optional)
- [ ] Create test project in admin
- [ ] Visit /webscanners/zap/
- [ ] Click "Create Scan"
- [ ] Enter test domain (e.g., example.com)
- [ ] Click "Start Scan"
- [ ] JSON response shows: `{"status": "success", "scan_id": "..."}`
- [ ] Scan appears in list after refresh

---

## Phase 3: Git Repository Setup

### 3.1 Git Initialization
- [ ] Check if git initialized: `git status`
  - If not: `git init`
- [ ] Remote configured: `git remote -v` shows origin URL
- [ ] .gitignore present: `ls -la .gitignore`
  - [ ] Contains db.sqlite3
  - [ ] Contains venv/
  - [ ] Contains .env
  - [ ] Contains __pycache__/
  - [ ] Contains *.pyc

### 3.2 Pre-Commit Checks
```bash
# Run these checks before committing
python manage.py check
python manage.py test 2>&1 | tail -5
flake8 . --max-line-length=100 --exclude=venv,migrations
```
- [ ] `python manage.py check` passes
- [ ] No critical test failures (warnings OK)
- [ ] Code style check passes (optional but recommended)

### 3.3 First Commit
```bash
git add .
git commit -m "feat: Consolidated VAPT Scanner architecture with 9 scanners

- Create consolidated scanner modules (web, network, static, tools)
- Fix URL namespace routing for vaptapi, arachniscanner, burpscanner
- Implement background threading for non-blocking scans
- Integrate result display with scan interface
- Add comprehensive documentation
- Support Kali Linux deployment
- JWT authentication + organization isolation"
```
- [ ] Commit message is descriptive and follows format
- [ ] No uncommitted changes: `git status` shows clean
- [ ] Commit visible: `git log --oneline -1`

### 3.4 GitHub Repository Creation
- [ ] GitHub account exists and logged in
- [ ] New repository created: https://github.com/NEW
- [ ] Repository name: VAPT_Scanner
- [ ] Not initialized with README/gitignore/license
- [ ] Copy repository URL (HTTPS or SSH)

### 3.5 Remote Configuration
```bash
git remote add origin https://github.com/YOUR_USERNAME/VAPT_Scanner.git
git branch -M main
```
- [ ] Remote URL set correctly: `git remote -v`
- [ ] Shows: `origin https://github.com/YOUR_USERNAME/VAPT_Scanner.git (fetch)`
- [ ] Branch renamed to main: `git branch`

### 3.6 Push to GitHub
```bash
git push -u origin main
```
- [ ] Push completes without errors
- [ ] GitHub repository now shows files
- [ ] README_GITHUB.md displays as main page
- [ ] Commit history visible on GitHub
- [ ] All files present on GitHub

---

## Phase 4: Kali Linux Deployment

### 4.1 Pre-Deployment on Kali
- [ ] SSH access to Kali machine (or local if running on Kali)
- [ ] User has sudo privileges
- [ ] Kali is fully updated: `sudo apt-get update && sudo apt-get upgrade -y`
- [ ] At least 20GB free disk space: `df -h /`
- [ ] Python 3.10+ installed: `python3 --version`
- [ ] Git installed: `git --version`

### 4.2 Clone on Kali
```bash
cd /opt/
sudo git clone https://github.com/YOUR_USERNAME/VAPT_Scanner.git
sudo chown -R $USER:$USER VAPT_Scanner
cd VAPT_Scanner
```
- [ ] Repository cloned successfully
- [ ] All files present: `ls -la`
- [ ] Setup scripts present: `ls -la setup_kali.sh`

### 4.3 Run Setup Script
```bash
chmod +x setup_kali.sh
./setup_kali.sh
```
- [ ] Script execution completes without critical errors
- [ ] Python virtual environment created: `ls venv/bin/python*`
- [ ] All tools installed: Script ends successfully
- [ ] Dependencies installed: `source venv/bin/activate && pip list | grep -i django`

### 4.4 Manual Setup (If script fails)
```bash
# Follow KALI_SETUP_GUIDE.md step by step
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```
- [ ] Virtual env activated
- [ ] Dependencies installed without errors
- [ ] Database migrations completed
- [ ] Superuser created

### 4.5 Verify Scanner Tools on Kali
```bash
# Run all tool version checks
nmap --version
nikto -help | head -3
zaproxy -version 2>/dev/null || echo "ZAP installed"
bandit --version
semgrep --version
checkov --version
```
- [ ] All tools report versions or are installed
- [ ] No "command not found" errors
- [ ] Note any tools that failed to install

### 4.6 Services Setup (Optional - Production)
```bash
sudo cp systemd/vapt-scanner.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable vapt-scanner
sudo systemctl start vapt-scanner
sudo systemctl status vapt-scanner
```
- [ ] Service file copied
- [ ] Service enabled
- [ ] Service status shows "active (running)"

### 4.7 Nginx Configuration (Optional - Production)
```bash
# See KALI_SETUP_GUIDE.md for full nginx config
# Copy nginx config
sudo cp nginx/vapt-scanner.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/vapt-scanner.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```
- [ ] Nginx config syntax valid
- [ ] Nginx restart successful
- [ ] Service accessible at http://localhost (or configured domain)

---

## Phase 5: Post-Deployment Testing

### 5.1 Web Interface Access
```bash
# Development mode
python manage.py runserver 0.0.0.0:8000

# Or production with gunicorn
gunicorn vapt.wsgi --bind 0.0.0.0:8000
```
- [ ] Server starts successfully
- [ ] Web interface accessible at http://localhost:8000
- [ ] Login page loads
- [ ] Admin panel accessible

### 5.2 Full Scanner Test Cycle

#### Test 1: Web Scanner (ZAP)
```
1. Visit http://localhost:8000/webscanners/zap/
2. Create or select project
3. Enter target URL: http://example.com
4. Click "Scan"
5. Observe: JSON response with scan_id
6. Refresh page: Scan appears in list
7. Wait: Status updates (Running → Completed)
8. Results: Vulnerabilities display
```
- [ ] All steps completed without errors
- [ ] Scan status transitions work
- [ ] Results display correctly

#### Test 2: Network Scanner (Nmap)
```
1. Visit http://localhost:8000/networkscanners/nmap/
2. Enter target: 192.168.1.0/24 (local network)
3. Click "Scan"
4. Wait: 30 seconds to 15 minutes
5. Results: Open ports displayed
```
- [ ] Scan starts successfully
- [ ] Results show port information
- [ ] No permission errors

#### Test 3: Code Scanner (Bandit)
```
1. Visit http://localhost:8000/staticscanners/bandit/
2. Enter path: /path/to/test/python/project
3. Click "Scan"
4. Wait: 30 seconds to 2 minutes
5. Results: Python security issues displayed
```
- [ ] Scan completes successfully
- [ ] Vulnerabilities identified
- [ ] Issues are legitimate

### 5.3 Performance Baseline
- [ ] Note scan execution times:
  - [ ] ZAP: Expected 5-30 minutes (depends on site)
  - [ ] Nmap: Expected 1-15 minutes
  - [ ] Bandit: Expected 30 seconds - 2 minutes
  - [ ] Semgrep: Expected 1-5 minutes
  - [ ] Nikto: Expected 2-5 minutes

### 5.4 Error Handling
- [ ] Attempt invalid inputs:
  - [ ] Empty target field → Shows error
  - [ ] Invalid IP/domain → Shows error
  - [ ] Non-existent path → Shows error
- [ ] Attempt without authentication:
  - [ ] Redirect to login works
- [ ] Test permission checks:
  - [ ] Non-analyst user can't scan: Forbidden error
  - [ ] Analyst user can scan: Success

### 5.5 Data Persistence
- [ ] Browser refresh doesn't lose data
- [ ] Scan results persist after reload
- [ ] Database correctly stores scans:
  ```bash
  python manage.py shell
  >>> from webscanners.models import WebScanDb
  >>> WebScanDb.objects.count()  # Should be > 0
  ```
- [ ] Admin interface shows scans: Admin → Web Scans → List

### 5.6 Notifications (If Enabled)
- [ ] Scan completion sends notification
- [ ] User receives notification alert
- [ ] Notification contains timestamp

---

## Phase 6: Production Hardening (Optional but Recommended)

### 6.1 Security Settings
Update `vapt/settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'api.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```
- [ ] DEBUG set to False
- [ ] ALLOWED_HOSTS configured
- [ ] SSL settings enabled
- [ ] Cookies set secure

### 6.2 Environment Variables
Create `.env` file (add to .gitignore):
```
DEBUG=False
SECRET_KEY=<generate-new-secret>
DATABASE_URL=postgresql://user:pass@localhost:5432/vapt
ALLOWED_HOSTS=yourdomain.com
```
- [ ] .env file created
- [ ] SECRET_KEY regenerated
- [ ] Database credentials in .env
- [ ] .env added to .gitignore

### 6.3 Database Backup
```bash
# PostgreSQL backup
pg_dump -U vapt_user vapt_database > backup_$(date +%Y%m%d).sql

# SQLite backup
cp db.sqlite3 backup_db_$(date +%Y%m%d).sqlite3
```
- [ ] Backup script created
- [ ] First backup completed
- [ ] Backup size reasonable
- [ ] Backup stored safely

### 6.4 SSL Certificate
```bash
# Using certbot with Let's Encrypt
sudo certbot certonly --standalone -d yourdomain.com
# Copy certificates to nginx/apache config
```
- [ ] SSL certificate obtained
- [ ] Certificate installed
- [ ] HTTPS accessible: https://yourdomain.com
- [ ] No SSL warnings

### 6.5 Firewall Rules
```bash
# Example for UFW on Ubuntu/Kali
sudo ufw allow 22/tcp     # SSH
sudo ufw allow 80/tcp     # HTTP
sudo ufw allow 443/tcp    # HTTPS
sudo ufw enable
```
- [ ] Firewall rules configured
- [ ] Necessary ports open
- [ ] Unnecessary ports closed

### 6.6 Monitoring Setup (Optional)
- [ ] Log rotation configured: `sudo apt-get install logrotate`
- [ ] System monitoring setup: `sudo apt-get install htop`
- [ ] Database monitoring: Check connection pool
- [ ] Application monitoring: Log file location known

---

## Phase 7: Documentation & Handover

### 7.1 Project Documentation
- [ ] README.md updated with deployment info
- [ ] QUICK_START.md reviewed and accurate
- [ ] KALI_SETUP_GUIDE.md tested and correct
- [ ] API documentation complete: SCANNER_ARCHITECTURE.md
- [ ] Troubleshooting guide created: Linked in README

### 7.2 Code Documentation
- [ ] All views have docstrings
- [ ] Complex logic has inline comments
- [ ] Scanner implementations documented
- [ ] Database models documented

### 7.3 Operations Handbook
Create `OPERATIONS.md`:
```
## Daily Operations
- Check disk space for scan results
- Review error logs for issues
- Monitor performance metrics

## Weekly Tasks
- Review scan history and trends
- Clean up old temporary files
- Check for security updates

## Monthly Tasks
- Database backup verification
- Security audit
- Performance review
- Dependency updates
```
- [ ] Operations handbook created
- [ ] Daily/Weekly/Monthly tasks defined
- [ ] Emergency procedures documented
- [ ] On-call rotation defined

### 7.4 Knowledge Transfer
- [ ] Admin trained on deployment
- [ ] Analysts trained on scanner usage
- [ ] Support team has access to documentation
- [ ] Escalation procedures documented

### 7.5 Version Control Finalization
```bash
# Create release tag
git tag -a v2.0 -m "Release 2.0 - Consolidated Architecture"
git push origin v2.0

# Create GitHub Release
# On GitHub: Releases → Create Release
# Tag: v2.0
# Title: VAPT Scanner 2.0 - Consolidated Architecture
# Description: Copy from IMPLEMENTATION_SUMMARY.md
```
- [ ] Git tag created and pushed
- [ ] GitHub Release created
- [ ] Release notes comprehensive
- [ ] Download instructions clear

---

## Phase 8: Monitoring & Maintenance

### 8.1 Health Checks
Create health check endpoint or monitoring script:
```bash
#!/bin/bash
# Check service status
curl http://localhost:8000/admin/ -f > /dev/null && echo "✓ Web" || echo "✗ Web"
curl http://localhost:8000/api/ -f > /dev/null && echo "✓ API" || echo "✗ API"
which nmap > /dev/null && echo "✓ Nmap" || echo "✗ Nmap"
which bandit > /dev/null && echo "✓ Bandit" || echo "✗ Bandit"
```
- [ ] Health check script created
- [ ] All components report healthy
- [ ] Health check runs successfully

### 8.2 Log Monitoring
```bash
# View application logs
tail -f logs/vapt.log

# View errors only
grep ERROR logs/vapt.log | tail -20

# Check system logs
sudo journalctl -u vapt-scanner -n 50
```
- [ ] Log file location known
- [ ] Logs contain useful information
- [ ] Error messages are actionable
- [ ] Log rotation configured

### 8.3 Performance Monitoring
```bash
# Check resource usage
top -u vapt_user
# Check disk usage for scans
du -sh /opt/VAPT_Scanner/
# Check database size
sudo du -sh /var/lib/postgresql/
```
- [ ] CPU usage within normal range
- [ ] Memory usage acceptable
- [ ] Disk usage monitored
- [ ] Database growth tracked

### 8.4 Security Updates
```bash
# Check for updates
pip list --outdated
sudo apt-get update && apt-cache search security

# Update dependencies safely
pip install --upgrade <package>
python manage.py test  # Ensure compatibility
```
- [ ] Update process documented
- [ ] Testing process before production
- [ ] Rollback plan if needed
- [ ] Update schedule established

### 8.5 Backup Verification
```bash
# Test backup restoration
# 1. Create backup
# 2. Delete test data
# 3. Restore from backup
# 4. Verify data integrity
```
- [ ] Backup creation automated
- [ ] Restoration process tested
- [ ] Data integrity verified
- [ ] Backup retention policy set

---

## Final Sign-Off

```
✅ All phases completed
✅ All tests passed
✅ All documentation complete
✅ All tools functional
✅ Production ready

Status: 🟢 READY FOR DEPLOYMENT
```

### Signed Off By:
- Date: _____________
- Reviewer: _____________
- Authorized By: _____________

---

## Quick Command Reference

```bash
# Start development server
python manage.py runserver 0.0.0.0:8000

# Start production server
gunicorn vapt.wsgi --bind 0.0.0.0:8000

# Run tests
python manage.py test

# Check status
systemctl status vapt-scanner

# View logs
tail -f /var/log/vapt-scanner.log

# Create backup
python manage.py dumpdata > backup.json

# Restore backup
python manage.py loaddata backup.json
```

---

**Document Version**: 2.0  
**Last Updated**: March 3, 2026  
**Next Review**: After First Deployment
