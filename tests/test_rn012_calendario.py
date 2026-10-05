from datetime import date
from decimal import Decimal

import pytest
from fabrica import despesa, documento, politica_aplicavel

from reembolso.modelo import Status
from reembolso.motor import calcular


def test_rn012_d012_sabado_aprovado():
    assert date(2026, 7, 18).weekday() == 5  # sábado
    d012 = despesa(1, id="d-012", data="2026-07-18", fornecedor="Padaria Uniao", valor="47.20")
    item = calcular(documento(d012), politica_aplicavel())[0]
    assert item.status == Status.APROVADO
    assert item.valor_reembolsavel == Decimal("47.20")


@pytest.mark.parametrize(
    "data",
    ["2026-07-13", "2026-07-18", "2026-07-19", "2026-12-25"],
    ids=["segunda", "sabado", "domingo", "natal"],
)
def test_rn012_todos_os_dias_tem_o_mesmo_tratamento(data):
    item = calcular(
        documento(despesa(1, data=data, valor="70.00"), fim="2026-12-31"), politica_aplicavel()
    )[0]
    assert item.status == Status.LIMITADO
    assert item.valor_reembolsavel == Decimal("60.00")
