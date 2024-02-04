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


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                username=email,
                password=password,
            )

            if not user or not user.is_verified:
                raise AuthenticationFailed(
                    _("Unable to log in. User credentials are invalid or the user is not verified."),
                    code="authorization")

            attrs["user"] = user
            return attrs
