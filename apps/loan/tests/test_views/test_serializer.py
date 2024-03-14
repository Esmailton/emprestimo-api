from django.test import TestCase
from apps.loan.models import Installment, Loan, LoanIp
from apps.loan.api.serializer.installment_serializer import InstallmentSerializer
from apps.loan.api.serializer.payment_serializer import PaymentSerializer
from apps.loan.api.serializer.loan_serializer import LoanSerializer
from apps.loan.tests.test_models.integration_tests.model_base import ModelBase

from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
import datetime
from django.db import IntegrityError


class TestInstallmentSerializer(TestCase):

    def test_validate_due_date(self):
        data = {'due_date': timezone.now().date() - datetime.timedelta(days=1)}
        serializer = InstallmentSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_amount(self):
        data = {'amount': -10}
        serializer = InstallmentSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_unique_installment_number_per_loan(self):

        loan = Loan.objects.create(
            contracted_amount=1000, remaining_amount=1000, tax_fees=5,
            number_of_installments=12, ip=ModelBase.create_loan_ip(), status="0")

        data = {'loan': loan, 'installment_number': 1,
                'amount': 200, "due_date": "2025-03-10"}

        serializer = InstallmentSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class TestLoanSerializer(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.ip = LoanIp.objects.create(ip_address='127.0.0.1')

    def test_validate_contracted_amount(self):
        data = {'contracted_amount': -100}
        serializer = LoanSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_create_loan(self):
        data = {'contracted_amount': 1000, 'description': 'Capital de Giro',
                'remaining_amount': 1000, 'number_of_installments': 12,
                'tax_fees': 5, 'status': '1', 'bank': "BANCO FOO", "ip": self.ip, "client": "Jhon"}
        request = APIRequestFactory().post('/api/v1/loan/')
        request.user = self.user
        serializer = LoanSerializer(data=data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        loan = serializer.save()
        self.assertEqual(loan.user, self.user)
        self.assertEqual(loan.ip.ip_address, '127.0.0.1')


class TestPaymentSerializer(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.ip = ModelBase.create_loan_ip()

        self.loan = Loan.objects.create(
            contracted_amount=1000, remaining_amount=1000, tax_fees=5, number_of_installments=12,
            ip=self.ip, client="Jhon", status="1")

        self.installment = Installment.objects.create(
            loan=self.loan, installment_number=1, amount=100, due_date="2025-04-03", status="1")

    def test_validate_installment(self):
        data = {'loan': self.loan.pk, 'installment': 999}
        serializer = PaymentSerializer(data=data)
        with self.assertRaises((ValidationError, IntegrityError)):
            serializer.is_valid(raise_exception=True)
