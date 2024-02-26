from .serializers import BotOrderSerializer
from rest_framework import viewsets
from ...models import BotUser, Order


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = BotUser.objects.all()
    serializer_class = BotOrderSerializer


class OrderModelViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = BotOrderSerializer
