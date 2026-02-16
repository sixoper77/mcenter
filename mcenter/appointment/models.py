from django.conf import settings
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, RangeOperators
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Clinic(models.Model):
    name = models.CharField(max_length=255, null=False, blank=True)
    legal_address = models.CharField(max_length=255, null=False, blank=True)
    physical_address = models.CharField(max_length=255, null=False, blank=True)

    class Meta:
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return f"{self.name} {self.legal_address} {self.physical_address}"


class Doctor(models.Model):
    doctor = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    specialization = models.CharField(max_length=255, null=False, blank=True)
    clinic = models.ManyToManyField(
        Clinic,
        related_name="doctors",
    )

    class Meta:
        indexes = [models.Index(fields=["doctor", "specialization"])]

    def __str__(self):
        return f"{self.doctor.get_full_name()} {self.specialization}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Подтверджена"
        PAID = "paid", "Оплачен"
        STARTED = "started", "Начата"
        AWAITING = "awaiting", "Ожидается"
        COMPLETED = "completed", "Завершена"

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Доктор",
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пациент",
        related_name="patient_appointments",
    )
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        verbose_name="Клиника",
        related_name="clinic_appointments",
    )
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    status = models.CharField(choices=Status.choices, default=Status.AWAITING)
    timestamp = DateTimeRangeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["doctor", "created_at", "status"])]
        constraints = [
            ExclusionConstraint(
                name="unique_timestamp_for_doctor_appointment",
                expressions=[
                    ("timestamp", RangeOperators.OVERLAPS),
                    ("doctor", RangeOperators.EQUAL),
                ],
                condition=Q(status__in=["paid", "awaiting", "confirmed", "started"]),
            ),
            ExclusionConstraint(
                name="unique_timestamp_for_patient",
                expressions=[
                    ("timestamp", RangeOperators.OVERLAPS),
                    ("patient", RangeOperators.EQUAL),
                ],
                condition=Q(status__in=["awaiting", "started", "paid", "confirmed"]),
            ),
        ]

    def __str__(self):
        start_time = (
            self.timestamp.lower.strftime("%Y-%m-%d %H:%M")
            if self.timestamp
            else "No time"
        )
        return f"{self.patient} {self.doctor} {start_time}"

    def clean(self):
        if self.doctor_id and self.patient_id:
            if self.doctor.doctor_id == self.patient_id:
                raise ValidationError("Доктор не может быть записан сам к себе")

        if self.clinic_id and self.doctor_id:
            if not self.doctor.clinic.filter(id=self.clinic_id).exists():
                raise ValidationError("Доктор не работает в этой клиннике")
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
