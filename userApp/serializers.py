from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Otp

User = get_user_model()


class OtpSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=6, trim_whitespace=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = '__all__'
        exclude = ['is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups']

        extra_kwargs = {
            'password': {'write_only': True},
        }

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'username']


class getOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = '__all__'