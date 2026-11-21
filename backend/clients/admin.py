"""Клиенты в админке."""

from django.contrib import admin

from clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Список клиентов без роста и веса."""

    list_display = ('last_name', 'first_name', 'trainer', 'phone', 'telegram_username', 'active')
    list_select_related = ('trainer',)
    search_fields = (
        'last_name',
        'first_name',
        'phone',
        'telegram_username',
        'trainer__last_name',
        'trainer__first_name',
    )
    list_filter = ('active',)
    fields = (
        'trainer',
        'first_name',
        'last_name',
        'phone',
        'telegram_user_id',
        'telegram_username',
        'active',
    )
