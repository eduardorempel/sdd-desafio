"""Textos das justificativas (spec §4, DT-008)."""

from datetime import date
from decimal import Decimal


def reais(valor: Decimal) -> str:
    """Formata como `R$ 1.234,56`."""
    texto = f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {texto}"


def dados_invalidos(detalhe: str) -> str:
    return f"Dados inválidos: {detalhe} (RN-013)."


def valor_negativo(valor: Decimal) -> str:
    return (
        f"Valor negativo ({reais(valor)}) não é reembolsável e não abate outras despesas (RN-005)."
    )


def fora_do_periodo(data: date, inicio: date, fim: date) -> str:
    return f"Data {data} fora do período de {inicio} a {fim} (RN-004)."


def aprovado() -> str:
    return (
        "Despesa aprovada: passou por todas as regras e é reembolsada integralmente "
        "(RN-001, RN-004 a RN-008)."
    )
