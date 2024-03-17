from rest_framework import serializers
from ...models import User


class RegistrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
