from django.db import transaction
from rest_framework import serializers
from users.models import Users
from users.serializers import UserSerializer

from appointment.models import Clinic, Doctor


class ClinickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ("name", "legal_address", "physical_address")

    def create(self, validated_data):
        return Clinic.objects.create(**validated_data)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ("doctor", "clinic", "specialization")

    def create(self, validated_data):
        with transaction.atomic():
            new_doctor = Doctor.objects.create(**validated_data)
            doctor = new_doctor.doctor
            doctor.role = Users.RoleChoise.DOCTOR
            doctor.save()
            return new_doctor
