"""
URL configuration for the quiz app.

This module defines the URL patterns for the quiz application. It maps URLs to their corresponding views 
to handle quiz-related operations such as displaying quizzes, creating new quizzes, and setting quiz questions.

Each URL is associated with a specific view that handles the HTTP request and generates the appropriate response.

URLs:
- `/`: Displays the homepage with a list of quizzes (via `quiz_home` view).
- `/create_quiz/`: Allows the creation of a new quiz (via `create_quiz` view).
- `/set_questions/<uuid:quiz_id>/`: Used to set the questions for a specific quiz (via `set_questions` view).
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.quiz_home, name='quiz_home'),
    path('create_quiz/',views.create_quiz,name='create_quiz'),
    path('set_questions/<uuid:quiz_id>/', views.set_questions, name='set_questions'),
]
