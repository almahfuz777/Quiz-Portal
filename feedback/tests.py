from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from quiz.models import Quiz
from participation.models import Participant
from feedback.models import Feedback
from django.utils.timezone import now, timedelta
import random
import string


def generate_unique_email():
    """Generate a random unique email for testing purposes."""
    return "testuser" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) + "@example.com"


def generate_unique_username():
    """Generate a random unique username for testing purposes."""
    return "testuser" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))


class FeedbackViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()

        # Create a test user
        self.user = User.objects.create_user(
            username=generate_unique_username(),
            email=generate_unique_email(),
            password="password123"
        )

        # Create another user to test "view feedbacks" from another user
        self.another_user = User.objects.create_user(
            username=generate_unique_username(),
            email=generate_unique_email(),
            password="password123"
        )

        # Create a public quiz
        self.quiz = Quiz.objects.create(
            title="Sample Quiz",
            description="A test quiz for feedback functionality.",
            quiz_type="public",
            duration=timedelta(minutes=30),
            expiry_date=now() + timedelta(days=1),
            created_by=self.user,
        )

        # Create participants for the quiz
        self.participant = Participant.objects.create(user=self.user, quiz=self.quiz)
        self.another_participant = Participant.objects.create(user=self.another_user, quiz=self.quiz)

        # Create feedback for the test user
        self.feedback = Feedback.objects.create(
            quiz=self.quiz,
            participant=self.participant,
            comment="Great quiz!",
            content="I really enjoyed it.",
        )

        # Create feedback for another user
        self.another_feedback = Feedback.objects.create(
            quiz=self.quiz,
            participant=self.another_participant,
            comment="Could be better.",
            content="I had issues with the timer.",
        )

    def test_my_feedback_view(self):
        """Test that 'my_feedback' shows only the logged-in user's feedbacks."""
        self.client.login(email=self.user.email, password="password123")
        response = self.client.get(reverse("my_feedback"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.feedback.comment)  # User's feedback is shown
        self.assertNotContains(response, self.another_feedback.comment)  # Another user's feedback is not shown
        self.assertTemplateUsed(response, "feedback/my_feedback.html")

    def test_view_feedback_view(self):
        """Test that 'view_feedbacks' shows all feedbacks for a specific quiz."""
        self.client.login(email=self.user.email, password="password123")
        response = self.client.get(reverse("view_feedback", args=[self.quiz.quiz_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.feedback.comment)  # User's feedback is shown
        self.assertContains(response, self.another_feedback.comment)  # Another user's feedback is also shown
        self.assertTemplateUsed(response, "feedback/view_feedback.html")


    def test_submit_feedback_post_valid(self):
        """Test POST request with valid data to 'submit_feedback'."""
        self.client.login(email=self.user.email, password="password123")
        Feedback.objects.filter(participant=self.participant, quiz=self.quiz).delete()

        response = self.client.post(
            reverse("submit_feedback", args=[self.quiz.quiz_id]),
            data={
                "comment": "New feedback",
                "content": "This is additional content for feedback.",
            }
        )

        self.assertEqual(response.status_code, 302)  # Redirects after successful submission
        self.assertTrue(
            Feedback.objects.filter(
                quiz=self.quiz,
                participant=self.participant,
                comment="New feedback"
            ).exists()
        )