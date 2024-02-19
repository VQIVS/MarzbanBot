from django.urls import path, include
from .views import ConfigurationModelViewSet, ProductModelViewSet, TelegramChannelModelViewSet, TutorialModelViewSet, \
    ChannelAdminModelViewSet, MessageModelViewSet, UserModelViewSet, CustomObtainAuthToken, PaymentMethodModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

app_name = "v1-website"

router = DefaultRouter()

router.register('Configuration', ConfigurationModelViewSet, basename='Configuration')
router.register('Product', ProductModelViewSet, basename='Product')
router.register('TelegramChannel', TelegramChannelModelViewSet, basename='TelegramChannel')
router.register('Tutorial', TutorialModelViewSet, basename='Tutorial')
router.register('ChannelAdminModelViewSet', ChannelAdminModelViewSet, basename='ChannelAdminModelViewSet')
router.register('MessageModelViewSet', MessageModelViewSet, basename='MessageModelViewSet')
router.register('User', UserModelViewSet, basename='User')
router.register('PaymentMethod', PaymentMethodModelViewSet, basename='PaymentMethod')
router.register('payment',PaymentMethodModelViewSet, basename='Payment')

urlpatterns = [
    path('', include(router.urls)),
    path('Token/', obtain_auth_token, name='api_token'),
    path('Token/login/', CustomObtainAuthToken.as_view(), name='custom-login'),
]
