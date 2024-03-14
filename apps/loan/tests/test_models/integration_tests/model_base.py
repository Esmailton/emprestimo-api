
from faker import Factory as FakerFactory
from apps.loan.models import Loan, Installment, Payment, LoanIp
from django.contrib.auth.models import User
from decimal import Decimal

faker = FakerFactory.create()


class ModelBase:
    @staticmethod
    def create_user(username='jhon'):
        return User.objects.create(username=username)

    @staticmethod
    def create_loan(user=None, contracted_amount=Decimal('1050.00')):
        if user is None:
            user = ModelBase.create_user()
        loan = Loan.objects.create(
            description="CAPITAL DE GIRO",
            contracted_amount=contracted_amount,
            remaining_amount=Decimal('1050.00') +
            (Decimal('1050.00') * 5 / 100),
            number_of_installments=faker.random_int(min=1, max=12),
            tax_fees=5,
            bank="BANCO DO BRASIL",
            status="1",
            client="jhon",
            ip=ModelBase.create_loan_ip(),
            user=user
        )
        return loan

    @staticmethod
    def create_installment(loan=None, status='1'):
        if loan is None:
            loan = ModelBase.create_loan()
        return Installment.objects.create(
            amount=faker.pydecimal(left_digits=4, right_digits=2),
            installment_number=faker.random_int(min=1, max=12),
            status=status,
            due_date=faker.date_this_year(),
            loan=loan
        )

    @staticmethod
    def create_payment(loan=None, installment=None):
        if loan is None:
            loan = ModelBase.create_loan()
        if installment is None:
            installment = ModelBase.create_installment(loan)
        return Payment.objects.create(
            payment_method="2",
            amount=100,
            installment=installment,
        )

    @staticmethod
    def create_loan_ip():
        return LoanIp.objects.create(
            ip_address="127.0.0.1"
        )
