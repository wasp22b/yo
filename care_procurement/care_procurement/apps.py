from django.apps import AppConfig

PLUGIN_NAME = "care_procurement"


class CareProcurementConfig(AppConfig):
    name = PLUGIN_NAME
    verbose_name = "Care Procurement"

    def ready(self):
        from care_procurement import signals  # noqa: F401
