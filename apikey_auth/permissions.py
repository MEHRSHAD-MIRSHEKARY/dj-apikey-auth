from rest_framework.permissions import BasePermission
from .authentication import ApiKeyAuthentication, APIKeyUser


class HasAPIKeyPermission(BasePermission):
    """
    Custom permission to allow access only to users authenticated with an API key.
    """

    def has_permission(self, request, view):
        """Checks if the user is authenticated using an API key."""
        return isinstance(request.user, APIKeyUser)
