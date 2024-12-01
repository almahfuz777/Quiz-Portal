from django.db import models
from django.contrib.auth import get_user_model
from participation.models import Participant
from quiz.models import Quiz
import uuid

User = get_user_model()

class Feedback(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="feedbacks")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="feedbacks")
    comment = models.TextField()
    content = models.TextField(blank=True, null=True)  # Optional additional feedback content
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.participant.email} for {self.quiz.title}"
