from django.test import TestCase
from apps.loan.models import Installment
from apps.loan.tests.test_models.integration_tests.model_base import ModelBase
from django.contrib.auth.models import User
from decimal import Decimal
from django.db import IntegrityError
from django.core.exceptions import ValidationError


class InstallmentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='jhon')
        self.loan = ModelBase.create_loan(user=self.user)
        self.ip = ModelBase.create_loan_ip()

    def test_create_installment(self):
        installment = Installment.objects.create(
            amount=Decimal('100.00'),
            installment_number=1,
            due_date='2024-03-15',
            loan=self.loan
        )
        self.assertEqual(installment.amount, Decimal('100.00'))

    def test_missing_required_fields(self):
        with self.assertRaises((IntegrityError, ValidationError)):
            Installment.objects.create()
