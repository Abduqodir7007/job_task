from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from common.models import TimestampedModel
from config.constants import Constants
from config.managers import SoftDeleteManager

User = get_user_model()


from django.utils import timezone


class Payment(TimestampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    method = models.CharField(
        max_length=20, choices=Constants.PaymentMethod.CHOICES, default=Constants.PaymentMethod.DEFAULT
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Constants.PaymentStatus.CHOICES, default=Constants.PaymentStatus.DEFAULT
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.full_name}"

    class Meta:
        ordering = ["-created_at"]
