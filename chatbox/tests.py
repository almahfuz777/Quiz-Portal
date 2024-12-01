from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Message

# Get the custom user model
User = get_user_model()

class ChatboxTests(TestCase):
    """
    Test case for the Chatbox application.

    This class contains tests for the chatbox home view, message submission, 
    message display, and timestamp functionality.

    Methods
    -------
    setUp() :
        Creates a test user and initial messages.
    test_chatbox_home_view() :
        Tests that the chatbox home page is accessible and displays the correct messages.
    test_message_submission() :
        Tests that submitting a new message works as expected.
    test_message_display_for_logged_in_user() :
        Tests that a logged-in user can see the messages.
    test_message_creation_timestamp() :
        Tests that messages have a timestamp when created.
    """

    def setUp(self):
        """
        Set up the test environment by creating a user and initial messages.

        Creates a test user and logs them in. It also creates two initial messages
        that will be used for testing the views and functionality.
        """
        # Create the user with a username along with email and password
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.client.login(email='testuser@example.com', password='testpassword')

        # Create some test messages
        self.message1 = Message.objects.create(user=self.user, content="Hello, this is the first message.")
        self.message2 = Message.objects.create(user=self.user, content="Another test message.")

    def test_chatbox_home_view(self):
        """
        Test that the chatbox home page is accessible and displays messages.

        Verifies that the home page loads successfully, the correct template is used,
        and the messages created in the `setUp` method are displayed.
        """
        response = self.client.get(reverse('chatbox_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'chatbox/chatbox_home.html')
        self.assertContains(response, "Hello, this is the first message.")
        self.assertContains(response, "Another test message.")

    def test_message_submission(self):
        """
        Test that submitting a new message works.

        Simulates submitting a new message through the chatbox form and checks that
        the message is added to the database and the page is correctly redirected.
        """
        data = {'content': 'New message from the test user!'}
        response = self.client.post(reverse('chatbox_home'), data)
        
        # Check that the message was added to the database
        self.assertEqual(Message.objects.count(), 3)
        self.assertEqual(Message.objects.last().content, 'New message from the test user!')

        # Check redirection or success after posting
        self.assertRedirects(response, reverse('chatbox_home'))
        
    def test_message_display_for_logged_in_user(self):
        """
        Test that the logged-in user can see messages in the chat.

        Verifies that the messages created in the `setUp` method are visible
        when a logged-in user accesses the chatbox home page.
        """
        response = self.client.get(reverse('chatbox_home'))
        self.assertContains(response, self.message1.content)
        self.assertContains(response, self.message2.content)

    def test_message_creation_timestamp(self):
        """
        Test that messages have a timestamp when created.

        Verifies that when a new message is created, it automatically gets a timestamp.
        """
        new_message = Message.objects.create(user=self.user, content="Message with timestamp.")
        self.assertIsNotNone(new_message.timestamp)
