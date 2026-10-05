import copy
import json
from decimal import Decimal
from pathlib import Path

import pytest

from reembolso.entrada import EntradaInvalida
from reembolso.politica import ler_politica

POLITICA_V4 = Path(__file__).parent.parent / "exemplos" / "envelope" / "politica-v4.json"

_REMOVER = object()


def _politica(**alteracoes):
    """Política pequena e válida; `alteracoes` usa `__` como separador de caminho."""
    doc = {
        "versao": "teste",
        "moeda_base": "BRL",
        "padrao": {
            "alimentacao": {"limite": 60.00, "periodicidade": "dia"},
            "hospedagem": {"limite": 250.00, "periodicidade": "diaria"},
        },
        "centros_custo": {
            "CC-ADM": {"alimentacao": {"limite": 45.00, "periodicidade": "dia"}},
        },
        "nota_fiscal_obrigatoria_acima_de": 100.00,
    }
    doc = copy.deepcopy(doc)
    for caminho, valor in alteracoes.items():
        alvo = doc
        *pais, campo = caminho.split("__")
        for pai in pais:
            alvo = alvo[pai]
        if valor is _REMOVER:
            del alvo[campo]
        else:
            alvo[campo] = valor
    return json.dumps(doc, ensure_ascii=False)


def test_rn015_politica_v4_aceita():
    politica = ler_politica(POLITICA_V4.read_text(encoding="utf-8"))
    assert politica.moeda_base == "BRL"
    assert politica.limiar_nota_fiscal == Decimal("100.00")
    assert politica.padrao == {
        "alimentacao": Decimal("60.00"),
        "transporte_urbano": Decimal("80.00"),
        "hospedagem": Decimal("250.00"),
    }
    assert set(politica.centros) == {"cc-eng-plataforma", "cc-comercial", "cc-adm"}
    assert politica.centros["cc-comercial"].limites["representacao"] == Decimal("300.00")
    assert politica.centros["cc-eng-plataforma"].limites["hospedagem"] == Decimal("0.00")
    assert "hospedagem" not in politica.centros["cc-adm"].limites


def test_rn015_chave_do_centro_mantem_grafia_do_documento():
    politica = ler_politica(POLITICA_V4.read_text(encoding="utf-8"))
    assert politica.centros["cc-comercial"].codigo == "CC-COMERCIAL"


def test_rn015_politica_minima_valida():
    politica = ler_politica(_politica())
    assert politica.padrao["alimentacao"] == Decimal("60.00")
    assert politica.centros["cc-adm"].limites == {"alimentacao": Decimal("45.00")}


@pytest.mark.parametrize(
    "texto",
    ['{"moeda_base": ', '{"moeda_base": "BRL", "x": NaN}', '{"x": Infinity}', '{"x": -Infinity}'],
    ids=["json_ilegivel", "nan", "infinity", "menos_infinity"],
)
def test_rn015_documento_ilegivel_erro_geral(texto):
    with pytest.raises(EntradaInvalida, match="política"):
        ler_politica(texto)


