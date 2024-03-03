from django.urls import path, include
from .views import (
    ConfigurationModelViewSet,
    ProductModelViewSet,
    TelegramChannelModelViewSet,
    TutorialModelViewSet,
    ChannelAdminModelViewSet,
    MessageModelViewSet,
    PaymentMethodModelViewSet,
)
from rest_framework.routers import DefaultRouter

app_name = "v1-website"

router = DefaultRouter()

router.register("configuration", ConfigurationModelViewSet, basename="configuration")
router.register("product", ProductModelViewSet, basename="product")
router.register("telegram-channel", TelegramChannelModelViewSet, basename="telegram-channel")
router.register("tutorial", TutorialModelViewSet, basename="tutorial")
router.register("channel-admin", ChannelAdminModelViewSet, basename="channel-admin")
router.register("message", MessageModelViewSet, basename="message")
router.register("payment-method", PaymentMethodModelViewSet, basename="payment-method")
router.register("payment", PaymentMethodModelViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
]
