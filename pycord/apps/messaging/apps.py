from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "pycord.apps.messaging"
    label = "messaging"

    def ready(self) -> None:  # noqa: D401 — Django hook
        from . import signals  # noqa: F401
