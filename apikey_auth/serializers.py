from rest_framework import serializers
from .models import APIKey

class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = ['id', 'user', 'key', 'created_at', 'expires_at', 'is_active']
        read_only_fields = ['id', 'key', 'created_at', 'user']  # Prevent manual key input

    def create(self, validated_data):
        """Ensure API key is generated on creation."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
