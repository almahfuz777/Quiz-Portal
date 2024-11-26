# core/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """Save user info to the custom User model."""
        user = super().save_user(request, sociallogin, form)
        data = sociallogin.account.extra_data

        # Update user fields with data from the provider
        user.email = data.get('email', '')  # Email from GitHub
        user.username = data.get('login', '')  # Username from GitHub
        user.is_verified = True  # Mark social-authenticated users as verified
        user.save()
        return user
