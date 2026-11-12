from decimal import Decimal

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.test import TestCase

from clients.models import Client
from trainers.models import Trainer


class ClientModelTests(TestCase):
    def test_client_is_not_in_admin(self):
        self.assertNotIn(Client, admin.site._registry)

    def test_height_and_weight_must_be_positive_when_set(self):
        trainer = Trainer(phone='+79991234567', first_name='Иван', last_name='Петров')
        trainer.set_password('Cabinet-pass-1')
        trainer.save()
        client = Client(trainer=trainer, telegram_user_id=100, first_name='Анна', height=0)
        with self.assertRaises(ValidationError):
            client.save()
        client.height = None
        client.weight = Decimal('0')
        with self.assertRaises(ValidationError):
            client.save()
        client.weight = None
        client.save()
        self.assertIsNone(client.height)
        self.assertIsNone(client.weight)
