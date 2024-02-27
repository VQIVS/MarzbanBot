from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet, OrderModelViewSet

router = DefaultRouter()
router.register("user", UserModelViewSet, basename="BotUser")
router.register("order", OrderModelViewSet, basename="BotOrder")
urlpatterns = [
    path("", include(router.urls)),
]
