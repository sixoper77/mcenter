from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        DOCTOR = "doctor", "Доктор"
        PATIENT = "patient", "Пользователь"

    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=150)
    surname = models.CharField(max_length=255, null=False, blank=True)
    image = models.ImageField(upload_to="users_images/", blank=True)
    role = models.CharField(
        max_length=20,
        choices=RoleChoices.choices,
        default=RoleChoices.PATIENT,
        verbose_name="Роль",
    )
    phone = PhoneNumberField(unique=True,default='+1')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
