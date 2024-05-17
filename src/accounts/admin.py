from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from .models import Information, User


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "role"),
            },
        ),
    )

    list_display = ("email", "first_name", "last_name")
    list_filter = ("role", "is_active", "is_staff", "is_superuser", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)


@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ("user", "address")
    search_fields = ("user__email", "address")
