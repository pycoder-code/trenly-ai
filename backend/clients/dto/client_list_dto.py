"""Команда списка клиентов."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ClientListDto:
    """Чей список клиентов запросить."""

    trainer_id: int
