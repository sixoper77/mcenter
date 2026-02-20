from django.core.exceptions import ValidationError as DjangoValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.exceptions import ValidationError as DRFValidationError

from users.models import User

from .filters import AppointmentFilter
from .models import Appointment
from .permissions import IsDoctor, IsPatient
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
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser,
        IsPatient,
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == User.RoleChoices.DOCTOR:
            return queryset.filter(doctor__doctor=self.request.user)
        elif self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(patient=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(patient=self.request.user)
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [
                permissions.IsAuthenticated,
                IsPatient | permissions.IsAdminUser,
            ]
        elif self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = [
                permissions.IsAuthenticated,
                permissions.IsAdminUser | IsDoctor,
            ]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]
