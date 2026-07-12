from django.contrib import admin

from .models import Asset, AssetAllocation


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):

    list_display = (
        "asset_tag",
        "asset_name",
        "category",
        "department",
        "status",
        "condition",
    )

    list_filter = (
        "category",
        "department",
        "status",
        "condition",
    )

    search_fields = (
        "asset_tag",
        "asset_name",
        "serial_number",
    )

    ordering = (
        "asset_tag",
    )
    
@admin.register(AssetAllocation)
class AssetAllocationAdmin(admin.ModelAdmin):

    list_display = (
        "asset",
        "employee",
        "allocated_date",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "asset__asset_tag",
        "employee__username",
    )