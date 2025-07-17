"""api app mixins."""
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import AdminOrReadOnly


class GenreCategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Mixin for category and genre Viewset."""

    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, AdminOrReadOnly)
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['name', ]
