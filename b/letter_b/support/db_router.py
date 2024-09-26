from typing import Any

from django.db.models import Model


class DatabaseRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """

    def db_for_read(self, model: type[Model], **hints: dict[str, Any]):
        """
        Always read from REPLICA database
        """
        return "replica"

    def db_for_write(self, model: type[Model], **hints: dict[str, Any]):
        """
        Always write to DEFAULT database
        """
        return "default"

    def allow_relation(self, obj1: type[Model], obj2: type[Model], **hints: dict[str, Any]):
        """
        Objects from REPLICA and DEFAULT are de same, then True always
        """
        return True

    def allow_migrate(self, db: str, app_label: str, model_name: str | None = None, **hints: dict[str, Any]):
        """
        Only DEFAULT database
        """
        return db == "default"
