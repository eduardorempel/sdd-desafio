"""Construtores de objetos do modelo para os testes de regra (plan §6)."""

from datetime import date
from decimal import Decimal

from reembolso.modelo import Despesa, Documento, Invalida
from reembolso.normalizacao import arredondar, normalizar_texto


def despesa(
    posicao: int = 1,
    *,
    id: str | None = None,
    data: str = "2026-07-10",
    categoria: str = "alimentacao",
    fornecedor: str | None = None,
    valor: str = "10.00",
    tem_nota_fiscal: bool = True,
) -> Despesa:
    """Despesa válida. Por padrão, cada posição tem `id` e fornecedor próprios."""
    id = id or f"d-{posicao:03d}"
    return Despesa(
        posicao=posicao,
        id=id,
        data=date.fromisoformat(data),
        categoria=normalizar_texto(categoria),
        fornecedor=normalizar_texto(fornecedor or f"Fornecedor {id}"),
        tem_nota_fiscal=tem_nota_fiscal,
        valor_informado=Decimal(valor),
        valor_considerado=arredondar(Decimal(valor)),
    )


def invalida(posicao: int = 1, *, id: str | None = "d-x", valor: str | None = "10.00") -> Invalida:
    return Invalida(
        posicao=posicao,
        id=id,
        valor_informado=None if valor is None else Decimal(valor),
        detalhe="tem_nota_fiscal ausente",
    )


def documento(*despesas, inicio: str = "2026-07-01", fim: str = "2026-07-31") -> Documento:
    return Documento(
        colaborador={"id": "c-0417"},
        periodo={"competencia": "2026-07", "inicio": inicio, "fim": fim},
        inicio=date.fromisoformat(inicio),
        fim=date.fromisoformat(fim),
        despesas=list(despesas),
    )
