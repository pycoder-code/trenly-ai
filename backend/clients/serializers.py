from rest_framework import serializers

from clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()
    weight = serializers.DecimalField(
        max_digits=5,
        decimal_places=1,
        coerce_to_string=False,
        allow_null=True,
    )

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'phone', 'height', 'weight', 'status')

    def get_phone(self, client: Client) -> str | None:
        return client.phone or None
