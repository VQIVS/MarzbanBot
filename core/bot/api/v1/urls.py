from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet, OrderModelViewSet

app_name = "v1-bot"

router = DefaultRouter()
router.register("bot-user", UserModelViewSet, basename="user")
router.register("bot-order", OrderModelViewSet, basename="order")


urlpatterns = [
    path("bot/", include(router.urls)),
    path("users/", UserModelViewSet.as_view({'get': 'get_all_users'}), name="user-get-all"),
    path("orders/", OrderModelViewSet.as_view({'get': 'get_all_orders'}), name="order-get-all"),
]
