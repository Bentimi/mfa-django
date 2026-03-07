from django.urls import path
from registrationApp import views as reg

urlpatterns = [
    path('register/', reg.register_User, name='register'),
    path('login/', reg.login_user, name='login'),
    path('logout/', reg.logout_user, name='logout'),
]