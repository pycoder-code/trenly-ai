"""Ответ с парой токенов."""

from rest_framework import serializers


class TrainerAuthResponseSerializer(serializers.Serializer):
    """Токен доступа и токен обновления."""

    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
