from dataclasses import replace
from decimal import Decimal

import pytest
from fabrica import contexto, despesa, documento, politica_aplicavel

from reembolso.etapas import periodo
from reembolso.modelo import Motivo, Status
from reembolso.motor import calcular


def test_rn004_d008_antes_do_periodo_recusada():
    d008 = despesa(1, id="d-008", data="2026-04-15", valor="41.00")
    item = calcular(documento(d008), politica_aplicavel())[0]
    assert item.status == Status.RECUSADO
    assert item.motivo == Motivo.FORA_DO_PERIODO
    assert item.valor_reembolsavel == Decimal("0.00")
    assert "RN-004" in item.justificativa


def test_rn004_depois_do_periodo_recusada():
    assert (
        calcular(documento(despesa(1, data="2026-08-01")), politica_aplicavel())[0].motivo
        == Motivo.FORA_DO_PERIODO
    )


@pytest.mark.parametrize(
    "data", ["2026-07-01", "2026-07-31"], ids=["primeiro_dia", "d-014_ultimo_dia"]
)
def test_rn004_bordas_incluidas(data):
    assert periodo(despesa(1, data=data), contexto()) is None


def test_rn004_competencia_divergente_nao_muda_resultado():
    doc = documento(despesa(1, data="2026-07-10"), despesa(2, data="2026-04-15"))
    divergente = replace(doc, periodo={**doc.periodo, "competencia": "2026-04"})
    assert calcular(divergente, politica_aplicavel()) == calcular(doc, politica_aplicavel())
