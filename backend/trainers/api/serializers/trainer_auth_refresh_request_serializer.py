"""Тело обмена токена обновления."""

from rest_framework import serializers


class TrainerAuthRefreshRequestSerializer(serializers.Serializer):
    """Секрет токена обновления."""

    refresh_token = serializers.CharField()
