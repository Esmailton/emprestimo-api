from apps.loan.models import Payment
from rest_framework import serializers
from apps.loan.choices import InstallmentsStatus


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ("id", "payment_method",
                  "amount", "created_at", "installment")

    def validate_installment(self, value):
        req_amount = float(self.context['request'].data.get('amount'))
        if value.status == InstallmentsStatus.PAGA:
            raise serializers.ValidationError(
                "A Parcela associada já foi paga.")
        elif float(value.amount) != float(req_amount):
            raise serializers.ValidationError(
                "O Valor diferente do valor da parcela!")
        return value
