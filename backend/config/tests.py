from django.test import TestCase


class ApiScaffoldTests(TestCase):
    def test_health(self):
        response = self.client.get('/api/health/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    def test_schema(self):
        response = self.client.get('/api/schema/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('openapi:', body)
        self.assertIn('paths: {}', body)
