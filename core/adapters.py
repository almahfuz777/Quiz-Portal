from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """Save user info to the custom User model."""
        user = super().save_user(request, sociallogin, form)
        data = sociallogin.account.extra_data

        # Check if email exists in the social login data
        email = data.get('email')

        # If email is found, update the user and save the information
        if email:
            user.email = email
            user.username = data.get('login', '')  # GitHub uses 'login' for username, Google uses 'name' or 'given_name'
            user.is_verified = True  # Mark as verified since the user authenticated via social login
            user.save()
            return user

        # # If no email is found, show an error message and redirect to profile to update email
        # else:
        #     messages.error(request, "Your account does not have a public email address. Please provide one.")
        #     return redirect('login')  # Redirect the user to their profile to update email
