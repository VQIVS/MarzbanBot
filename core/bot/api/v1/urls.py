from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet, OrderModelViewSet

app_name = "v1-bot"

router = DefaultRouter()
router.register("bot-user", UserModelViewSet, basename="user")
router.register("bot-order", OrderModelViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
