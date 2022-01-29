from django.contrib import admin

from django_api.apps.core.models import AuditAction
from django_api.support.django_helpers import CustomModelAdminMixin


@admin.register(AuditAction)
class AuditActionAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    search_fields = ["user_id"]
