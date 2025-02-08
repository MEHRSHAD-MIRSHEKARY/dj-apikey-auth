from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import api_keys_view, APIKeyViewSet


router = DefaultRouter()
router.register(r'apikeys', APIKeyViewSet, basename='api-key')

urlpatterns = [
    path("api-keys/", api_keys_view, name="api_keys"),
]

urlpatterns += router.urls

# Create a router and register the viewset