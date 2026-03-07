from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from userApp.models import Otp

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    extra_kwargs = {
         'username': {
             'error_messages': {
                 'required': 'Username is required.',
                 'blank': 'Username cannot be blank.',
                 'unique': 'This username is already taken.'
             }
         },
         'email': {
             'error_messages': {
                 'required': 'Email is required.',
                 'blank': 'Email cannot be blank.',
                 'unique': 'This email is already registered.'
             }
         },
     }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['username'],
            password=data['password']
        )

        if user is None:
            raise serializers.ValidationError("Invalid user credentials")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        
        data['user'] = user
        return data