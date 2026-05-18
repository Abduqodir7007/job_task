from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "first_name", "last_name", "is_active", "display_roles")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    @admin.display(description="Roles")
    def display_roles(self, obj):
        return ", ".join([r.get_name_display() for r in obj.roles.all()])


    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "roles")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser","user_permissions")}),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )
