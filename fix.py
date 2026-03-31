import re

path = 'dashboard/scans_data/scans_query.py'
with open(path, 'r', encoding='utf-8') as f:
    data = f.read()

data = data.replace('from pentest.models import PentestScanDb, PentestScanResultsDb\n', '')
data = re.sub(r'def all_manual_scan.*?return all_manual_scan', 'def all_manual_scan(project_id, query):\n    return 0', data, flags=re.DOTALL)
data = re.sub(r'def all_pentest_web.*?return all_pentest_web', 'def all_pentest_web(project_id, query):\n    return 0', data, flags=re.DOTALL)
data = re.sub(r'def all_pentest_net.*?return all_pentest_net', 'def all_pentest_net(project_id, query):\n    return 0', data, flags=re.DOTALL)

data = re.sub(r'\s+pentest_all_\w+ = PentestScanResultsDb\.objects\.filter\([\s\S]*?\)', '', data)
data = data.replace('            pentest_all_critical,\n', '')
data = data.replace('            pentest_all_high,\n', '')
data = data.replace('            pentest_all_medium,\n', '')
data = data.replace('            pentest_all_low,\n', '')
data = data.replace('            pentest_all_open,\n', '')
data = data.replace('            pentest_all_close,\n', '')
data = data.replace('            pentest_all_false,\n', '')

with open(path, 'w', encoding='utf-8') as f:
    f.write(data)
