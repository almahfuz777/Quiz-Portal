from django.contrib.auth.models import AbstractUser
from django.db import models
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

class User(AbstractUser):
    email = models.EmailField(unique=True)
    email_token = models.CharField(unique=True, max_length=200, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    
    # django default change:
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    created_quizzes = models.ManyToManyField(
        'quiz.Quiz', related_name='quiz_authors', blank=True
    )
    
    def __str__(self):
        return self.email
    
