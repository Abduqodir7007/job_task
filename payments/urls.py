from django.urls import path
from .views import PaymentCreateListView, PaymentReport

urlpatterns = [
    path("payments/", PaymentCreateListView.as_view(), name="payment-create"),
    path("reports/", PaymentReport.as_view(), name="payment-report"),
]
