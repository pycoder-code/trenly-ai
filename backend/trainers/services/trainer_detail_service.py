"""Сценарий имени и фото текущего тренера."""

from trainers.dto import TrainerDetailDto
from trainers.entities import TrainerEntity
from trainers.repositories import TrainerRepository


class TrainerDetailService:
    """Возвращает тренера из токена доступа."""

    def run(self, params: TrainerDetailDto) -> TrainerEntity | None:
        """Тренер с адресом фото или пусто, если строки уже нет."""
        trainer = TrainerRepository().get_by_id(params.trainer_id)
        if trainer is None:
            return None
        trainer.set_photo_url(params.origin)
        return trainer
