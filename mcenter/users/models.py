from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    class RoleChoise(models.TextChoices):
        DOCTOR = "doctor", "Доктор"
        PATIENT = "patient", "Пользователь"

    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=150)
    surname = models.CharField(max_length=255, null=False, blank=True)
    image = models.ImageField(upload_to="users_images/", blank=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoise.choices,
        default=RoleChoise.PATIENT,
        verbose_name="Роль",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
