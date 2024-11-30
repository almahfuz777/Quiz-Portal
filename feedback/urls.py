"""
URL patterns for handling feedback submission and viewing in the Quiz Portal.
"""
from django.urls import path
from . import views
urlpatterns = [
    path('<str:quiz_id>/feedbacks/submit/<int:participant_id>/', views.submit_feedback, name='submit_feedback'),
    path('<str:quiz_id>/feedbacks/<int:participant_id>/', views.view_feedbacks, name='view_feedbacks'),
]
