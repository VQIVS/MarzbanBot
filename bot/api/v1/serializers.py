from rest_framework import serializers
from ...models import User, Order

class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BotOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
