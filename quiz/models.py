from django.db import models
from django.conf import settings
import uuid
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from django.contrib.auth.models import User
from core.models import Tag

class Quiz(models.Model):
    """Represents a Quiz in the system.

    Attributes:
        quiz_id (UUID): Unique identifier for the quiz.
        created_by (User): The user who created the quiz.
        tags (Tag): Tags associated with the quiz.
        title (str): The title of the quiz.
        description (str, optional): A description of the quiz.
        quiz_type (str): Type of quiz, either 'public' or 'private'.
        password (str, optional): Password required to access the quiz if it's private.
        duration (timedelta): Duration of the quiz in HH:MM:SS format.
        expiry_date (datetime, optional): The expiry date and time of the quiz.
        can_view_score_immediately (bool): Whether users can view their score immediately after completing the quiz.
        created_at (datetime): Timestamp when the quiz was created.

    Methods:
        save: Overridden save method to hash the password for private quizzes.
        check_password: Checks the given raw password against the hashed password for private quizzes.
        is_active: Returns whether the quiz is active based on the expiry date.
        __str__: Returns the title of the quiz when represented as a string.
    """
    
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
        """
        Overrides the default save method to hash the password for private quizzes.

        If the quiz is private and a password is provided, the password is hashed
        before saving the model.

        Args:
            ``*args``: Variable length argument list.
            ``**kwargs``: Arbitrary keyword arguments.
        """
        # Hash password if it's private
        if self.quiz_type == 'private' and self.password and not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """
        Overrides the default save method to hash the password for private quizzes.

        If the quiz is private and a password is provided, the password is hashed
        before saving the model.

        Args:
            ``*args``: Variable length argument list.
            ``**kwargs``: Arbitrary keyword arguments.
        """     
        return check_password(raw_password, self.password)  # Check hashed password
        
    def is_active(self):
        """Check if the quiz is active (not expired).
        
        Returns:
            bool: True if the quiz is active, False if expired. 
        """
        if self.expiry_date is None:
            return True  # If no expiry date is set, the quiz is always active
        return now() < self.expiry_date
    
    def __str__(self):
        """
        Returns the title of the quiz as its string representation.
        
        Returns:
            str: The title of the quiz.
        """
        return self.title

class Question(models.Model):
    """
    Represents a question in a quiz.

    Attributes:
        question_id (UUID): Unique identifier for the question.
        quiz (Quiz): The quiz this question belongs to.
        question_no (int): The number of the question in the quiz.
        text (str): The text of the question.
        option_a (str): The text of option A.
        option_b (str): The text of option B.
        option_c (str): The text of option C.
        option_d (str): The text of option D.
        correct_option (str): The correct option ('A', 'B', 'C', or 'D').

    Methods:
        get_correct_option: Returns the text of the correct option.
        __str__: Returns a string representation of the question.
    """
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
        """
        Returns the correct option text.
            
        Returns:
            str: The correct option text (e.g., "Option A").
        """
        return getattr(self, f"option_{self.correct_option.lower()}")

    def __str__(self):
        return f"Q{self.question_no}: {self.text}"

class QuizStats(models.Model):
    """
    Stores statistics for a quiz, such as total participants, highest score, and average score.

    Attributes:
        stats_id (UUID): Unique identifier for the stats entry.
        quiz (Quiz): The quiz this stats entry belongs to.
        total_participants (int): Total number of participants who attempted the quiz.
        highest_score (float): The highest score achieved in the quiz.
        average_score (float): The average score across all participants.

    Methods:
        update_stats: Updates the statistics based on new participant scores.
        __str__: Returns a string representation of the quiz stats.
    """
    stats_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, related_name="stats")
    total_participants = models.IntegerField(default=0)
    highest_score = models.FloatField(null=True, blank=True)
    average_score = models.FloatField(null=True, blank=True)

    def update_stats(self, scores):
        """
        Update stats based on new scores.
        
        Args:
            scores (list of float): List of scores achieved by participants.
        """
        if scores:
            self.total_participants = len(scores)
            self.highest_score = max(scores)
            self.average_score = sum(scores) / len(scores)
        else:
            self.highest_score = self.average_score = None
        self.save()

    def __str__(self):
        """
        Returns a string representation of the quiz stats.
        
        Returns:
            str: A string representation of the quiz stats (e.g., "Stats for Quiz 1").
        """
        return f"Stats for {self.quiz.title}"
    