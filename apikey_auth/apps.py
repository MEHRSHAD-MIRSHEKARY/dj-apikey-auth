from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ApikeyAuthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apikey_auth"
    verbose_name = _("Django ApiKey Auth")
    
