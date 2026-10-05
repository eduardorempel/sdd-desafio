import copy
import json
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from reembolso.cambio import ler_cambio
from reembolso.entrada import EntradaInvalida

CAMBIO = Path(__file__).parent.parent / "exemplos" / "envelope" / "cambio.json"

_REMOVER = object()


def _cambio(**alteracoes):
    """Câmbio pequeno e válido; `alteracoes` usa `__` como separador de caminho."""
    doc = copy.deepcopy(
        {
            "moeda_base": "BRL",
            "fonte": "teste",
            "taxas": {
                "2026-07-13": {"USD": 5.42, "EUR": 5.91},
                "2026-07-14": {"USD": 5.44},
            },
        }
    )
    for caminho, valor in alteracoes.items():
        alvo = doc
        *pais, campo = caminho.split("__")
        for pai in pais:
            alvo = alvo[pai]
        if valor is _REMOVER:
            del alvo[campo]
        else:
            alvo[campo] = valor
    return json.dumps(doc)


def test_rn018_documento_cambio_exemplo_aceito():
    cambio = ler_cambio(CAMBIO.read_text(encoding="utf-8"), "BRL")
    assert cambio.moeda_base == "BRL"
    assert set(cambio.taxas) == {"USD", "EUR"}
    assert len({data for lista in cambio.taxas.values() for data, _ in lista}) == 12
    assert cambio.taxas["EUR"][1] == (date(2026, 7, 14), Decimal("5.93"))


def test_rn018_documento_taxas_ordenadas_por_data():
    texto = _cambio(taxas={"2026-07-14": {"USD": 5.44}, "2026-07-13": {"USD": 5.42}})
    datas = [data for data, _ in ler_cambio(texto, "BRL").taxas["USD"]]
    assert datas == [date(2026, 7, 13), date(2026, 7, 14)]


def test_rn018_documento_taxa_sem_arredondamento():
    texto = _cambio(taxas={"2026-07-13": {"USD": 5.4219}})
    assert ler_cambio(texto, "BRL").taxas["USD"][0][1] == Decimal("5.4219")


@pytest.mark.parametrize(
    "texto",
    ['{"moeda_base": ', '{"moeda_base": "BRL", "taxas": NaN}', '{"x": Infinity}'],
    ids=["json_ilegivel", "nan", "infinity"],
)
def test_rn018_documento_ilegivel_erro_geral(texto):
    with pytest.raises(EntradaInvalida, match="câmbio"):
        ler_cambio(texto, "BRL")


@pytest.mark.parametrize(
    "alteracoes",
    [
        {"moeda_base": _REMOVER},
        {"taxas": _REMOVER},
        {"moeda_base": 986},
        {"moeda_base": ""},
        {"taxas": [{"USD": 5.42}]},
        {"moeda_base": "USD"},
        {"taxas__2026-7-13": {"USD": 5.42}},
        {"taxas__2026-02-30": {"USD": 5.42}},
        {"taxas__2026-07-13": [5.42]},
        {"taxas__2026-07-13__USD": 0},
        {"taxas__2026-07-13__USD": -5.42},
        {"taxas__2026-07-13__USD": "5,42"},
        {"taxas__2026-07-13__USD": True},
        {"taxas__2026-07-13__ usd ": 5.43},
    ],
    ids=[
        "sem_moeda_base",
        "sem_taxas",
        "moeda_base_numero",
        "moeda_base_vazia",
        "taxas_nao_e_objeto",
        "moeda_base_diferente_da_politica",
        "data_fora_do_formato",
        "data_inexistente",
        "taxas_da_data_nao_e_objeto",
        "taxa_zero",
        "taxa_negativa",
        "taxa_texto",
        "taxa_booleana",
        "moedas_iguais_depois_da_normalizacao",
    ],
)
def test_rn018_documento_invalido_erro_geral(alteracoes):
    with pytest.raises(EntradaInvalida, match="câmbio"):
        ler_cambio(_cambio(**alteracoes), "BRL")


def test_rn018_documento_que_nao_e_objeto_erro_geral():
    with pytest.raises(EntradaInvalida):
        ler_cambio("[]", "BRL")


def test_rn018_documento_campos_informativos_nao_validados():
    ler_cambio(_cambio(fonte=1, observacao=["x"], extra=None), "BRL")


def test_rn018_documento_codigo_de_moeda_normalizado():
    cambio = ler_cambio(_cambio(taxas={"2026-07-13": {" usd ": 5.42}}), "BRL")
    assert set(cambio.taxas) == {"USD"}


def test_rn018_documento_moeda_base_comparada_apos_normalizacao():
    assert ler_cambio(_cambio(moeda_base=" brl "), "BRL").moeda_base == "BRL"
