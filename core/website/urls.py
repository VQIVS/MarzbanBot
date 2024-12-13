from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("website.api.v1.urls")),
]
