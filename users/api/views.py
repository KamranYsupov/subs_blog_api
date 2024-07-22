from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from .serializes import RegisterUserSerializer

User = get_user_model()


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serialized = self.get_serializer(data=request.data)
        if serialized.is_valid():
            user = User.objects.create_user(
                email=serialized.data.get('email'),
                password=serialized.data.get('password'),
            )
            serialized_data = serialized.data.copy()
            serialized_data.pop('password')
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)
