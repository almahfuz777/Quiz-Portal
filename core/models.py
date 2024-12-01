from django.contrib.auth.models import AbstractUser
from django.db import models
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser model to support email-based authentication, email verification, and social login integration.

    Attributes:
        email (EmailField): The user's email address, which must be unique.
        email_token (CharField): A token used for email verification, unique for each user.
        is_verified (BooleanField): A flag to indicate if the user's email has been verified.
        created_quizzes (ManyToManyField): A many-to-many relationship with the Quiz model, indicating which quizzes the user has created.

    Methods:
        __str__: Returns the user's email as the string representation of the user.
    """

    # Email field to be used for authentication
    email = models.EmailField(unique=True)
    
    # Token used for email verification
    email_token = models.CharField(unique=True, max_length=200, null=True, blank=True)
    
    # Boolean to mark if the user's email has been verified
    is_verified = models.BooleanField(default=False)
    
    # Override the default USERNAME_FIELD to use email instead of username
    USERNAME_FIELD = 'email'
    
    # Specify the fields that are required to create a superuser
    REQUIRED_FIELDS = ['username']


    
    
    def __str__(self):
        """
        Returns the string representation of the User model, which is the user's email address.

        Returns:
            str: The email address of the user.
        """
        return self.email
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
