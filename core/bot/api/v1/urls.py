from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet, OrderModelViewSet

router = DefaultRouter()
router.register("BotUser", UserModelViewSet, basename="BotUser")
router.register("BotOrder", OrderModelViewSet, basename="BotOrder")
urlpatterns = [
    path("", include(router.urls)),
]
