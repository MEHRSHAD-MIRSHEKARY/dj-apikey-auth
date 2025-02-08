from django.urls import path
from .views import api_keys_view

urlpatterns = [
    path("api-keys/", api_keys_view, name="api_keys"),
]
