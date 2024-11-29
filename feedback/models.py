from django.db import models
from quiz.models import Quiz, Participant
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta

# Feedback model for storing quiz feedback from participants
class Feedback(models.Model):
    # ForeignKey linking feedback to a specific quiz, cascades on deletion
    quiz = models.ForeignKey(
        'quiz.Quiz', on_delete=models.CASCADE, related_name="feedbacks",
        help_text="The quiz this feedback is related to."
    )

     # ForeignKey linking feedback to a specific participant, cascades on deletion
    participant = models.ForeignKey(
        'quiz.Participant', on_delete=models.CASCADE, related_name="feedbacks",
        help_text="The participant providing feedback."
    )

    comment = models.TextField(help_text="Your feedback on the quiz.") # TextField to store the main feedback comment from the participant
    content = models.TextField(help_text="Additional content or feedback details.", blank=True, null=True) # Optional TextField for additional feedback details
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'participant')  # Ensure one feedback per participant per quiz.
        ordering = ['-created_at']  # Show the most recent feedback first.

    def __str__(self):
        return f"Feedback by {self.participant.user.username} on {self.quiz.title}" #Returns a string identifying the participant and quiz title.
    
    def is_recent(self):
        """Check if the feedback is recent (within the last 7 days)."""
        return now() - self.created_at <= timedelta(days=7)

