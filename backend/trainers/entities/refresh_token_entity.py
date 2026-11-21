"""Принятый токен обновления."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class RefreshTokenEntity:
    """Токен обновления, который сервер только что забрал."""

    trainer_id: int
    expires_at: datetime
    trainer_is_active: bool
