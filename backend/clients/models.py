from django.core.exceptions import ValidationError
from django.db import models

from common.models import TimeStampedModel
from trainers.models import Trainer
from trainers.phones import normalize_phone, validate_phone


class Client(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'активен'
        DISCONNECTED = 'disconnected', 'отключён'

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
    phone = models.CharField(
        'телефон',
        max_length=12,
        blank=True,
        validators=[validate_phone],
    )
    height = models.PositiveSmallIntegerField('рост', null=True, blank=True)
    weight = models.DecimalField(
        'вес',
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
    )
    status = models.CharField(
        'статус',
        max_length=16,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self) -> str:
        return self.first_name

    def clean(self):
        super().clean()
        if self.phone:
            self.phone = normalize_phone(self.phone)
        if self.height is not None and self.height <= 0:
            raise ValidationError({'height': 'Рост должен быть больше нуля.'})
        if self.weight is not None and self.weight <= 0:
            raise ValidationError({'weight': 'Вес должен быть больше нуля.'})

    def save(self, *args, **kwargs):
        if self.phone:
            self.phone = normalize_phone(self.phone)
        self.full_clean()
        super().save(*args, **kwargs)
