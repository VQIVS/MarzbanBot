from django.urls import path, include

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("api/v1/", include("bot.api.v1.urls")),
]
