from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:quiz_id>/submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('my-feedback/', views.my_feedback, name='my_feedback'),
    path('<uuid:quiz_id>/feedbacks/', views.view_feedback, name='view_feedback'),
]
