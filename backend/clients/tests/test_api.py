from decimal import Decimal

from django.test import TestCase

from clients.models import Client
from trainers.tests.test_admin import PASSWORD, create_trainer


class ClientListTests(TestCase):
    def setUp(self):
        self.trainer = create_trainer()
        self.other = create_trainer(phone='+79990000009', first_name='Ольга', last_name='Смирнова')
        self.token = self.client.post(
            '/api/trainer-sessions',
            {'phone': '+79991234567', 'password': PASSWORD},
            content_type='application/json',
        ).json()['token']

    def test_own_client_and_hidden_stranger(self):
        own = Client.objects.create(trainer=self.trainer, telegram_user_id=1, first_name='Анна')
        Client.objects.create(
            trainer=self.other,
            telegram_user_id=2,
            first_name='ЧужойКлиент',
            telegram_username='hidden_name',
        )
        body = self._list()
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]['id'], own.pk)
        self.assertEqual(body[0]['first_name'], 'Анна')
        self.assertNotIn('ЧужойКлиент', str(body))

    def test_missing_last_name(self):
        Client.objects.create(trainer=self.trainer, telegram_user_id=1, first_name='Анна')
        self.assertEqual(self._list()[0]['last_name'], '')

    def test_optional_measurements_when_set(self):
        Client.objects.create(
            trainer=self.trainer,
            telegram_user_id=1,
            first_name='Анна',
            phone='8 999 000-00-03',
            height=180,
            weight=Decimal('70.5'),
        )
        row = self._list()[0]
        self.assertEqual(row['phone'], '+79990000003')
        self.assertEqual(row['height'], 180)
        self.assertEqual(row['weight'], 70.5)

    def test_optional_measurements_when_empty(self):
        Client.objects.create(trainer=self.trainer, telegram_user_id=1, first_name='Анна')
        row = self._list()[0]
        self.assertIsNone(row['phone'])
        self.assertIsNone(row['height'])
        self.assertIsNone(row['weight'])

    def test_disconnected_status(self):
        Client.objects.create(
            trainer=self.trainer,
            telegram_user_id=1,
            first_name='Анна',
            status=Client.Status.DISCONNECTED,
        )
        self.assertEqual(self._list()[0]['status'], 'disconnected')

    def test_response_omits_telegram_fields(self):
        Client.objects.create(
            trainer=self.trainer,
            telegram_user_id=4242,
            telegram_username='ann',
            first_name='Анна',
        )
        row = self._list()[0]
        self.assertNotIn('telegram_user_id', row)
        self.assertNotIn('telegram_username', row)
        self.assertNotIn(4242, row.values())
        self.assertNotIn('ann', row.values())

    def test_without_login(self):
        response = self.client.get('/api/clients')
        self.assertEqual(response.status_code, 401)

    def _list(self):
        response = self.client.get('/api/clients', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, 200)
        return response.json()
