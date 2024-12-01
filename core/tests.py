"""
Here is all functions that will verify the validity of the core app functionality
"""
from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
import uuid
from .utils import send_email_token
from Quiz_Portal import settings
import random
import string

def generate_unique_email():
    return "testuser" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) + "@example.com"

def generate_unique_username():
    return "testuser" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) 

class UserViewsTestCase(TestCase):
    
    """

    This class test the all the functions of views file
    """
    def setUp(self):
        """
        Set up initial test data, such as creating a user.
        """
        unique_username = generate_unique_username()
        unique_email = generate_unique_email()
        self.user_data = {
            'username': unique_username,
            'email': unique_email,
            'password1': 'password123',
            'password2': 'password123',
        }
        self.user = get_user_model().objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password1']
        )

    def test_signup_view_post_valid(self):
        """
        Test the signup view with valid data.
        """
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertRedirects(response, reverse('login'))

    def test_signup_view_post_password_mismatch(self):
        """
        Test the signup view with mismatched passwords.
        """
        invalid_data = self.user_data.copy()
        invalid_data['password2'] = 'mismatchpassword'
        response = self.client.post(reverse('signup'), invalid_data)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Password do not match' for message in messages))
        self.assertEqual(response.status_code, 200)

    def test_signup_view_post_existing_email(self):
        """
        Test signup with an already existing email.
        """
        response = self.client.post(reverse('signup'), self.user_data)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Email already exists' for message in messages))

    def test_signup_view_post_existing_username(self):
        """
        Test signup with an already existing username.
        """
        data = self.user_data.copy()
        data['email'] = 'newemail@example.com'
        response = self.client.post(reverse('signup'), data)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Username already taken' for message in messages))

    def test_verify_view_valid_token(self):
        """
        Test the verify view with a valid token.
        """
        valid_token = str(uuid.uuid4())
        unique_username = f'testuser_{uuid.uuid4().hex}'

        user = get_user_model().objects.create_user(
            username=unique_username,
            email='test@example.com',
            password='password123',
            email_token=valid_token,
            is_verified=False
        )
        
        response = self.client.get(reverse('verify', kwargs={'token': valid_token}))
        self.assertRedirects(response, reverse('quiz_home'))

    def test_verify_view_invalid_token(self):
        """
        Test the verify view with an invalid token.
        """
        invalid_token = str(uuid.uuid4())
        response = self.client.get(reverse('verify', kwargs={'token': invalid_token}))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Invalid verification token' for message in messages))

    def test_user_login_valid(self):
        """
        Test the login view with valid credentials.
        """
        response = self.client.post(reverse('login'), {
            'email': self.user_data['email'],
            'password': self.user_data['password1']
        })
        self.assertRedirects(response, reverse('quiz_home'))

    def test_user_login_invalid(self):
        """
        Test the login view with invalid credentials.
        """
        response = self.client.post(reverse('login'), {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Username or password is incorrect' for message in messages))

    def test_user_logout(self):
        """
        Test the logout view.
        """
        self.client.login(email=self.user_data['email'], password=self.user_data['password1'])
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)


class TestSendEmailToken(TestCase):
    """
    This class test the code of utils file
    """
    @patch('core.utils.send_mail')
    def test_send_email_token_success(self, mock_send_mail):
        """
        Test the send_email_token function with a successful email send.
        """
        mock_send_mail.return_value = 1
        email = 'test@example.com'
        token = '12345'

        result = send_email_token(email, token)

        self.assertTrue(result)
        mock_send_mail.assert_called_once_with(
            'Your account needs to be verified',
            'click on the link to verify http://127.0.0.1:8000/verify/12345',
            settings.EMAIL_HOST_USER,
            [email],
        )

    @patch('core.utils.send_mail')
    def test_send_email_token_failure(self, mock_send_mail):
        """
        Test the send_email_token function with a failure in email sending.
        """
        mock_send_mail.side_effect = Exception('SMTP error')
        email = 'test@example.com'
        token = '12345'
        result = send_email_token(email, token)
        self.assertFalse(result)
