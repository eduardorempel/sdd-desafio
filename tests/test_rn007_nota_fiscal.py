from decimal import Decimal

import pytest
from fabrica import despesa, documento

from reembolso.etapas import nota_fiscal
from reembolso.modelo import Motivo, Status
from reembolso.motor import calcular


def _transporte(posicao, id, valor, tem_nota_fiscal=False):
    return despesa(
        posicao,
        id=id,
        data="2026-07-06",
        categoria="transporte_urbano",
        valor=valor,
        tem_nota_fiscal=tem_nota_fiscal,
    )


def test_rn007_d003_valor_exatamente_100_nao_exige_nota():
    assert nota_fiscal(_transporte(1, "d-003", "100.00"), documento()) is None


@pytest.mark.parametrize(
    ("id_", "categoria", "valor"),
    [("d-004", "transporte_urbano", "100.01"), ("d-013", "hospedagem", "690.00")],
    ids=["d-004_um_centavo_acima", "d-013_hospedagem"],
)
def test_rn007_acima_de_100_sem_nota_recusada(id_, categoria, valor):
    item = calcular(
        documento(despesa(1, id=id_, categoria=categoria, valor=valor, tem_nota_fiscal=False))
    )[0]
    assert item.status == Status.RECUSADO
    assert item.motivo == Motivo.NOTA_FISCAL_AUSENTE
    assert item.valor_reembolsavel == Decimal("0.00")
    assert "RN-007" in item.justificativa


def test_rn007_acima_de_100_com_nota_passa():
    d = despesa(1, categoria="hospedagem", valor="150.00", tem_nota_fiscal=True)
    assert nota_fiscal(d, documento()) is None


def test_rn007_compara_valor_arredondado():
    # 100.004 arredonda para 100.00 (RN-003) e não exige nota.
    assert nota_fiscal(_transporte(1, "x", "100.004"), documento()) is None
    assert nota_fiscal(_transporte(1, "y", "100.005"), documento()) is not None


def test_rn007_usa_valor_da_despesa_e_nao_a_soma_do_dia():
    # Duas despesas de 60,00 sem nota no mesmo dia somam 120,00, mas nenhuma passa de 100,00.
    resultados = calcular(
        documento(_transporte(1, "a", "60.00"), _transporte(2, "b", "60.00", tem_nota_fiscal=True))
    )
    assert all(r.motivo != Motivo.NOTA_FISCAL_AUSENTE for r in resultados)
