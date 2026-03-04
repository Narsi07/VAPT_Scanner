# 📋 CORE TOOLS ONLY - Updated Configuration

**Date**: March 3, 2026  
**Focus**: Remove non-core tools (Burp, Arachni) - Focus on existing, functional tools  
**Jira Integration**: Enabled for vulnerability management  

---

## Changes Made

### 1. Removed Non-Core Tools

**Removed**:
- ❌ Burp Suite (Commercial, requires license)
- ❌ Arachni Scanner (Deprecated)

**Kept**:
- ✅ OWASP ZAP (Web apps)
- ✅ Nmap (Network scanning)
- ✅ OpenVAS (Vulnerabilities)
- ✅ Bandit (Python security)
- ✅ Semgrep (Multi-language)
- ✅ Checkov (Infrastructure)
- ✅ Nikto (Web servers)
- ✅ SSL Scanner (SSL/TLS)
- ✅ DNS Enumeration (Recon)

### 2. Files Removed from Code

```
webscanners/arachniscanner/     ← Removed (but kept for compatibility if needed)
webscanners/burpscanner/        ← Removed (but kept for compatibility if needed)

URL imports removed from:
- webscanners/urls.py (removed ArachniScannerView, BurpScannerView)
- webscanners/scanner_consolidated.py (removed stub classes)
- vaptapi/urls.py (removed Burp and Arachni endpoints)
```

### 3. Updated Configuration Files

**Updated Files**:
1. `webscanners/urls.py` - Removed Burp/Arachni routes
2. `webscanners/scanner_consolidated.py` - Removed stub classes
3. `vaptapi/urls.py` - Removed Burp/Arachni API endpoints
4. `vapt/local_settings.sample.py` - Added comprehensive tool configs

### 4. Core Endpoints (Only These)

```
WEB APPLICATION SCANNING:
POST/GET  /webscanners/zap/              → OWASP ZAP scanning

NETWORK VULNERABILITY:
POST/GET  /networkscanners/nmap/         → Port scanning + service detection
POST/GET  /networkscanners/openvas/      → Full network vulnerability assessment
POST/GET  /networkscanners/nmap_vulners/ → Enhanced vulnerability detection

CODE & INFRASTRUCTURE:
POST/GET  /staticscanners/bandit/        → Python code security analysis
POST/GET  /staticscanners/semgrep/       → Multi-language pattern detection
POST/GET  /staticscanners/checkov/       → Infrastructure as Code security

ADDITIONAL TOOLS:
POST/GET  /tools/nikto/                  → Web server scanning
POST/GET  /tools/sslscan/                → SSL/TLS certificate analysis
POST/GET  /tools/dns_enum/               → DNS enumeration & subdomain discovery
```

---

## ✅ What's Configured

### 1. Security Scanners Settings

All scanners have configuration templates in `vapt/local_settings.sample.py`:

```python
# Copy to local_settings.py and configure:

ZAP_CONFIG = {
    'proxy_address': '127.0.0.1',
    'proxy_port': 8090,
    'timeout': 300,
}

NMAP_CONFIG = {
    'path': '/usr/bin/nmap',
    'timeout': 900,
    'common_arguments': ['-sV', '-sC'],
}

OPENVAS_CONFIG = {
    'host': '127.0.0.1',
    'port': 9392,
    'username': 'admin',
    'password': 'admin',
}

BANDIT_CONFIG = {
    'path': '/usr/bin/bandit',
    'timeout': 300,
    'severity_level': 'medium',
}

# ... and more for Semgrep, Checkov, Nikto, SSL, DNS
```

### 2. Jira Ticketing Integration ✅

Already implemented in `jiraticketing/`:

```python
JIRA_CONFIG = {
    'enabled': True,
    'server_url': 'https://jira.example.com',
    'username': 'jira_user',
    'password': 'jira_password',
    'project_key': 'VULN',
    'auto_create_tickets': False,
}
```

**Features**:
- Link vulnerabilities to Jira tickets
- Auto-create tickets for critical findings
- Track remediation status
- Bidirectional sync (future)

**API Endpoint**:
```
POST /archerysec/api/v1/update-jira/
```

### 3. User Interface

**Settings Section** (AdminPanel):
```
Admin → Settings → Jira Ticketing
                 → Scanner Configuration  
                 → Notification Settings
```

All configuration matches reference GitHub project format.

---

## 🚀 How to Use

### 1. Copy and Configure Settings

```bash
# Copy example settings
cp vapt/local_settings.sample.py vapt/local_settings.py

# Edit for your environment
nano vapt/local_settings.py
# or
vim vapt/local_settings.py
```

### 2. Configure Each Scanner

Edit `vapt/local_settings.py`:

