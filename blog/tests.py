from django.test import TestCase
from django.urls import reverse
from core.models import User
from .models import Blog

class BlogModelTest(TestCase):
    """
    Tests for the Blog model.

    This test suite verifies the creation, string representation, and 
    functionality of the Blog model.
    """
    def setUp(self):
        """
        Sets up a user and a blog for testing.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.blog = Blog.objects.create(
            title="Test Blog",
            content="This is a test blog content.",
            author=self.user
        )

    def test_blog_creation(self):
        """
        Test that the blog is created correctly.
        """
        self.assertEqual(self.blog.title, "Test Blog")
        self.assertEqual(self.blog.content, "This is a test blog content.")
        self.assertEqual(self.blog.author, self.user)

    def test_blog_string_representation(self):
        """
        Test the string representation of the blog.
        """
        self.assertEqual(str(self.blog), "Test Blog")


class BlogViewTest(TestCase):
    """
    Tests for the Blog views (list, detail, and creation views).
    """
    def setUp(self):
        """
        Sets up a user, logs them in, and creates a blog for testing views.
        """
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.client.login(username="testuser@example.com", password="password123")

        self.blog = Blog.objects.create(
            title="Test Blog",
            content="This is a test blog content.",
            author=self.user
        )

    def test_blog_list_view(self):
        """
        Test the blog list view.
        """
        response = self.client.get(reverse('blog_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')
        self.assertContains(response, "Test Blog")

    def test_blog_detail_view(self):
        """
        Test the blog detail view.
        """
        response = self.client.get(reverse('blog_detail', args=[self.blog.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_detail.html')
        self.assertContains(response, "This is a test blog content.")

    def test_blog_creation_view(self):
        """
        Test the blog creation view.
        """
        response = self.client.post(reverse('create_blog'), {
            'title': 'New Blog',
            'content': 'Content of the new blog'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after creation
        self.assertEqual(Blog.objects.count(), 2)  # Initial + new blog


class BlogURLTest(TestCase):
    """
    Tests for the URLs associated with the Blog app.
    """
    def test_blog_urls(self):
        """
        Verifies that the URLs of the Blog app work as expected.
        """
        url_list = [
            reverse('blog_list'),          # Blog list
            reverse('create_blog'),        # Blog creation
        ]
        for url in url_list:
            response = self.client.get(url)
            if url == reverse('create_blog'):  # Create requires login
                self.assertEqual(response.status_code, 302)  # Redirect to login
            else:
                self.assertEqual(response.status_code, 200)
