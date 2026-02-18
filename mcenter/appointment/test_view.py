import pytest
from django.urls import reverse

from users.models import User

from .models import Clinic, Doctor


@pytest.mark.django_db
class TestClinicAPI:
    def test_create_clinic_as_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)

        payload = {
            "name": "Новая Клиника",
            "legal_address": "ул. Тестовая, 10",
            "physical_address": "ул. Тестовая, 10",
        }
        response = api_client.post("/appointment/clinic/", payload)

        assert response.status_code == 201
        assert Clinic.objects.filter(name="Новая Клиника").exists()

    def test_create_clinic_forbidden_for_regular_user(self, api_client, regular_user):
        api_client.force_authenticate(user=regular_user)
        payload = {
            "name": "Хакерская Клиника",
            "legal_address": "...",
            "physical_address": "...",
        }
        response = api_client.post("/appointment/clinic/", payload)
        assert response.status_code == 403
        assert not Clinic.objects.filter(name="Хакерская Клиника").exists()


@pytest.mark.django_db
class TestDoctorRoleChangeAPI:
    def test_create_doctor_successfully_changes_role(
        self, api_client, admin_user, regular_user, clinic
    ):
        api_client.force_authenticate(user=admin_user)
        payload = {
            "doctor": regular_user.id,
            "clinic": clinic.id,
            "specialization": "Терапевт",
        }
        response = api_client.post("/appointment/doctor/", payload)  # Укажи свой URL
        assert response.status_code == 201
        assert Doctor.objects.filter(doctor=regular_user, clinic=clinic).exists()
        regular_user.refresh_from_db()
        assert regular_user.role == User.RoleChoices.DOCTOR

    def test_create_doctor_unauthorized(self, api_client):
        payload = {"doctor": 1, "clinic": 1, "specialization": "Хирург"}
        response = api_client.post("/appointment/doctor/", payload)

        assert response.status_code == 403
