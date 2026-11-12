from django.db.models import ProtectedError
from django.test import TestCase

from clients.models import Client
from trainers.models import Trainer


class TrainerModelTests(TestCase):
    def test_trainer_with_clients_is_protected(self):
        trainer = Trainer(phone='+79991234567', first_name='Иван', last_name='Петров')
        trainer.set_password('Cabinet-pass-1')
        trainer.save()
        Client.objects.create(trainer=trainer, telegram_user_id=100, first_name='Анна')
        with self.assertRaises(ProtectedError):
            trainer.delete()
