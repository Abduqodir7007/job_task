from .models import Payment
from rest_framework import serializers
from users.serializers import UserDetailSerializer
from django.utils.translation import gettext_lazy as _

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("amount", "method")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(_("Payment amount must be greater than zero."))
        return value


class PaymentDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ("id", "user", "amount", "method", "status", "created_at")
        read_only_fields = ("id", "user", "created_at")
