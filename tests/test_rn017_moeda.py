import json
from decimal import Decimal

import pytest
from fabrica import politica_aplicavel

from reembolso.entrada import ler_despesa, ler_documento
from reembolso.modelo import Despesa, Invalida, Motivo
from reembolso.motor import calcular
from reembolso.normalizacao import normalizar_moeda

_REMOVER = object()


def _despesa(**alteracoes):
    item = {
        "id": "e-010",
        "data": "2026-07-27",
        "categoria": "alimentacao",
        "fornecedor": "Bistro Central",
        "valor": Decimal("88.00"),
        "tem_nota_fiscal": True,
    }
    for campo, valor in alteracoes.items():
        if valor is _REMOVER:
            del item[campo]
        else:
            item[campo] = valor
    return item


def test_rn017_moeda_ausente_e_brl():
    despesa = ler_despesa(_despesa(), posicao=1)
    assert isinstance(despesa, Despesa)
    assert despesa.moeda == "BRL"


@pytest.mark.parametrize("moeda, esperada", [(" usd ", "USD"), ("eur", "EUR"), ("BRL", "BRL")])
def test_rn017_moeda_normalizada(moeda, esperada):
    assert ler_despesa(_despesa(moeda=moeda), posicao=1).moeda == esperada


def test_rn017_qualquer_codigo_nao_vazio_e_aceito():
    assert ler_despesa(_despesa(moeda="XYZ"), posicao=1).moeda == "XYZ"


@pytest.mark.parametrize(
    "moeda", ["", "   ", 840, None, ["USD"]], ids=["vazia", "espacos", "numero", "nula", "lista"]
)
def test_rn017_moeda_vazia_ou_nao_texto_e_dados_invalidos(moeda):
    invalida = ler_despesa(_despesa(moeda=moeda), posicao=1)
    assert isinstance(invalida, Invalida)
    assert "moeda" in invalida.detalhe


def test_rn017_moeda_invalida_nao_impede_as_demais():
    texto = json.dumps(
        {
            "colaborador": {"id": "c-0912"},
            "periodo": {"inicio": "2026-07-01", "fim": "2026-07-31"},
            "despesas": [
                {**_despesa(id="e-010", valor=88)},
                {**_despesa(id="e-011", valor=10, moeda="")},
                {**_despesa(id="e-012", valor=10, moeda=840, data="2026-07-28")},
                {**_despesa(id="e-013", valor=20, data="2026-07-29")},
            ],
        }
    )
    resultados = calcular(ler_documento(texto), politica_aplicavel(), etapas=[])
    assert [r.motivo for r in resultados] == [
        None,
        Motivo.DADOS_INVALIDOS,
        Motivo.DADOS_INVALIDOS,
        None,
    ]
    assert [r.moeda for r in resultados] == ["BRL", None, None, "BRL"]
    assert resultados[0].valor_reembolsavel == Decimal("88.00")


def test_rn017_normalizar_moeda_mantem_o_resto():
    assert normalizar_moeda("  us d ") == "US D"
