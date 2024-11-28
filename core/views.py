"""
This module defines the views for the core application.

The views include user authentication, signup, login, logout, and email verification functionality.
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utils import send_email_token
import uuid
from django.contrib import messages

def homepage(req):
    """
    Render the homepage of the application.

    :param req: The HTTP request object.
    :type req: HttpRequest
    :return: A rendered homepage HTML page.
    :rtype: HttpResponse
    """
    return render(req, 'core/homepage.html')


User = get_user_model()  # Custom User model

def signup(request):
    """
    Handle user signup and send a verification email.

    This function checks if the provided user details are valid, creates a new user if valid, and sends
    an email with a verification link.

    :param request: The HTTP request object containing signup details.
    :type request: HttpRequest
    :return: A rendered signup page or a redirect to the login page.
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return render(request, 'core/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'core/signup.html')

        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken")
            return render(request, 'core/signup.html')

        # Create user and send verification email
        token = str(uuid.uuid4())
        user_obj = User.objects.create_user(
            username=uname,
            email=email,
            password=pass1,
            email_token=token,
            is_verified=False
        )
        send_email_token(email, token)

        messages.success(request, "A verification link has been sent to your email")
        return redirect('login')

    return render(request, 'core/signup.html')


def verify(request, token):
    """
    Verify the user's email using the provided token.

    This function marks a user's account as verified if the token is valid and unverified.
    Otherwise, it redirects to appropriate pages based on the token's validity.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param token: The email verification token.
    :type token: str
    :return: A redirect to the quiz home or login page.
    :rtype: HttpResponse
    """
    try:
        user_obj = User.objects.get(email_token=token)
        if user_obj.is_verified:
            messages.error(request, "Your email account is already verified")
            return redirect('quiz_home')

        user_obj.is_verified = True
        user_obj.save()
        return redirect('quiz_home')
    except User.DoesNotExist:
        messages.error(request, "Invalid verification token")
        return redirect('login')


def user_login(request):
    """
    Handle user login.

    This function authenticates the user based on email and password and redirects them to
    the quiz home page if successful. If authentication fails, it displays an error message.

    :param request: The HTTP request object containing login details.
    :type request: HttpRequest
    :return: A rendered login page or a redirect to the quiz home page.
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('password')
        user = authenticate(request, username=email, password=passw)
        print(passw)
        if user is not None:
            login(request, user)
            return redirect('quiz_home')
        else:
            messages.error(request, "Username or password is incorrect")
            return render(request, 'core/login.html')

    return render(request, 'core/login.html')


def user_logout(request):
    """
    Handle user logout.

    This function logs out the current user and redirects them to the login page.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: A redirect to the login page.
    :rtype: HttpResponse
    """
    logout(request)
    return redirect('login')
