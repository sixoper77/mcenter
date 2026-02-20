import pytest
from users.models import User

@pytest.mark.django_db
class TestUserAuthAPI:
    register_url = "/users/api/registration/"
    login_url = "/users/api/login/"

    def test_user_registration_success(self, api_client):
        payload = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "Password123!",
            "password_confirmed": "Password123!",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "surname": "Ivanovich",
            "phone": "+380991234567"
        }
        response = api_client.post(self.register_url, payload, format="json")
        assert response.status_code == 201
        assert User.objects.filter(email="new@example.com").exists()

    def test_user_registration_password_mismatch(self, api_client):
        payload = {
            "username": "baduser",
            "email": "bad@example.com",
            "password": "Password123!",
            "password_confirmed": "WrongPassword!",
            "first_name": "Ivan",
            "last_name": "Ivanov",
            "surname": "Ivanovich",
            "phone": "+380997654321"
        }
        response = api_client.post(self.register_url, payload, format="json")
        assert response.status_code == 400
        assert not User.objects.filter(email="bad@example.com").exists()

    def test_user_login_success(self, api_client, regular_user):
        payload = {
            "email": regular_user.email,
            "password": "password123"
        }
        response = api_client.post(self.login_url, payload, format="json")
        assert response.status_code == 200

    def test_user_login_invalid_credentials(self, api_client, regular_user):
        payload = {
            "email": regular_user.email,
            "password": "WrongPassword123!"
        }
        response = api_client.post(self.login_url, payload, format="json")
        assert response.status_code == 400