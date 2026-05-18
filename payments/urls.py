from django.urls import path
from .views import PaymentCreateListView 

urlpatterns = [
    path("payments/", PaymentCreateListView.as_view(), name="payment-create"),
]
