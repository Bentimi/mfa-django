from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class OtpSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=6)

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