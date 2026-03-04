# 🎟️ Jira Ticketing Integration Guide

**VAPT Scanner Jira Integration** for vulnerability management and tracking

---

## Overview

The VAPT Scanner includes built-in Jira integration that allows you to:

✅ **Link vulnerabilities to Jira tickets**  
✅ **Auto-create tickets for critical findings**  
✅ **Track remediation status**  
✅ **Sync findings with project management**  
✅ **Maintain audit trail**

---

## Setup Instructions

### Step 1: Get Jira Credentials

You need:
1. **Jira Server URL**: `https://your-jira.domain.com`
2. **Username**: Your Jira user
3. **API Token** (recommended): 
   - Go to: https://id.atlassian.com/manage-profile/security/api-tokens
   - Create new token
   - Copy the token value

### Step 2: Configure in VAPT Scanner

#### Option A: Via Environment File

Create `.env` file in project root:

```env
JIRA_SERVER_URL=https://your-jira.domain.com
JIRA_USERNAME=your-jira-user
JIRA_API_TOKEN=your-api-token-here
JIRA_PROJECT_KEY=VULN
JIRA_ISSUE_TYPE=Bug
JIRA_AUTO_CREATE=False
```

Then load in Django settings:

```python
# In vapt/local_settings.py
import os
from dotenv import load_dotenv

load_dotenv()

JIRA_CONFIG = {
    'enabled': True,
    'server_url': os.getenv('JIRA_SERVER_URL'),
    'username': os.getenv('JIRA_USERNAME'),
    'password': os.getenv('JIRA_API_TOKEN'),  # Use token as password
    'project_key': os.getenv('JIRA_PROJECT_KEY', 'VULN'),
    'issue_type': os.getenv('JIRA_ISSUE_TYPE', 'Bug'),
    'auto_create_tickets': os.getenv('JIRA_AUTO_CREATE', 'False').lower() == 'true',
    'verify_ssl': True,
}
```

#### Option B: Via Django Settings

Edit `vapt/local_settings.py`:

```python
JIRA_CONFIG = {
    'enabled': True,
    'server_url': 'https://your-jira.domain.com',
    'username': 'your-jira-user',
    'password': 'your-api-token',  # Use API token instead of password
    'project_key': 'VULN',  # Your Jira project key
    'issue_type': 'Bug',  # Or 'Task', 'Security', etc.
    'auto_create_tickets': False,  # Set to True to auto-create
    'verify_ssl': True,
}

# Auto-create severity threshold
JIRA_AUTO_TICKET_SEVERITY = 'HIGH'  # 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'
```

#### Option C: Via Django Admin

1. Log in to Django admin: `/admin/`
2. Navigate to: **Jiraticketing → Jira Settings**
3. Click: **Add Jira Setting**
4. Fill in form:
   - **Jira Server**: `https://your-jira.domain.com`
   - **Jira Username**: Your username
   - **Jira Password**: Your API token (encrypted)
   - **Jira Project**: VULN
   - **Organization**: Select your org
5. Click: **Save**

---

## Usage

### Method 1: Manual Ticket Creation

After scan completes with vulnerabilities:

1. Go to: **Vulnerability Details** page
2. Look for button: **Create Jira Ticket** (if enabled)
3. Click button
4. Confirm details:
   - Title: Vulnerability title (auto-populated)
   - Description: Vulnerability details (auto-populated)
   - Priority: Select based on severity (auto-mapped)
5. Click: **Create**
6. Confirmation shows: Ticket URL and ID

**Browser redirects** to newly created Jira ticket

### Method 2: Bulk Ticket Creation

For multiple vulnerabilities:

1. Go to: **Scan Results** page
2. Select vulnerabilities (checkboxes)
3. Click: **Create Tickets** (bulk action)
4. Choose:
   - Filter by severity
   - Link to existing ticket or create new
   - Auto-assign to team
5. Click: **Create Selected**
6. System creates batch of tickets

### Method 3: Automatic Ticket Creation

If configured with `auto_create_tickets: True`:

1. Scan completes
2. System automatically creates tickets for:
   - Severity = CRITICAL
   - Severity = HIGH (if threshold set to HIGH)
3. Tickets linked automatically
4. User gets notification

---

## Vulnerability to Jira Mapping

### Severity Mapping

