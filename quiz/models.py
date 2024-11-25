from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from django.contrib.auth.models import User

class Quiz(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    
    QUIZ_TYPE_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]
    
    TAG_CHOICES = [
        ('math', 'Math'),
        ('science', 'Science'),
        ('history', 'History'),
        ('geography', 'Geography'),
        ('programming', 'Programming'),
        ('literature', 'Literature'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    quiz_type = models.CharField(
        max_length=10, choices=QUIZ_TYPE_CHOICES, default=PUBLIC
    )
    password = models.CharField(max_length=50, blank=True, null=True)
    duration = models.DurationField(help_text="Duration in HH:MM:SS format")
    expiry_date = models.DateTimeField(help_text="Quiz expiration date and time")
    can_view_score_immediately = models.BooleanField(default=False)
    tags = models.CharField(
        max_length=50, choices=TAG_CHOICES, blank=True, null=True, help_text="Select a tag"
    )    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_quizzes", null=True)

    def save(self, *args, **kwargs):
        # Hash password if it's private
        if self.quiz_type == 'private' and self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Check hashed password
        
    def is_active(self):
        """Check if the quiz is active (not expired)."""
        return now() < self.expiry_date
    
    def __str__(self):
        return self.title

    def stats(self):
        """Calculate stats for the quiz."""
        participants = self.participants.all()
        if not participants:
            return {
                "total_participants": 0,
                "highest_score": 0,
                "average_score": 0
            }
        
        scores = [participant.score for participant in participants]
        
        return {
            "total_participants": len(scores),
            "highest_score": max(scores),
            "average_score": sum(scores) / len(scores),
        }


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_no = models.PositiveIntegerField(default=1, null=True, blank=True)  # Allow null values for existing rows
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(
        max_length=1,
        choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')],
        help_text="Correct option (A/B/C/D)",
    )

    def get_correct_option(self):
        """Returns the correct option text."""
        return getattr(self, f"option_{self.correct_option.lower()}")

    def __str__(self):
        return f"Q{self.question_no}: {self.text}"



class Participant(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participations"
    )
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="participants"
    )
    score = models.IntegerField(default=0)
    participated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title}"