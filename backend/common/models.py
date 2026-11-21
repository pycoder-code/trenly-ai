"""Общие поля таблиц."""

from django.db import models


class TimeStampedModel(models.Model):
    """Момент создания и последнего изменения записи."""

    created_at = models.DateTimeField('создан', auto_now_add=True)
    updated_at = models.DateTimeField('обновлён', auto_now=True)

    class Meta:
        """Модель не создаёт свою таблицу."""

        abstract = True
