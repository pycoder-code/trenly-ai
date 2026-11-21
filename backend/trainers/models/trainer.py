"""Таблица тренера."""

from common.models import TimeStampedModel
from django.db import models


class Trainer(TimeStampedModel):
    """Учётная запись тренера кабинета."""

    class Status(models.TextChoices):
        """Активен или заблокирован."""

        ACTIVE = 'active', 'активен'
        BLOCKED = 'blocked', 'заблокирован'

    phone = models.CharField('телефон', max_length=12, unique=True)
    password = models.CharField('пароль', max_length=128)
    first_name = models.CharField('имя', max_length=150)
    last_name = models.CharField('фамилия', max_length=150)
    photo = models.CharField('фото', max_length=255, blank=True)
    status = models.CharField(
        'статус',
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        """Название тренера в админке."""

        verbose_name = 'тренер'
        verbose_name_plural = 'тренеры'

    def __str__(self) -> str:
        """Имя и фамилия тренера."""
        return f'{self.first_name} {self.last_name}'
