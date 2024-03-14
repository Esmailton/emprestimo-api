from rest_framework import serializers
from apps.loan.models import LoanIp


class LoanIPSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanIp
        filds = ('ip_address',)
