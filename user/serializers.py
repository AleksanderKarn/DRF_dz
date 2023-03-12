from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'country',
            'first_name',
            'last_name',

        )

    def validate_password(self, value: str) -> str:
        return make_password(value)
