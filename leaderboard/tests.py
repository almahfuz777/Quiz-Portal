from django.test import TestCase
from django.urls import reverse
from core.models import User
from quiz.models import Quiz  # Assuming we have a Quiz model
from .models import Leaderboard, Participation  # Assuming we have Leaderboard and Participation models

class LeaderboardModelTest(TestCase):
    def setUp(self):
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
        self.assertEqual(self.leaderboard1.participant.username, "user1")
        self.assertEqual(self.leaderboard2.participant.username, "user2")
        self.assertEqual(self.leaderboard1.score, 80)
        self.assertEqual(self.leaderboard2.score, 90)
        self.assertEqual(self.leaderboard1.rank, 2)
        self.assertEqual(self.leaderboard2.rank, 1)

    def test_leaderboard_string_representation(self):
        self.assertEqual(str(self.leaderboard1), "user1 - Test Quiz - 80 points")
        self.assertEqual(str(self.leaderboard2), "user2 - Test Quiz - 90 points")


class LeaderboardViewTest(TestCase):
    def setUp(self):
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
        response = self.client.get(reverse('leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leaderboard/leaderboard.html')
        self.assertContains(response, "Leaderboard")
        self.assertContains(response, "user")
        self.assertContains(response, "Test Quiz")
        self.assertContains(response, "80")


class LeaderboardURLTest(TestCase):
    def test_leaderboard_urls(self):
        url_list = [
            reverse('leaderboard'),  # Leaderboard page
        ]
        for url in url_list:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)  # Check if URL is accessible
