"""
URL configuration for Quiz_Portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Examples:

Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')

Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('', include('core.urls')),  # Routes homepage to the core app
    path('blog/', include('blog.urls')),  # Routes '/blog/' to the blog app
    path('quiz/', include('quiz.urls')), 
    path('accounts/', include('allauth.urls')), 
    path('profile/', include('User_Profile.urls')), #User Profile App
    path('participation/', include('participation.urls')),
    path('leaderboard/', include('leaderboard.urls')), #for leaderboard
    path('feedback/',include('feedback.urls')),
    path('chatbox/',include('chatbox.urls')),

]
