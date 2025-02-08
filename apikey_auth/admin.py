from django.contrib import admin
from django.utils.html import format_html
from .models import APIKey

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ("user_display", "key_short", "created_at", "expires_at", "is_active", "status")
    autocomplete_fields = ("user",)
    search_fields = ("key",)
    list_filter = ("is_active", "expires_at")
    list_editable = ("is_active",)
    readonly_fields = ("key", "created_at", "user_display")
    actions = ["activate_keys", "deactivate_keys"]
    fieldsets = (
        (None, {
            "fields": ("user", "key", "created_at")
        }),
        ("Status", {
            "fields": ("is_active", "expires_at"),
        }),
    )

    def user_display(self, obj):
        """Show the user associated with the API key or 'Anonymous' if null."""
        return obj.user if obj.user else "Anonymous"
    user_display.short_description = "User"

    def key_short(self, obj):
        """Display only a short part of the API key for security reasons."""
        return f"{obj.key[:10]}..." if obj.key else "N/A"
    key_short.short_description = "API Key"

    def status(self, obj):
        """Show the API key status with colors."""
        color = "green" if obj.is_active else "red"
        return format_html(f'<b style="color: {color};">{"Active" if obj.is_active else "Inactive"}</b>')
    status.short_description = "Status"

    def activate_keys(self, request, queryset):
        """Activate selected API keys."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} API keys activated.")
    activate_keys.short_description = "Activate selected API keys"

    def deactivate_keys(self, request, queryset):
        """Deactivate selected API keys."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} API keys deactivated.")
    deactivate_keys.short_description = "Deactivate selected API keys"
