from django.apps import AppConfig

class LeaderboardConfig(AppConfig):
    """
    Configuration class for the Leaderboard app.

    Attributes
    ----------
    default_auto_field : str
        The field type for auto-generated primary keys.
    name : str
        The name of the Django app.

    Methods
    -------
    ready() :
        Optional method to initialize app-specific logic once Django is fully loaded.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leaderboard'
