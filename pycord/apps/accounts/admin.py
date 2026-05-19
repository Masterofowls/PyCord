from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "display_name", "status", "is_staff")
    list_filter = ("status", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "display_name", "puid")
    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "Profile",
            {
                "fields": (
                    "display_name",
                    "avatar",
                    "status",
                    "bio",
                    "accent_color",
                    "puid",
                )
            },
        ),
    )
    readonly_fields = ("puid",)
