from .serializers import BotOrderSerializer, BotOrderSerializer
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



