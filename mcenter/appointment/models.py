from django.conf import settings
from django.db import models
from django.db.models import F, Q


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
        indexes = [models.Index(fields=["doctor","specialization"])]

    def __str__(self):
        return f"{self.doctor.get_full_name()} {self.specialization}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Подтверджена"
        PAID = "paid", "Оплачен"
        STARTED = "started", "Начата"
        AWAITS = "awaiting", "Ожидается"
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
    status = models.CharField(choices=Status.choices, default=Status.AWAITS)
    started_at = models.DateTimeField(verbose_name="Начало приема")
    ended_at = models.DateTimeField(null=True, blank=True, verbose_name="Конец приема")

    class Meta:
        indexes = [models.Index(fields=["doctor", "created_at", "status"])]
        constraints = [
            models.CheckConstraint(
                condition=Q(ended_at__gt=F("started_at")),
                name="ended_time_gt_started_time",
            ),
            models.UniqueConstraint(
                name="unique_doctor_started_at_time",
                fields=["doctor", "started_at"],
            ),
        ]

    def __str__(self):
        return f"{self.patient} {self.doctor} {self.started_at}"
