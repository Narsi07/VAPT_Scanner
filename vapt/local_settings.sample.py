# -*- coding: utf-8 -*-
# VAPT Security Platform

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

INTERNAL_IPS = ["172.26.0.1", "127.0.0.1"]

ADMINS = [("admin", "admin@example.com")]
