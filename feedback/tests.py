from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from quiz.models import Quiz, Participant
from feedback.models import Feedback
#from feedback.forms import FeedbackForm
from django.utils.timezone import now, timedelta
import random
import string

def generate_unique_email():
    # Generate a random string to append to the email to make it unique
    return "testuser" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) + "@example.com"
def generate_unique_username():
    # Generate a random string to append to the email to make it unique
    return "testuser" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) 


class FeedbackViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()

        # Ensure unique email address for the test user by calling the helper function
        unique_email = generate_unique_email()
        unique_username = generate_unique_username()
        self.user = User.objects.create_user(
            username= unique_username,  
            email=unique_email  # Generate a unique email for each test run
        )
        self.user.set_password("password123")  # Explicitly set and hash the password
        self.user.save()
        
        # Create the quiz
        self.quiz = Quiz.objects.create(
            title="Sample Quiz",
            description="A test quiz for feedback functionality.",
            quiz_type="public",
            duration=timedelta(minutes=30),
            expiry_date=now() + timedelta(days=1),
            created_by=self.user,
        )
        
        # Create the participant
        self.participant = Participant.objects.create(user=self.user, quiz=self.quiz)
        
        # Create the feedback for the test
        self.feedback = Feedback.objects.create(
            quiz=self.quiz,
            participant=self.participant,
            comment="Great quiz!",
            content="I really enjoyed it.",
        )


    def test_view_feedbacks_resolves(self):
        """Test URL resolves to the correct view."""
        url = reverse("view_feedbacks", args=[self.quiz.id, self.participant.id])
        from feedback.views import view_feedbacks
        self.assertEqual(resolve(url).func, view_feedbacks)

    def test_view_feedbacks_authenticated(self):
        """Test feedbacks are displayed correctly for an authenticated user."""
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("view_feedbacks", args=[self.quiz.id, self.participant.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.feedback.comment)
        self.assertTemplateUsed(response, "feedback/view_feedback.html")

    def test_view_feedbacks_unauthenticated(self):
        """Test unauthenticated users can still view feedbacks."""
        response = self.client.get(
            reverse("view_feedbacks", args=[self.quiz.id, self.participant.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.feedback.comment)

    def test_submit_feedback_resolves(self):
        """Test URL resolves to the correct view."""
        url = reverse("submit_feedback", args=[self.quiz.id, self.participant.id])
        from feedback.views import submit_feedback
        self.assertEqual(resolve(url).func, submit_feedback)

    def test_submit_feedback_get_authenticated(self):
        """Test GET request for feedback submission for an authenticated user."""
        self.client.login(email=self.user.email, password="password123")
        response = self.client.get(
            reverse("submit_feedback", args=[self.quiz.id, self.participant.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "feedback/submit_feedback.html")

    def test_submit_feedback_post_valid(self):
        """Test POST request with valid feedback data."""
        # Attempt to log in with the created test user
        login_response = self.client.login(email=self.user.email, password="password123")

        # Debugging outputs
        print(f"Login response: {login_response}")  # Should be True if login succeeds
        print(f"Email: {self.user.email}, Password: password123")
        print(f"Does user exist? {get_user_model().objects.filter(email=self.user.email).exists()}")

        # Ensure login is successful
        self.assertTrue(login_response, "Login failed!")

        # Clear any existing feedback for the participant and quiz
        Feedback.objects.filter(quiz=self.quiz, participant=self.participant).delete()

        # Valid feedback data
        response = self.client.post(
            reverse("submit_feedback", args=[self.quiz.id, self.participant.id]),
            data={
                "quiz": self.quiz.id,  # Pass the quiz ID
                "participant": self.participant.id,  # Pass the participant ID
                "comment": "New feedback",  # Valid comment
                "content": "This is additional content for feedback.",  # Valid content
            },
        )

        # Debug: Check response status code
        print(f"Response status code: {response.status_code}")

        # Ensure we get a 302 redirect after feedback submission
        self.assertEqual(response.status_code, 302)

        # Check if the new feedback has been saved in the database
        self.assertTrue(
            Feedback.objects.filter(
                quiz=self.quiz,
                participant=self.participant,
                comment="New feedback"
            ).exists()
        )



    def test_submit_feedback_post_invalid(self):
        """Test POST request with invalid feedback data."""
        self.client.login(email=self.user.email, password="password123")
        response = self.client.post(
            reverse("submit_feedback", args=[self.quiz.id, self.participant.id]),
            data={"comment": ""},  # Missing required fields
        )
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        self.assertFalse(
            Feedback.objects.filter(quiz=self.quiz, participant=self.participant).count() > 1
        )
        self.assertContains(response, "This field is required.")
