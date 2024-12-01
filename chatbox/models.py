from django.db import models
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()

class Message(models.Model):
    """
    Model representing a message in the chatbox.

    Each message is associated with a user and contains the content of the message.
    It also stores the timestamp of when the message was sent.

    Attributes
    ----------
    user : ForeignKey
        The user who sent the message.
    content : TextField
        The content of the message.
    timestamp : DateTimeField
        The time when the message was sent.

    Methods
    -------
    __str__() :
        Returns a string representation of the message, including the user and timestamp.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each message to a user
    content = models.TextField()  # The message content
    timestamp = models.DateTimeField(auto_now_add=True)  # The time when the message is sent

    def __str__(self):
        """
        String representation of the Message object.

        Returns a string in the format:
        "Message by <username> at <timestamp>"
        """
        return f"Message by {self.user.username} at {self.timestamp}"
