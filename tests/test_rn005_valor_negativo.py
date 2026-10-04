from decimal import Decimal

from fabrica import despesa, documento

from reembolso.etapas import valor_negativo
from reembolso.modelo import Motivo, Status
from reembolso.motor import calcular


def test_rn005_d009_estorno_recusado():
    d009 = despesa(1, id="d-009", categoria="transporte_urbano", valor="-45.00")
    item = calcular(documento(d009))[0]
    assert item.status == Status.RECUSADO
    assert item.motivo == Motivo.VALOR_NEGATIVO
    assert item.valor_reembolsavel == Decimal("0.00")
    assert item.valor_considerado == Decimal("-45.00")
    assert "RN-005" in item.justificativa


def test_rn005_valor_zero_aprovado():
    item = calcular(documento(despesa(1, valor="0.00")))[0]
    assert item.status == Status.APROVADO
    assert item.motivo is None
    assert item.valor_reembolsavel == Decimal("0.00")


def test_rn005_negativo_que_arredonda_a_zero_aprovado():
    item = calcular(documento(despesa(1, valor="-0.004")))[0]
    assert item.status == Status.APROVADO
    assert item.valor_considerado == Decimal("0.00")
    assert item.valor_reembolsavel == Decimal("0.00")


def test_rn005_etapa_recusa_menos_um_centavo():
    assert valor_negativo(despesa(1, valor="-0.01"), documento()).motivo == Motivo.VALOR_NEGATIVO


def test_rn005_etapa_passa_positivo():
    assert valor_negativo(despesa(1, valor="0.01"), documento()) is None
