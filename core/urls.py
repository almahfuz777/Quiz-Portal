from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for the homepage view
    path('', views.homepage, name='homepage'),  
    # The homepage view that renders the landing page of the application.
    # - URL: '/'
    # - View: views.homepage
    # - Name: 'homepage'

    # URL pattern for the signup view
    path('signup/', views.signup, name='signup'), 
    # The signup view that handles user registration.
    # - URL: '/signup/'
    # - View: views.signup
    # - Name: 'signup'

    # URL pattern for the email verification view
    path('verify/<uuid:token>/', views.verify, name='verify'),
    # The verification view that verifies the user's email using a unique token.
    # - URL: '/verify/<token>'
    # - View: views.verify
    # - Name: 'verify'
    # - The <uuid:token> is a dynamic URL parameter that represents a unique verification token.

    # URL pattern for the login view
    path('login/', views.user_login, name='login'),
    # The login view that authenticates users with their email and password.
    # - URL: '/login/'
    # - View: views.user_login
    # - Name: 'login'

    # URL pattern for the logout view
    path('logout/', views.user_logout, name='logout')
    # The logout view that logs the user out of the application.
    # - URL: '/logout/'
    # - View: views.user_logout
    # - Name: 'logout'
]
