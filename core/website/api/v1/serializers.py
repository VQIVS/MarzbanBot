from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from ...models import (
    Configuration,
    Product,
    TelegramChannel,
    Tutorial,
    ChannelAdmin,
    Message,

    PaymentMethod, MajorProduct,
)
from django.utils.translation import gettext as _


class ConfigurationSerializer(ModelSerializer):
    class Meta:
        model = Configuration
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class TelegramChannelSerializer(ModelSerializer):
    class Meta:
        model = TelegramChannel
        fields = "__all__"


class TutorialSerializer(ModelSerializer):
    class Meta:
        model = Tutorial
        fields = "__all__"


class ChannelAdminSerializer(ModelSerializer):
    class Meta:
        model = ChannelAdmin
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)


class PaymentMethodSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"


class MajorProductSerializer(ModelSerializer):
    class Meta:
        model = MajorProduct
        fields = "__all__"
