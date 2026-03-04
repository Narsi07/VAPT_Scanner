# VAPT Scanner - Consolidated Scanner Architecture
## Functional & Organized Scanning Sections

### Last Updated: March 3, 2026

---

## Overview

The VAPT Scanner has been reorganized with **consolidated scanning modules** where each scanner tool integrates:
- ✅ Scan launch interface
- ✅ Scan execution (background threading)
- ✅ Real-time result display
- ✅ Result management

**No more duplicate display-only sections!**

---

## Architecture Overview

```
VAPT Scanner Modules
├── webscanners/          (Web Application Security)
│   ├── ZAP Scanner
│   ├── Arachni Scanner (stub)
│   └── Burp Suite (commercial)
├── networkscanners/      (Network Infrastructure)
│   ├── Nmap Scanner
│   ├── OpenVAS Scanner
│   └── Nmap-Vulners (Enhanced)
├── staticscanners/       (Code & Infrastructure Analysis)
│   ├── Bandit (Python)
│   ├── Semgrep (Multi-language)
│   └── Checkov (Infrastructure as Code)
├── tools/                (Additional Security Tools)
│   ├── Nikto (Web Server)
│   ├── SSL Scanner (TLS/SSL)
│   └── DNS Enumeration
└── pentest/              (Manual Penetration Testing)
```

---

## Web Application Scanners

### OWASP ZAP Scanner
**Endpoint**: `/webscanners/zap/`

**Capabilities**:
- Dynamic web application scanning
- Authentication-aware scanning
- API endpoint testing
- JavaScript handling

**Usage**:
```bash
# GET - Display scan list and launch interface
GET /webscanners/zap/

# POST - Launch new scan
POST /webscanners/zap/
Parameters:
  - project_id: UUID of project
  - scan_url: Target URL to scan
  - project_name: Project name
```

**Response**: JSON with scan_id and status
```json
{
    "status": "success",
    "scan_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Scan started successfully"
}
```

**Result Display**: Automatically shown after POST
- Real-time scan progress
- Live vulnerability updates
- Scan status and completion time

---

### Arachni Scanner
**Endpoint**: `/webscanners/arachni/`

**Status**: Deprecated (stub for template compatibility)

**Alternative**: Use OWASP ZAP instead

---

### Burp Suite Scanner
**Endpoint**: `/webscanners/burp/`

**Status**: Requires commercial Burp Suite installation

**Requirements**:
- Burp Suite Professional license
- API token configuration
- Proxy setup

---

## Network Infrastructure Scanners

### Nmap Network Scanner
**Endpoint**: `/networkscanners/nmap/`

**Capabilities**:
- Port scanning (TCP/UDP)
- Service version detection
- OS fingerprinting
- Host discovery

**Usage**:
```bash
# GET - Display Nmap scans
GET /networkscanners/nmap/

# POST - Launch Nmap scan
POST /networkscanners/nmap/
Parameters:
  - target: IP address or hostname
  - scan_type: Nmap flags (default: -sV for version detection)
```

**Scan Types**:
- `-sV`: Service version detection (default)
- `-sU`: UDP scan
- `-A`: Aggressive scan (OS, service, scripts)
- `-O`: OS detection
- `--script vuln`: Vulnerability detection

---

### OpenVAS Vulnerability Scanner
**Endpoint**: `/networkscanners/openvas/`

**Capabilities**:
- Comprehensive vulnerability assessment
- Network-wide scanning
- NVT database updates
- Severity ratings and recommendations

**Usage**:
```bash
# GET - Display OpenVAS scans
GET /networkscanners/openvas/

# POST - Launch OpenVAS scan
POST /networkscanners/openvas/
Parameters:
  - target: IP or network range
  - profile: Scan profile (default: "Full and very deep")
```

**Requirements**:
- OpenVAS service running
- gvm-tools installed
- Proper authentication configured

---

### Nmap-Vulners Scanner
**Endpoint**: `/networkscanners/nmap_vulners/`

**Capabilities**:
- Enhanced vulnerability detection
- Vulners database integration
- CVE mapping
- Exploitability scoring

**Usage**:
```bash
# GET - Display Nmap-Vulners scans
GET /networkscanners/nmap_vulners/

# POST - Launch scan with vulnerability detection
POST /networkscanners/nmap_vulners/
Parameters:
  - target: IP address or hostname
```

