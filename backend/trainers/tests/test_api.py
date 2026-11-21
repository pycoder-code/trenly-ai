"""Вход тренера и обновление пары токенов."""

from datetime import timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.core import signing
from django.test import TestCase
from django.utils import timezone

from trainers.models import RefreshToken, Trainer
from trainers.repositories import hash_refresh_secret
from trainers.tests.test_admin import PASSWORD, create_trainer

UNAUTHORIZED = {'detail': 'Неверные учётные данные.'}


class TrainerAuthTests(TestCase):
    """Пара токенов и отказы входа."""

    def test_active_trainer_logs_in(self):
        """Активный тренер получает пару, токен доступа открывает кабинет."""
        trainer = create_trainer()
        response = self._login()
        self.assertEqual(response.status_code, 201)
        body = response.json()
        access_token = body['access_token']
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        self.assertEqual(payload['sub'], str(trainer.pk))
        self.assertLessEqual(payload['exp'] - timezone.now().timestamp(), 15 * 60)
        clients = self.client.get('/api/clients', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(clients.status_code, 200)
        refresh_as_bearer = self.client.get(
            '/api/clients',
            HTTP_AUTHORIZATION=f'Bearer {body["refresh_token"]}',
        )
        self.assertEqual(refresh_as_bearer.status_code, 401)
        self.assertEqual(refresh_as_bearer.json(), UNAUTHORIZED)

    def test_wrong_password(self):
        """Неверный пароль не открывает кабинет."""
        create_trainer()
        response = self._login(password='wrong-password-1')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), UNAUTHORIZED)

    def test_unknown_phone_matches_wrong_password(self):
        """Неизвестный телефон отвечает так же, как неверный пароль."""
        create_trainer()
        wrong = self._login(password='wrong-password-1')
        unknown = self._login(phone='+79990000000')
        self.assertEqual(unknown.status_code, 401)
        self.assertEqual(unknown.json(), wrong.json())

    def test_leading_eight(self):
        """Номер с восьмёрки узнаёт того же тренера."""
        create_trainer()
        response = self._login(phone='8 999 123-45-67')
        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', response.json())
        self.assertIn('refresh_token', response.json())

    def test_foreign_phone_is_rejected(self):
        """Чужой номер не доходит до проверки пароля."""
        create_trainer()
        response = self._login(phone='+1 202 555 0143')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'phone': ['Телефон должен быть российским номером.']})

    def test_empty_phone_is_rejected(self):
        """Пустой телефон не доходит до проверки пароля."""
        create_trainer()
        response = self._login(phone='')
        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', response.json())
        self.assertNotIn('access_token', response.json())

    def test_unsigned_and_expired_access_token(self):
        """Чужой и просроченный токен доступа не открывают кабинет."""
        trainer = create_trainer()
        legacy = signing.dumps({'trainer_id': trainer.pk}, salt='trainer-auth')
        legacy_response = self.client.get('/api/clients', HTTP_AUTHORIZATION=f'Bearer {legacy}')
        self.assertEqual(legacy_response.status_code, 401)
        self.assertEqual(legacy_response.json(), UNAUTHORIZED)
        expired = jwt.encode(
            {'sub': str(trainer.pk), 'exp': timezone.now() - timedelta(minutes=1)},
            settings.SECRET_KEY,
            algorithm='HS256',
        )
        expired_response = self.client.get('/api/clients', HTTP_AUTHORIZATION=f'Bearer {expired}')
        self.assertEqual(expired_response.status_code, 401)
        self.assertEqual(expired_response.json(), UNAUTHORIZED)

    def test_refresh_rotation_and_rejected_secrets(self):
        """Новая пара гасит прежний секрет. Просроченный и неизвестный не проходят."""
        create_trainer()
        first = self._login().json()
        rotated = self.client.post(
            '/api/refresh-tokens',
            {'refresh_token': first['refresh_token']},
            content_type='application/json',
        )
        self.assertEqual(rotated.status_code, 201)
        reused = self.client.post(
            '/api/refresh-tokens',
            {'refresh_token': first['refresh_token']},
            content_type='application/json',
        )
        self.assertEqual(reused.status_code, 401)
        self.assertEqual(reused.json(), UNAUTHORIZED)
        clients = self.client.get(
            '/api/clients',
            HTTP_AUTHORIZATION=f'Bearer {rotated.json()["access_token"]}',
        )
        self.assertEqual(clients.status_code, 200)
        unknown = self.client.post(
            '/api/refresh-tokens',
            {'refresh_token': 'missing-secret'},
            content_type='application/json',
        )
        self.assertEqual(unknown.status_code, 401)
        trainer = Trainer.objects.get(phone='+79991234567')
        stale = 'stale-refresh-secret'
        RefreshToken.objects.create(
            trainer=trainer,
            secret_hash=hash_refresh_secret(stale),
            expires_at=timezone.now() - timedelta(seconds=1),
        )
        expired = self.client.post(
            '/api/refresh-tokens',
            {'refresh_token': stale},
            content_type='application/json',
        )
        self.assertEqual(expired.status_code, 401)
        self.assertEqual(expired.json(), UNAUTHORIZED)

    def test_blocked_trainer_and_revoked_token(self):
        """Заблокированный тренер не входит, выданные токены гаснут."""
        trainer = create_trainer()
        pair = self._login().json()
        self._change_trainer(trainer, status=Trainer.Status.BLOCKED)
        blocked_login = self._login()
        self.assertEqual(blocked_login.status_code, 401)
        self.assertEqual(blocked_login.json(), UNAUTHORIZED)
        revoked = self.client.get('/api/clients', HTTP_AUTHORIZATION=f'Bearer {pair["access_token"]}')
        self.assertEqual(revoked.status_code, 401)
        self.assertEqual(revoked.json(), UNAUTHORIZED)
        refresh = self.client.post(
            '/api/refresh-tokens',
            {'refresh_token': pair['refresh_token']},
            content_type='application/json',
        )
        self.assertEqual(refresh.status_code, 401)
        self.assertEqual(refresh.json(), UNAUTHORIZED)
        self.assertEqual(RefreshToken.objects.filter(trainer=trainer).count(), 0)

    def _change_trainer(self, trainer, *, status, password=''):
        """Меняет тренера формой админки."""
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'Admin-pass-1')
        self.client.force_login(admin_user)
        response = self.client.post(
            f'/admin/trainers/trainer/{trainer.pk}/change/',
            {
                'phone': trainer.phone,
                'first_name': trainer.first_name,
                'last_name': trainer.last_name,
                'status': status,
                'password1': password,
                'password2': password,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def _login(self, phone='+79991234567', password=PASSWORD):
        """Запрашивает пару токенов."""
        return self.client.post(
            '/api/access-tokens',
            {'phone': phone, 'password': password},
            content_type='application/json',
        )


class OpenApiTests(TestCase):
    """Схема описывает кабинет."""

    def test_schema_lists_cabinet_paths_and_bearer(self):
        """В схеме есть пути кабинета, Bearer и нет старого поля token."""
        response = self.client.get('/api/schema/')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertIn('/api/access-tokens', body)
        self.assertIn('/api/refresh-tokens', body)
        self.assertIn('/api/clients', body)
        self.assertIn('Bearer', body)
        self.assertIn('bearer', body)
        self.assertIn('access_token', body)
        self.assertIn('refresh_token', body)
        without_named_tokens = body.replace('access_token', '').replace('refresh_token', '')
        self.assertNotIn('token:', without_named_tokens)
