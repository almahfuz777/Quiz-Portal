from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_home, name='quiz_home'),
    path('create_quiz/',views.create_quiz,name='create_quiz'),
    path('set_questions/<int:quiz_id>/', views.set_questions, name='set_questions'),

    # path('participate/',views.participate,name='participate'),
]
