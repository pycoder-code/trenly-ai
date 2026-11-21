"""Чтение имени и фото текущего тренера."""

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from trainers.api.authentication import INVALID_CREDENTIALS, TrainerTokenAuthentication
from trainers.api.serializers import TrainerDetailResponseSerializer
from trainers.dto import TrainerDetailDto
from trainers.services import TrainerDetailService


class TrainerDetailView(APIView):
    """Отдаёт имя, фамилию и адрес фото тренера из токена доступа."""

    authentication_classes = (TrainerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=TrainerDetailResponseSerializer)
    def get(self, request):
        """Имя, фамилия и адрес фото или отказ, если тренера уже нет."""
        params = TrainerDetailDto(trainer_id=request.user.pk, origin=request.build_absolute_uri('/'))
        trainer = TrainerDetailService().run(params)
        if trainer is None:
            return Response({'detail': INVALID_CREDENTIALS}, status=401)
        return Response(TrainerDetailResponseSerializer(trainer).data)
