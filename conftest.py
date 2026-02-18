import pytest
from rest_framework.test import APIClient
from users.models import User
from appointment.models import Clinic, Doctor

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        username="admin", 
        email="admin@medcenter.com", 
        password="strongpassword123",
        phone="+38012479729358"
    )

@pytest.fixture
def regular_user():
    return User.objects.create_user(
        username="johndoe", 
        email="john@example.com", 
        password="password123",
        phone="+38023475929"
    )

@pytest.fixture
def clinic():
    return Clinic.objects.create(
        name="Центральная Клиника", 
        legal_address="ул. Мира, 1", 
        physical_address="ул. Мира, 1"
    )