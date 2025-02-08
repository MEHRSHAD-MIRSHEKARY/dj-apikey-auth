from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import APIKey

@login_required
def api_keys_view(request):
    """Render the API keys for the logged-in user in a modern template."""
    api_keys = APIKey.objects.select_related("user").all()  # ✅ Fetch only the logged-in user's API keys


    return render(request, "api_keys.html", {"api_keys": api_keys})
