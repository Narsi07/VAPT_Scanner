# -*- coding: utf-8 -*-
# VAPT Security Platform

from rest_framework import serializers


class ZapScansSerializer(serializers.Serializer):
    url = serializers.URLField(read_only=True)
    project_id = serializers.UUIDField(required=True, help_text=("Provide ScanId"))


class ZapSettingsSerializer(serializers.Serializer):
    zap_api_key = serializers.CharField()
    zap_host = serializers.CharField()
    zap_port = serializers.IntegerField()
    zap_enabled = serializers.BooleanField()
