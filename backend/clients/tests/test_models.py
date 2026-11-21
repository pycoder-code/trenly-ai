"""Клиент не попадает в админку."""

from django.contrib import admin
from django.test import TestCase

from clients.models import Client


class ClientModelTests(TestCase):
    """Личные данные клиента скрыты от администратора."""

    def test_client_is_not_in_admin(self):
        """Клиент не зарегистрирован в админке."""
        self.assertNotIn(Client, admin.site._registry)
