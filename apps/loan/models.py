from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import Base
from apps.loan.choices import InstallmentsStatus, PAYMENTS_METHODS, LOAN_STATUS
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta
import operator


def positive_validator(value):
    if value <= 0:
        raise ValidationError(_("Valor Invalido!"))


class LoanIp(Base, models.Model):
    ip_address = models.GenericIPAddressField(
        _("Endereço IP"), null=True, blank=True, max_length=100)

    class Meta:
        verbose_name = _("Ip")
        verbose_name_plural = _("Ips")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ip_address}"


class Loan(Base, models.Model):
    description = models.CharField(
        _("Descrição do Empréstimo"), max_length=30)
    contracted_amount = models.DecimalField(
        _("Valor Contratado"), max_digits=10, decimal_places=2, validators=[positive_validator],)
    remaining_amount = models.DecimalField(
        _("Falta Pagar"), max_digits=10, decimal_places=2, validators=[positive_validator], null=True, blank=True,)
    nominal_amount = models.DecimalField(
        _("Valor Total a Pagar"), max_digits=10, decimal_places=2, null=True, blank=True)
    number_of_installments = models.PositiveIntegerField(
        _("Quantidade de Parcelas"))
    tax_fees = models.DecimalField(
        _("Juros"), max_digits=20, decimal_places=2, validators=[positive_validator],)
    bank = models.CharField(_("Banco"), max_length=20)
    client = models.CharField(_("Cliente"), max_length=60)
    status = models.CharField(_("Status Empréstimo"), choices=LOAN_STATUS,
                              help_text="0=OUTROS 1=ATIVO 2=QUITADO 3=CANCELADO 4=ATRASO")
    ip = models.OneToOneField(LoanIp, on_delete=models.CASCADE,
                              related_name='ips')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='loans', null=True, blank=True)

    class Meta:
        verbose_name = _("Empréstimo")
        verbose_name_plural = _("Empréstimos")
        ordering = ["-created_at"]

    def calculate_nominal_amount(self):
        total_fee = self.number_of_installments * (self.tax_fees / 100)
        amount = (self.contracted_amount * total_fee)
        return self.contracted_amount + amount

    def generate_installments(self):
        installments = []
        for i in range(self.number_of_installments):
            installment_number = i + 1
            due_date = self.created_at + relativedelta(months=i+1)
            installment = Installment(
                loan=self,
                amount=operator.truediv(
                    self.nominal_amount, self.number_of_installments),
                installment_number=installment_number,
                status="1",
                due_date=due_date
            )
            installments.append(installment)
        Installment.objects.bulk_create(installments)

    def __str__(self):
        return f"{self.description}"


class Installment(Base, models.Model):
    amount = models.DecimalField(
        _("Valor"), max_digits=10, decimal_places=2, validators=[positive_validator])
    installment_number = models.PositiveIntegerField(_("Número Parcela"))
    status = models.SmallIntegerField(
        _("Status Parcela"), choices=InstallmentsStatus.choices,
        help_text="0=OUTROS ATIVA=1 PAGA=2")
    due_date = models.DateField(_("Data Vencimento"))
    loan = models.ForeignKey(
        Loan, on_delete=models.CASCADE, related_name='installments')

    class Meta:
        verbose_name = _("Parcela")
        verbose_name_plural = _("Parcelas")
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.amount} - {self.installment_number}"


class Payment(Base, models.Model):
    payment_method = models.CharField(
        _("Metodo de Pagamento"), choices=PAYMENTS_METHODS, null=True, blank=True,
        help_text="0=OUTROS 1=PIX 2=BOLETO 3=CARTÃO 4=TRANSFERÊNCIA 5=DINHEIRO")
    amount = models.DecimalField(
        _("Valor Transação"), max_digits=10, decimal_places=2, validators=[positive_validator],)
    installment = models.ForeignKey(
        Installment, on_delete=models.CASCADE, related_name='payment_installments')

    class Meta:
        verbose_name = _("Transação")
        verbose_name_plural = _("Transações")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.payment_method}"
