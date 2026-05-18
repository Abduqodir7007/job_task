from rest_framework.generics import ListCreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .permissions import IsPaymentRole, IsReportRole, IsAdminRole
from .models import Payment
from .serializers import PaymentSerializer, PaymentDetailSerializer


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
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PaymentSerializer
        return PaymentDetailSerializer

