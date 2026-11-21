"""Проверка токена доступа тренера."""

import jwt
from django.conf import settings
from jwt import InvalidTokenError
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from trainers.repositories import TrainerRepository

INVALID_CREDENTIALS = 'Неверные учётные данные.'


class TrainerPrincipal:
    """Тренер, вошедший по токену доступа."""

    is_authenticated = True
    is_anonymous = False

    def __init__(self, trainer_id: int) -> None:
        """Запоминает идентификатор тренера."""
        self.pk = trainer_id
        self.id = trainer_id


class TrainerTokenAuthentication(BaseAuthentication):
    """Пускает в кабинет только по действующему токену доступа."""

    def authenticate(self, request):
        """Тренер по заголовку Bearer или пусто, если заголовка нет."""
        header = request.headers.get('Authorization', '')
        if not header:
            return None
        scheme, _, token = header.partition(' ')
        if scheme != 'Bearer' or not token:
            raise AuthenticationFailed(INVALID_CREDENTIALS)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            trainer_id = int(payload['sub'])
        except (InvalidTokenError, KeyError, TypeError, ValueError) as auth_error:
            raise AuthenticationFailed(INVALID_CREDENTIALS) from auth_error
        trainer = TrainerRepository().get_by_id(trainer_id)
        if trainer is None or not trainer.is_active:
            raise AuthenticationFailed(INVALID_CREDENTIALS)
        return TrainerPrincipal(trainer.id), token

    def authenticate_header(self, request):
        """Схема, которую клиент должен прислать после отказа."""
        return 'Bearer'
