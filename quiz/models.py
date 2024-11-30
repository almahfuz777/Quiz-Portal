from django.db import models
from django.conf import settings
import uuid
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from django.contrib.auth.models import User
from core.models import Tag

class Quiz(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    
    QUIZ_TYPE_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]
    
    quiz_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_quizzes", null=True)
    tags = models.ManyToManyField(Tag, related_name='quizzes', blank=True)  # Many-to-Many relation with Tag
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    quiz_type = models.CharField(
        max_length=10, choices=QUIZ_TYPE_CHOICES, default=PUBLIC
    )
    password = models.CharField(max_length=50, blank=True, null=True)
    duration = models.DurationField(help_text="Duration in HH:MM:SS format")
    expiry_date = models.DateTimeField(help_text="Quiz expiration date and time", null=True, blank=True)
    can_view_score_immediately = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at'] # Order quizzes by creation date (latest first)
        
    def save(self, *args, **kwargs):
        # Hash password if it's private
        if self.quiz_type == 'private' and self.password and not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # Check hashed password
        
    def is_active(self):
        """Check if the quiz is active (not expired)."""
        if self.expiry_date is None:
            return True  # If no expiry date is set, the quiz is always active
        return now() < self.expiry_date
    
    def __str__(self):
        return self.title

class Question(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    class Meta:
        ordering = ['question_no']
    
    def get_correct_option(self):
        """Returns the correct option text."""
        return getattr(self, f"option_{self.correct_option.lower()}")

    def __str__(self):
        return f"Q{self.question_no}: {self.text}"

class QuizStats(models.Model):
    stats_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, related_name="stats")
    total_participants = models.IntegerField(default=0)
    highest_score = models.FloatField(null=True, blank=True)
    average_score = models.FloatField(null=True, blank=True)

    def update_stats(self, scores):
        """Update stats based on new scores."""
        if scores:
            self.total_participants = len(scores)
            self.highest_score = max(scores)
            self.average_score = sum(scores) / len(scores)
        else:
            self.highest_score = self.average_score = None
        self.save()

    def __str__(self):
        return f"Stats for {self.quiz.title}"
    