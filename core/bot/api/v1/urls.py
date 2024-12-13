from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (OrderModelViewSet, SendMessageToAllUsers, UserModelViewSet,
                    send_message_to_user)

app_name = "v1-bot"

router = DefaultRouter()
router.register("bot-user", UserModelViewSet, basename="user")
router.register("bot-order", OrderModelViewSet, basename="order")


urlpatterns = [
    path("bot/", include(router.urls)),
    path(
        "users/",
        UserModelViewSet.as_view({"get": "get_all_users"}),
        name="user-get-all",
    ),
    path(
        "orders/",
        OrderModelViewSet.as_view({"get": "get_all_orders"}),
        name="order-get-all",
    ),
    path(
        "send-message-to-all-users/",
        SendMessageToAllUsers.as_view(),
        name="send-message-to-all-users",
    ),
    path(
        "send-message-to-user/<int:user_id>/",
        send_message_to_user,
        name="send_message_to_user",
    ),
]