@pytest.mark.parametrize(
    "alteracoes",
    [
        {"padrao": _REMOVER},
        {"centros_custo": _REMOVER},
        {"moeda_base": _REMOVER},
        {"nota_fiscal_obrigatoria_acima_de": _REMOVER},
        {"padrao": ["alimentacao"]},
        {"centros_custo": []},
        {"centros_custo__CC-ADM": "alimentacao"},
        {"padrao__alimentacao": 60},
        {"padrao__alimentacao__limite": -1},
        {"padrao__alimentacao__limite": "60"},
        {"padrao__alimentacao__limite": True},
        {"padrao__alimentacao__limite": _REMOVER},
        {"centros_custo__CC-ADM__alimentacao__limite": -1},
        {"nota_fiscal_obrigatoria_acima_de": -1},
        {"nota_fiscal_obrigatoria_acima_de": "100"},
        {"nota_fiscal_obrigatoria_acima_de": True},
        {"moeda_base": "USD"},
        {"moeda_base": ""},
        {"moeda_base": 986},
        {"padrao__alimentacao__periodicidade": "mes"},
        {"padrao__alimentacao__periodicidade": 1},
        {"padrao__alimentacao__periodicidade": _REMOVER},
        {"padrao__Alimentação": {"limite": 50, "periodicidade": "dia"}},
        {"centros_custo__ cc-adm ": {}},
    ],
    ids=[
        "sem_padrao",
        "sem_centros_custo",
        "sem_moeda_base",
        "sem_limiar",
        "padrao_nao_e_objeto",
        "centros_custo_nao_e_objeto",
        "tabela_do_centro_nao_e_objeto",
        "entrada_de_categoria_nao_e_objeto",
        "limite_negativo",
        "limite_texto",
        "limite_booleano",
        "sem_limite",
        "limite_negativo_no_centro",
        "limiar_negativo",
        "limiar_texto",
        "limiar_booleano",
        "moeda_base_usd",
        "moeda_base_vazia",
        "moeda_base_numero",
        "periodicidade_mes",
        "periodicidade_numero",
        "sem_periodicidade",
        "categorias_iguais_depois_da_normalizacao",
        "centros_iguais_depois_da_normalizacao",
    ],
)
def test_rn015_documento_invalido_erro_geral(alteracoes):
    with pytest.raises(EntradaInvalida, match="política"):
        ler_politica(_politica(**alteracoes))


def test_rn015_documento_que_nao_e_objeto_erro_geral():
    with pytest.raises(EntradaInvalida):
        ler_politica("[]")


def test_rn015_moeda_base_normalizada():
    assert ler_politica(_politica(moeda_base=" brl ")).moeda_base == "BRL"


def test_rn015_centros_custo_vazio_aceito():
    assert ler_politica(_politica(centros_custo={})).centros == {}


def test_rn015_limite_zero_aceito():
    politica = ler_politica(_politica(padrao__hospedagem__limite=0))
    assert politica.padrao["hospedagem"] == Decimal("0")


def test_rn015_limite_inteiro_lido_como_decimal():
    politica = ler_politica(_politica(padrao__alimentacao__limite=60))
    assert isinstance(politica.padrao["alimentacao"], Decimal)


@pytest.mark.parametrize("periodicidade", ["Dia", " dia ", "DIARIA", " diaria "])
def test_rn015_periodicidade_normalizada(periodicidade):
    politica = ler_politica(_politica(padrao__alimentacao__periodicidade=periodicidade))
    assert politica.padrao["alimentacao"] == Decimal("60.00")


def test_rn015_chaves_de_categoria_e_centro_normalizadas():
    politica = ler_politica(
        _politica(
            padrao={" Alimentação ": {"limite": 60, "periodicidade": "dia"}},
            centros_custo={" Cc-Adm ": {"ALIMENTACAO": {"limite": 45, "periodicidade": "dia"}}},
        )
    )
    assert set(politica.padrao) == {"alimentacao"}
    assert politica.centros["cc-adm"].codigo == " Cc-Adm "
    assert set(politica.centros["cc-adm"].limites) == {"alimentacao"}


@pytest.mark.parametrize(
    "alteracoes",
    [
        {"acrescimo_em_viagem_percentual": "x"},
        {"versao": 4},
        {"vigencia": "julho"},
        {"observacao": ["x"]},
        {"padrao__alimentacao__observacao": 0},
        {"projeto": None},
    ],
    ids=[
        "acrescimo_texto",
        "versao_numero",
        "vigencia_texto",
        "observacao_lista",
        "observacao_na_categoria",
        "campo_desconhecido",
    ],
)
def test_rn015_campos_informativos_nao_validados(alteracoes):
    ler_politica(_politica(**alteracoes))
