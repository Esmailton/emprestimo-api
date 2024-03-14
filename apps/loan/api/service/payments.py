import operator
from apps.loan.models import Loan, Installment, Payment
from apps.loan.choices import InstallmentsStatus


class PaymentService:

    def __init__(self, payment: Payment):
        self.payment = payment
        self.loan = self.payment.installment.loan
        self.paid_amount = payment.amount

    def __update_loan(self, loan: Loan, paid_amount: float):

        remainder = loan.remaining_amount
        loan.remaining_amount = self.__get_remainder(
            remainder, paid_amount)
        loan.save()

    def __get_remainder(self, loan_amount: float, paid_amount: float) -> float:
        remaining_amount = operator.sub(loan_amount, paid_amount)
        return remaining_amount

    def __update_installment(self, installment: Installment):
        installment.status = InstallmentsStatus.PAGA
        installment.save()

    def process_payment(self):
        self.__update_installment(self.payment.installment)
        self.__update_loan(self.loan, self.paid_amount)
