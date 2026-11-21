"""Тренеры в админке."""

from django import forms
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.db.models import Count

from trainers.models import Trainer


class TrainerAdminForm(forms.ModelForm):
    """Телефон и пароль тренера."""

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
        fields = ('phone', 'first_name', 'last_name', 'status')

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
        """Сохраняет тренера."""
        raw_password = form.cleaned_data.get('password1') or None
        if raw_password:
            obj.password = make_password(raw_password)
        obj.save()
