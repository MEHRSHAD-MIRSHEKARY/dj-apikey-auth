from rest_framework import serializers
from apikey_auth.models import APIKey


class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = [
            "id",
            "user",
            "key",
            "created_at",
            "expires_at",
            "is_active",
            "requests_count",
            "max_requests",
            "reset_at",
        ]
        read_only_fields = [
            "id",
            "key",
            "created_at",
            "user",
            "requests_count",
            "max_requests",
            "reset_at",
        ]

    def create(self, validated_data):
        """Ensure API key is generated on creation."""
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
