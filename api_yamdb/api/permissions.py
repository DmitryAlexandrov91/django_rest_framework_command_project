"""Custom permissions."""
from rest_framework import permissions


class IsAdmin(permissions.IsAdminUser):
    """Permisson for admin to work with users."""

    def has_permission(self, request, view):
        return (request.user
                and request.user.is_authenticated
                and request.user.is_admin)


class AdminOrReadOnly(IsAdmin):
    """Permisson for SAFE_METHODS or admin only."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin)


class ReviewsCommentsPermissions(permissions.BasePermission):
    """Permissions for reviews and comments."""

    def has_permission(self, request, view):
        """Safe methods processing."""
        return (request.user.is_authenticated or request.method
                in permissions.SAFE_METHODS
                )

    def has_object_permission(self, request, view, obj):
        """Customize permissions depends on the user's role."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or (request.user.is_moder and request.method in ['PATCH', 'DELETE']
                )
            or (request.user.is_authenticated and obj.author == request.user)
        )
