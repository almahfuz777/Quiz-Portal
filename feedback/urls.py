from django.urls import path
from . import views

urlpatterns = [
    path('<int:quiz_id>/feedbacks/<int:participant_id>/', views.view_feedbacks, name='view_feedbacks'),
    path('<int:quiz_id>/feedbacks/submit/<int:participant_id>/', views.submit_feedback, name='submit_feedback'),
]
