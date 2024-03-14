from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from apps.loan.models import Loan, Installment, Payment
from apps.loan.tests.test_models.integration_tests.model_base import ModelBase


class TestLoanViews(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='test_password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.loan = Loan.objects.create(
            description='CAPITAL DE GIRO',
            contracted_amount=1000,
            remaining_amount=1000,
            number_of_installments=12,
            tax_fees=5,
            bank='BANCO DO BRASIL',
            status="1",
            ip=ModelBase.create_loan_ip(),
            user=self.user
        )
        self.installment = Installment.objects.create(
            amount=100,
            installment_number=1,
            status='1',
            due_date='2024-03-15',
            loan=self.loan
        )
        self.payment = Payment.objects.create(
            payment_method='Credit Card',
            amount=50,
            installment=self.installment
        )

    def test_loan_list_create_view(self):
        url = reverse('loan:loan')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_loan_detail_view(self):
        url = reverse('loan:loan-detail', kwargs={'pk': self.loan.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_installment_create_list_view(self):
        url = reverse('loan:installment')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payment_list_create_view(self):
        url = reverse('loan:payment')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payment_detail_view(self):
        url = reverse('loan:payment', kwargs={'pk': self.payment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