---

## Static Code Analysis Scanners

### Bandit - Python Security Scanner
**Endpoint**: `/staticscanners/bandit/`

**Capabilities**:
- Python code security analysis
- Built-in security test suite
- Plugin-based extensibility
- Severity/confidence ratings

**Usage**:
```bash
# GET - Display Bandit scans
GET /staticscanners/bandit/

# POST - Launch Bandit scan
POST /staticscanners/bandit/
Parameters:
  - scan_path: Path to Python codebase
  - project_id: Project UUID
  - project_name: Project name
```

**Detects**:
- Hardcoded credentials
- SQL injection vulnerabilities
- Insecure randomness
- Weak cryptographic functions
- Command injection risks

---

### Semgrep - Pattern-Based Static Analysis
**Endpoint**: `/staticscanners/semgrep/`

**Capabilities**:
- Multi-language support
- Pattern-based scanning
- Rule engine
- Fast incremental scans

**Usage**:
```bash
# GET - Display Semgrep scans
GET /staticscanners/semgrep/

# POST - Launch Semgrep scan
POST /staticscanners/semgrep/
Parameters:
  - scan_path: Path to source code
  - project_id: Project UUID
  - project_name: Project name
```

**Supported Languages**:
- Python, Java, Go, JavaScript/TypeScript
- C#, Ruby, PHP, Rust
- Dockerfile, YAML, JSON

---

### Checkov - Infrastructure as Code Scanner
**Endpoint**: `/staticscanners/checkov/`

**Capabilities**:
- Terraform scanning
- CloudFormation analysis
- Kubernetes manifest validation
- ARM template checking

**Usage**:
```bash
# GET - Display Checkov scans
GET /staticscanners/checkov/

# POST - Launch Checkov scan
POST /staticscanners/checkov/
Parameters:
  - scan_path: Path to IaC files
  - project_id: Project UUID
```

**Supported Formats**:
- Terraform (.tf)
- YAML (.yml, .yaml)
- JSON (.json)
- CloudFormation

---

## Additional Security Tools

### Nikto Web Server Scanner
**Endpoint**: `/tools/nikto/`

**Capabilities**:
- Web server vulnerability scanning
- Plugin-based scanning
- CGI scanning
- HTTPS support

**Usage**:
```bash
# GET - Display Nikto scans
GET /tools/nikto/

# POST - Launch Nikto scan
POST /tools/nikto/
Parameters:
  - host: Target hostname or IP
  - port: Target port (default: 80)
```

**Detects**:
- Server misconfigurations
- Outdated software
- Common vulnerabilities
- Directory traversal issues

---

### SSL/TLS Certificate Scanner
**Endpoint**: `/tools/sslscan/`

**Capabilities**:
- SSL/TLS configuration analysis
- Certificate validation
- Cipher strength testing
- Protocol version checking

**Usage**:
```bash
# GET - Display SSL scans
GET /tools/sslscan/

# POST - Launch SSL scan
POST /tools/sslscan/
Parameters:
  - host: Target hostname
  - port: Target port (default: 443)
```

**Tests**:
- Certificate validity
- Certificate chain validation
- Supported protocols
- Acceptable ciphers
- Known vulnerabilities

---

### DNS Enumeration
**Endpoint**: `/tools/dns_enum/`

**Capabilities**:
- DNS record enumeration
- Subdomain discovery
- Zone transfer testing
- Domain information gathering

**Usage**:
```bash
# GET - Display DNS enumerations
GET /tools/dns_enum/

# POST - Launch DNS enumeration
POST /tools/dns_enum/
Parameters:
  - domain: Target domain
```

---

## Consolidated URL Structure

### Web Scanners
```
/webscanners/             → Scanner list and general interface
/webscanners/zap/         → ZAP scanner (launch + results)
/webscanners/arachni/     → Arachni scanner (deprecated)
/webscanners/burp/        → Burp suite (commercial)
/webscanners/list_scans/  → All scan history
/webscanners/scan_delete/ → Delete scan
```

### Network Scanners
```
/networkscanners/nmap/           → Nmap scanner (launch + results)
/networkscanners/openvas/        → OpenVAS scanner (launch + results)
/networkscanners/nmap_vulners/   → Nmap-Vulners (launch + results)
/networkscanners/list_scans/     → Scan history
/networkscanners/scan_delete/    → Delete scan
```

