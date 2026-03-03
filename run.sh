#!/bin/bash
#export TIME_ZONE='Asia/Kolkata'
# Prod Server
export DJANGO_DEBUG=1
gunicorn -b 0.0.0.0:8000 vapt.wsgi:application --workers=1 --threads=10 --timeout=1800

