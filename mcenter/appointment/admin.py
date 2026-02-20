from django.contrib import admin

from .models import Appointment, Clinic, Doctor


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "legal_address",
        "physical_address",
    ]
    search_fields = [
        "^name",
    ]
    list_filter = [
        "name",
    ]
    ordering = ("-id",)
    save_on_top = True


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = [
        "doctor",
        "specialization",
        "get_clinics",
    ]
    search_fields = [
        "doctor__username",
        "^specialization",
        "clinic__name",
    ]
    list_filter = [
        "specialization",
        "clinic",
    ]
    ordering = ("-id",)
    save_on_top = True

    @admin.display(description="Клинники")
    def get_clinics(self, obj):
        return ", ".join([clinic.name for clinic in obj.clinic.all()])


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        "doctor",
        "patient",
        "clinic",
        "status",
        "timestamp",
    ]
    search_fields = [
        "doctor__doctor__username",
        "patient__username",
        "clinic__name",
        "status",
    ]
    list_filter = [
        "doctor",
        "clinic",
        "status",
        "created_at",
    ]
    ordering = ("-id",)
    save_on_top = True
