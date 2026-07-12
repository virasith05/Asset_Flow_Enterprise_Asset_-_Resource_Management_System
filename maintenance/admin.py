from django.contrib import admin

from .models import MaintenanceRecord


@admin.register(MaintenanceRecord)
class MaintenanceAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "technician",
        "maintenance_date",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "asset__asset_tag",
        "technician",
    )