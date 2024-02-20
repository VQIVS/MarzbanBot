from ...models import (
    Configuration,
    Product,
    TelegramChannel,
    Tutorial,
    ChannelAdmin,
    User,
)
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    ConfigurationSerializer,
    ProductSerializer,
    TelegramChannelSerializer,
    TutorialSerializer,
    ChannelAdminSerializer,
    MessageSerializer,
    WebsiteUserSerializer,
    PaymentMethodSerializer,
)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = WebsiteUserSerializer


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


class MessageModelViewSet(ModelViewSet):
    queryset = ChannelAdmin.objects.all()
    serializer_class = MessageSerializer


class PaymentMethodModelViewSet(ModelViewSet):
    queryset = ChannelAdmin.objects.all()
    serializer_class = PaymentMethodSerializer
