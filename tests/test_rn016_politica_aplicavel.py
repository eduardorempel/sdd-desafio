from decimal import Decimal
from pathlib import Path

import pytest

from reembolso import justificativas
from reembolso.politica import Origem, TipoOrigem, ler_politica, politica_aplicavel

POLITICA_V4 = ler_politica(
    (Path(__file__).parent.parent / "exemplos" / "envelope" / "politica-v4.json").read_text(
        encoding="utf-8"
    )
)


def _regra(centro_custo, categoria):
    return politica_aplicavel(POLITICA_V4, centro_custo).regra(categoria)


@pytest.mark.parametrize("centro_custo", [None, "", "  "], ids=["ausente", "vazio", "espacos"])
def test_rn016_sem_centro_usa_padrao(centro_custo):
    assert _regra(centro_custo, "alimentacao") == (
        Decimal("60.00"),
        Origem(TipoOrigem.PADRAO, None),
    )


@pytest.mark.parametrize("centro_custo", ["CC-COMERCIAL", " cc-comercial ", "Cc-Comercial"])
def test_rn016_centro_cadastrado_com_grafia_do_documento(centro_custo):
    assert _regra(centro_custo, "alimentacao") == (
        Decimal("90.00"),
        Origem(TipoOrigem.CENTRO, "CC-COMERCIAL"),
    )


def test_rn016_centro_nao_cadastrado_usa_padrao():
    assert _regra("CC-SUPORTE-N2", "hospedagem") == (
        Decimal("250.00"),
        Origem(TipoOrigem.NAO_CADASTRADO, "CC-SUPORTE-N2"),
    )


def test_rn016_centro_nao_cadastrado_so_remove_espacos_das_pontas():
    assert _regra(" CC-Suporte-N2 ", "alimentacao") == (
        Decimal("60.00"),
        Origem(TipoOrigem.NAO_CADASTRADO, "CC-Suporte-N2"),
    )


def test_rn016_categoria_ausente_no_centro_herda_da_padrao():
    assert _regra("CC-ADM", "hospedagem") == (
        Decimal("250.00"),
        Origem(TipoOrigem.HERDADA, "CC-ADM"),
    )


def test_rn016_categoria_do_centro_usa_limite_do_centro():
    assert _regra("CC-ADM", "alimentacao") == (
        Decimal("45.00"),
        Origem(TipoOrigem.CENTRO, "CC-ADM"),
    )


def test_rn016_categoria_em_nenhuma_tabela_cita_o_centro():
    assert _regra("CC-ADM", "representacao") == (None, Origem(TipoOrigem.CENTRO, "CC-ADM"))


def test_rn016_limite_zero_do_centro_nao_herda():
    limite, origem = _regra("CC-ENG-PLATAFORMA", "hospedagem")
    assert limite == Decimal("0.00")
    assert origem == Origem(TipoOrigem.CENTRO, "CC-ENG-PLATAFORMA")


def test_rn016_representacao_no_comercial():
    assert _regra("CC-COMERCIAL", "representacao")[0] == Decimal("300.00")


def test_rn016_padrao_sem_representacao():
    assert _regra(None, "representacao") == (None, Origem(TipoOrigem.PADRAO, None))


def test_rn016_limiar_vem_do_documento():
    assert politica_aplicavel(POLITICA_V4, "CC-ADM").limiar_nota_fiscal == Decimal("100.00")


@pytest.mark.parametrize(
    "origem, texto",
    [
        (Origem(TipoOrigem.PADRAO, None), "política padrão"),
        (Origem(TipoOrigem.CENTRO, "CC-COMERCIAL"), "centro de custo CC-COMERCIAL"),
        (
            Origem(TipoOrigem.HERDADA, "CC-ADM"),
            "centro de custo CC-ADM usando limite herdado da política padrão",
        ),
        (
            Origem(TipoOrigem.NAO_CADASTRADO, "CC-SUPORTE-N2"),
            "política padrão; centro de custo CC-SUPORTE-N2 não cadastrado",
        ),
        (
            Origem(TipoOrigem.NAO_CADASTRADO, "CC-Suporte-N2"),
            "política padrão; centro de custo CC-Suporte-N2 não cadastrado",
        ),
    ],
    ids=["padrao", "centro", "herdada", "nao_cadastrado", "nao_cadastrado_grafia_original"],
)
def test_rn016_texto_da_origem(origem, texto):
    assert justificativas.origem(origem) == texto


def test_rn016_texto_da_origem_pela_selecao():
    _, origem = _regra(" cc-comercial ", "alimentacao")
    assert justificativas.origem(origem) == "centro de custo CC-COMERCIAL"
