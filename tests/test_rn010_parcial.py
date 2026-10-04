from decimal import Decimal

from fabrica import despesa, documento

from reembolso.modelo import Motivo, Status
from reembolso.motor import calcular


def test_rn010_d014_reembolsada_ate_o_limite():
    d014 = despesa(1, id="d-014", data="2026-07-31", categoria="ALIMENTACAO", valor="61.00")
    item = calcular(documento(d014))[0]
    assert item.status == Status.LIMITADO
    assert item.motivo == Motivo.LIMITE_DIARIO
    assert item.valor_reembolsavel == Decimal("60.00")
    assert item.valor_considerado == Decimal("61.00")
    assert "RN-010" in item.justificativa


def test_rn010_um_centavo_acima_do_limite_nao_e_recusada():
    item = calcular(documento(despesa(1, valor="60.01")))[0]
    assert item.status == Status.LIMITADO
    assert item.valor_reembolsavel == Decimal("60.00")
