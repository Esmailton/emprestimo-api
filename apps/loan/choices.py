from django.db.models import IntegerChoices


class InstallmentsStatus(IntegerChoices):
    OUTROS = 0
    ATIVA = 1
    PAGA = 2


class PaymentsMethods(IntegerChoices):
    OUTROS = 0
    PIX = 1
    BOLETO = 2
    CARTAO = 3
    TRANSFERENCIA = 4
    DINHEIRO = 5


class LoanStatus(IntegerChoices):
    OUTROS = 0
    ATIVO = 1
    QUITADO = 2
    CANCELADO = 3
