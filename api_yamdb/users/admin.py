"""User model for group project."""
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """UserAdmin model."""

    list_display = (
        'id', 'username', 'first_name', 'last_name', 'role', 'is_superuser'
    )
    list_editable = ('role',)
    fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'bio',
        'is_superuser',
    )
    list_display_links = ('username',)
    list_filter = ('role',)
    search_fields = ('username',)
