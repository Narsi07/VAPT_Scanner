# -*- coding: utf-8 -*-
# VAPT Security Platform

from rest_framework import serializers


class Json_to_Yaml_serializer(serializers.Serializer):
    json_object = serializers.JSONField()


class Yaml_to_Json_serializer(serializers.Serializer):
    yaml_object = serializers.CharField()
