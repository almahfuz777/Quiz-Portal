from django.db import models
from quiz.models import Quiz, Participant
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta

class Feedback(models.Model):
    quiz = models.ForeignKey(
        'quiz.Quiz', on_delete=models.CASCADE, related_name="feedbacks",
        help_text="The quiz this feedback is related to."
    )
    participant = models.ForeignKey(
        'quiz.Participant', on_delete=models.CASCADE, related_name="feedbacks",
        help_text="The participant providing feedback."
    )
    comment = models.TextField(help_text="Your feedback on the quiz.")
    content = models.TextField(help_text="Additional content or feedback details.", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'participant')  # Ensure one feedback per participant per quiz.
        ordering = ['-created_at']  # Show the most recent feedback first.

    def __str__(self):
        return f"Feedback by {self.participant.user.username} on {self.quiz.title}"

    def is_recent(self):
        """Check if the feedback is recent (within the last 7 days)."""
        return now() - self.created_at <= timedelta(days=7)

