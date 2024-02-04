from rest_framework import serializers
from ...models import User, Order
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class BotUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BotOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


