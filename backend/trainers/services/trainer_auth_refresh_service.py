"""Новая пара токенов по токену обновления."""

import secrets

import jwt
from django.conf import settings
from django.db import transaction
from django.utils import timezone

from trainers.dto import TrainerAuthRefreshDto
from trainers.entities import TokenPairEntity
from trainers.repositories import RefreshTokenRepository, hash_refresh_secret


class TrainerAuthRefreshService:
    """Меняет действующий токен обновления на новую пару."""

    def run(self, params: TrainerAuthRefreshDto) -> TokenPairEntity | None:
        """Новая пара или пусто, если секрет недействителен."""
        with transaction.atomic():
            taken = RefreshTokenRepository().take(params.refresh_token)
            if taken is None or taken.expires_at <= timezone.now() or not taken.trainer_is_active:
                return None
            return self._pair(taken.trainer_id)

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
