from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:quiz_id>/participate/', views.participate, name='participate'),
    path('<uuid:quiz_id>/quiz_info/', views.quiz_info, name='quiz_info'),  # Quiz info URL
    
]
