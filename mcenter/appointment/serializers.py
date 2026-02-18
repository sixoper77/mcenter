from django.db import transaction
from rest_framework import serializers

from .models import Clinic, Doctor
from users.models import User


class ClinicSerializer(serializers.ModelSerializer):
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
        clinic = validated_data.pop('clinic',[])
        with transaction.atomic():
            new_doctor = Doctor.objects.create(**validated_data)
            new_doctor.clinic.set(clinic)
            doctor = new_doctor.doctor
            doctor.role = User.RoleChoices.DOCTOR
            doctor.save()
            return new_doctor
