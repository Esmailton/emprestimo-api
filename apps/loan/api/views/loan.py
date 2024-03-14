from rest_framework import generics
from apps.loan.models import Loan, Installment
from apps.loan.api.serializer.loan_serializer import LoanSerializer
from apps.loan.api.serializer.installment_serializer import InstallmentSerializer

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


class LoanListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save()
        loan = serializer.instance
        loan.generate_installments()

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)


class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_queryset(self):
        return Loan.objects.filter(user=self.request.user)


class LoanInstallmentListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    pagination_class = PageNumberPagination
    lookup_field = "installments"
