"""Ответ с именем и фото текущего тренера."""

from rest_framework import serializers


class TrainerDetailResponseSerializer(serializers.Serializer):
    """Имя, фамилия и адрес фото тренера."""

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    photo = serializers.CharField(source='photo_url', allow_null=True)
