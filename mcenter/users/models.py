from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    surname = models.CharField(max_length=255, null=False, blank=True)
    image = models.ImageField(upload_to="users_images", blank=True)
