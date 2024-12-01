from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbox_home, name='chatbox_home'),  # Maps the home page of the chatbox
]
