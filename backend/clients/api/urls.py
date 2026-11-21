"""Пути API клиента."""

from django.urls import path

from clients.api.views import ClientListView

urlpatterns = [
    path('clients', ClientListView.as_view(), name='clients'),
]
