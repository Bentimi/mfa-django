from django.urls import path
from registrationApp import views as reg

urlpatterns = [
    path('login/', reg.login_user, name='login'),
]