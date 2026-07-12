from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "resource",
        "booked_by",
        "start_time",
        "end_time",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "resource__asset_tag",
        "booked_by__username",
    )