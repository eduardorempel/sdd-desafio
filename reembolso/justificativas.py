"""Textos das justificativas (spec §4, DT-008)."""

from datetime import date
from decimal import Decimal

from reembolso.politica import Origem, TipoOrigem

_NOMES_CATEGORIA = {
    "alimentacao": "alimentação",
    "transporte_urbano": "transporte urbano",
    "hospedagem": "hospedagem",
    "representacao": "representação",
}


def reais(valor: Decimal) -> str:
    """Formata como `R$ 1.234,56`."""
    texto = f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"R$ {texto}"


def origem(origem: Origem) -> str:
    """Política de onde veio a entrada da categoria (RN-016, DT-011)."""
    match origem.tipo:
        case TipoOrigem.PADRAO:
            return "política padrão"
        case TipoOrigem.CENTRO:
            return f"centro de custo {origem.codigo}"
        case TipoOrigem.HERDADA:
            return f"centro de custo {origem.codigo} usando limite herdado da política padrão"
        case TipoOrigem.NAO_CADASTRADO:
            return f"política padrão; centro de custo {origem.codigo} não cadastrado"


def dados_invalidos(detalhe: str) -> str:
    return f"Dados inválidos: {detalhe} (RN-013)."


def cotacao_indisponivel(moeda: str, data: date) -> str:
    """Cita a moeda e a data da despesa (spec §4)."""
    return f"Sem cotação de {moeda} em {data} nem em data anterior (RN-018)."


def valor_negativo(valor: Decimal) -> str:
    return (
        f"Valor negativo ({reais(valor)}) não é reembolsável e não abate outras despesas (RN-005)."
    )


def fora_do_periodo(data: date, inicio: date, fim: date) -> str:
    return f"Data {data} fora do período de {inicio} a {fim} (RN-004)."


def categoria_nao_reembolsavel(categoria: str, politica: Origem) -> str:
    """Cita a política aplicada (spec §4, RN-016)."""
    return (
        f"Categoria '{categoria}' não é reembolsável pela política aplicada "
        f"({origem(politica)}) (RN-001, RN-016)."
    )


def duplicata(id_mantida: str) -> str:
    return (
        f"Duplicata de {id_mantida} (mesma data, categoria, fornecedor, moeda e valor); "
        f"mantida {id_mantida} (RN-006)."
    )


def nota_fiscal_ausente(limiar: Decimal) -> str:
    return f"Valor acima de {reais(limiar)} sem nota fiscal (RN-007)."


def _enumerar(ids: list[str]) -> str:
    if len(ids) == 1:
        return ids[0]
    return f"{', '.join(ids[:-1])} e {ids[-1]}"


def limite_diario(
    categoria: str,
    limite: Decimal,
    politica: Origem,
    data: date,
    consumido: Decimal,
    consumidoras: list[str],
    excedente: Decimal,
) -> str:
    """Cita o limite, a política de onde ele veio (RN-016) e, se houver, o valor já
    consumido no dia e quem o consumiu (spec §4)."""
    nome = _NOMES_CATEGORIA.get(categoria, categoria)
    limite_de = f"Limite diário de {nome} de {reais(limite)} ({origem(politica)})"
    if not consumidoras:
        return f"{limite_de} aplicado; excedente de {reais(excedente)} cortado (RN-008, RN-010)."
    por = f"por {_enumerar(consumidoras)} em {data}"
    if consumido >= limite:
        return f"{limite_de} já consumido {por} (RN-008, RN-009)."
    return (
        f"{limite_de}, com {reais(consumido)} já consumido {por}; "
        f"excedente de {reais(excedente)} cortado (RN-008, RN-009, RN-010)."
    )


def aprovado() -> str:
    return (
        "Despesa aprovada: passou por todas as regras e é reembolsada integralmente "
        "(RN-001, RN-004 a RN-008)."
    )
