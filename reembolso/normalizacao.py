"""Normalização de texto (RN-002), de moeda (RN-017) e arredondamento (RN-003)."""

import unicodedata
from decimal import ROUND_HALF_UP, Context, Decimal

CENTAVO = Decimal("0.01")

# Precisão suficiente para quantizar qualquer valor da entrada sem InvalidOperation.
_CONTEXTO = Context(prec=1000)


def normalizar_texto(texto: str) -> str:
    """Remove espaços das pontas, passa para minúsculas e remove acentos (RN-002, DT-007).

    Espaços internos e demais caracteres são mantidos.
    """
    decomposto = unicodedata.normalize("NFD", texto.strip().lower())
    sem_acentos = "".join(c for c in decomposto if unicodedata.category(c) != "Mn")
    return unicodedata.normalize("NFC", sem_acentos)


def normalizar_moeda(codigo: str) -> str:
    """Remove espaços das pontas e passa para maiúsculas (RN-017, DT-007)."""
    return codigo.strip().upper()


def arredondar(valor: Decimal) -> Decimal:
    """Arredonda para centavos com a metade se afastando do zero (RN-003, DT-001).

    O zero negativo (-0.00) vira 0.00 (DT-005).
    """
    arredondado = valor.quantize(CENTAVO, rounding=ROUND_HALF_UP, context=_CONTEXTO)
    if arredondado.is_zero():
        return Decimal("0.00")
    return arredondado
