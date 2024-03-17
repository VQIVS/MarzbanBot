from rest_framework import serializers
from ...models import BotUser, Order


class BotUserSerializer(serializers.ModelSerializer):
    """
    This class defines the Serializer for the BotUser model.
    """

    class Meta:
        model = BotUser
        fields = "__all__"


class BotOrderSerializer(serializers.ModelSerializer):
    """
    This class defines the Serializer for the Order model.

    """

    class Meta:
        model = Order
        fields = "__all__"


class SendMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)
