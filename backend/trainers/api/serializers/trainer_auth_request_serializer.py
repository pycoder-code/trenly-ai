"""Тело входа тренера."""

import re

from rest_framework import serializers

_SEPARATORS = re.compile(r'[\s()\-]')


class TrainerAuthRequestSerializer(serializers.Serializer):
    """Телефон и пароль."""

    phone = serializers.CharField()
    password = serializers.CharField()

    def validate_phone(self, value: str) -> str:
        """Приводит телефон к виду +7 и десять цифр."""
        if not value.strip():
            raise serializers.ValidationError('Укажите телефон.')
        compact = _SEPARATORS.sub('', value.strip())
        if compact.startswith('+'):
            digits = compact[1:]
        else:
            digits = compact
            if len(digits) == 11 and digits.startswith('8'):
                digits = '7' + digits[1:]
        if not digits.isdigit() or len(digits) != 11 or not digits.startswith('7'):
            raise serializers.ValidationError('Телефон должен быть российским номером.')
        return f'+{digits}'
