"""reviews admin zone settings."""
from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """TitleAdmin model."""

    list_display = ('id', 'name', 'genres', 'category', 'year')
    list_editable = ('category', 'year')
    fields = ('name', 'category', 'year', 'description', 'genre')
    list_display_links = ('name',)
    list_filter = ('category',)
    search_fields = ('name',)
    filter_horizontal = ('genre',)

    def genres(self, obj):
        """Return a list of genres of the title."""
        genres_queryset = obj.genre.all()
        title_genres = list(genres_queryset.values_list(
            'name', flat=True))
        return title_genres


class TitleInline(admin.StackedInline):
    """For CategoryAdmin model."""

    model = Title
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """CategoryAdmin model."""

    inlines = (
        TitleInline,
    )
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    list_editable = ('slug',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """GenreAdmin model."""

    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    list_editable = ('slug',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """ReviewAdmin model."""

    list_display = ('id', 'text', 'pub_date', 'score',)
    list_editable = ('score',)
    list_display_links = ('text',)
    list_filter = ('score',)
    search_fields = ('text',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """CommentAdmin model."""

    list_display = ('id', 'text', 'pub_date')
    list_display_links = ('text',)
    list_filter = ('author',)
    search_fields = ('pub_date',)
