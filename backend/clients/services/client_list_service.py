"""Сценарий списка клиентов."""

from clients.dto import ClientListDto
from clients.entities import ClientEntity
from clients.repositories import ClientRepository


class ClientListService:
    """Возвращает клиентов одного тренера."""

    def run(self, params: ClientListDto) -> list[ClientEntity]:
        """Клиенты, подключённые к тренеру."""
        return ClientRepository().list_for_trainer(params.trainer_id)
