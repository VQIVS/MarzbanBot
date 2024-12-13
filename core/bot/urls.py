from django.urls import include, path

from .views import send_message

app_name = "api-v1"

urlpatterns = [
    path("api/v1/", include("bot.api.v1.urls")),
    path("send-message/", send_message, name="send_message_to_all_users"),
]
