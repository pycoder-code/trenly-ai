"""Команда входа тренера."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TrainerAuthDto:
    """Телефон и пароль для входа."""

    phone: str
    password: str
