import re
import os

list_scans = 'templates/webscanners/scans/list_scans.html'
with open(list_scans, 'r', encoding='utf-8') as f:
    data = f.read()
data = re.sub(r'<a href="{% url ''report_upload:upload'' %}"[^>]+>.*?</a>', '', data, flags=re.DOTALL)
with open(list_scans, 'w', encoding='utf-8') as f:
    f.write(data)

project_html = 'templates/dashboard/project.html'
with open(project_html, 'r', encoding='utf-8') as f:
    data = f.read()
data = re.sub(r'<tbody>{% for data in pentest %}.*?</tbody>', '<tbody></tbody>', data, flags=re.DOTALL)
with open(project_html, 'w', encoding='utf-8') as f:
    f.write(data)

all_high = 'templates/dashboard/all_high_vuln.html'
with open(all_high, 'r', encoding='utf-8') as f:
    data = f.read()
data = re.sub(r'{% for data in pentest_all_high %}.*?{% endfor %}', '', data, flags=re.DOTALL)
with open(all_high, 'w', encoding='utf-8') as f:
    f.write(data)
