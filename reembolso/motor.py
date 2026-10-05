"""Execução das etapas da spec §8 sobre as despesas de um documento."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from decimal import Decimal

from reembolso import etapas as regras
from reembolso import justificativas
from reembolso.cambio import Cambio
from reembolso.etapas import Contexto
from reembolso.modelo import (
    Corte,
    Despesa,
    Documento,
    Invalida,
    Motivo,
    Recusa,
    Resultado,
    Status,
)
from reembolso.politica import PoliticaAplicavel

ZERO = Decimal("0.00")


@dataclass(frozen=True)
class PorItem:
    """Etapa que decide sobre cada despesa isoladamente: `None` (passa) ou `Recusa`."""

    regra: Callable[[Despesa, Contexto], Recusa | None]


@dataclass(frozen=True)
class EmGrupo:
    """Etapa que recebe todas as despesas vivas, em ordem de posição, e decide sobre o conjunto.

    Devolve as decisões indexadas pela posição; despesas ausentes do dicionário passam.
    """

    regra: Callable[[list[Despesa], Contexto], dict[int, Recusa | Corte]]


Etapa = PorItem | EmGrupo

# Ordem das etapas da spec §8. As etapas 1 e 2 acontecem em entrada.py.
ETAPAS: list[Etapa] = [
    PorItem(regras.valor_negativo),  # RN-005 → VALOR_NEGATIVO
    PorItem(regras.periodo),  # RN-004 → FORA_DO_PERIODO
    PorItem(regras.categoria),  # RN-001 → CATEGORIA_NAO_REEMBOLSAVEL
    EmGrupo(regras.duplicatas),  # RN-006 → DUPLICATA
    PorItem(regras.nota_fiscal),  # RN-007 → NOTA_FISCAL_AUSENTE
    EmGrupo(regras.limites_por_data),  # RN-008, RN-009, RN-010 → LIMITE_DIARIO
]


def _decisoes(etapa: Etapa, vivas: list[Despesa], contexto: Contexto) -> dict:
    if isinstance(etapa, PorItem):
        decisoes = {d.posicao: etapa.regra(d, contexto) for d in vivas}
        return {posicao: r for posicao, r in decisoes.items() if r is not None}
    return etapa.regra(list(vivas), contexto)


def _recusado(despesa: Despesa | Invalida, recusa: Recusa) -> Resultado:
    return Resultado(
        id=despesa.id,
        valor_informado=despesa.valor_informado,
        valor_considerado=getattr(despesa, "valor_considerado", None),
        valor_reembolsavel=ZERO,
        status=Status.RECUSADO,
        motivo=recusa.motivo,
        justificativa=recusa.justificativa,
        moeda=getattr(despesa, "moeda", None),  # nula em DADOS_INVALIDOS (RN-013)
    )


def _final(despesa: Despesa, corte: Corte | None) -> Resultado:
    """Status final da seção 4 da spec: aprovado se reembolsável = considerado."""
    if corte is None or corte.valor_reembolsavel == despesa.valor_considerado:
        valor, status, motivo = despesa.valor_considerado, Status.APROVADO, None
        texto = justificativas.aprovado()
    else:
        valor, status, motivo = corte.valor_reembolsavel, Status.LIMITADO, corte.motivo
        texto = corte.justificativa
    return Resultado(
        id=despesa.id,
        valor_informado=despesa.valor_informado,
        valor_considerado=despesa.valor_considerado,
        valor_reembolsavel=valor,
        status=status,
        motivo=motivo,
        justificativa=texto,
        moeda=despesa.moeda,
    )


def calcular(
    documento: Documento,
    politica: PoliticaAplicavel,
    cambio: Cambio | None = None,
    etapas: Sequence[Etapa] | None = None,
) -> list[Resultado]:
    """Aplica as etapas em ordem e devolve um `Resultado` por despesa, na ordem da entrada.

    Todas as etapas recebem o mesmo `Contexto` (DT-009). Uma despesa recusada sai da
    lista viva e não chega às etapas seguintes nem consome limite (spec §8).
    """
    etapas = ETAPAS if etapas is None else etapas
    contexto = Contexto(documento, politica, cambio)
    resultados: dict[int, Resultado] = {}
    vivas: list[Despesa] = []
    for despesa in documento.despesas:
        if isinstance(despesa, Invalida):
            recusa = Recusa(Motivo.DADOS_INVALIDOS, justificativas.dados_invalidos(despesa.detalhe))
            resultados[despesa.posicao] = _recusado(despesa, recusa)
        else:
            vivas.append(despesa)

    cortes: dict[int, Corte] = {}
    for etapa in etapas:
        por_posicao = {d.posicao: d for d in vivas}
        for posicao, decisao in _decisoes(etapa, vivas, contexto).items():
            if isinstance(decisao, Recusa):
                resultados[posicao] = _recusado(por_posicao[posicao], decisao)
            else:
                cortes[posicao] = decisao
        vivas = [d for d in vivas if d.posicao not in resultados]

    for despesa in vivas:
        resultados[despesa.posicao] = _final(despesa, cortes.get(despesa.posicao))
    return [resultados[posicao] for posicao in sorted(resultados)]
