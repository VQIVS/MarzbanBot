from rest_framework import serializers
from ...models import BotUser, Order


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotUser
        fields = "__all__"


class BotOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
