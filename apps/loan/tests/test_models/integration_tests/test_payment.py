from django.test import TestCase
from apps.loan.models import Payment
from apps.loan.tests.test_models.integration_tests.model_base import ModelBase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import IntegrityError


class PaymentModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='jhon')
        self.loan = ModelBase.create_loan(user=self.user)
        self.installment = ModelBase.create_installment(loan=self.loan)

    def test_create_payment(self):
        payment = Payment.objects.create(
            payment_method="3",
            amount=100,
            installment=self.installment,
        )
        self.assertEqual(payment.payment_method, "3")

    def test_missing_required_fields(self):
        with self.assertRaises((ValidationError, IntegrityError)):
            Payment.objects.create()

    def test_payment_string_representation(self):
        payment = Payment(payment_method="3")
        self.assertEqual(str(payment), "3")
