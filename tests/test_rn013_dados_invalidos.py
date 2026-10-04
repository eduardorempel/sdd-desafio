from decimal import Decimal

import pytest

from reembolso.entrada import EntradaInvalida, ler_json


def test_rn013_json_invalido_erro_geral():
    with pytest.raises(EntradaInvalida):
        ler_json('{"colaborador": ')


def test_rn013_nan_erro_geral():
    with pytest.raises(EntradaInvalida):
        ler_json('{"valor": NaN}')


@pytest.mark.parametrize("literal", ["Infinity", "-Infinity"])
def test_rn013_infinity_erro_geral(literal):
    with pytest.raises(EntradaInvalida):
        ler_json(f'{{"valor": {literal}}}')


def test_dt001_float_lido_como_decimal():
    valor = ler_json('{"valor": 33.333}')["valor"]
    assert isinstance(valor, Decimal)
    assert valor == Decimal("33.333")


def test_dt001_metade_nao_sofre_erro_de_float():
    assert ler_json('{"valor": 10.005}')["valor"] == Decimal("10.005")
