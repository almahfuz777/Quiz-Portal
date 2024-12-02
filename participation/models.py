from django.db import models

from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from quiz.models import Quiz, Question
import uuid

User = get_user_model()

class Participant(models.Model):
    """
    Participant model that links a user to a specific quiz they have participated in. 
    Stores the participant's score and timing details for the quiz.
    
    Attributes:
        participant_id: A unique identifier for the participant.
        user: The user who participated in the quiz (ForeignKey to the User model).
        quiz: The quiz the user participated in (ForeignKey to the Quiz model).
        score: The participant's score in the quiz, calculated based on correct responses.
        start_time: The time when the participant started the quiz.
        end_time: The time when the participant completed the quiz.
    """
    participant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participations")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="participants")
    score = models.FloatField(default=0.0)
    start_time = models.DateTimeField(default=now)
    end_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"

    def calculate_score(self):
        """
        Calculates the score for the participant based on correct responses.
        
        The score is calculated by counting the number of correct responses 
        out of the total number of questions in the quiz, then multiplying 
        by 100 to get the percentage score.
        
        This method updates the participant's score and saves it in the database.
        """
        correct_responses = self.responses.filter(is_correct=True).count()  # Count the correct responses
        total_questions = self.quiz.questions.count()
        self.score = (correct_responses / total_questions) * 100  # Calculate score as percentage
        self.save()  # Save the score to the database


class Response(models.Model):
    """
    Response model to store the participant's response to each question in the quiz.
    
    Attributes:
        response_id: A unique identifier for each response.
        participant: The participant who submitted the response (ForeignKey to the Participant model).
        question: The question that was answered (ForeignKey to the Question model).
        selected_option: The option selected by the participant (A, B, C, or D).
        is_correct: A flag indicating whether the selected option is correct.
    """
    response_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    selected_option = models.CharField(max_length=1, choices=[('A', 'Option A'), ('B', 'Option B'), ('C', 'Option C'), ('D', 'Option D')])

    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Response: {self.participant.user.username} - {self.question.text[:30]}"
