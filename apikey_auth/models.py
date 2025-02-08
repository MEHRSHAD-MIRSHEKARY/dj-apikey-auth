import secrets
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

User = settings.AUTH_USER_MODEL

class APIKey(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="api_keys",
        null=True,
        blank=True,
        verbose_name=_("User"),
        help_text=_("The user who owns this API key."),
    )
    key = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
        verbose_name=_("API Key"),
        help_text=_("A unique API key used for authentication."),
        db_comment="The API key used for authentication."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the API key was created."),
        db_comment="Timestamp when the API key was generated."
    )
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Expiration Date"),
        help_text=_("The date and time when the API key will expire. Leave blank for no expiration."),
        db_comment="Optional expiration date for the API key."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Indicates whether the API key is active."),
        db_comment="Status flag to enable or disable an API key."
    )

    class Meta:
        verbose_name = _("API Key")
        verbose_name_plural = _("API Keys")
        ordering = ["-created_at"]
        db_table_comment = "Table storing API keys used for authentication."

    def save(self, *args, **kwargs):
        """Generate a secure API key if not already set."""
        if not self.key:
            self.key = secrets.token_urlsafe(48)  
        super().save(*args, **kwargs)

    def has_expired(self):
        """Check if the API key has expired."""
        return self.expires_at and self.expires_at < now()

    def __str__(self):
        return f"{self.user if self.user else 'Anonymous'} - {self.key[:10]}..."
