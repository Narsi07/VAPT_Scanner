@echo off
set DJANGO_DEBUG=1

.\venv\Scripts\python.exe -m waitress --listen=*:8000 --threads=10 --channel-timeout=1800 vapt.wsgi:application