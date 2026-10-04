from datetime import date
from decimal import Decimal

import pytest

from reembolso.entrada import EntradaInvalida, ler_json, validar_documento


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


def _documento(**alteracoes):
    doc = {
        "colaborador": {"id": "c-0417", "nome": "Marina Volpi"},
        "periodo": {"competencia": "2026-07", "inicio": "2026-07-01", "fim": "2026-07-31"},
        "despesas": [],
    }
    for caminho, valor in alteracoes.items():
        alvo = doc
        *pais, campo = caminho.split("__")
        for pai in pais:
            alvo = alvo[pai]
        if valor is _REMOVER:
            del alvo[campo]
        else:
            alvo[campo] = valor
    return doc


_REMOVER = object()


@pytest.mark.parametrize(
    "alteracoes",
    [
        {"periodo__fim": _REMOVER},
        {"periodo__inicio": _REMOVER},
        {"periodo__inicio": "2026-02-30"},
        {"periodo__inicio": "2026-7-1"},
        {"periodo__fim": 20260731},
        {"periodo__inicio": "2026-08-01"},
        {"colaborador__id": "  "},
        {"colaborador__id": 417},
        {"colaborador__id": _REMOVER},
        {"colaborador": _REMOVER},
        {"colaborador": "c-0417"},
        {"periodo": _REMOVER},
        {"periodo": ["2026-07-01", "2026-07-31"]},
        {"despesas": _REMOVER},
        {"despesas": {"id": "d-001"}},
        {"despesas": [{"id": "d-001"}, "d-002"]},
    ],
    ids=[
        "sem_periodo_fim",
        "sem_periodo_inicio",
        "periodo_inicio_inexistente",
        "periodo_inicio_fora_do_formato",
        "periodo_fim_nao_texto",
        "inicio_posterior_ao_fim",
        "colaborador_id_so_espacos",
        "colaborador_id_numerico",
        "sem_colaborador_id",
        "sem_colaborador",
        "colaborador_nao_objeto",
        "sem_periodo",
        "periodo_nao_objeto",
        "sem_despesas",
        "despesas_nao_lista",
        "item_nao_objeto",
    ],
)
def test_rn013_erro_geral_documento_invalido(alteracoes):
    with pytest.raises(EntradaInvalida):
        validar_documento(_documento(**alteracoes))


def test_rn013_erro_geral_documento_nao_objeto():
    with pytest.raises(EntradaInvalida):
        validar_documento([])


def test_rn013_erro_geral_nao_ocorre_com_competencia_malformada():
    cabecalho = validar_documento(_documento(periodo__competencia="julho"))
    assert cabecalho.inicio == date(2026, 7, 1)
    assert cabecalho.fim == date(2026, 7, 31)


def test_rn013_erro_geral_nao_ocorre_com_despesas_vazia():
    assert validar_documento(_documento(despesas=[])).itens == []


def test_rn013_erro_geral_nao_ocorre_com_campos_informativos_e_desconhecidos():
    doc = _documento(colaborador__nome=123, colaborador__centro_custo=None, extra={"x": 1})
    validar_documento(doc)


def test_rn013_erro_geral_nao_ocorre_com_inicio_igual_ao_fim():
    validar_documento(_documento(periodo__inicio="2026-07-31"))
