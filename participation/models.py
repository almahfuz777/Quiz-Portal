from django.db import models

from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from quiz.models import Quiz, Question
import uuid

User = get_user_model()

class Participant(models.Model):
    participant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participations")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="participants")
    score = models.FloatField(default=0.0)
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"

    def calculate_score(self):
        """Calculates the score for the participant based on correct responses."""
        correct_responses = self.responses.filter(is_correct=True).count()  # Count the correct responses
        total_questions = self.quiz.questions.count()
        self.score = (correct_responses / total_questions) * 100  # Calculate score as percentage
        self.save()  # Save the score to the database


class Response(models.Model):
    response_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    selected_option = models.CharField(max_length=1, choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')])

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Response: {self.participant.user.username} - {self.question.text[:30]}"
