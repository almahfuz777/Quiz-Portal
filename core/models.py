from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    email_token = models.CharField(max_length=200, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    # django default change:
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']