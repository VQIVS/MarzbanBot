from django.urls import path, include
from .views import (
    ConfigurationModelViewSet,
    ProductModelViewSet,
    TelegramChannelModelViewSet,
    TutorialModelViewSet,
    ChannelAdminModelViewSet,
    MessageModelViewSet,
    UserModelViewSet,
    PaymentMethodModelViewSet,
)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

app_name = "v1-website"

router = DefaultRouter()

router.register("Configuration", ConfigurationModelViewSet, basename="Configuration")
router.register("Product", ProductModelViewSet, basename="Product")
router.register(
    "TelegramChannel", TelegramChannelModelViewSet, basename="TelegramChannel"
)
router.register("Tutorial", TutorialModelViewSet, basename="Tutorial")
router.register(
    "ChannelAdmin",
    ChannelAdminModelViewSet,
    basename="ChannelAdmin",
)
router.register(
    "Message", MessageModelViewSet, basename="Message"
)
router.register("User", UserModelViewSet, basename="User")
router.register("PaymentMethod", PaymentMethodModelViewSet, basename="PaymentMethod")
router.register("payment", PaymentMethodModelViewSet, basename="Payment")

urlpatterns = [
    path("", include(router.urls)),
    path("Token/", obtain_auth_token, name="api_token"),
]