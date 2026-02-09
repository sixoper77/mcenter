from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)

    class Meta:
        model = Users
        fields = [
            "username",
            "first_name",
            "last_name",
            "surname",
            "password",
            "surname",
        ]
        
