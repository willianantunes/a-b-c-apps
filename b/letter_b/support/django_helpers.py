import os

from django.db.models import ForeignKey


class CustomModelAdminMixin:
    """
    Instead of declaring all the fields you want to expose concerning your model on Django Admin,
    you can use this fixture. It adds `list_display`, `readonly_fields`, and `raw_id_fields` for you automatically.
    """

    def __init__(self, model, admin_site):
        if self.list_display and self.list_display[0] == "__str__":
            self.list_display = [field.name for field in model._meta.fields if field.name != "id"]
        if not self.list_filter:
            self.list_filter = ["created_at", "updated_at"]
        if not self.readonly_fields:
            self.readonly_fields = ["created_at", "updated_at"]
        if not self.raw_id_fields:
            # Only for FOREIGN KEY fields
            raw_id_fields = []
            for key, value in model._meta._forward_fields_map.items():
                if type(value) is ForeignKey and not key.endswith("id"):
                    raw_id_fields.append(key)
            if raw_id_fields:
                self.raw_id_fields = raw_id_fields
        super(CustomModelAdminMixin, self).__init__(model, admin_site)


def strtobool(value: str) -> bool:
    value = value.lower()
    if value in ("y", "yes", "on", "1", "true", "t"):
        return True
    return False


def eval_env_as_boolean(varname, standard_value) -> bool:
    return bool(strtobool(os.getenv(varname, str(standard_value))))


def getenv_or_raise_exception(varname: str) -> str:
    """
    Retrieve a environment variable that MUST be set or raise an appropriate exception.
    """
    env = os.getenv(varname)

    if env is None:
        raise EnvironmentError(f"Environment variable {varname} is not set!")

    return env
