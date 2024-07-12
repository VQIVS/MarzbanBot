from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import BotOrderSerializer, BotUserSerializer, SendMessageSerializer
from ...models import BotUser, Order
from rest_framework.response import Response
from telebot import TeleBot
from website.models import Configuration

# conf = Configuration.objects.first()
# bot = TeleBot(conf.token)


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = BotUser.objects.all()
    serializer_class = BotUserSerializer

    @swagger_auto_schema(tags=["Bot Users"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Bot Users"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Bot Users"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Bot Users"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Bot Users"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Bot Users"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Bot Users"])
    def get_all_users(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SendMessageToAllUsers(APIView):
    @swagger_auto_schema(
        tags=["Send Message"],
        request_body=SendMessageSerializer,
        responses={
            200: openapi.Response("Messages sent to all users"),
            400: "Bad request",
            405: "Method not allowed",
        },
    )
    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        if serializer.is_valid():
            message_text = serializer.validated_data["message"]
            users = BotUser.objects.all()
            for user in users:
                try:
                    # Use the TeleBot instance to send messages
                    bot.send_message(user.user_id, message_text)
                except Exception as e:
                    print(f"Failed to send message to user {user.user_id}: {str(e)}")
            return JsonResponse({"message": "Messages sent to all users."}, status=200)
        else:
            return JsonResponse(
                {"error": "Invalid request data.", "details": serializer.errors},
                status=400,
            )


@swagger_auto_schema(
    method="post",
    operation_summary="Send message to a specific user",
    request_body=SendMessageSerializer,
    responses={
        200: "Message sent successfully",
        400: "Bad request",
        404: "User not found",
    },
)
@api_view(["POST"])
def send_message_to_user(request, user_id):
    if request.method == "POST":
        serializer = SendMessageSerializer(data=request.data)
        if serializer.is_valid():
            message_text = serializer.validated_data["message"]
            try:
                user = BotUser.objects.get(user_id=user_id)
                # Send message using telebot
                bot.send_message(user.user_id, message_text)
                return JsonResponse(
                    {"message": f"Message sent to user {user_id}."}, status=200
                )
            except BotUser.DoesNotExist:
                return JsonResponse({"error": f"User {user_id} not found."}, status=404)
            except Exception as e:
                return JsonResponse(
                    {"error": f"Failed to send message: {str(e)}"}, status=400
                )
        else:
            return JsonResponse(
                {"error": "Invalid request data.", "details": serializer.errors},
                status=400,
            )


class OrderModelViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = BotOrderSerializer

    @swagger_auto_schema(tags=["Bot Orders"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Bot Orders"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Bot Orders"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Bot Orders"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Bot Orders"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Bot Orders"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Bot Orders"])
    def get_all_orders(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
