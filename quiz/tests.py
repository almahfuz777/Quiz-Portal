from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Quiz, Tag, Question
from datetime import timedelta, datetime
from django.utils.timezone import make_aware, now
from django.core.exceptions import ValidationError
from core.models import User

class QuizModelTest(TestCase):
    """
    Test case for the Quiz model.

    Tests the creation, attributes, and methods of the Quiz model.
    """
    def setUp(self):
        """
        Sets up a test user, tag, and quiz instance for testing.

        Creates:
        - A user instance using `core.models.User`.
        - A tag instance.
        - A public quiz instance with default attributes.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        # self.client.login(username="testuser@example.com", password="password123")

        self.tag = Tag.objects.create(name="Sample Tag")
        
        self.quiz = Quiz.objects.create(
            title="Sample Quiz",
            description="A sample quiz description",
            quiz_type=Quiz.PUBLIC,
            created_by=self.user,
            duration=timedelta(hours=1),
            can_view_score_immediately=True
        )
        self.quiz.tags.add(self.tag)
        
    def test_quiz_creation(self):
        """Test that a quiz is created with the correct attributes."""
        self.assertEqual(self.quiz.title, "Sample Quiz")
        self.assertEqual(self.quiz.description, "A sample quiz description")
        self.assertEqual(self.quiz.quiz_type, Quiz.PUBLIC)
        self.assertEqual(self.quiz.created_by, self.user)
        self.assertEqual(self.quiz.duration, timedelta(hours=1))
        self.assertTrue(self.quiz.can_view_score_immediately)
        self.assertEqual(self.quiz.tags.first().name, "Sample Tag")

    def test_is_active(self):
        """Test the `is_active` method for quizzes."""
        self.assertTrue(self.quiz.is_active())  # Active as no expiry date is set

        self.quiz.expiry_date = make_aware(datetime.now() - timedelta(days=1))
        self.quiz.save()
        self.assertFalse(self.quiz.is_active())  # Not active as expiry date is in the past

        self.quiz.expiry_date = make_aware(datetime.now() + timedelta(days=1))
        self.quiz.save()
        self.assertTrue(self.quiz.is_active())  # Active as expiry date is in the future

    def test_string_representation(self):
        """Test the string representation of a quiz."""
        self.assertEqual(str(self.quiz), "Sample Quiz")


class PrivateQuizModelTest(TestCase):
    """
    Test case for private quizzes in the Quiz model.

    Tests validation, creation, and attributes specific to private quizzes.
    """
    def setUp(self):
        """
        Sets up a user and related objects for testing.
        """
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.tag = Tag.objects.create(name="Private Tag")

    def test_private_quiz_requires_password(self):
        """Test that a private quiz cannot be created without a password."""
        with self.assertRaises(ValidationError) as context:
            Quiz.objects.create(
                title="Private Quiz Without Password",
                quiz_type=Quiz.PRIVATE,
                created_by=self.user,
                duration=timedelta(hours=2)
            )
        self.assertEqual(str(context.exception), "['A password is required for private quizzes.']")
    
    def test_private_quiz_creation_with_password(self):
        """Test creating a private quiz with a password."""
        private_quiz = Quiz.objects.create(
            title="Private Quiz",
            quiz_type=Quiz.PRIVATE,
            password="securepassword",
            created_by=self.user,
            duration=timedelta(hours=2)
        )
        self.assertIsNotNone(private_quiz.pk)  # Ensure the quiz is saved
        
    def test_private_quiz_attributes(self):
        """
        Test the attributes of a private quiz instance.

        Asserts:
        - The quiz's attributes match the expected values.
        - The associated tag is correctly linked.
        """
        private_quiz = Quiz.objects.create(
            title="Private Quiz",
            description="This is a private quiz.",
            quiz_type=Quiz.PRIVATE,
            password="securepassword",
            created_by=self.user,
            duration=timedelta(hours=2),
            can_view_score_immediately=False
        )
        private_quiz.tags.add(self.tag)
        
        # Verify the attributes
        self.assertEqual(private_quiz.title, "Private Quiz")
        self.assertEqual(private_quiz.description, "This is a private quiz.")
        self.assertEqual(private_quiz.quiz_type, Quiz.PRIVATE)
        self.assertEqual(private_quiz.created_by, self.user)
        self.assertEqual(private_quiz.duration, timedelta(hours=2))
        self.assertFalse(private_quiz.can_view_score_immediately)
        self.assertEqual(private_quiz.tags.first().name, "Private Tag")


class QuizViewTest(TestCase):
    """
    Test case for views related to the Quiz model.

    Includes tests for quiz home, creation, and setting questions.
    """
    def setUp(self):
        """
        Sets up a test user, tag, and quiz instance for testing views.

        Logs in the test user for authenticated view testing.
        """
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

        self.tag = Tag.objects.create(name="Test Tag")
        self.quiz = Quiz.objects.create(
            title="Test Quiz",
            description="This is a test quiz.",
            quiz_type=Quiz.PUBLIC,
            created_by=self.user,
            duration=timedelta(hours=1),
            can_view_score_immediately=True,
            expiry_date=make_aware(datetime.now() + timedelta(days=1)),
        )
        self.quiz.tags.add(self.tag)
        
    def test_quiz_home_view(self):
        """Test that the quiz home page loads and filters quizzes correctly."""
        response = self.client.get(reverse('quiz_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/quiz_home.html')
        self.assertIn('quizzes', response.context)
        self.assertIn(self.quiz, response.context['quizzes'])

    def test_create_quiz_get(self):
        """Test that the create quiz form loads."""
        response = self.client.get(reverse('create_quiz'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/create_quiz.html')
        self.assertIn('tags', response.context)

    def test_create_quiz_post(self):
        """Test creating a quiz via POST."""
        data = {
            'title': 'New Quiz',
            'description': 'A new test quiz',
            'quiz_type': 'public',
            'duration_hours': 1,
            'duration_minutes': 30,
            'duration_seconds': 0,
            'expiry_date': (now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M"),
            'tags': [self.tag.id],
            'can_view_score': 'on',
        }
        response = self.client.post(reverse('create_quiz'), data)
        self.assertEqual(response.status_code, 302)  # Should redirect to set_questions
        new_quiz = Quiz.objects.get(title='New Quiz')
        self.assertIsNotNone(new_quiz)
        self.assertEqual(new_quiz.description, 'A new test quiz')
        
    def test_create_private_quiz_post(self):
        """Test creating a private quiz requires a password."""
        data = {
            'title': 'Private Quiz',
            'description': 'This is a private quiz.',
            'quiz_type': 'private',
            'password': 'securepassword',
            'duration_hours': 2,
            'duration_minutes': 0,
            'duration_seconds': 0,
            'expiry_date': (now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M"),
            'tags': [self.tag.id],
            'can_view_score': 'on',
        }
        response = self.client.post(reverse('create_quiz'), data)
        self.assertEqual(response.status_code, 302)

    def test_create_private_quiz_without_password(self):
        """Test that a private quiz cannot be created without a password."""
        data = {
            'title': 'Invalid Private Quiz',
            'description': 'This should fail.',
            'quiz_type': 'private',
            'duration_hours': 2,
            'duration_minutes': 0,
            'duration_seconds': 0,
        }
        response = self.client.post(reverse('create_quiz'), data)
        self.assertEqual(response.status_code, 400)  # Check for bad request status
        self.assertIn(b"A password is required for private quizzes.", response.content)  # Check error message
        self.assertFalse(Quiz.objects.filter(title='Invalid Private Quiz').exists())

    def test_set_questions_view_get(self):
        """Test loading the set questions page."""
        response = self.client.get(reverse('set_questions', kwargs={'quiz_id': self.quiz.quiz_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/set_questions.html')

    def test_set_questions_view_post(self):
        """Test setting questions for a quiz."""
        data = {
            'question_text[]': ['What is 2 + 2?'],
            'option_a[]': ['4'],
            'option_b[]': ['3'],
            'option_c[]': ['5'],
            'option_d[]': ['6'],
            'correct_option[]': ['A'],
        }
        response = self.client.post(reverse('set_questions', kwargs={'quiz_id': self.quiz.quiz_id}), data)
        self.assertEqual(response.status_code, 302)  # Should redirect to quiz_home
        self.assertEqual(Question.objects.count(), 1)
        question = Question.objects.first()
        self.assertEqual(question.text, 'What is 2 + 2?')
        self.assertEqual(question.correct_option, 'A')
        
    def test_private_quiz_password_not_stored_in_plaintext(self):
        """Ensure that the password is hashed and not stored as plain text."""
        private_quiz = Quiz.objects.create(
            title="Private Quiz",
            quiz_type=Quiz.PRIVATE,
            password="securepassword",
            created_by=self.user,
            duration=timedelta(hours=2)
        )
        # Verify the password is hashed in the database
        self.assertNotEqual(private_quiz.password, "securepassword")
        self.assertTrue(private_quiz.password.startswith("pbkdf2_sha256$"))  # Check that it is hashed

    def test_check_password(self):
        """Test that the check_password method works correctly."""
        private_quiz = Quiz.objects.create(
            title="Private Quiz",
            quiz_type=Quiz.PRIVATE,
            password="securepassword",
            created_by=self.user,
            duration=timedelta(hours=2)
        )

        # Correct password should return True
        self.assertTrue(private_quiz.check_password("securepassword"))

        # Incorrect password should return False
        self.assertFalse(private_quiz.check_password("wrongpassword"))
