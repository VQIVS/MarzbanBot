from .serializers import BotOrderSerializer, BotOrderSerializer, CustomAuthTokenSerializer
from rest_framework import viewsets
from ...models import User, Order
from rest_framework.authtoken.views import ObtainAuthToken

# from ...models import Email, User, Order
""" commented for v1 """


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = BotOrderSerializer


""" commented for v1 """


# class EmailModelViewSet(viewsets.ModelViewSet):
#     queryset = Email.objects.all()
#     serializer_class = EmailSerializer
#


class OrderModelViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = BotOrderSerializer


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


