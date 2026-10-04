"""Textos das justificativas (spec §4, DT-008)."""

from decimal import Decimal


def reais(valor: Decimal) -> str:
    """Formata como `R$ 1.234,56`."""
    texto = f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {texto}"


def dados_invalidos(detalhe: str) -> str:
    return f"Dados inválidos: {detalhe} (RN-013)."


def aprovado() -> str:
    return (
        "Despesa aprovada: passou por todas as regras e é reembolsada integralmente "
        "(RN-001, RN-004 a RN-008)."
    )
