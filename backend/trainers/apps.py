"""Приложение Django для тренеров."""

from django.apps import AppConfig


class TrainersConfig(AppConfig):
    """Регистрирует домен тренера и схему Bearer."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trainers'
    verbose_name = 'Тренеры'

    def ready(self) -> None:
        """Подключает описание Bearer в OpenAPI."""
        from trainers.api import schema  # noqa: F401
