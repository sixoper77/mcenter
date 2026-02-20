import pytest
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from users.models import User
from appointment.models import Clinic, Doctor,Appointment

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
    
    
    
@pytest.fixture
def doctor(db, clinic):
    doc_user = User.objects.create_user(
        username="dr_ivanov", 
        first_name="Иван", 
        last_name="Иванов",
        password="simplePass126",
        email="ivanov1234@gmail.com",
        phone="+38023475928",
        role=User.RoleChoices.DOCTOR
    )
    doc = Doctor.objects.create(doctor=doc_user, specialization="Хирург")
    doc.clinic.add(clinic)
    return doc

@pytest.fixture
def appointment(db, regular_user, doctor, clinic):
    now = timezone.now()
    return Appointment.objects.create(
        patient=regular_user,
        doctor=doctor,
        clinic=clinic,
        timestamp=(now, now + timedelta(minutes=30)),
        status="awaiting"
    )