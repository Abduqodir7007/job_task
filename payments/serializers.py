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


class PaymentReportByPaymentMethodSerializer(serializers.Serializer):
    click = serializers.DecimalField(max_digits=15, decimal_places=2)
    payme = serializers.DecimalField(max_digits=15, decimal_places=2)
    uzum = serializers.DecimalField(max_digits=15, decimal_places=2)
class PaymentReportSerializer(serializers.Serializer):
    payments_by_method = PaymentReportByPaymentMethodSerializer()
    total_sales = serializers.DecimalField(max_digits=15, decimal_places=2)

    