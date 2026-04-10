from django.shortcuts import render
from django.contrib.auth import get_user_model, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from userApp.serializers import OtpSerializer, UpdateUserSerializer, UserSerializer, getOtpSerializer
from userApp.models import Otp
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import ensure_csrf_cookie


User =  get_user_model()

# Create your views here.

@api_view(['PUT'])
@permission_classes([AllowAny])
def verify_otp(request):
    serializer = OtpSerializer(data=request.data)
    userId = request.session.get("otp_user_id")
    # print("User ID from session:", userId)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    code = serializer.validated_data['code']
    try:
        otp = Otp.objects.get(user_id=userId, code=code, status=True)
    except Otp.DoesNotExist:
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    
    if otp.expires_at < timezone.now():
        return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
    
    login(request, otp.user, backend='registrationApp.auth_backend.AuthenticationBackend')

    refresh = RefreshToken.for_user(otp.user)

    response = Response({"message": "Login successful"})

    response.set_cookie(
        "access_token",
        str(refresh.access_token),
        httponly=True,
        secure=True,
        samesite="Lax"
    )

    response.set_cookie(
        "refresh_token",
        str(refresh),
        httponly=True,
        secure=True,
        samesite="Lax"
    )

    otp.status = False
    otp.code = None
    otp.save()

    request.session.pop("otp_user_id", None)

    return response

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def get_user_details(request):

    if request.method == 'GET':
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        user = request.user

        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    if request.user.role != "staff" and request.user.role != "admin":
        return Response({"error": "Forbidden Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def view_user(request, user_id):
    if request.user.role != "staff" and request.user.role != "admin":
        return Response({"error": "Forbidden Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        serializer = UpdateUserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def getOtp(request):
    otp = Otp.objects.all()
    serializer = getOtpSerializer(otp, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)