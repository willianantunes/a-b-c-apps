from django.apps import AppConfig
from health_check.plugins import plugin_dir


class ExampleConfig(AppConfig):
    name = "letter_b.apps.example"

    def ready(self):
        """
        Adds healthcheck configuration.
        """
        from health_check.cache.backends import CacheBackend
        from health_check.db.backends import DatabaseBackend

        from letter_b.support.healthcheck.checkers import CustomDatabaseBackendHealthCheck
        from letter_b.support.healthcheck.checkers import DjangoSTOMPHealthCheck

        plugin_dir.register(CacheBackend)
        plugin_dir.register(DatabaseBackend)

        plugin_dir.register(CustomDatabaseBackendHealthCheck)
        plugin_dir.register(DjangoSTOMPHealthCheck)
