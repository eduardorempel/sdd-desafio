"""Construtores de objetos do modelo para os testes de regra (plan §6)."""

import json
from datetime import date
from decimal import Decimal
from pathlib import Path

from reembolso.cambio import Cambio, ler_cambio
from reembolso.etapas import Contexto
from reembolso.modelo import Despesa, Documento, Invalida
from reembolso.normalizacao import arredondar, normalizar_texto
from reembolso.politica import PoliticaAplicavel, ler_politica
from reembolso.politica import politica_aplicavel as _politica_aplicavel

POLITICA_V4 = Path(__file__).parent.parent / "exemplos" / "envelope" / "politica-v4.json"
CAMBIO = Path(__file__).parent.parent / "exemplos" / "envelope" / "cambio.json"


def despesa(
    posicao: int = 1,
    *,
    id: str | None = None,
    data: str = "2026-07-10",
    categoria: str = "alimentacao",
    fornecedor: str | None = None,
    valor: str = "10.00",
    tem_nota_fiscal: bool = True,
    moeda: str = "BRL",
) -> Despesa:
    """Despesa válida. Por padrão, cada posição tem `id` e fornecedor próprios.

    Fora de BRL, `valor_considerado` fica nulo até a etapa de conversão (DT-010).
    """
    id = id or f"d-{posicao:03d}"
    return Despesa(
        posicao=posicao,
        id=id,
        data=date.fromisoformat(data),
        categoria=normalizar_texto(categoria),
        fornecedor=normalizar_texto(fornecedor or f"Fornecedor {id}"),
        tem_nota_fiscal=tem_nota_fiscal,
        valor_informado=Decimal(valor),
        valor_considerado=arredondar(Decimal(valor)) if moeda == "BRL" else None,
        moeda=moeda,
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


def politica_aplicavel(
    centro_custo: str | None = None, documento: dict | None = None
) -> PoliticaAplicavel:
    """Política aplicável lida de `politica-v4.json` ou de `documento`; padrão por padrão."""
    if documento is None:
        texto = POLITICA_V4.read_text(encoding="utf-8")
    else:
        texto = json.dumps(documento)
    return _politica_aplicavel(ler_politica(texto), centro_custo)


def contexto(
    doc: Documento | None = None,
    politica: PoliticaAplicavel | None = None,
    cambio: Cambio | None = None,
) -> Contexto:
    """Contexto para chamar uma etapa diretamente (DT-009)."""
    return Contexto(doc or documento(), politica or politica_aplicavel(), cambio)


def cambio() -> Cambio:
    """`exemplos/envelope/cambio.json`, validado contra a moeda base BRL."""
    return ler_cambio(CAMBIO.read_text(encoding="utf-8"), "BRL")
