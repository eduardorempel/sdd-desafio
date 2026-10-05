from decimal import Decimal

import pytest
from fabrica import contexto, despesa, documento, politica_aplicavel

from reembolso.etapas import categoria
from reembolso.modelo import Motivo, Status
from reembolso.motor import calcular


def test_rn001_d005_coworking_recusada():
    d005 = despesa(1, id="d-005", categoria="coworking", valor="89.00")
    item = calcular(documento(d005), politica_aplicavel())[0]
    assert item.status == Status.RECUSADO
    assert item.motivo == Motivo.CATEGORIA_NAO_REEMBOLSAVEL
    assert item.valor_reembolsavel == Decimal("0.00")
    assert "RN-001" in item.justificativa


@pytest.mark.parametrize(
    "nome", ["alimentacao", "transporte_urbano", "hospedagem", "ALIMENTACAO", " Alimentação "]
)
def test_rn001_categorias_reembolsaveis_aceitas(nome):
    assert categoria(despesa(1, categoria=nome), contexto()) is None


@pytest.mark.parametrize("nome", ["transporte", "transporte urbano", "hotel", "alimentacao_extra"])
def test_rn001_lista_fechada_nao_aceita_parecidas(nome):
    assert categoria(despesa(1, categoria=nome), contexto()).motivo == (
        Motivo.CATEGORIA_NAO_REEMBOLSAVEL
    )
