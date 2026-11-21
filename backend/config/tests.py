"""Живость процесса и схема API."""

from django.test import TestCase


class ApiScaffoldTests(TestCase):
    """Служебные пути проекта."""

    def test_health(self):
        """Процесс отвечает, что жив."""
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    def test_schema(self):
        """Схема содержит пути кабинета."""
        response = self.client.get('/api/schema/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('openapi:', body)
        self.assertIn('/api/access-tokens', body)
        self.assertIn('/api/refresh-tokens', body)
        self.assertIn('/api/clients', body)
