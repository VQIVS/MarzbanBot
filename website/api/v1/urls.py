from django.urls import path, include
from .views import ConfigurationModelViewSet, ProductModelViewSet, TelegramChannelModelViewSet, TutorialModelViewSet, ChannelAdminModelViewSet
from rest_framework.routers import DefaultRouter
app_name = "v1-website"


router = DefaultRouter()

router.register('Configuration', ConfigurationModelViewSet, basename='Configuration')
router.register('Product', ProductModelViewSet, basename='Product')
router.register('TelegramChannel', TelegramChannelModelViewSet, basename='TelegramChannel')
router.register('Tutorial', TutorialModelViewSet, basename='Tutorial')
router.register('ChannelAdminModelViewSet', ChannelAdminModelViewSet, basename='ChannelAdminModelViewSet')


urlpatterns = [
    path('', include(router.urls))
]