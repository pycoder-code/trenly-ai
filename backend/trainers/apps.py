from django.apps import AppConfig


class TrainersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trainers'
    verbose_name = 'Тренеры'

    def ready(self) -> None:
        from trainers import schema  # noqa: F401
