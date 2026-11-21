"""Чтение клиентов из базы."""

from clients.entities import ClientEntity
from clients.models import Client


class ClientRepository:
    """Переводит строки клиентов в сущности."""

    def list_for_trainer(self, trainer_id: int) -> list[ClientEntity]:
        """Клиенты тренера, от старых к новым."""
        rows = Client.objects.filter(trainer_id=trainer_id).order_by('created_at', 'id')
        return [self._to_entity(row) for row in rows]

    def _to_entity(self, row: Client) -> ClientEntity:
        """Строка таблицы как сущность клиента."""
        return ClientEntity(
            id=row.pk,
            trainer_id=row.trainer_id,
            telegram_user_id=row.telegram_user_id,
            telegram_username=row.telegram_username,
            first_name=row.first_name,
            last_name=row.last_name,
            phone=row.phone,
            height=row.height,
            weight=row.weight,
            active=row.active,
        )
