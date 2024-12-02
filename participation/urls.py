"""
URL patterns for the participation app.

These URLs handle the routes related to quiz participation and displaying quiz information.
Each path includes a UUID for identifying the specific quiz.

URL Patterns:
---------------
1. `<uuid:quiz_id>/participate/`:
    - View: `participate`
    - Purpose: Displays the participation page for a specific quiz, allowing users to answer quiz questions.

2. `<uuid:quiz_id>/quiz_info/`:
    - View: `quiz_info`
    - Purpose: Displays detailed information about a specific quiz, such as its description, duration, and quiz statistics.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:quiz_id>/participate/', views.participate, name='participate'),
    path('<uuid:quiz_id>/quiz_info/', views.quiz_info, name='quiz_info'),  # Quiz info URL
    
]
