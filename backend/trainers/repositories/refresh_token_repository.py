"""Хранение хешей токенов обновления."""

import hashlib
from datetime import datetime

from trainers.entities import RefreshTokenEntity, TrainerStatus
from trainers.models import RefreshToken


def hash_refresh_secret(raw_secret: str) -> str:
    """Хеш сырого секрета токена обновления."""
    return hashlib.sha256(raw_secret.encode()).hexdigest()


class RefreshTokenRepository:
    """Сохраняет и забирает токены обновления."""

    def add(self, trainer_id: int, secret_hash: str, expires_at: datetime) -> None:
        """Сохраняет хеш нового токена обновления."""
        RefreshToken.objects.create(
            trainer_id=trainer_id,
            secret_hash=secret_hash,
            expires_at=expires_at,
        )

    def take(self, raw_secret: str) -> RefreshTokenEntity | None:
        """Забирает токен по секрету и тут же гасит его."""
        row = RefreshToken.objects.select_related('trainer').filter(secret_hash=hash_refresh_secret(raw_secret)).first()
        if row is None:
            return None
        taken = self._to_entity(row)
        row.delete()
        return taken

    def _to_entity(self, row: RefreshToken) -> RefreshTokenEntity:
        """Строка таблицы как сущность токена обновления."""
        return RefreshTokenEntity(
            trainer_id=row.trainer_id,
            expires_at=row.expires_at,
            trainer_is_active=row.trainer.status == TrainerStatus.ACTIVE,
        )
