from apps.loan.models import Loan, LoanIp
from rest_framework import serializers
from apps.loan.api.serializer.installment_serializer import InstallmentSerializer


class LoanSerializer(serializers.ModelSerializer):
    installments = InstallmentSerializer(many=True, read_only=True)
    ip = serializers.CharField(read_only=True)

    class Meta:
        model = Loan
        fields = ("pk", "client", "contracted_amount", "ip", "description", "bank", "remaining_amount", "number_of_installments",
                  "tax_fees", "status", "user", "created_at", "installments", "nominal_amount",)

    def calculate_nominal_amount(self, installments, tax_fees, contracted_amount):
        total_fee = installments * (tax_fees / 100)
        amount = (contracted_amount * total_fee)
        return contracted_amount + amount

    def create(self, validated_data):
        ip_address = self.context['request'].META.get('REMOTE_ADDR')
        user = self.context['request'].user
        loan_ip = LoanIp.objects.create(ip_address=ip_address)

        total_amount = self.calculate_nominal_amount(
            validated_data['number_of_installments'],
            validated_data['tax_fees'],
            validated_data['contracted_amount']
        )

        validated_data['nominal_amount'] = total_amount
        validated_data['remaining_amount'] = total_amount
        validated_data['ip'] = loan_ip
        validated_data['user'] = user
        validated_data['status'] = "1"
        return super().create(validated_data)
