import tempfile
from pathlib import Path

from django.contrib import admin
from django.contrib.auth.models import User
from django.core.files.storage import storages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from clients.models import Client
from trainers.models import Trainer

PASSWORD = 'Cabinet-pass-1'


def create_trainer(phone='+79991234567', first_name='Иван', last_name='Петров', **kwargs):
    trainer = Trainer(phone=phone, first_name=first_name, last_name=last_name, **kwargs)
    trainer.set_password(PASSWORD)
    trainer.save()
    return trainer


class TrainerAdminTests(TestCase):
    def setUp(self):
        self.photo_dir = tempfile.TemporaryDirectory()
        self.settings_override = override_settings(TRAINER_PHOTO_ROOT=Path(self.photo_dir.name))
        self.settings_override.enable()
        storages._storages.pop('trainer_photos', None)
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'Admin-pass-1')
        self.client.force_login(self.admin_user)

    def tearDown(self):
        storages._storages.pop('trainer_photos', None)
        self.settings_override.disable()
        self.photo_dir.cleanup()

    def post_trainer(self, phone, *, photo=None, first_name='Иван', last_name='Петров'):
        data = {
            'phone': phone,
            'first_name': first_name,
            'last_name': last_name,
            'status': Trainer.Status.ACTIVE,
            'password1': PASSWORD,
            'password2': PASSWORD,
        }
        if photo is not None:
            data['photo_file'] = photo
        return self.client.post('/admin/trainers/trainer/add/', data)

    def test_create_without_photo(self):
        response = self.post_trainer('8 999 123-45-67')
        self.assertEqual(response.status_code, 302)
        trainer = Trainer.objects.get()
        self.assertEqual(trainer.phone, '+79991234567')
        self.assertEqual(trainer.status, Trainer.Status.ACTIVE)
        self.assertEqual(trainer.photo, '')
        self.assertTrue(trainer.check_password(PASSWORD))
        self.assertNotEqual(trainer.password, PASSWORD)

    def test_create_with_photo(self):
        photo = SimpleUploadedFile('face.jpg', b'portrait-bytes', content_type='image/jpeg')
        response = self.post_trainer('+79991234567', photo=photo)
        self.assertEqual(response.status_code, 302)
        trainer = Trainer.objects.get()
        self.assertEqual(trainer.photo, f'trainers/{trainer.pk}/photo.jpg')
        stored = Path(self.photo_dir.name) / trainer.photo
        self.assertEqual(stored.read_bytes(), b'portrait-bytes')

    def test_duplicate_phone_is_rejected(self):
        create_trainer()
        response = self.post_trainer('+79991234567', first_name='Мария', last_name='Иванова')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Trainer.objects.count(), 1)

    def test_same_number_in_another_spelling_is_rejected(self):
        create_trainer(phone='+7 999 123-45-67')
        response = self.post_trainer('8 999 123-45-67', first_name='Мария', last_name='Иванова')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Trainer.objects.count(), 1)

    def test_list_shows_status_and_client_count(self):
        trainer = create_trainer()
        Client.objects.create(trainer=trainer, telegram_user_id=1, first_name='Анна')
        Client.objects.create(trainer=trainer, telegram_user_id=2, first_name='Борис')
        response = self.client.get('/admin/trainers/trainer/')
        self.assertEqual(response.status_code, 200)
        row = next(item for item in response.context['cl'].result_list if item.pk == trainer.pk)
        self.assertEqual(row._client_count, 2)
        self.assertContains(response, 'активен')

    def test_client_personal_data_is_hidden(self):
        trainer = create_trainer()
        Client.objects.create(
            trainer=trainer,
            telegram_user_id=501,
            telegram_username='secret_user',
            first_name='ТайныйКлиент',
            last_name='Скрытый',
            phone='+79990000002',
            height=180,
            weight='70.5',
        )
        self.assertNotIn(Client, admin.site._registry)
        for url in ('/admin/', '/admin/trainers/trainer/'):
            response = self.client.get(url)
            self.assertNotContains(response, 'ТайныйКлиент')
            self.assertNotContains(response, 'secret_user')
            self.assertNotContains(response, '+79990000002')
        missing = self.client.get('/admin/trainers/client/')
        self.assertEqual(missing.status_code, 404)

    def test_block_and_unblock(self):
        trainer = create_trainer()
        change_url = f'/admin/trainers/trainer/{trainer.pk}/change/'
        blocked = self.client.post(
            change_url,
            {
                'phone': trainer.phone,
                'first_name': trainer.first_name,
                'last_name': trainer.last_name,
                'status': Trainer.Status.BLOCKED,
                'password1': '',
                'password2': '',
            },
        )
        self.assertEqual(blocked.status_code, 302)
        trainer.refresh_from_db()
        self.assertEqual(trainer.status, Trainer.Status.BLOCKED)

        unblocked = self.client.post(
            change_url,
            {
                'phone': trainer.phone,
                'first_name': trainer.first_name,
                'last_name': trainer.last_name,
                'status': Trainer.Status.ACTIVE,
                'password1': '',
                'password2': '',
            },
        )
        self.assertEqual(unblocked.status_code, 302)
        trainer.refresh_from_db()
        self.assertEqual(trainer.status, Trainer.Status.ACTIVE)

    def test_trainer_cannot_log_into_admin(self):
        create_trainer()
        self.client.logout()
        response = self.client.post(
            '/admin/login/',
            {'username': '+79991234567', 'password': PASSWORD},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
