"""Связь тренера с клиентами."""

from clients.models import Client
from django.db.models import ProtectedError
from django.test import TestCase

from trainers.tests.test_admin import create_trainer


class TrainerModelTests(TestCase):
    """Тренера с клиентами нельзя удалить."""

    def test_trainer_with_clients_is_protected(self):
        """Удаление тренера с клиентом запрещено."""
        trainer = create_trainer()
        Client.objects.create(trainer=trainer, telegram_user_id=100, first_name='Анна')
        with self.assertRaises(ProtectedError):
            trainer.delete()
