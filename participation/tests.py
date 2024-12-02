from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils.timezone import now
from quiz.models import Quiz, Question
from participation.models import Participant, Response
from core.models import Tag

User = get_user_model()


class ParticipantResponseModelTest(TestCase):
    def setUp(self):
        """
        Sets up initial data for testing.
        """
        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

        # Create a tag
        self.tag = Tag.objects.create(name="General Knowledge")

        # Create a quiz
        self.quiz = Quiz.objects.create(
            title="Sample Quiz",
            description="This is a sample quiz.",
            quiz_type=Quiz.PUBLIC,
            duration=timedelta(minutes=30),
            created_by=self.user
        )
        self.quiz.tags.add(self.tag)

        # Create questions
        self.question1 = Question.objects.create(
            quiz=self.quiz,
            question_no=1,
            text="What is 2 + 2?",
            option_a="3",
            option_b="4",
            option_c="5",
            option_d="6",
            correct_option="B"
        )
        self.question2 = Question.objects.create(
            quiz=self.quiz,
            question_no=2,
            text="What is the capital of France?",
            option_a="Paris",
            option_b="London",
            option_c="Berlin",
            option_d="Rome",
            correct_option="A"
        )

        # Create a participant
        self.participant = Participant.objects.create(
            user=self.user,
            quiz=self.quiz,
            start_time=now(),
            end_time=now() + timedelta(minutes=25)
        )

    def test_participant_creation(self):
        """Test the creation of a participant."""
        self.assertEqual(self.participant.user, self.user)
        self.assertEqual(self.participant.quiz, self.quiz)
        self.assertEqual(self.participant.score, 0.0)

    def test_response_creation(self):
        """Test creating a response and linking it to a participant and question."""
        response = Response.objects.create(
            participant=self.participant,
            question=self.question1,
            selected_option="B",
            is_correct=True
        )
        self.assertEqual(response.participant, self.participant)
        self.assertEqual(response.question, self.question1)
        self.assertEqual(response.selected_option, "B")
        self.assertTrue(response.is_correct)

    def test_calculate_score(self):
        """Test the score calculation method."""
        # Create correct and incorrect responses
        Response.objects.create(
            participant=self.participant,
            question=self.question1,
            selected_option="B",
            is_correct=True
        )
        Response.objects.create(
            participant=self.participant,
            question=self.question2,
            selected_option="C",
            is_correct=False
        )

        # Calculate the score
        self.participant.calculate_score()

        # Verify the score (1 correct out of 2 questions = 50%)
        self.assertEqual(self.participant.score, 50.0)

    def test_participant_str_representation(self):
        """Test the string representation of the Participant model."""
        self.assertEqual(str(self.participant), f"{self.user.username} - {self.quiz.title}")

    def test_response_str_representation(self):
        """Test the string representation of the Response model."""
        response = Response.objects.create(
            participant=self.participant,
            question=self.question1,
            selected_option="B",
            is_correct=True
        )
        self.assertEqual(
            str(response),
            f"Response: {self.participant.user.username} - {self.question1.text[:30]}"
        )
        
