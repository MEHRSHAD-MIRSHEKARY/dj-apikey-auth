from apikey_auth.api.views.base import BaseViewSet
from rest_framework import mixins
from apikey_auth.models import APIKey
from apikey_auth.api.serializers.helper.get_serializer_cls import (
    apikey_serializer_class,
)


class APIKeyViewSet(
    BaseViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    """
    API ViewSet for managing API keys.
    Allows users to create, list, retrieve, update, and delete their API keys.
    """

    serializer_class = apikey_serializer_class()

    def get_queryset(self):
        """Ensure users can only access their own API keys."""
        return APIKey.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Auto-generate API key and assign user."""
        serializer.save(user=self.request.user)
