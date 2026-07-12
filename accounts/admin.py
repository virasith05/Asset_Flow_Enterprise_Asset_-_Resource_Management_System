from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "phone",
                    "role",
                    "is_active_employee",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional Information",
            {
                "fields": (
                    "phone",
                    "role",
                    "is_active_employee",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "role",
        "is_active_employee",
        "is_staff",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_superuser",
    )