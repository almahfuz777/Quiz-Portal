from django.db import models
from django.contrib.auth import get_user_model
from participation.models import Participant
from quiz.models import Quiz
import uuid

User = get_user_model()

class Feedback(models.Model):
    """
    Represents feedback submitted by a participant for a quiz.

    Attributes:
        participant (ForeignKey): The participant who provided the feedback, linked to the Participant model.
        quiz (ForeignKey): The quiz for which the feedback is submitted, linked to the Quiz model.
        comment (TextField): The main feedback comment from the participant.
        content (TextField, optional): Additional feedback content, can be left empty.
        created_at (DateTimeField): The timestamp when the feedback was created, set automatically.
    """
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="feedbacks")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="feedbacks")
    comment = models.TextField()
    content = models.TextField(blank=True, null=True)  # Optional additional feedback content
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        """
        Returns a string representation of the Feedback object, 
        showing the participant's email and the quiz title.
        """
        return f"Feedback by {self.participant.email} for {self.quiz.title}"