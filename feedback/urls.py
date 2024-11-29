from django.urls import path
from . import views

urlpatterns = [
    path('<int:quiz_id>/feedbacks/<int:participant_id>/', views.view_feedbacks, name='view_feedbacks'),  
    # URL pattern for viewing all feedback for a specific quiz and participant

    path('<int:quiz_id>/feedbacks/submit/<int:participant_id>/', views.submit_feedback, name='submit_feedback'),
    # URL pattern for submitting feedback for a specific quiz and participant
]
