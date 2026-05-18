"""Project-wide constants."""

from django.utils.translation import gettext_lazy as _


class Constants:

    class UserRoles:
        """Constants for user roles."""

        ADMIN = "admin"
        PAYMENT = "payment"
        REPORTS = "reports"
        USER = "user"

        DEFAULT = USER
        CHOICES = (
            (ADMIN, _("Admin")),
            (PAYMENT, _("Payment")),
            (REPORTS, _("Reports")),
            (USER, _("User")),
        )

    class PaymentStatus:
        """Constants for payment statuses."""

        PENDING = "pending"
        COMPLETED = "completed"
        FAILED = "failed"

        DEFAULT = PENDING
        CHOICES = (
            (PENDING, _("Pending")),
            (COMPLETED, _("Completed")),
            (FAILED, _("Failed")),
        )

    class PaymentMethod:
        """Constants for payment methods."""

        PAYME = "payme"
        CLICK = "click"
        UZUM = "uzum"
        STRIPE = "stripe"

        DEFAULT = PAYME
        CHOICES = (
            (PAYME, _("Payme")),
            (CLICK, _("Click")),
            (UZUM, _("Uzum")),
            (STRIPE, _("Stripe")),
        )
