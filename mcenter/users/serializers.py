from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Users


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = (
            "username",
            "first_name",
            "last_name",
            "surname",
            "image",
            "role",
        )

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class UserRegistrationsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirmed = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = (
            "username",
            "first_name",
            "last_name",
            "surname",
            "image",
            "password",
            "password_confirmed",
            "email",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirmed"]:
            raise ValidationError("Password must mutch the confirmed password")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirmed")
        return Users.objects.create_user(**validated_data)
