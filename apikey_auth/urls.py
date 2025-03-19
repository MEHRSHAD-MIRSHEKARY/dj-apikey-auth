from django.urls import path
from rest_framework.routers import DefaultRouter

from apikey_auth.api.views import APIKeyViewSet
from apikey_auth.views import APIKeyListView

router = DefaultRouter()
router.register(r"apikey", APIKeyViewSet, basename="api-key")

urlpatterns = [
    path("api_keys/", APIKeyListView.as_view(), name="api_keys"),
]

urlpatterns += router.urls
