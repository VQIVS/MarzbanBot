from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet, OrderModelViewSet

app_name = "api-bot-v1"

router = DefaultRouter()
router.register("user", UserModelViewSet, basename="BotUser")
router.register("order", OrderModelViewSet, basename="BotOrder")
urlpatterns = [
    path("bot/", include(router.urls)),
    path("users/", UserModelViewSet.as_view({'get': 'get_all_users'}), name="user-get-all"),
    path("orders/", OrderModelViewSet.as_view({'get': 'get_all_orders'}), name="order-get-all"),
]