### Static Analysis
```
/staticscanners/bandit/          → Bandit scanner (launch + results)
/staticscanners/semgrep/         → Semgrep scanner (launch + results)
/staticscanners/checkov/         → Checkov scanner (launch + results)
/staticscanners/list_scans/      → Scan history
/staticscanners/scan_delete/     → Delete scan
```

### Tools
```
/tools/nikto/              → Nikto scanner (launch + results)
/tools/sslscan/            → SSL/TLS scanner (launch + results)
/tools/dns_enum/           → DNS enumeration (launch + results)
```

---

## Common Features (All Scanners)

### Result Display
✅ **Integrated Result Viewing**
- No need to navigate to separate result page
- Results shown immediately after scan completion
- Real-time scan progress
- Detailed vulnerability information

### Result Management
```bash
# View scan history
GET /[scanner_module]/list_scans/

# View vulnerability details
GET /[scanner_module]/list_vuln_info/?scan_id=XXX

# Mark vulnerability status
POST /[scanner_module]/vuln_mark/
Parameters:
  - vuln_id: Vulnerability ID
  - status: Open/Closed/In Review
  - false_positive: Yes/No
  - note: Additional notes

# Delete vulnerability
POST /[scanner_module]/vuln_delete/
Parameters:
  - vuln_id: Vulnerability ID

# Delete entire scan
POST /[scanner_module]/scan_delete/
Parameters:
  - scan_id: Scan ID
```

---

## Background Task Execution

All scanners execute in **background threads** to prevent blocking:

1. **POST request** triggers scan
2. **Response**: Immediate JSON with scan_id
3. **Background execution**: Scan runs in separate thread
4. **Notification**: User notified when complete
5. **Auto-refresh**: Results display updates automatically

---

## Scan Status Workflow

```
Pending → Running → Completed
         ↓
         Error ← Failed
         
Failed states:
- Invalid input
- Path not found
- Tool not installed
- Process timeout
- Permission denied
```

---

## API Response Format

### Successful Scan Launch
```json
{
    "status": "success",
    "scan_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "Scan started successfully"
}
```

### Error Response
```json
{
    "status": "error",
    "message": "Error description"
}
```

---

## Installation & Tool Requirements

### Install All Tools
```bash
# System packages
sudo apt-get install -y \
    nmap \
    nikto \
    zaproxy \
    bandit \
    sslscan

# Python packages
pip install semgrep checkov python-nmap gvm-tools
```

### Verify Installation
```bash
nmap --version
nikto --version
semgrep --version
checkov --version
```

---

## Security Best Practices

1. **Always scan in authorized environments only**
2. **Set appropriate scan timeouts**
3. **Use narrowly scoped targets**
4. **Review results regularly**
5. **Track remediation progress**
6. **Keep tools updated**

---

## Troubleshooting

### Scan Won't Start
- Check tool is installed: `which nmap`
- Verify target is accessible
- Check disk space
- Review logs: `python manage.py logs`

### Results Not Showing
- Verify scan has completed: Check scan status
- Check for errors in notifications
- Verify user has permission to view project
- Clear browser cache

### Tool Not Found
```bash
# Install missing tool
sudo apt-get install [tool-name]
pip install [package-name]

# Verify installation
which [tool-name]
```

---

## Performance Tips

1. **Split large scopes**: Scan smaller ranges for faster results
2. **Use appropriate profiles**: Don't use aggressive scans for large networks
3. **Schedule off-peak**: Run heavy scans during low-traffic times
4. **Clean up old scans**: Delete completed scans to free resources
5. **Monitor resources**: Check CPU/memory during scans

---

## Version Information

- **Django**: 4.2.9
- **Python**: 3.10+
- **Kali Linux**: 2023.4+

**Scanner Versions**:
- Nmap: 7.90+
- OWASP ZAP: 2.11+
- Bandit: 1.7+
- Semgrep: 1.45+
- Checkov: 2.11+
- Nikto: 2.1.5+

---

## References

- **OWASP ZAP**: https://www.zaproxy.org/
- **Nmap**: https://nmap.org/
- **Bandit**: https://bandit.readthedocs.io/
- **Semgrep**: https://semgrep.dev/
- **Checkov**: https://www.checkov.io/
- **Nikto**: https://cirt.net/Nikto2

---

**Status**: ✅ Fully Functional & Ready for Production
