# -*- coding: utf-8 -*-
# VAPT Security Platform

import hashlib
import uuid

from webscanners.models import WebScanResultsDb, WebScansDb


def check_false_positive(title, severity, scan_url):
    dup_data = title + severity + scan_url
    duplicate_hash = hashlib.sha256(dup_data.encode("utf-8")).hexdigest()
    return duplicate_hash
