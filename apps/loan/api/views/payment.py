from rest_framework import generics
from apps.loan.models import Payment
from apps.loan.api.serializer.payment_serializer import PaymentSerializer
from rest_framework.pagination import PageNumberPagination
from apps.loan.api.service.payments import PaymentService
from rest_framework.permissions import IsAuthenticated


class PaymentListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Payment.objects.filter(installment__loan__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()
        service = PaymentService(serializer.instance)
        service.process_payment()
        return super().perform_create(serializer)


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
