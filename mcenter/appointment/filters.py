import django_filters
from .models import Appointment


class AppointmentFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name="created_at__date")

    class Meta:
        model = Appointment
        fields = {
            "status": ["exact"],
        }