```
VAPT Severity  →  Jira Priority
═════════════════════════════════
CRITICAL       →  Blocker
HIGH           →  Highest / High
MEDIUM         →  Medium
LOW            →  Low
INFO           →  Lowest
```

### Field Mapping

```
Jira Field             VAPT Data
═════════════════════════════════════════
Summary/Title          Vulnerability Title
Description            Vuln Details + Recommendations
Priority               Based on Severity
Issue Type             Configured (Bug, Task, etc.)
Project                Jira Project Key
Labels                 Scanner Name + Severity
Environment            Target/URL
Components             Tested Component
Assignee               Analyst (optional)
```

### Example Ticket Created

```
Title: SQL Injection in Login Form

Description:
VULNERABILITY: SQL Injection
SEVERITY: HIGH
CVSS Score: 7.5

DESCRIPTION:
SQL injection vulnerability found in login form parameter 'username'

TARGET: https://example.com/login
SCANNER: OWASP ZAP
SCAN DATE: 2026-03-03

RECOMMENDATION:
- Use parameterized queries
- Input validation
- WAF rules

LINK TO SCAN: /webscanners/zap/scan_id/details/
```

---

## API Integration

### Create Ticket Programmatically

```bash
curl -X POST http://localhost:8000/archerysec/api/v1/update-jira/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vulnerability_id": "vuln-123",
    "severity": "HIGH",
    "title": "SQL Injection",
    "description": "SQL injection in login form",
    "target": "https://example.com/login",
    "create_new": true
  }'
```

**Response**:
```json
{
  "status": "success",
  "ticket_id": "VULN-456",
  "ticket_url": "https://your-jira.com/browse/VULN-456",
  "message": "Ticket created successfully"
}
```

---

## Settings & Configuration

### Environment Variables

```bash
# Jira Server
JIRA_SERVER_URL=https://jira.company.com

# Authentication
JIRA_USERNAME=vapt-bot@company.com
JIRA_API_TOKEN=your-api-token-here

# Project Settings  
JIRA_PROJECT_KEY=VULN
JIRA_ISSUE_TYPE=Bug

# Automation
JIRA_AUTO_CREATE=False
JIRA_AUTO_TICKET_SEVERITY=HIGH

# SSL
JIRA_VERIFY_SSL=True
```

### Django Settings

File: `vapt/local_settings.py`

```python
JIRA_CONFIG = {
    'enabled': True,
    'server_url': 'YOUR_JIRA_URL',
    'username': 'YOUR_USERNAME',
    'password': 'YOUR_API_TOKEN',
    'project_key': 'YOUR_PROJECT_KEY',
    'issue_type': 'Bug',
    'auto_create_tickets': False,
    'verify_ssl': True,
}

JIRA_AUTO_TICKET_SEVERITY = 'HIGH'
```

---

## Troubleshooting

### "Connection refused" to Jira

**Problem**: Can't connect to Jira server

**Solutions**:
1. Check Jira URL is correct: `https://jira.company.com`
2. Verify SSH/network access to Jira
3. Check firewall rules
4. Verify Jira is running: `curl -I https://your-jira-url`

### "Invalid credentials"

**Problem**: Authentication fails

**Solutions**:
1. Use API token (not password if 2FA enabled)
2. Verify username is correct
3. Check token hasn't expired
4. Regenerate token if needed

### "Project not found"

**Problem**: Project key doesn't exist

**Solutions**:
1. Check project key is correct (case-sensitive)
2. Verify user has access to project
3. List user's projects: Jira UI → Your Work

### "Issue type not valid"

**Problem**: Configured issue type doesn't exist

**Solutions**:
1. Use valid issue type: Bug, Task, Story, etc.
2. Check project supports selected type
3. Create custom issue type if needed

### "Can't create ticket" but connection works

**Problem**: Authentication succeeds but creation fails

**Solutions**:
1. Check user has "Create Issue" permission
2. Verify project has issue type selected
3. Check required fields are populated
4. Look at VAPT logs for details

---

## Logging

View Jira operations in logs:

```bash
# View last 50 lines
tail -n 50 logs/vapt.log

# Watch live logs
tail -f logs/vapt.log

# Search for Jira errors
grep -i jira logs/vapt.log | grep -i error
```

