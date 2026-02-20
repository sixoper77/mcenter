from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
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
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "surname",
            "image",
            "password",
            "password_confirmed",
            "email",
            "phone",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirmed"]:
            raise ValidationError("Password must mutch the confirmed password")
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirmed")
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
    )
    email = serializers.EmailField()

    def validate(self, attrs):
        password = attrs.get("password")
        email = attrs.get("email")
        if password and email:
            user = authenticate(
                request=self.context.get("request"),
                password=password,
                username=email,
            )

            if not user:
                raise ValidationError("User not found")
            if not user.is_active:
                raise ValidationError("User account is disabled")

            attrs["user"] = user
            return attrs
        raise ValidationError("Must include email and password")
