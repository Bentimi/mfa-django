from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Otp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    status = models.BooleanField(default=True)