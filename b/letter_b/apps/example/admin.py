from django.contrib import admin

from letter_b.apps.example.models import AuditAction
from letter_b.support.django_helpers import CustomModelAdminMixin


@admin.register(AuditAction)
class AuditActionAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    search_fields = ["user_id"]
