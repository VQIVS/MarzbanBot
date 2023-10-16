from django.urls import path, include
urlpatterns = [
    path("api/v1/", include("website.api.v1.urls")),
]