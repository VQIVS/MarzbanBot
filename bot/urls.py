from django.urls import path, include
urlpatterns = [
    path("api/v1/", include("bot.api.v1.urls")),
]