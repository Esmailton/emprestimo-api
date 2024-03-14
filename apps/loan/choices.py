from django.utils.translation import gettext_lazy as _
from django.db.models import IntegerChoices


class InstallmentsStatus(IntegerChoices):
    OUTROS = 0
    ATIVA = 1
    PAGA = 2


PAYMENTS_METHODS = [
    ("0", _("OUTROS")),
    ("1", _("PIX")),
    ("2", _("BOLETO")),
    ("3", _("CARTÃO")),
    ("4", _("TRANSFERÊNCIA")),
    ("5", _("DINHEIRO")),
]

LOAN_STATUS = [
    ("0", _("OUTROS")),
    ("1", _("ATIVO")),
    ("2", _("QUITADO")),
    ("3", _("CANCELADO")),
    ("4", _("EM ATRASO")),
]
