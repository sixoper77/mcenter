from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.viewsets import ModelViewSet

from appointment.serializers import ClinickSerializer,DoctorSerializer


class ClinickAPIView(generics.CreateAPIView):
    serializer_class = ClinickSerializer
    permission_classes = [permissions.IsAdminUser]
    
    
class DoctorAPIView(generics.CreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAdminUser]
