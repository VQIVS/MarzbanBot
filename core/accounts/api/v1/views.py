from rest_framework import generics
from .serializers import RegistrationsSerializer
from rest_framework.response import Response
from rest_framework import status


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationsSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {"email": serializer.validated_data["email"]}
            return Response(data, status=status.HTTP_201_CREATED)
