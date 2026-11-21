"""Представления API тренера."""

from trainers.api.views.trainer_auth_refresh_view import TrainerAuthRefreshView
from trainers.api.views.trainer_auth_view import TrainerAuthView
from trainers.api.views.trainer_detail_view import TrainerDetailView

__all__ = ['TrainerAuthRefreshView', 'TrainerAuthView', 'TrainerDetailView']
