"""Приложение Django для клиентов."""

from django.apps import AppConfig


class ClientsConfig(AppConfig):
    """Регистрирует домен клиента."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clients'
    verbose_name = 'Клиенты'
