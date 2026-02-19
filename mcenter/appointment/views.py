from django.core.exceptions import ValidationError as DjangoValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.exceptions import ValidationError as DRFValidationError

from .filters import AppointmentFilter
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
    queryset = Appointment.objects.select_related(
        "doctor",
        "clinic",
    )
    serializer_class = AppointmentSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_class = AppointmentFilter
    search_fields = [
        "doctor__doctor__first_name",
        "doctor__doctor__last_name",
        "doctor__doctor__surname",
        "patient__last_name",
    ]
    ordering_fields = ["-created_at"]
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(patient=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(patient=self.request.user)

        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)
