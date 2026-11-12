from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import FileSystemStorage, storages

from trainers.models import Trainer


class TrainerPhotoFileStorage(FileSystemStorage):
    """Закрытый каталог на диске. Повторная загрузка заменяет файл по тому же ключу."""

    def __init__(self, **kwargs):
        kwargs.setdefault('location', str(settings.TRAINER_PHOTO_ROOT))
        kwargs['base_url'] = None
        super().__init__(**kwargs)

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name


def trainer_photo_key(trainer_id: int) -> str:
    return f'trainers/{trainer_id}/photo.jpg'


def store_trainer_photo(trainer: Trainer, uploaded: File) -> None:
    storage = storages['trainer_photos']
    key = trainer_photo_key(trainer.pk)
    if storage.exists(key):
        storage.delete(key)
    uploaded.seek(0)
    storage.save(key, uploaded)
    trainer.photo = key
    trainer.save(update_fields=['photo', 'updated_at'])
