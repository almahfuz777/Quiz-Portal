from django.db import models
from core.models import User

class Blog(models.Model):
    """
    Represents a blog post in the system.

    Attributes
    ----------
    title : str
        The title of the blog post.
    content : str
        The content or body text of the blog post.
    author : ForeignKey
        A reference to the user who created the blog post.
    created_at : datetime
        The date and time when the blog post was created.
    updated_at : datetime
        The date and time when the blog post was last updated.
    """
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the string representation of the Blog model.

        Returns
        -------
        str
            The title of the blog post.
        """
        return self.title
