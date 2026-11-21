"""Ответ списка клиентов."""

from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers


@extend_schema_serializer(component_name='Client')
class ClientListResponseSerializer(serializers.Serializer):
    """Поля клиента, которые видит тренер."""

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=150, label='Имя')
    last_name = serializers.CharField(max_length=150, allow_blank=True, required=False, label='Фамилия')
    phone = serializers.CharField(allow_null=True, read_only=True)
    height = serializers.IntegerField(allow_null=True, min_value=0, max_value=32767, required=False, label='Рост')
    weight = serializers.DecimalField(
        max_digits=5,
        decimal_places=1,
        coerce_to_string=False,
        allow_null=True,
    )
    active = serializers.BooleanField(label='Активен')

    def to_representation(self, instance):
        """Пустой телефон отдаёт как null."""
        data = super().to_representation(instance)
        if data['phone'] == '':
            data['phone'] = None
        return data
