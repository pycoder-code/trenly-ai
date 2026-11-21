"""Тренеры в админке."""

from django import forms
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.files.storage import storages
from django.db.models import Count

from trainers.models import Trainer

PHOTO_CONTENT_TYPES = {'image/jpeg', 'image/png', 'image/webp'}


class TrainerAdminForm(forms.ModelForm):
    """Телефон, пароль и фото тренера."""

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        required=False,
    )
    password2 = forms.CharField(
        label='Пароль ещё раз',
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        """Модель и поля, которые форма пишет сама."""

        model = Trainer
        fields = ('phone', 'first_name', 'last_name', 'photo', 'status')

    def clean(self):
        """Пароль обязателен у нового тренера и совпадает в обоих полях."""
        cleaned = super().clean()
        password1 = cleaned.get('password1')
        password2 = cleaned.get('password2')
        if not self.instance.pk and not password1:
            self.add_error('password1', 'Укажите пароль.')
        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', 'Пароли не совпадают.')
            elif password1:
                validate_password(password1, self.instance)
        return cleaned

    def __init__(self, *args, **kwargs):
        """Подсказывает, что новый файл заменит уже сохранённое фото."""
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.photo:
            self.fields['photo'].help_text = 'Сейчас фото есть. Новый файл заменит его.'

    def clean_photo(self):
        """Оставляет пустое поле или файл изображения."""
        upload = self.cleaned_data.get('photo')
        content_type = getattr(upload, 'content_type', '') or ''
        if not upload or not content_type:
            return upload
        if content_type not in PHOTO_CONTENT_TYPES:
            self.add_error('photo', 'Фото должно быть JPEG, PNG или WebP.')
        return upload


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    """Список тренеров."""

    form = TrainerAdminForm
    list_display = ('phone', 'first_name', 'last_name', 'status', 'client_count')
    search_fields = ('phone', 'first_name', 'last_name')

    def get_queryset(self, request):
        """Добавляет число клиентов для списка."""
        return super().get_queryset(request).annotate(_client_count=Count('clients'))

    @admin.display(description='Клиенты', ordering='_client_count')
    def client_count(self, obj: Trainer) -> int:
        """Сколько клиентов подключено к тренеру."""
        return obj._client_count

    def save_model(self, request, obj, form, change):
        """Сохраняет тренера и убирает прежний файл фото."""
        previous = ''
        if change and obj.pk:
            previous = Trainer.objects.filter(pk=obj.pk).values_list('photo', flat=True).first() or ''
        raw_password = form.cleaned_data.get('password1') or None
        if raw_password:
            obj.password = make_password(raw_password)
        obj.save()
        current = obj.photo.name or ''
        if previous and previous != current:
            storage = storages['trainer_photos']
            if storage.exists(previous):
                storage.delete(previous)
