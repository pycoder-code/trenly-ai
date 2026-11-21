"""Сущность клиента."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ClientEntity:
    """Подопечный одного тренера."""

    id: int
    trainer_id: int
    telegram_user_id: int
    telegram_username: str
    first_name: str
    last_name: str
    phone: str
    height: int | None
    weight: Decimal | None
    active: bool
