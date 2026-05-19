from rest_framework.permissions import BasePermission
from config.constants import Constants


class IsPaymentRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.roles.filter(name=Constants.UserRoles.PAYMENT).exists()
        )


class IsReportRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.roles.filter(name=Constants.UserRoles.REPORTS).exists()
        )


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.roles.filter(name=Constants.UserRoles.ADMIN).exists()
        )
