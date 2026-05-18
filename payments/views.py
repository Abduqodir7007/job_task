from decimal import Decimal
from .utils import build_date_filter
from rest_framework.generics import ListCreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .permissions import IsPaymentRole, IsReportRole, IsAdminRole
from .models import Payment
from .serializers import PaymentSerializer, PaymentDetailSerializer, PaymentReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Sum, DecimalField
from django.db.models.functions import Coalesce


class PaymentCreateListView(ListCreateAPIView):
    queryset = Payment.objects.select_related("user").all()
    permission_classes = [IsPaymentRole, IsAdminRole]
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = PageNumberPagination

    filterset_fields = {
        "status": ["exact", "iexact"],
        "method": ["exact", "iexact"],
        "amount": ["gte", "lte"],
        "user__first_name": ["exact", "iexact"],
        "user__last_name": ["exact", "iexact"],
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status="completed") # set status to completed for testing


    def get_serializer_class(self):
        if self.request.method == "POST":
            return PaymentSerializer
        return PaymentDetailSerializer


class PaymentReport(APIView):
    permission_classes = [IsReportRole, IsAdminRole]
    serializer_class = PaymentReportSerializer

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        date_filter = build_date_filter(start_date, end_date)
        payments = Payment.objects.filter(date_filter)

        payment_by_method = payments.aggregate(
            payme=Coalesce(Sum("amount", filter=Q(method="payme"), output_field=DecimalField()), Decimal("0")),
            click=Coalesce(Sum("amount", filter=Q(method="click"), output_field=DecimalField()), Decimal("0")),
            uzum=Coalesce(Sum("amount", filter=Q(method="uzum"), output_field=DecimalField()), Decimal("0")),
        )

        total_sales = payments.aggregate(
            total_sales=Coalesce(Sum("amount", output_field=DecimalField()), Decimal("0"))
        )["total_sales"]

        serializer_input = {
            "payments_by_method": {
                "click": payment_by_method.get("click"),
                "payme": payment_by_method.get("payme"),
                "uzum": payment_by_method.get("uzum"),
            },
            "total_sales": total_sales,
        }

        serializer = PaymentReportSerializer(data=serializer_input)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
