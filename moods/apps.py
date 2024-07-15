from django.apps import AppConfig


class MoodsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "moods"

    def ready(self):
        import moods.signals  # noqa: F401

        pass
