from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from registrationApp.serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth import get_user_model, login
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from userApp.models import Otp
import random
from django.utils import timezone
# from services.emails.welcome import send_otp_email
# from services.resend import send_email

User = get_user_model()

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_User(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        # login(request, user)

        otp_code = str(random.randint(100000, 999999))

        Otp.objects.update_or_create(
            user=user,
            defaults={
                'code': otp_code,
                'status': True,
                'expires_at': timezone.now() + timezone.timedelta(minutes=5)
            }
        )

        # send_otp_email(user, otp=otp_code)
        # send_email(user, otp=otp_code)

        # store user in session
        request.session["otp_user_id"] = user.id
        # session  = request.session['otp_user_id']
        # print("Session user id:", session)
        print(f"OTP for user {user.email}: {otp_code}")
        return Response({
            "message": "OTP sent to your email", "otp_code": otp_code
            }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    refresh_token = request.COOKIES.get("refresh_token")
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response