from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "status", "method", "created_at")
    list_filter = ("status", "method", "created_at")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    readonly_fields = ("user", "amount", "status", "method", "created_at", "updated_at")
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
