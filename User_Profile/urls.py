from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_home, name='profile_home'),
    path('user-stats/', views.user_stats, name='user_stats'),
    path('user-info/', views.user_info, name='user_info'),
    path('settings/', views.settings, name='settings'),
]