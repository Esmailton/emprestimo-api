from django.test import TestCase
from apps.loan.models import Loan
from apps.loan.tests.test_models.integration_tests.model_base import ModelBase
from django.contrib.auth.models import User
from decimal import Decimal
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from parameterized import parameterized


class LoanModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='jhon')

    def test_create_loan(self):
        loan = ModelBase.create_loan(user=self.user)
        self.assertEqual(loan.description, 'CAPITAL DE GIRO')

    def test_missing_required_fields(self):
        with self.assertRaises((IntegrityError, ValidationError)):
            Loan.objects.create()

    def calculate_nominal_amount(self):
        total_fee = Decimal(self.number_of_installments) * \
            (Decimal(self.tax_fees) / Decimal(100))
        amount = (self.contracted_amount * total_fee)
        return self.contracted_amount + amount

    def test_loan_string_representation(self):
        loan = Loan(description='CAPITAL DE GIRO')
        self.assertEqual(str(loan), 'CAPITAL DE GIRO')

    def test_loan_ordering(self):
        loan1 = ModelBase.create_loan(user=self.user)
        loan2 = ModelBase.create_loan(user=self.user, contracted_amount=2000)
        loans = Loan.objects.all()
        self.assertEqual(loans[0], loan2)
        self.assertEqual(loans[1], loan1)

    @parameterized.expand(
        [
            ("description", 30),
            ("bank", 20),
        ]
    )
    def test_loan_fields_max_length(self, field, max_length):
        loan = ModelBase.create_loan(user=self.user)
        setattr(loan, field, "X" * (max_length + 1))
        with self.assertRaises(ValidationError):
            loan.full_clean()
