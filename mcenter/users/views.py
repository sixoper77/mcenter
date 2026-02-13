from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Users
from users.serializers import UserRegistrationsSerializer, UserSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationsSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh_token = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user, context={"request": request}).data,
                "refresh": str(refresh_token),
                "access": str(refresh_token.access_token),
                "message": "Registration was successful",
            },
            status=status.HTTP_201_CREATED,
        )


class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()
    permission_classes = [permissions.AllowAny]
