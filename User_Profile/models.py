from django.db import models
from django.conf import settings

class Profile(models.Model):
    """
    Represents a user profile.

    Attributes
    ----------
    user : ForeignKey
        A one-to-one relation to the built-in User model.
    bio : str, optional
        A short biography of the user.
    profile_picture : ImageField, optional
        The user's profile picture.
    location : str, optional
        The user's location.
    date_of_birth : DateField, optional
        The user's date of birth.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        """
        Returns a string representation of the Profile model.

        Returns
        -------
        str
            A string representation of the profile, indicating the associated user.
        """
        return f"Profile of {self.user.username}"

# Signals for Auto creation of profile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a user profile automatically when a new user is created.

    Parameters
    ----------
    sender : model
        The model that triggered the signal (User model in this case).
    instance : User
        The instance of the User model that was created.
    created : bool
        Indicates whether a new instance was created.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    Saves the profile whenever the User model instance is saved.

    Parameters
    ----------
    sender : model
        The model that triggered the signal (User model in this case).
    instance : User
        The instance of the User model being saved.
    """
    instance.profile.save()
