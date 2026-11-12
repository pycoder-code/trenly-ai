from django.contrib.auth.hashers import check_password, make_password
from django.db import models

from common.models import TimeStampedModel
from trainers.phones import normalize_phone, validate_phone


class Trainer(TimeStampedModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'активен'
        BLOCKED = 'blocked', 'заблокирован'

    phone = models.CharField(
        'телефон',
        max_length=12,
        unique=True,
        validators=[validate_phone],
    )
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

    is_authenticated = True
    is_anonymous = False

    class Meta:
        verbose_name = 'тренер'
        verbose_name_plural = 'тренеры'

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def set_password(self, raw_password: str) -> None:
        self.password = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        self.phone = normalize_phone(self.phone)
        super().save(*args, **kwargs)
