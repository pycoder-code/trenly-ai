"""Таблица токена обновления."""

from common.models import TimeStampedModel
from django.db import models

from trainers.models.trainer import Trainer


class RefreshToken(TimeStampedModel):
    """Хеш секрета, которым тренер получает новую пару токенов."""

    trainer = models.ForeignKey(
        Trainer,
        verbose_name='тренер',
        on_delete=models.CASCADE,
        related_name='refresh_tokens',
    )
    secret_hash = models.CharField('хеш секрета', max_length=64, unique=True)
    expires_at = models.DateTimeField('истекает')

    class Meta:
        """Название токена обновления в админке."""

        verbose_name = 'токен обновления'
        verbose_name_plural = 'токены обновления'

    def __str__(self) -> str:
        """Идентификатор тренера, которому выдан токен."""
        return f'{self.trainer_id}'
