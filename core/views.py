from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .utils import send_email_token
import uuid

def homepage(req):
    return render(req, 'core/homepage.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request,'core/dashboard.html')

User = get_user_model()  # Custom User model

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse('Passwords do not match!')

        if User.objects.filter(email=email).exists():
            return HttpResponse('Email is already in use!')

        if User.objects.filter(username=uname).exists():
            return HttpResponse('Username is already taken!')
        print(email," ",pass1)
        # Create user and send verification email
        token = str(uuid.uuid4())
        user_obj = User.objects.create_user(
            username=uname,
            email=email,
            password=pass1,
            email_token=token,
            is_verified = False
        )
        send_email_token(email, token)

        return HttpResponse('A verification email has been sent to your email address.')
    return render(request, 'core/signup.html')


def verify(request, token):
    try:
        user_obj = User.objects.get(email_token=token)
        if user_obj.is_verified:
            return HttpResponse('Your account is already verified!')

        user_obj.is_verified = True
        user_obj.save()
        return redirect('quiz_home')
    except User.DoesNotExist:
        return HttpResponse('Invalid verification token!')
    

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('password')
        user=authenticate(request,username=email,password = passw)
        print(passw)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            return HttpResponse("Username or Password is incorrect!!!")
        
    return render(request,'core/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')