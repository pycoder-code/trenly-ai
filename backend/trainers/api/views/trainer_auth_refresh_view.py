"""Новая пара токенов по токену обновления."""

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from trainers.api.authentication import INVALID_CREDENTIALS
from trainers.api.serializers import TrainerAuthRefreshRequestSerializer, TrainerAuthResponseSerializer
from trainers.dto import TrainerAuthRefreshDto
from trainers.services import TrainerAuthRefreshService


class TrainerAuthRefreshView(APIView):
    """Создаёт новую пару по действующему токену обновления."""

    authentication_classes = ()
    permission_classes = ()

    @extend_schema(
        request=TrainerAuthRefreshRequestSerializer,
        responses={201: TrainerAuthResponseSerializer},
    )
    def post(self, request):
        """Новая пара или отказ, если секрет недействителен."""
        serializer = TrainerAuthRefreshRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        params = TrainerAuthRefreshDto(refresh_token=serializer.validated_data['refresh_token'])
        pair = TrainerAuthRefreshService().run(params)
        if pair is None:
            return Response({'detail': INVALID_CREDENTIALS}, status=401)
        return Response(
            {'access_token': pair.access_token, 'refresh_token': pair.refresh_token},
            status=201,
        )
