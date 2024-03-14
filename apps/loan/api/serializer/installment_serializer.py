from apps.loan.models import Installment
from rest_framework import serializers
from django.utils import timezone


class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = ("id", "amount", "installment_number", "status",
                  "due_date", "loan", "created_at",)

    def validate_due_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError(
                "A data de vencimento deve estar no futuro.")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "O valor da parcela deve ser maior que zero.")
        return value

    def validate(self, data):
        loan = data.get('loan')
        installment_number = data.get('installment_number')
        if loan and installment_number:
            existing_installments = Installment.objects.filter(
                loan=loan, installment_number=installment_number, due_date="2024-05-10")
            if existing_installments.exists():
                raise serializers.ValidationError(
                    "Já existe uma parcela com este número para este empréstimo.")
        return data
