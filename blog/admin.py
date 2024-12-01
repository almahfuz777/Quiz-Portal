from django.contrib import admin
from .models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Blog model in the Django admin interface.

    Attributes
    ----------
    list_display : tuple
        Specifies the fields to be displayed in the list view of the Blog model.
    search_fields : tuple
        Defines the fields to be used for search functionality in the admin interface.
    list_filter : tuple
        Specifies the fields by which the list can be filtered in the admin interface.
    """
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at',)
