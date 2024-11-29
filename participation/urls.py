from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:quiz_id>/participate/', views.participate, name='participate'),
]
