"""Пути API тренера."""

from django.urls import path

from trainers.api.views import TrainerAuthRefreshView, TrainerAuthView, TrainerDetailView

urlpatterns = [
    path('access-tokens', TrainerAuthView.as_view(), name='access-tokens'),
    path('refresh-tokens', TrainerAuthRefreshView.as_view(), name='refresh-tokens'),
    path('trainers/me', TrainerDetailView.as_view(), name='trainers-me'),
]
