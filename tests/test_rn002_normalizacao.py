import pytest

from reembolso.normalizacao import normalizar_texto


@pytest.mark.parametrize("categoria", ["ALIMENTACAO", " Alimentação ", "alimentacao"])
def test_rn002_grafias_de_alimentacao_viram_alimentacao(categoria):
    assert normalizar_texto(categoria) == "alimentacao"


def test_rn002_fornecedor_ignora_maiusculas():
    assert normalizar_texto("Bistro Central") == normalizar_texto("bistro central")


def test_rn002_fornecedor_ignora_espacos_nas_pontas():
    assert normalizar_texto("BISTRO CENTRAL ") == normalizar_texto("Bistro Central")


def test_rn002_mantem_espacos_internos():
    assert normalizar_texto("  Bistro   Central  ") == "bistro   central"


def test_rn002_cedilha_vira_c():
    assert normalizar_texto("Açaí da Praça") == "acai da praca"


def test_rn002_maiusculas_acentuadas():
    assert normalizar_texto("ÁÉÍÓÚ ÂÊÔ ÃÕ À Ç") == "aeiou aeo ao a c"


def test_rn002_mantem_outros_caracteres():
    assert normalizar_texto("transporte_urbano-2/x") == "transporte_urbano-2/x"
