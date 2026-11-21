"""Вход тренера по телефону и паролю."""

import secrets

import jwt
from django.conf import settings
from django.utils import timezone

from trainers.dto import TrainerAuthDto
from trainers.entities import TokenPairEntity
from trainers.repositories import RefreshTokenRepository, TrainerRepository, hash_refresh_secret


class TrainerAuthService:
    """Выдаёт пару токенов активному тренеру."""

    def run(self, params: TrainerAuthDto) -> TokenPairEntity | None:
        """Пара токенов или пусто, если тренер не найден, заблокирован или пароль не подходит."""
        trainer = TrainerRepository().get_by_phone(params.phone)
        if trainer is None or not trainer.is_active or not trainer.check_password(params.password):
            return None
        return self._pair(trainer.id)

    def _pair(self, trainer_id: int) -> TokenPairEntity:
        """Новый токен доступа и токен обновления."""
        raw_secret = secrets.token_urlsafe(32)
        RefreshTokenRepository().add(
            trainer_id=trainer_id,
            secret_hash=hash_refresh_secret(raw_secret),
            expires_at=timezone.now() + settings.REFRESH_TOKEN_TTL,
        )
        payload = {'sub': str(trainer_id), 'exp': timezone.now() + settings.ACCESS_TOKEN_TTL}
        access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return TokenPairEntity(access_token=access_token, refresh_token=raw_secret)
