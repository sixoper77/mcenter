from rest_framework import generics, permissions, status

from .models import User
from .serializers import (
    UserLoginSerializer,
    UserRegistrationsSerializer,
    UserSerializer,
)
from .services import get_response_for_user


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationsSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return get_response_for_user(
            request,
            user,
            status.HTTP_201_CREATED,
            "Registration was successful",
        )


class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return get_response_for_user(
            request,
            user,
            status.HTTP_200_OK,
            "Login was successful",
        )
