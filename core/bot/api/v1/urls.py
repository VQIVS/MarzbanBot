from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserModelViewSet, OrderModelViewSet


"""commented for v1 """
# from .views import UserModelViewSet, EmailModelViewSet, OrderModelViewSet

app_name = "v1-bot"

router = DefaultRouter()
router.register("BotUser", UserModelViewSet, basename="BotUser")

"""commented for v1 """

# router.register('BotEmail', EmailModelViewSet, basename='BotEmail')
router.register("BotOrder", OrderModelViewSet, basename="BotOrder")

urlpatterns = [
    path("", include(router.urls)),
]