**Log entries**:
```
[INFO] Jira ticket created: VULN-456
[INFO] Linked vulnerability to ticket: VULN-456
[ERROR] Jira connection failed: Connection timeout
[WARNING] Jira field mapping incomplete for severity
```

---

## Best Practices

### 1. Use API Tokens
- ✅ Create API token in Jira settings
- ✅ Use token instead of password
- ✅ Regenerate periodically
- ❌ Don't hardcode in code

### 2. Separate Project Key
- ✅ Create dedicated "VULN" project
- ✅ Use for all scan findings only
- ✅ Archive closed tickets quarterly
- ❌ Mix with normal project tickets

### 3. Automated Workflow
- ✅ Set JIRA_AUTO_CREATE = True for critical findings
- ✅ Configure ticket workflow in Jira
- ✅ Auto-assign to security team
- ✅ Set auto-resolver workflow

### 4. Monitoring
- ✅ Review tickets weekly
- ✅ Track remediation progress
- ✅ Close resolved tickets
- ✅ Generate reports from Jira

### 5. Security
- ✅ Store credentials in .env file
- ✅ Add .env to .gitignore
- ✅ Use HTTPS for Jira connection
- ✅ Audit Jira access logs

---

## Integration Workflow

```
SCAN COMPLETE
     ↓
HIGH SEVERITY FOUND?
     ├─ YES → Create Ticket
     │        ├─ Post to Jira
     │        ├─ Store ticket ID
     │        ├─ Send notification
     │        └─ Link to vuln record
     └─ NO → Skip ticket creation

USER VIEWS VULNERABILITY
     ↓
SEES "CREATE TICKET" BUTTON
     ├─ Manually creates ticket
     │  OR
     └─ Views existing ticket (if already created)

TEAM MANAGES TICKET IN JIRA
     ├─ Assign to developer
     ├─ Track progress
     ├─ Close when fixed
     └─ VAPT shows status
```

---

## Example Scenarios

### Scenario 1: Auto-Create High Severity

```python
# Settings
JIRA_AUTO_CREATE = True
JIRA_AUTO_TICKET_SEVERITY = 'HIGH'

# When scan finds HIGH severity vuln:
→ Ticket automatically created in Jira
→ VAPT stores ticket ID
→ User sees ticket in VAPT UI
→ Can track in Jira
```

### Scenario 2: Manual Creation for Critical

```python
# Settings
JIRA_AUTO_CREATE = False

# When scan finds CRITICAL vuln:
→ User views vulnerability details
→ Clicks "Create Jira Ticket"
→ Ticket created in Jira
→ Returns to VAPT with ticket ID
→ All auto-linked
```

### Scenario 3: Bulk Link Existing

```
Scenario: 50 old vulnerabilities need Jira links

Steps:
1. Go to Scan Results
2. Filter by Severity = HIGH
3. Select all (50 items)
4. Click "Link to Jira" (bulk action)
5. Choose: Link to existing or create new
6. All linked in bulk
```

---

## Advanced Configuration

### Custom Field Mapping

```python
# In vapt/local_settings.py
JIRA_FIELD_MAPPING = {
    'summary': 'vulnerability_title',
    'description': 'vulnerability_details',
    'priority': 'severity_to_jira_priority',
    'components': ['component_name'],
    'labels': ['scanner', 'severity'],
    'environment': 'target_url',
    'customfield_10000': 'cvss_score',
}
```

### Custom Issue Type

```python
JIRA_CONFIG = {
    ...
    'issue_type': 'Security Issue',  # Custom type
    ...
}
```

### Auto-Assignment

```python
JIRA_AUTO_ASSIGN = {
    'CRITICAL': 'security-lead@company.com',
    'HIGH': 'security-team@company.com',
    'MEDIUM': 'devops-team@company.com',
}
```

---

## Support

### Jira Documentation
- https://developer.atlassian.com/cloud/jira/rest/v2/

### VAPT Ticketing Module
- File: `jiraticketing/views.py`
- File: `jiraticketing/models.py`
- API: `vaptapi/urls.py`

### Troubleshooting
- Check: `logs/vapt.log` for errors
- Check: Jira audit log for failed attempts
- Verify: Network connectivity to Jira

---

**Last Updated**: March 3, 2026  
**Status**: ✅ Fully Integrated
