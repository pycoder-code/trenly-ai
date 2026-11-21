"""Таблица клиента."""

from common.models import TimeStampedModel
from django.db import models
from trainers.models import Trainer


class Client(TimeStampedModel):
    """Подопечный тренера."""

    trainer = models.ForeignKey(
        Trainer,
        verbose_name='тренер',
        on_delete=models.PROTECT,
        related_name='clients',
    )
    telegram_user_id = models.BigIntegerField('Telegram ID', unique=True)
    telegram_username = models.CharField('Telegram username', max_length=32, blank=True)
    first_name = models.CharField('имя', max_length=150)
    last_name = models.CharField('фамилия', max_length=150, blank=True)
    phone = models.CharField('телефон', max_length=12, blank=True)
    height = models.PositiveSmallIntegerField('рост', null=True, blank=True)
    weight = models.DecimalField(
        'вес',
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
    )
    active = models.BooleanField('активен', default=True)

    class Meta:
        """Название клиента в админке."""

        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self) -> str:
        """Имя клиента."""
        return self.first_name
