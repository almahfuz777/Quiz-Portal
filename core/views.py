from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model, authenticate, login,logout
from django.contrib.auth.decorators import login_required
from .utils import send_email_token
import uuid
from django.contrib import messages

def homepage(req):
    return render(req, 'core/homepage.html')

User = get_user_model()  # Custom User model

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request,"Password do not match")
            return render(request,'core/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exist")
            return render(request,'core/signup.html')
            

        if User.objects.filter(username=uname).exists():
            messages.error(request,"Username already taken")
            return render(request,'core/signup.html')
        
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

        messages.success(request,"A verification link has sent to your email")
        return redirect('login')

    return render(request, 'core/signup.html')


def verify(request, token):
    try:
        user_obj = User.objects.get(email_token=token)
        if user_obj.is_verified:
            messages.error(request, "You email account is already verified")
            return redirect('quiz_home')

        user_obj.is_verified = True
        user_obj.save()
        return redirect('quiz_home')
    except User.DoesNotExist:
        messages.error(request,"Invalid verification token")
        return redirect('login')
    

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        passw = request.POST.get('password')
        user=authenticate(request,username=email,password = passw)
        print(passw)
        if user is not None:
            login(request,user)
            return redirect('quiz_home')
        else:
          messages.error(request, "Username or password is incorrect")
          return render(request,'core/login.html')
        
    return render(request,'core/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')