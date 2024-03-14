from rest_framework import generics
from apps.loan.models import Installment
from apps.loan.api.serializer.installment_serializer import InstallmentSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


class InstallmentListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    pagination_class = PageNumberPagination
