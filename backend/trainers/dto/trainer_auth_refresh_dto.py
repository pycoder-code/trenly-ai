"""Команда новой пары токенов."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TrainerAuthRefreshDto:
    """Секрет токена обновления."""

    refresh_token: str
