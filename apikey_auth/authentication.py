from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.timezone import now
from .models import APIKey


class APIKeyUser:
    """
    Proxy user object for API key authentication.
    Acts like a Django user but is not stored in the database.
    """

    def __init__(self, api_key_instance):
        self.api_key_instance = api_key_instance
        self.id = api_key_instance.pk 
        self.username = f"APIKey-{api_key_instance.pk}"
        self.is_authenticated = True  

    def __str__(self):
        return f"APIKeyUser: {self.username}"


class ApiKeyAuthentication(BaseAuthentication):
    """
    Custom authentication for API key-based access.
    """

    def authenticate(self, request):
        """Authenticate the request using an API key."""
        api_key = request.headers.get("Authorization")
        if not api_key:
            return None  # No API key present, proceed to other authentication

        # Validate the API key
        try:
            api_key_instance = APIKey.objects.get(key=api_key, is_active=True)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API Key.")

        # Check if the API key has expired
        if api_key_instance.expires_at and api_key_instance.expires_at < now():
            raise AuthenticationFailed("API Key has expired.")

        # Return APIKeyUser as the authenticated user
        return (APIKeyUser(api_key_instance), None)
