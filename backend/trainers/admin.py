from django import forms
from django.contrib import admin
from django.contrib.auth.password_validation import validate_password
from django.db.models import Count

from trainers.models import Trainer
from trainers.phones import normalize_phone, validate_phone
from trainers.storage import store_trainer_photo


class TrainerAdminForm(forms.ModelForm):
    phone = forms.CharField(label='Телефон', max_length=32, validators=[validate_phone])
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
    photo_file = forms.FileField(label='Фото', required=False)

    class Meta:
        model = Trainer
        fields = ('phone', 'first_name', 'last_name', 'status')

    def clean_phone(self):
        return normalize_phone(self.cleaned_data['phone'])

    def clean(self):
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
    form = TrainerAdminForm
    list_display = ('phone', 'first_name', 'last_name', 'status', 'client_count')
    search_fields = ('phone', 'first_name', 'last_name')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_client_count=Count('clients'))

    @admin.display(description='Клиенты', ordering='_client_count')
    def client_count(self, obj: Trainer) -> int:
        return obj._client_count

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password1')
        if password:
            obj.set_password(password)
        super().save_model(request, obj, form, change)
        photo = form.cleaned_data.get('photo_file')
        if photo:
            store_trainer_photo(obj, photo)
