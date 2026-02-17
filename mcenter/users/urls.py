from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import UserLoginAPIView, UserProfileAPIView, UserRegisterAPIView

urlpatterns = [
    path("api/registration/", UserRegisterAPIView.as_view()),
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh", TokenRefreshView.as_view()),
    path("api/profile/<int:pk>/", UserProfileAPIView.as_view()),
    path("api/login/", UserLoginAPIView.as_view()),
]