```python
# ZAP must be running as proxy
ZAP_CONFIG = {
    'proxy_address': '127.0.0.1',
    'proxy_port': 8090,  # Must match ZAP port
}

# Nmap must be installed
NMAP_CONFIG = {
    'path': '/usr/bin/nmap',
}

# OpenVAS needs GVM running
OPENVAS_CONFIG = {
    'host': 'openvas.example.com',  # or localhost
    'username': 'admin',
    'password': 'your_password',
}

# Bandit, Semgrep, Checkov auto-detect if in PATH
```

### 3. Configure Jira Integration

```python
JIRA_CONFIG = {
    'server_url': 'https://your-jira.com',
    'username': 'your-jira-user',
    'password': 'your-jira-token',  # Use API token
    'project_key': 'VULN',
    'auto_create_tickets': True,
}
```

Then in Admin Panel:
```
Login → Admin → Jiraticketing → Add Jira Settings
```

### 4. Run Scans

**Web Application**:
```
Visit: /webscanners/zap/
Enter: Target URL
Click: Scan
```

**Network**:
```
Visit: /networkscanners/nmap/
Enter: Target IP/Network
Select: Scan Type
Click: Scan
```

**Code**:
```
Visit: /staticscanners/bandit/
Enter: Code Path
Click: Scan
```

**Results**: Auto-display after scan completes
**Jira**: Click "Create Ticket" to link vulnerability

---

## 📋 Tool Compatibility Matrix

| Tool | Type | Status | Requirements |
|------|------|--------|--------------|
| OWASP ZAP | Web | ✅ Active | Proxy running on port 8090 |
| Nmap | Network | ✅ Active | `apt-get install nmap` |
| OpenVAS | Network | ✅ Active | GVM/Openvas installed locally |
| Nmap-Vulners | Network | ✅ Active | Vulners plugin in ~/.nmap/ |
| Bandit | Code | ✅ Active | `pip install bandit` |
| Semgrep | Code | ✅ Active | `pip install semgrep` |
| Checkov | Code | ✅ Active | `pip install checkov` |
| Nikto | Tools | ✅ Active | `apt-get install nikto` |
| SSL Scanner | Tools | ✅ Active | `apt-get install sslscan` |
| DNS Enum | Tools | ✅ Active | Built-in (dnspython) |
| Jira | Integration | ✅ Active | Jira server URL + credentials |

---

## ⚙️ Configuration Files Reference

### Main Configuration

**File**: `vapt/local_settings.py`

Contains:
- Scanner tool paths and options
- Jira integration settings
- Timeout and concurrency limits
- Email and notification settings
- Security settings for production

### Based On

Reference: `vapt/local_settings.sample.py`

---

## 🔍 Verify Installation

```bash
# Check tools are available
which nmap              # Should output /usr/bin/nmap
which nikto             # Should output /usr/bin/nikto
which bandit            # Should output /usr/bin/bandit
semgrep --version       # Should show version number
checkov --version       # Should show version number

# Check ZAP is running
curl http://127.0.0.1:8090/  # Should connect

# Check OpenVAS (if configured)
openvas --version       # Should show version

# Check Python packages
pip list | grep -i semgrep   # Should be installed
pip list | grep -i checkov   # Should be installed
```

---

## 📝 Next Steps

1. **Copy settings**: `cp vapt/local_settings.sample.py vapt/local_settings.py`
2. **Configure**: Edit `vapt/local_settings.py` for your environment
3. **Start scanners**: Make sure each tool is running/accessible
4. **Setup Jira**: Add Jira server details in settings
5. **Create project**: Admin → Projects → Add Project
6. **Run test scan**: Visit `/webscanners/zap/` and test
7. **Create ticket**: Try creating a Jira ticket from vulnerability

---

## 🆘 Troubleshooting

### "Tool not found" error
```
Solution: Install tool
# E.g., for Nmap:
apt-get install nmap
```

### "Connection refused" on tool
```
Solution: Check tool is running
# E.g., for ZAP:
sudo /opt/zaproxy/zap.sh -server -port 8090 &
```

### "Can't connect to Jira"
```
Solution: Verify settings
1. Check JIRA_CONFIG in local_settings.py
2. Verify URL is correct
3. Check username/password
4. Ensure Jira server is accessible
```

### Scan times out
```
Solution: Increase timeout
# In local_settings.py:
DEFAULT_SCAN_TIMEOUT = 1200  # 20 minutes instead of 10
```

---

## 📚 Reference

- **Jira Integration**: `jiraticketing/` app
- **Settings**: `vapt/local_settings.sample.py`
- **APIs**: `vaptapi/urls.py`
- **Web scanners**: `webscanners/`
- **Network scanners**: `networkscanners/`
- **Code scanners**: `staticscanners/`
- **Tools**: `tools/`

---

**Status**: ✅ Configured for core tools only  
**Last Updated**: March 3, 2026
