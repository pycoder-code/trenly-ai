"""Админка тренеров."""

from clients.models import Client
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.core.files.storage import storages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from trainers.models import Trainer

PASSWORD = 'Cabinet-pass-1'


def create_trainer(phone='+79991234567', first_name='Иван', last_name='Петров', **kwargs):
    """Создаёт тренера и возвращает строку таблицы."""
    return Trainer.objects.create(
        phone=phone,
        password=make_password(PASSWORD),
        first_name=first_name,
        last_name=last_name,
        photo=kwargs.get('photo', ''),
        status=kwargs.get('status', Trainer.Status.ACTIVE),
    )


class TrainerAdminTests(TestCase):
    """Администратор заводит и блокирует тренеров."""

    def setUp(self):
        """Вход администратора."""
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'Admin-pass-1')
        self.client.force_login(self.admin_user)

    def tearDown(self):
        """Убирает файлы фото, записанные тестом."""
        storage = storages['trainer_photos']
        for trainer in Trainer.objects.all():
            name = trainer.photo.name
            if name and storage.exists(name):
                storage.delete(name)

    def post_trainer(self, phone, *, first_name='Иван', last_name='Петров'):
        """Отправляет форму нового тренера."""
        return self.client.post(
            '/admin/trainers/trainer/add/',
            {
                'phone': phone,
                'first_name': first_name,
                'last_name': last_name,
                'status': Trainer.Status.ACTIVE,
                'password1': PASSWORD,
                'password2': PASSWORD,
            },
        )

    def test_create_without_photo(self):
        """Тренер создаётся без фото, пароль хранится хешем."""
        response = self.post_trainer('+79991234567')
        self.assertEqual(response.status_code, 302)
        trainer = Trainer.objects.get()
        self.assertEqual(trainer.phone, '+79991234567')
        self.assertEqual(trainer.status, Trainer.Status.ACTIVE)
        self.assertFalse(trainer.photo)
        self.assertTrue(check_password(PASSWORD, trainer.password))
        self.assertNotEqual(trainer.password, PASSWORD)

    def test_create_with_photo(self):
        """Имя фото выбирает хранилище Django."""
        photo = SimpleUploadedFile('trainer-create.jpg', b'first-photo', content_type='image/jpeg')
        response = self.client.post(
            '/admin/trainers/trainer/add/',
            {
                'phone': '+79991234567',
                'first_name': 'Иван',
                'last_name': 'Петров',
                'status': Trainer.Status.ACTIVE,
                'password1': PASSWORD,
                'password2': PASSWORD,
                'photo': photo,
            },
        )
        self.assertEqual(response.status_code, 302)
        trainer = Trainer.objects.get()
        self.assertEqual(trainer.photo, 'trainer-create.jpg')
        storage = storages['trainer_photos']
        with storage.open(trainer.photo.name) as stored:
            self.assertEqual(stored.read(), b'first-photo')

    def test_replace_photo(self):
        """Новый файл заменяет фото тренера."""
        trainer = create_trainer()
        first = SimpleUploadedFile('trainer-replace.jpg', b'first-photo', content_type='image/jpeg')
        second = SimpleUploadedFile('trainer-replace.png', b'second-photo', content_type='image/png')
        change_url = f'/admin/trainers/trainer/{trainer.pk}/change/'
        saved = self.client.post(change_url, self._change_data(trainer, photo=first))
        self.assertEqual(saved.status_code, 302)
        replaced = self.client.post(change_url, self._change_data(trainer, photo=second))
        self.assertEqual(replaced.status_code, 302)
        trainer.refresh_from_db()
        self.assertEqual(trainer.photo, 'trainer-replace.png')
        storage = storages['trainer_photos']
        self.assertFalse(storage.exists('trainer-replace.jpg'))
        with storage.open(trainer.photo.name) as stored:
            self.assertEqual(stored.read(), b'second-photo')

    def test_duplicate_phone_is_rejected(self):
        """Второй тренер с тем же телефоном не создаётся."""
        create_trainer()
        response = self.post_trainer('+79991234567', first_name='Мария', last_name='Иванова')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Trainer.objects.count(), 1)

    def test_list_shows_status_and_client_count(self):
        """Список показывает статус и число клиентов."""
        trainer = create_trainer()
        Client.objects.create(trainer=trainer, telegram_user_id=1, first_name='Анна')
        Client.objects.create(trainer=trainer, telegram_user_id=2, first_name='Борис')
        response = self.client.get('/admin/trainers/trainer/')
        self.assertEqual(response.status_code, 200)
        row = next(item for item in response.context['cl'].result_list if item.pk == trainer.pk)
        self.assertEqual(row._client_count, 2)
        self.assertContains(response, 'активен')

    def test_client_list_shows_client_without_body_measures(self):
        """Список клиентов показывает имя и телефон и скрывает рост и вес."""
        trainer = create_trainer()
        client = Client.objects.create(
            trainer=trainer,
            telegram_user_id=501,
            telegram_username='secret_user',
            first_name='ТайныйКлиент',
            last_name='Скрытый',
            phone='+79990000002',
            height=180,
            weight='70.5',
        )
        listing = self.client.get('/admin/clients/client/')
        self.assertEqual(listing.status_code, 200)
        self.assertContains(listing, 'ТайныйКлиент')
        self.assertContains(listing, 'Скрытый')
        self.assertContains(listing, 'Иван Петров')
        self.assertContains(listing, '+79990000002')
        self.assertContains(listing, 'secret_user')
        self.assertNotContains(listing, '180')
        self.assertNotContains(listing, '70.5')
        card = self.client.get(f'/admin/clients/client/{client.pk}/change/')
        self.assertEqual(card.status_code, 200)
        self.assertContains(card, 'ТайныйКлиент')
        self.assertNotContains(card, 'name="height"')
        self.assertNotContains(card, 'name="weight"')

    def test_block_and_unblock(self):
        """Администратор блокирует и снова открывает тренера."""
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

    def _change_data(self, trainer, **extra):
        """Поля формы существующего тренера без смены пароля."""
        data = {
            'phone': trainer.phone,
            'first_name': trainer.first_name,
            'last_name': trainer.last_name,
            'status': trainer.status,
            'password1': '',
            'password2': '',
        }
        data.update(extra)
        return data

    def test_trainer_cannot_log_into_admin(self):
        """Тренер не входит в админку своим телефоном."""
        create_trainer()
        self.client.logout()
        response = self.client.post(
            '/admin/login/',
            {'username': '+79991234567', 'password': PASSWORD},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
