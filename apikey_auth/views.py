from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import APIKey
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from django.utils.timezone import now
from .models import APIKey
from .serializers import APIKeySerializer


@login_required
def api_keys_view(request):
    """Render the API keys for the logged-in user in a modern template."""
    api_keys = APIKey.objects.select_related("user").all() 


    return render(request, "api_keys.html", {"api_keys": api_keys})


class APIKeyViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    API ViewSet for managing API keys.
    Allows users to create, list, retrieve, update, and delete their API keys.
    """

    serializer_class = APIKeySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Ensure users can only access their own API keys."""
        return APIKey.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Auto-generate API key and assign user."""
        serializer.save(user=self.request.user)
