import factory
from apps.loan.models import Loan, Installment, Payment, LoanIp
from django.contrib.auth.models import User
from django.test import TestCase


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class LoanIpFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LoanIp

    ip_address = '127.0.0.1'


class LoanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Loan

    description = 'Test Loan'
    contracted_amount = 1000
    remaining_amount = 500
    nominal_amount = 1500
    number_of_installments = 12
    tax_fees = 5
    bank = 'Test Bank'
    client = 'Test Client'
    status = '1'
    ip = factory.SubFactory(LoanIpFactory)
    user = factory.SubFactory(UserFactory)


class InstallmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Installment

    amount = 500
    installment_number = 1
    status = 1
    due_date = '2024-03-20'
    loan = factory.SubFactory(LoanFactory)


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    payment_method = '1'
    amount = 200
    installment = factory.SubFactory(InstallmentFactory)


class ModelsTestCase(TestCase):
    def test_loan_create(self):
        loan = LoanFactory()
        self.assertIsInstance(loan, Loan)

    def test_installment_create(self):
        installment = InstallmentFactory()
        self.assertIsInstance(installment, Installment)

    def test_payment_create(self):
        payment = PaymentFactory()
        self.assertIsInstance(payment, Payment)

    def test_loanip_create(self):
        loan_ip = LoanIpFactory()
        self.assertIsInstance(loan_ip, LoanIp)
