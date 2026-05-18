from rest_framework.permissions import BasePermission


class IsPaymentRole(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.roles.filter(name="Payment").exists()


class IsReportRole(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.roles.filter(name="Report").exists()


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.roles.filter(name="Admin").exists()
