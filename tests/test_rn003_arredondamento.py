from decimal import Decimal

import pytest

from reembolso.normalizacao import arredondar


@pytest.mark.parametrize(
    ("valor", "esperado"),
    [
        ("33.333", "33.33"),
        ("10.005", "10.01"),
        ("-10.005", "-10.01"),
        ("10.004", "10.00"),
        ("72.5", "72.50"),
        ("100", "100.00"),
        ("-45.00", "-45.00"),
    ],
    ids=[
        "d-011",
        "metade_positiva",
        "metade_negativa",
        "abaixo_da_metade",
        "uma_casa",
        "inteiro",
        "negativo_exato",
    ],
)
def test_rn003_arredonda_para_centavos(valor, esperado):
    resultado = arredondar(Decimal(valor))
    assert resultado == Decimal(esperado)
    assert str(resultado) == esperado


def test_rn003_negativo_que_arredonda_a_zero_vira_zero_sem_sinal():
    resultado = arredondar(Decimal("-0.004"))
    assert resultado == Decimal("0")
    assert not resultado.is_signed()
    assert str(resultado) == "0.00"


def test_rn003_valor_muito_grande_nao_falha():
    assert arredondar(Decimal("1E+40")) == Decimal("1E+40")
