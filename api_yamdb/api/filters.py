"""Custom filters for api app."""
from django_filters import rest_framework

from reviews.models import Title


class TitleFilter(rest_framework.FilterSet):
    """Filter settings for TitleViewSet."""

    genre = rest_framework.CharFilter(
        field_name='genre__slug', lookup_expr='exact')
    category = rest_framework.CharFilter(
        field_name='category__slug', lookup_expr='exact')
    name = rest_framework.CharFilter(
        field_name='name', lookup_expr='exact')

    class Meta:
        """TitleFilter meta class."""

        model = Title
        fields = ['genre', 'category', 'year', 'name']
