"""Список клиентов кабинета."""

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from trainers.api.authentication import TrainerTokenAuthentication

from clients.api.serializers import ClientListResponseSerializer
from clients.dto import ClientListDto
from clients.services import ClientListService


class ClientListView(APIView):
    """Отдаёт клиентов вошедшего тренера."""

    authentication_classes = (TrainerTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=ClientListResponseSerializer(many=True))
    def get(self, request):
        """Клиенты, подключённые к тренеру из токена доступа."""
        params = ClientListDto(trainer_id=request.user.pk)
        clients = ClientListService().run(params)
        return Response(ClientListResponseSerializer(clients, many=True).data)
