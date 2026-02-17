from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer


def get_response_for_user(request, user, status,message):
    refresh_token = RefreshToken.for_user(user)
    return Response(
        {
            "user": UserSerializer(user, context={"request": request}).data,
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token),
            "message": "Registration was successful",
        },
        status=status,
    )
