"""Чтение тренера."""

from trainers.entities import TrainerEntity, TrainerStatus
from trainers.models import Trainer


class TrainerRepository:
    """Переводит строку тренера в сущность."""

    def get_by_id(self, trainer_id: int) -> TrainerEntity | None:
        """Тренер по идентификатору или пусто."""
        row = Trainer.objects.filter(pk=trainer_id).first()
        if row is None:
            return None
        return self._to_entity(row)

    def get_by_phone(self, phone: str) -> TrainerEntity | None:
        """Тренер по телефону или пусто."""
        row = Trainer.objects.filter(phone=phone).first()
        if row is None:
            return None
        return self._to_entity(row)

    def _to_entity(self, row: Trainer) -> TrainerEntity:
        """Строка таблицы как сущность тренера."""
        return TrainerEntity(
            id=row.pk,
            phone=row.phone,
            password_hash=row.password,
            first_name=row.first_name,
            last_name=row.last_name,
            photo=row.photo.url if row.photo else '',
            status=TrainerStatus(row.status),
        )
