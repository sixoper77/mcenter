from rest_framework.permissions import BasePermission

from users.models import User


class IsPatient(BasePermission):
    message = "Doctor can't make an appointment."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.RoleChoices.PATIENT
        )


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == User.RoleChoices.DOCTOR
        )
