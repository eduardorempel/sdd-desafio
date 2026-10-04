"""Textos das justificativas (spec §4, DT-008)."""

from datetime import date
from decimal import Decimal

_NOMES_CATEGORIA = {
    "alimentacao": "alimentação",
    "transporte_urbano": "transporte urbano",
    "hospedagem": "hospedagem",
}


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


def categoria_nao_reembolsavel(categoria: str) -> str:
    return f"Categoria '{categoria}' não é reembolsável pela política (RN-001)."


def duplicata(id_mantida: str) -> str:
    return (
        f"Duplicata de {id_mantida} (mesma data, categoria, fornecedor e valor); "
        f"mantida {id_mantida} (RN-006)."
    )


def nota_fiscal_ausente(limiar: Decimal) -> str:
    return f"Valor acima de {reais(limiar)} sem nota fiscal (RN-007)."


def limite_diario(categoria: str, limite: Decimal, excedente: Decimal) -> str:
    nome = _NOMES_CATEGORIA.get(categoria, categoria)
    return (
        f"Limite diário de {nome} de {reais(limite)} aplicado; "
        f"excedente de {reais(excedente)} cortado (RN-008, RN-010)."
    )


def aprovado() -> str:
    return (
        "Despesa aprovada: passou por todas as regras e é reembolsada integralmente "
        "(RN-001, RN-004 a RN-008)."
    )
