from rest_framework import generics, permissions

from .serializers import ClinicSerializer, DoctorSerializer


class ClinicAPIView(generics.CreateAPIView):
    serializer_class = ClinicSerializer
    permission_classes = [permissions.IsAdminUser]


class DoctorRoleChangeAPIView(generics.CreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAdminUser]
