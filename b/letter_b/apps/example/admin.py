from django.contrib import admin

from letter_b.apps.example.models import AuditAction
from letter_b.apps.example.models import Person
from letter_b.apps.example.models import TodoItem
from letter_b.support.django_helpers import CustomModelAdminMixin


@admin.register(AuditAction)
class AuditActionAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    search_fields = ["user_id"]


@admin.register(Person)
class PersonAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass


@admin.register(TodoItem)
class TodoItemAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    pass
