"""Выдача пары токенов по телефону и паролю."""

from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from trainers.api.authentication import INVALID_CREDENTIALS
from trainers.api.serializers import TrainerAuthRequestSerializer, TrainerAuthResponseSerializer
from trainers.dto import TrainerAuthDto
from trainers.services import TrainerAuthService


class TrainerAuthView(APIView):
    """Создаёт токен доступа и токен обновления."""

    authentication_classes = ()
    permission_classes = ()

    @extend_schema(request=TrainerAuthRequestSerializer, responses={201: TrainerAuthResponseSerializer})
    def post(self, request):
        """Пара токенов или отказ, если учётные данные не подходят."""
        serializer = TrainerAuthRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        params = TrainerAuthDto(
            phone=serializer.validated_data['phone'],
            password=serializer.validated_data['password'],
        )
        pair = TrainerAuthService().run(params)
        if pair is None:
            return Response({'detail': INVALID_CREDENTIALS}, status=401)
        return Response(
            {'access_token': pair.access_token, 'refresh_token': pair.refresh_token},
            status=201,
        )
