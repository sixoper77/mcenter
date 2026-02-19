from rest_framework import generics, permissions, viewsets

from .models import Appointment
from .permissions import IsPatient
from .serializers import AppointmentSerializer, ClinicSerializer, DoctorSerializer


class ClinicAPIView(generics.CreateAPIView):
    serializer_class = ClinicSerializer
    permission_classes = [permissions.IsAdminUser]


class DoctorRoleChangeAPIView(generics.CreateAPIView):
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAdminUser]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('doctor','clinic',)
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]
    

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(patient=self.request.user)
        
    def perform_create(self, serializer):
        return serializer.save(patient=self.request.user)
