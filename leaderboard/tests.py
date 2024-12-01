from django.test import TestCase
from django.urls import reverse
from core.models import User
from quiz.models import Quiz  # Assuming we have a Quiz model
from .models import Leaderboard, Participation  # Assuming we have Leaderboard and Participation models

class LeaderboardModelTest(TestCase):
    """
    Test case for the Leaderboard model.

    This test checks the functionality of the Leaderboard model, including
    the creation of leaderboard entries and the string representation of the entries.

    Methods
    -------
    setUp() :
        Creates the necessary test data for leaderboard, participation, and users.
    test_leaderboard_creation() :
        Verifies the correct creation of leaderboard entries.
    test_leaderboard_string_representation() :
        Verifies that the string representation of leaderboard entries is correct.
    """

    def setUp(self):
        """
        Sets up test data for the leaderboard model.

        Creates two users, a quiz, two participation entries, and two leaderboard entries 
        for testing leaderboard functionality.
        """
        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="password123"
        )
        self.quiz = Quiz.objects.create(
            title="Test Quiz"
        )

        # Create some leaderboard entries for the users
        self.participation1 = Participation.objects.create(
            user=self.user1,
            quiz=self.quiz,
            score=80
        )
        self.participation2 = Participation.objects.create(
            user=self.user2,
            quiz=self.quiz,
            score=90
        )
        
        # Create leaderboard entry
        self.leaderboard1 = Leaderboard.objects.create(
            participant=self.user1,
            quiz=self.quiz,
            score=self.participation1.score,
            rank=2
        )
        self.leaderboard2 = Leaderboard.objects.create(
            participant=self.user2,
            quiz=self.quiz,
            score=self.participation2.score,
            rank=1
        )

    def test_leaderboard_creation(self):
        """
        Test if leaderboard entries are created correctly.

        Verifies that the leaderboard entries have the correct participant, score, 
        and rank values.
        """
        self.assertEqual(self.leaderboard1.participant.username, "user1")
        self.assertEqual(self.leaderboard2.participant.username, "user2")
        self.assertEqual(self.leaderboard1.score, 80)
        self.assertEqual(self.leaderboard2.score, 90)
        self.assertEqual(self.leaderboard1.rank, 2)
        self.assertEqual(self.leaderboard2.rank, 1)

    def test_leaderboard_string_representation(self):
        """
        Test the string representation of leaderboard entries.

        Verifies that the string representation of the leaderboard entries is correct.
        """
        self.assertEqual(str(self.leaderboard1), "user1 - Test Quiz - 80 points")
        self.assertEqual(str(self.leaderboard2), "user2 - Test Quiz - 90 points")


class LeaderboardViewTest(TestCase):
    """
    Test case for the Leaderboard view.

    This test verifies that the leaderboard view correctly renders the leaderboard page 
    and displays the expected content.

    Methods
    -------
    setUp() :
        Creates a user and a quiz, and sets up the test data for the leaderboard view.
    test_leaderboard_view() :
        Verifies the correct behavior of the leaderboard view.
    """

    def setUp(self):
        """
        Set up test data for the leaderboard view.

        Creates a user, logs the user in, creates a quiz, and adds a leaderboard entry.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.client.login(username="testuser@example.com", password="password123")

        self.quiz = Quiz.objects.create(title="Test Quiz")
        
        # Simulating leaderboard data
        self.leaderboard1 = Leaderboard.objects.create(
            participant=self.user,
            quiz=self.quiz,
            score=80,
            rank=1
        )

    def test_leaderboard_view(self):
        """
        Test the leaderboard view.

        Verifies that the leaderboard view returns the correct status code, uses 
        the correct template, and contains the expected content.
        """
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboard/leaderboard.html')
        self.assertContains(response, "Leaderboard")
        self.assertContains(response, "user")
        self.assertContains(response, "Test Quiz")
