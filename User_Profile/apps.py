from django.apps import AppConfig

class UserProfileConfig(AppConfig):
    """
    Configuration for the User Profile application.

    This class sets up the default auto field type for models and specifies the 
    application name for the User Profile app.

    Attributes
    ----------
    default_auto_field : str
        The default type of primary key field for models.
    name : str
        The name of the application, 'User_Profile'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'User_Profile'
