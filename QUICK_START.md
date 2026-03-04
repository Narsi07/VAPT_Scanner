# VAPT Scanner - Quick Start Guide
## Using Consolidated Scanner Sections

---

## What Changed?

**OLD Structure**:
```
Scan Launch Page → Run Scan → View Results Page → Manage Results
[separate endpoints for each]
```

**NEW Structure**:
```
Scanner Page → Run Scan + View Results + Manage Results
[all-in-one consolidated endpoint]
```

---

## Using Each Scanner

### 1. OWASP ZAP Scanner (Web Apps)

**Access**: `http://localhost:8000/webscanners/zap/`

**Steps**:
1. Select project from dropdown
2. Enter target URL (e.g., `https://target.com`)
3. Click "Start Scan"
4. View live progress
5. Review results as they appear
6. Mark/edit vulnerabilities as needed

**Time**: 5-30 minutes depending on site size

---

### 2. Nmap Network Scanner

**Access**: `http://localhost:8000/networkscanners/nmap/`

**Steps**:
1. Enter target IP or hostname
2. Select scan type:
   - `-sV` (Service version detection) 
   - `-A` (Aggressive/OS detection)
   - `-sU` (UDP scan)
3. Click "Start Scan"
4. View open ports and services
5. Review service versions for vulnerabilities

**Time**: 1-15 minutes

---

### 3. Bandit (Python Code Scanner)

**Access**: `http://localhost:8000/staticscanners/bandit/`

**Steps**:
1. Select project
2. Enter path to Python code:
   ```
   /path/to/project
   /path/to/file.py
   ```
3. Click "Scan"
4. View security issues found
5. Verify each issue (mark as false positive if needed)

**Time**: 30 seconds - 2 minutes

---

### 4. Semgrep (Multi-Language Code Scanner)

**Access**: `http://localhost:8000/staticscanners/semgrep/`

**Steps**:
1. Select project
2. Enter code path
3. Click "Scan"
4. View pattern-based issues
5. Review code locations and fixes

**Supports**: Python, Java, JavaScript, Go, Ruby, PHP, etc.

**Time**: 1-5 minutes

---

### 5. Checkov (Infrastructure as Code)

**Access**: `http://localhost:8000/staticscanners/checkov/`

**Steps**:
1. Enter path to Terraform/CloudFormation files
2. Click "Scan"
3. Review compliance violations
4. Check misconfigurations

**Time**: 30 seconds - 2 minutes

---

### 6. OpenVAS (Network Vulnerability Scanner)

**Access**: `http://localhost:8000/networkscanners/openvas/`

**Steps**:
1. Enter target IP/network
2. Select scan profile
3. Click "Scan"
4. Wait for comprehensive assessment
5. Review severity ratings

**Time**: 30 minutes - 2 hours (thorough scan)

---

### 7. Nikto (Web Server Scanner)

**Access**: `http://localhost:8000/tools/nikto/`

**Steps**:
1. Enter target host
2. Enter port (default 80)
3. Click "Scan"
4. View server vulnerabilities

**Time**: 2-10 minutes

---

### 8. SSL/TLS Scanner

**Access**: `http://localhost:8000/tools/sslscan/`

**Steps**:
1. Enter target hostname
2. Leave port as 443 (default)
3. Click "Scan"
4. Review certificate and protocol info
5. Check for weak ciphers

**Time**: 1-3 minutes

---

### 9. DNS Enumeration

**Access**: `http://localhost:8000/tools/dns_enum/`

**Steps**:
1. Enter domain name
2. Click "Enumerate"
3. Review DNS records
4. Check for subdomain info

**Time**: 30 seconds - 2 minutes

---

## Common Actions

### View Scan Results
```
Click on scan in list → Auto-displays results
Results shown in real-time as scan progresses
```

### Mark Vulnerability Status
```
On result page:
1. Click vulnerability
2. Select status: Open / In Review / Closed
3. Mark as false positive if needed
4. Add notes
5. Save
```

### Delete Scan
```
In scan list:
1. Find scan
2. Click delete icon
3. Confirm deletion
```

### Export Results
```
After scan completes:
1. Click "Export"
2. Choose format: PDF / JSON / CSV
3. Download file
```

---

## Command Line (Optional)

If preferred, you can use tools directly:

### Nmap
```bash
nmap -sV target.com
nmap -A -p- 192.168.1.0/24
```

### Bandit
```bash
bandit -r /path/to/code -f json
```

### Semgrep
```bash
semgrep --config auto /path/to/code --json
```

### Checkov
```bash
checkov -d /path/to/iac --framework terraform
```

### Nikto
```bash
nikto -h target.com -p 80
```

### SSL Scan
```bash
sslscan target.com:443
```

---

## Tips & Tricks

### 1. Choose Right Scanner for Task
| Task | Scanner |
|------|---------|
| Web app vulnerabilities | ZAP |  
| Port scanning | Nmap |
| Python code security | Bandit |
| Multi-language patterns | Semgrep |
| Infrastructure as code | Checkov |
| Network assessment | OpenVAS |
| Server misconfig | Nikto |
| SSL/TLS issues | SSL Scanner |
| Domain info | DNS Enum |

### 2. Combine Scanners
```
1. Network Nmap scan → Find web servers
2. ZAP scan → Test each web app
3. SSL scan → Check certificates
4. Nikto → Server hardening
```

### 3. Manage Results Efficiently
- Review high severity first
- Group by vulnerability type
- Track remediation progress
- Schedule regular re-scans

### 4. Performance
- Scan during off-hours
- Use narrowed scope
- Adjust timeout for large environments
- Retry failed scans

---

## Troubleshooting

### Scan Not Starting?
```
Check:
1. Tool installed? → which [tool]
2. Valid target? → ping target
3. Permissions? → sudo check
4. Network? → Check connectivity
```

### Results Not Showing?
```
Check:
1. Scan completed? → Check status
2. Browser cache? → Ctrl+F5 refresh
3. User permission? → Check project access
4. Database? → Check Django logs
```

### Tool Errors?
```
Solution:
1. Update tool: apt-get update [tool]
2. Reinstall: pip install --upgrade [tool]
3. Check config: Review tool settings
4. See logs: python manage.py logs
```

---

## Quick Reference

| Tool | Endpoint | Time | Type |
|------|----------|------|------|
| ZAP | /webscanners/zap/ | 5-30m | Web |
| Nmap | /networkscanners/nmap/ | 1-15m | Network |
| OpenVAS | /networkscanners/openvas/ | 30m-2h | Network |
| Bandit | /staticscanners/bandit/ | 30s-2m | Python |
| Semgrep | /staticscanners/semgrep/ | 1-5m | Multi-lang |
| Checkov | /staticscanners/checkov/ | 30s-2m | IaC |
| Nikto | /tools/nikto/ | 2-10m | Server |
| SSL | /tools/sslscan/ | 1-3m | SSL/TLS |
| DNS | /tools/dns_enum/ | 30s-2m | DNS |

---

## Next Steps

1. **Start with Nmap**: Quick network assessment
2. **Follow with targeted scanner**: Based on findings
3. **Review results**: Understand vulnerabilities
4. **Plan remediation**: Fix issues in priority order
5. **Re-scan**: Verify fixes

---

**Ready to scan? Start at**: `http://localhost:8000/webscanners/`

Good luck! 🔒
