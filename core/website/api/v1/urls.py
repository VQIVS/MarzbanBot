from django.urls import path, include
from .views import (
    ConfigurationModelViewSet,
    ProductModelViewSet,
    TelegramChannelModelViewSet,
    TutorialModelViewSet,
    ChannelAdminModelViewSet,
    MessageModelViewSet,
    PaymentMethodModelViewSet,
    MajorProductModelViewSet
)
from rest_framework.routers import DefaultRouter

app_name = "v1-website"

router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    ]
router.register("configuration", ConfigurationModelViewSet, basename="Configuration")
router.register("product", ProductModelViewSet, basename="Product")
router.register(
    "telegram_channel", TelegramChannelModelViewSet, basename="TelegramChannel"
)
router.register("tutorial", TutorialModelViewSet, basename="Tutorial")
router.register(
    "channel_admin",
    ChannelAdminModelViewSet,
    basename="channel_admin",
)
router.register(
    "message", MessageModelViewSet, basename="Message"
)
router.register("payment_method", PaymentMethodModelViewSet, basename="PaymentMethod")
router.register("payment", PaymentMethodModelViewSet, basename="Payment")
router.register("major_product", MajorProductModelViewSet, basename="MajorProduct")

urlpatterns = [
    path("website/", include(router.urls)),
]
