"""Сериализаторы API тренера."""

from trainers.api.serializers.trainer_auth_refresh_request_serializer import (
    TrainerAuthRefreshRequestSerializer,
)
from trainers.api.serializers.trainer_auth_request_serializer import TrainerAuthRequestSerializer
from trainers.api.serializers.trainer_auth_response_serializer import TrainerAuthResponseSerializer
from trainers.api.serializers.trainer_detail_response_serializer import TrainerDetailResponseSerializer

__all__ = [
    'TrainerAuthRefreshRequestSerializer',
    'TrainerAuthRequestSerializer',
    'TrainerAuthResponseSerializer',
    'TrainerDetailResponseSerializer',
]
