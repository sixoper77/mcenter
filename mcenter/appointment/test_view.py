import pytest
from datetime import timedelta
from users.models import User

from .models import Clinic, Doctor,Appointment


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
        response = api_client.post("/appointment/doctor/", payload)
        assert response.status_code == 201
        assert Doctor.objects.filter(doctor=regular_user, clinic=clinic).exists()
        regular_user.refresh_from_db()
        assert regular_user.role == User.RoleChoices.DOCTOR

    def test_create_doctor_unauthorized(self, api_client):
        payload = {"doctor": 1, "clinic": 1, "specialization": "Хирург"}
        response = api_client.post("/appointment/doctor/", payload)

        assert response.status_code == 403


@pytest.mark.django_db
class TestAppointmentAPI:
    url = "/appointment/appointment/"

    def get_data(self, response):
        if isinstance(response.data, dict) and 'results' in response.data:
            return response.data['results']
        return response.data

    def test_create_appointment_assigns_patient_automatically(self, api_client, regular_user, doctor, clinic):
        api_client.force_authenticate(user=regular_user)
        
        payload = {
            "doctor": doctor.id,
            "clinic": clinic.id,
            "timestamp": {
                "lower": "2026-03-01 15:00:00",
                "upper": "2026-03-01 15:30:00"
            }
        }
        
        response = api_client.post(self.url, payload, format="json")
        
        assert response.status_code == 201
        assert Appointment.objects.count() == 1
        
        created_appointment = Appointment.objects.first()
        assert created_appointment.patient == regular_user

    def test_user_sees_only_own_appointments(self, api_client, regular_user, appointment):
        other_user = User.objects.create_user(username="spy", password="123")
        
        api_client.force_authenticate(user=other_user)
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert len(self.get_data(response)) == 0

        api_client.force_authenticate(user=regular_user)
        response = api_client.get(self.url)
        assert len(self.get_data(response)) == 1
        assert self.get_data(response)[0]['id'] == appointment.id

    def test_search_by_doctor_first_name(self, api_client, regular_user, appointment):
        api_client.force_authenticate(user=regular_user)
        
        response = api_client.get(f"{self.url}?search=Иван")
        assert response.status_code == 200
        assert len(self.get_data(response)) == 1
        
        response = api_client.get(f"{self.url}?search=Петр")
        assert len(self.get_data(response)) == 0

    def test_filter_by_status(self, api_client, regular_user, appointment):
        api_client.force_authenticate(user=regular_user)
        
        response = api_client.get(f"{self.url}?status=awaiting")
        assert response.status_code == 200
        assert len(self.get_data(response)) == 1
        
        response = api_client.get(f"{self.url}?status=paid")
        assert len(self.get_data(response)) == 0
        
    def test_double_booking_prevention(self, api_client, regular_user, doctor, clinic, appointment):
        another_user = User.objects.create_user(username="nagliy_tip", password="123")
        api_client.force_authenticate(user=another_user)
        
        start_time = appointment.timestamp.lower
        
        payload = {
            "doctor": doctor.id,
            "clinic": clinic.id,
            "timestamp": {
                "lower": start_time.isoformat(),
                "upper": (start_time + timedelta(minutes=15)).isoformat()
            }
        }
        
        response = api_client.post(self.url, payload, format="json")
        
        assert response.status_code == 400
        assert Appointment.objects.count() == 1
        
        
    def test_queryset_patient_sees_own(self, api_client, regular_user, appointment):
        api_client.force_authenticate(user=regular_user)
        response = api_client.get(self.url)
        assert response.status_code == 200
        data = self.get_data(response)
        assert len(data) == 1
        assert data[0]["id"] == appointment.id

    def test_queryset_doctor_sees_own(self, api_client, doctor, appointment):
        api_client.force_authenticate(user=doctor.doctor)
        response = api_client.get(self.url)
        assert response.status_code == 200
        data = self.get_data(response)
        assert len(data) == 1
        assert data[0]["id"] == appointment.id

    def test_queryset_admin_sees_all(self, api_client, admin_user, appointment):
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(self.url)
        assert response.status_code == 200
        assert len(self.get_data(response)) == 1

    def test_patient_can_create_appointment(self, api_client, regular_user, doctor, clinic):
        api_client.force_authenticate(user=regular_user)
        payload = {
            "doctor": doctor.id,
            "clinic": clinic.id,
            "timestamp": {
                "lower": "2026-05-01T10:00:00Z",
                "upper": "2026-05-01T10:30:00Z"
            }
        }
        response = api_client.post(self.url, payload, format="json")
        assert response.status_code == 201

    def test_patient_cannot_patch_appointment(self, api_client, regular_user, appointment):
        api_client.force_authenticate(user=regular_user)
        response = api_client.patch(f"{self.url}{appointment.id}/", {"status": "paid"})
        assert response.status_code == 403

    def test_doctor_cannot_create_appointment(self, api_client, doctor, clinic):
        api_client.force_authenticate(user=doctor.doctor)
        payload = {
            "doctor": doctor.id,
            "clinic": clinic.id,
            "timestamp": {
                "lower": "2026-05-02T10:00:00Z",
                "upper": "2026-05-02T10:30:00Z"
            }
        }
        response = api_client.post(self.url, payload, format="json")
        assert response.status_code == 403

    def test_doctor_can_patch_appointment(self, api_client, doctor, appointment):
        api_client.force_authenticate(user=doctor.doctor)
        response = api_client.patch(f"{self.url}{appointment.id}/", {"status": "paid"})
        assert response.status_code == 200

    def test_admin_can_create_and_patch_appointment(self, api_client, admin_user, doctor, clinic, appointment):
        api_client.force_authenticate(user=admin_user)
        
        payload = {
            "doctor": doctor.id,
            "clinic": clinic.id,
            "timestamp": {
                "lower": "2026-05-03T10:00:00Z",
                "upper": "2026-05-03T10:30:00Z"
            }
        }
        res_post = api_client.post(self.url, payload, format="json")
        assert res_post.status_code == 201

        res_patch = api_client.patch(f"{self.url}{appointment.id}/", {"status": "completed"})
        assert res_patch.status_code == 200