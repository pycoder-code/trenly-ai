"""Команда чтения текущего тренера."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TrainerDetailDto:
    """Чьё имя прочитать и с какого хоста открыть фото."""

    trainer_id: int
    origin: str
