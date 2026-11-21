"""Пара токенов кабинета."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TokenPairEntity:
    """Токен доступа и токен обновления."""

    access_token: str
    refresh_token: str
