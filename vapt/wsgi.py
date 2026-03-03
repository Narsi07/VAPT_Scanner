# -*- coding: utf-8 -*-
# VAPT Security Platform

"""
WSGI config for vapt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import warnings

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

from vapt.settings import base

warnings.filterwarnings("ignore", category=UserWarning, module="cffi")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vapt.settings.base")

static = os.path.join(base.BASE_DIR, "static")
application = WhiteNoise(
    get_wsgi_application(), root="templates/static", prefix="static/"
)
