"""Схема Bearer в OpenAPI."""

from drf_spectacular.extensions import OpenApiAuthenticationExtension

from trainers.api.authentication import TrainerTokenAuthentication


class TrainerTokenScheme(OpenApiAuthenticationExtension):
    """Показывает в схеме, что кабинет ждёт заголовок Authorization: Bearer."""

    target_class = TrainerTokenAuthentication
    name = 'Bearer'

    def get_security_definition(self, auto_schema):
        """Описание схемы Bearer для OpenAPI."""
        return {'type': 'http', 'scheme': 'bearer'}
