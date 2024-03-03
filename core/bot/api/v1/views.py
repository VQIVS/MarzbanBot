from .serializers import BotUserSerializer, BotOrderSerializer
from rest_framework import viewsets
from ...models import BotUser, Order


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer


class OrderModelViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = BotOrderSerializer
