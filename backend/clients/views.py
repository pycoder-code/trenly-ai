from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from clients.models import Client
from clients.serializers import ClientSerializer
from trainers.authentication import TrainerTokenAuthentication


class ClientListView(APIView):
    authentication_classes = [TrainerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=ClientSerializer(many=True))
    def get(self, request):
        clients = Client.objects.filter(trainer=request.user).order_by('created_at', 'id')
        return Response(ClientSerializer(clients, many=True).data)
