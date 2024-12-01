from django.apps import AppConfig

class BlogConfig(AppConfig):
    """
    Configuration for the Blog application.

    Attributes
    ----------
    default_auto_field : str
        Defines the default type of primary key field for models.
    name : str
        The name of the application, 'blog'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
