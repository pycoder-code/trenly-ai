"""Сущности тренера."""

from trainers.entities.refresh_token_entity import RefreshTokenEntity
from trainers.entities.token_pair_entity import TokenPairEntity
from trainers.entities.trainer_entity import TrainerEntity, TrainerStatus

__all__ = ['RefreshTokenEntity', 'TokenPairEntity', 'TrainerEntity', 'TrainerStatus']
