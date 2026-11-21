"""Пути входа тренера."""

from django.urls import path

from trainers.api.views import TrainerAuthRefreshView, TrainerAuthView

urlpatterns = [
    path('access-tokens', TrainerAuthView.as_view(), name='access-tokens'),
    path('refresh-tokens', TrainerAuthRefreshView.as_view(), name='refresh-tokens'),
]
