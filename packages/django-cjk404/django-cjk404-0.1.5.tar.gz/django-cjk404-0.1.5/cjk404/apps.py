from django.apps import AppConfig


class Managed404Config(AppConfig):
    """Forked from wagtail_managed404, which was abandoned in 2018"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "cjk404"
