from django.test import TestCase

from trainers.models import Trainer
from trainers.tests.test_admin import PASSWORD, create_trainer

UNAUTHORIZED = {'detail': 'Неверные учётные данные.'}


class TrainerSessionTests(TestCase):
    def test_active_trainer_logs_in(self):
        create_trainer()
        response = self.client.post(
            '/api/trainer-sessions',
            {'phone': '+79991234567', 'password': PASSWORD},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.json())

    def test_wrong_password(self):
        create_trainer()
        response = self._login(password='wrong-password-1')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), UNAUTHORIZED)

    def test_unknown_phone_matches_wrong_password(self):
        create_trainer()
        wrong = self._login(password='wrong-password-1')
        unknown = self._login(phone='+79990000000')
        self.assertEqual(unknown.status_code, 401)
        self.assertEqual(unknown.json(), wrong.json())

    def test_leading_eight(self):
        create_trainer()
        response = self._login(phone='8 999 123-45-67')
        self.assertEqual(response.status_code, 201)

    def test_blocked_trainer_and_revoked_token(self):
        trainer = create_trainer()
        token = self._login().json()['token']
        trainer.status = Trainer.Status.BLOCKED
        trainer.save(update_fields=['status', 'updated_at'])
        blocked_login = self._login()
        self.assertEqual(blocked_login.status_code, 401)
        self.assertEqual(blocked_login.json(), UNAUTHORIZED)
        revoked = self.client.get('/api/clients', HTTP_AUTHORIZATION=f'Bearer {token}')
        self.assertEqual(revoked.status_code, 401)
        self.assertEqual(revoked.json(), UNAUTHORIZED)

    def _login(self, phone='+79991234567', password=PASSWORD):
        return self.client.post(
            '/api/trainer-sessions',
            {'phone': phone, 'password': password},
            content_type='application/json',
        )


class OpenApiTests(TestCase):
    def test_schema_lists_cabinet_paths_and_bearer(self):
        response = self.client.get('/api/schema/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('/api/trainer-sessions', body)
        self.assertIn('/api/clients', body)
        self.assertIn('Bearer', body)
        self.assertIn('bearer', body)
