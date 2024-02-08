from ...models import Configuration, Product, TelegramChannel, Tutorial, ChannelAdmin, User
from rest_framework.viewsets import ModelViewSet
from .serializers import ConfigurationSerializer, ProductSerializer, TelegramChannelSerializer, TutorialSerializer, \
    ChannelAdminSerializer, MessageSerializer, WebsiteUserSerializer, CustomAuthTokenSerializer, PaymentMethodSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


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


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class PaymentMethodModelViewSet(ModelViewSet):
    queryset = ChannelAdmin.objects.all()
    serializer_class = PaymentMethodSerializer
