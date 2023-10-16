from ...models import Configuration, Product, TelegramChannel, Tutorial, ChannelAdmin
from rest_framework.viewsets import ModelViewSet
from .serializers import ConfigurationSerializer, ProductSerializer, TelegramChannelSerializer, TutorialSerializer, \
    ChannelAdminSerializer


class ConfigurationModelViewSet(ModelViewSet):
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer

class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class TelegramChannelModelViewSet(ModelViewSet):
    queryset = TelegramChannel.objects.all()
    serializer_class = TelegramChannelSerializer

class TutorialModelViewSet(ModelViewSet):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

class ChannelAdminModelViewSet(ModelViewSet):
    queryset = ChannelAdmin.objects.all()
    serializer_class = ChannelAdminSerializer

