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
    assert "política padrão" in item.justificativa


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


def _recusa(centro_custo, nome, politica=None):
    politica = politica or politica_aplicavel(centro_custo)
    return categoria(despesa(1, categoria=nome), contexto(politica=politica))


def test_rn001_d010_hospedagem_com_limite_zero_recusada():
    d010 = despesa(1, id="d-010", data="2026-07-14", categoria="hospedagem", valor="480.00")
    item = calcular(documento(d010), politica_aplicavel("CC-ENG-PLATAFORMA"))[0]
    assert item.status == Status.RECUSADO
    assert item.motivo == Motivo.CATEGORIA_NAO_REEMBOLSAVEL
    assert item.valor_reembolsavel == Decimal("0.00")
    assert "RN-001" in item.justificativa
    assert "centro de custo CC-ENG-PLATAFORMA" in item.justificativa


def test_rn001_d013_limite_zero_vem_antes_da_nota_fiscal():
    d013 = despesa(1, id="d-013", categoria="hospedagem", valor="690.00", tem_nota_fiscal=False)
    item = calcular(documento(d013), politica_aplicavel("CC-ENG-PLATAFORMA"))[0]
    assert item.motivo == Motivo.CATEGORIA_NAO_REEMBOLSAVEL


def test_rn001_f003_representacao_na_padrao_recusada():
    recusa = _recusa("CC-SUPORTE-N2", "representacao")
    assert recusa.motivo == Motivo.CATEGORIA_NAO_REEMBOLSAVEL
    assert "política padrão; centro de custo CC-SUPORTE-N2 não cadastrado" in recusa.justificativa


def test_rn001_e001_representacao_no_comercial_passa():
    assert _recusa("CC-COMERCIAL", "representacao") is None


def test_rn001_hospedagem_no_adm_passa_por_heranca():
    assert _recusa("CC-ADM", "hospedagem") is None


@pytest.mark.parametrize(
    "padrao, centro, centro_custo, nome",
    [
        ({"alimentacao": 0}, {}, None, "alimentacao"),
        ({"alimentacao": 60}, {"transporte_urbano": 0}, "CC-X", "transporte_urbano"),
        ({"alimentacao": 0}, {"transporte_urbano": 50}, "CC-X", "alimentacao"),
    ],
    ids=["padrao", "centro", "herdada_da_padrao"],
)
def test_rn001_limite_zero_em_qualquer_tabela_recusado(padrao, centro, centro_custo, nome):
    def tabela(limites):
        return {c: {"limite": v, "periodicidade": "dia"} for c, v in limites.items()}

    politica = politica_aplicavel(
        centro_custo,
        documento={
            "moeda_base": "BRL",
            "padrao": tabela(padrao),
            "centros_custo": {"CC-X": tabela(centro)},
            "nota_fiscal_obrigatoria_acima_de": 100,
        },
    )
    assert _recusa(centro_custo, nome, politica).motivo == Motivo.CATEGORIA_NAO_REEMBOLSAVEL


def test_rn001_observacao_nao_e_usada():
    politica = politica_aplicavel(
        documento={
            "moeda_base": "BRL",
            "padrao": {
                "alimentacao": {
                    "limite": 60,
                    "periodicidade": "dia",
                    "observacao": "nao reembolsavel",
                }
            },
            "centros_custo": {},
            "nota_fiscal_obrigatoria_acima_de": 100,
        }
    )
    assert _recusa(None, "alimentacao", politica) is None


@pytest.mark.parametrize(
    "centro_custo, nome, origem",
    [
        ("CC-ENG-PLATAFORMA", "hospedagem", "centro de custo CC-ENG-PLATAFORMA"),
        (" cc-eng-plataforma ", "hospedagem", "centro de custo CC-ENG-PLATAFORMA"),
        (
            " CC-Suporte-N2 ",
            "representacao",
            "política padrão; centro de custo CC-Suporte-N2 não cadastrado",
        ),
        ("CC-ADM", "representacao", "centro de custo CC-ADM"),
        (None, "coworking", "política padrão"),
    ],
    ids=["centro", "centro_com_outra_grafia", "nao_cadastrado_com_espacos", "em_nenhuma", "padrao"],
)
def test_rn001_justificativa_cita_a_origem(centro_custo, nome, origem):
    justificativa = _recusa(centro_custo, nome).justificativa
    assert "RN-001" in justificativa
    assert f"({origem})" in justificativa


def test_rn001_justificativa_cita_heranca_com_limite_zero_na_padrao():
    politica = politica_aplicavel(
        "CC-ADM",
        documento={
            "moeda_base": "BRL",
            "padrao": {"hospedagem": {"limite": 0, "periodicidade": "diaria"}},
            "centros_custo": {"CC-ADM": {"alimentacao": {"limite": 45, "periodicidade": "dia"}}},
            "nota_fiscal_obrigatoria_acima_de": 100,
        },
    )
    recusa = _recusa("CC-ADM", "hospedagem", politica)
    assert recusa.motivo == Motivo.CATEGORIA_NAO_REEMBOLSAVEL
    assert "centro de custo CC-ADM usando limite herdado da política padrão" in recusa.justificativa
