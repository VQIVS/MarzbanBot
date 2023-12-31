from rest_framework.serializers import ModelSerializer
from ...models import Configuration, Product, TelegramChannel, Tutorial, ChannelAdmin


class ConfigurationSerializer(ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class TelegramChannelSerializer(ModelSerializer):
    class Meta:
        model = TelegramChannel
        fields = '__all__'

class TutorialSerializer(ModelSerializer):
    class Meta:
        model = Tutorial
        fields = '__all__'

class ChannelAdminSerializer(ModelSerializer):
    class Meta:
        model = ChannelAdmin
        fields = '__all__'
