from django.urls import path
from apps.loan.api.views import installment, loan, payment

app_name = "loan"

urlpatterns = [
    path("v1/loan/", loan.LoanListCreateView.as_view(), name="loan"),

    path("v1/loan/<uuid:pk>/", loan.LoanDetailView.as_view(), name="loan-detail"),

    path("v1/loan/<uuid:pk>/installments",
         installment.InstallmentListView.as_view(), name="installment"),

    path("v1/payments/", payment.PaymentListCreateView.as_view(),
         name="payment"),

    path("v1/payments/<uuid:pk>/", payment.PaymentDetailView.as_view(),
         name="payment"),

    path("v1/installments/",
         installment.InstallmentListView.as_view(), name="installment"),



]
