"""
Custom adapter for handling social account authentication via Django Allauth.

"""
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib import messages

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """

    This class is used to customize the user creation process when logging in via social accounts (e.g., GitHub, Google).
    """

    def save_user(self, request, sociallogin, form=None):
        """
        Saves the user information to the custom User model after social authentication.

        This method is called during the process of creating or updating a user
        after a successful social login. It updates the user’s email, username,
        and verification status based on the information provided by the social
        login provider (e.g., GitHub, Google).

        :param request: The HTTP request object, which can be used to get request-specific data.
        :type request: HttpRequest

        :param sociallogin: The social login object, which contains details of the authenticated user
                             from the social provider (e.g., email, username).
        :type sociallogin: SocialLogin

        :param form: An optional form passed during signup (default is None).
        :type form: Form, optional

        :return: The user object after saving the information.
        :rtype: User
        """
        user = super().save_user(request, sociallogin, form)  # Call the parent method to create the user
        data = sociallogin.account.extra_data  # Get the extra data from the social login provider

        # Check if email exists in the social login data
        email = data.get('email')

        if email:
            # Update user details if email exists
            user.email = email
            user.username = data.get('login', '')  # GitHub uses 'login' for username, Google may use 'name' or 'given_name'
            user.is_verified = True  # Mark as verified since the user authenticated via social login
            user.save()  # Save the updated user information
            return user

