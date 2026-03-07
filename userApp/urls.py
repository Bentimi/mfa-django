from django.urls import path
from userApp import views as user 

urlpatterns = [
    path('verify-otp/', user.verify_otp, name='verify_otp'),
    path('me/', user.get_user_details, name='user_details'),
]