"""Сущность тренера и его состояние."""

from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import urljoin

from django.contrib.auth.hashers import check_password


class TrainerStatus(StrEnum):
    """Тренер активен или заблокирован."""

    ACTIVE = 'active'
    BLOCKED = 'blocked'


@dataclass
class TrainerEntity:
    """Учётная запись тренера кабинета."""

    id: int
    phone: str
    password_hash: str
    first_name: str
    last_name: str
    photo: str
    status: TrainerStatus
    photo_url: str | None = None

    def set_photo_url(self, origin: str) -> None:
        """Полный адрес фото. Локальный путь дополняется хостом."""
        if not self.photo:
            self.photo_url = None
            return
        if self.photo.startswith(('http://', 'https://')):
            self.photo_url = self.photo
            return
        self.photo_url = urljoin(origin, self.photo)

    def check_password(self, raw_password: str) -> bool:
        """Совпадает ли пароль с сохранённым хешем."""
        return check_password(raw_password, self.password_hash)

    @property
    def is_active(self) -> bool:
        """Тренер не заблокирован."""
        return self.status is TrainerStatus.ACTIVE
