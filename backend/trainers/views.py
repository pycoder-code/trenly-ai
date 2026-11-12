from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from trainers.authentication import (
    INVALID_CREDENTIALS,
    issue_trainer_token,
)
from trainers.models import Trainer
from trainers.phones import normalize_phone

SessionRequest = inline_serializer(
    name='TrainerSessionRequest',
    fields={
        'phone': serializers.CharField(),
        'password': serializers.CharField(),
    },
)
SessionResponse = inline_serializer(
    name='TrainerSessionResponse',
    fields={'token': serializers.CharField()},
)


class TrainerSessionView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(request=SessionRequest, responses={201: SessionResponse})
    def post(self, request):
        phone = request.data.get('phone', '')
        password = request.data.get('password', '')
        try:
            normalized = normalize_phone(phone)
        except ValidationError:
            return Response({'detail': INVALID_CREDENTIALS}, status=401)
        trainer = Trainer.objects.filter(phone=normalized).first()
        if (
            trainer is None
            or trainer.status != Trainer.Status.ACTIVE
            or not trainer.check_password(str(password))
        ):
            return Response({'detail': INVALID_CREDENTIALS}, status=401)
        return Response({'token': issue_trainer_token(trainer.pk)}, status=201)
