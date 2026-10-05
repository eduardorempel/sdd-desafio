from decimal import Decimal

import pytest
from fabrica import despesa, documento, politica_aplicavel

from reembolso.modelo import Motivo, Status
from reembolso.motor import calcular


@pytest.mark.parametrize(
    ("categoria", "limite"),
    [("alimentacao", "60.00"), ("transporte_urbano", "80.00"), ("hospedagem", "250.00")],
)
def test_rn008_limite_por_categoria(categoria, limite):
    no_limite, acima = calcular(
        documento(
            despesa(1, data="2026-07-10", categoria=categoria, valor=limite),
            despesa(2, data="2026-07-11", categoria=categoria, valor="999.00"),
        ),
        politica_aplicavel(),
    )
    assert no_limite.status == Status.APROVADO
    assert no_limite.valor_reembolsavel == Decimal(limite)
    assert acima.status == Status.LIMITADO
    assert acima.valor_reembolsavel == Decimal(limite)


def test_rn008_d010_hospedagem_vale_uma_diaria():
    d010 = despesa(1, id="d-010", data="2026-07-14", categoria="hospedagem", valor="480.00")
    item = calcular(documento(d010), politica_aplicavel())[0]
    assert item.status == Status.LIMITADO
    assert item.motivo == Motivo.LIMITE_DIARIO
    assert item.valor_reembolsavel == Decimal("250.00")
    assert "RN-008" in item.justificativa


def test_rn008_d001_d002_soma_reembolsada_60():
    resultados = calcular(
        documento(
            despesa(1, id="d-001", data="2026-07-03", valor="72.50"),
            despesa(2, id="d-002", data="2026-07-03", valor="38.00"),
        ),
        politica_aplicavel(),
    )
    assert sum(r.valor_reembolsavel for r in resultados) == Decimal("60.00")


def test_rn008_limite_e_por_data_e_categoria():
    resultados = calcular(
        documento(
            despesa(1, data="2026-07-03", categoria="alimentacao", valor="60.00"),
            despesa(2, data="2026-07-03", categoria="transporte_urbano", valor="80.00"),
            despesa(3, data="2026-07-04", categoria="alimentacao", valor="60.00"),
        ),
        politica_aplicavel(),
    )
    assert [r.status for r in resultados] == [Status.APROVADO] * 3


def _transporte(posicao, id, valor, data="2026-07-06", tem_nota_fiscal=False):
    return despesa(
        posicao,
        id=id,
        data=data,
        categoria="transporte_urbano",
        valor=valor,
        tem_nota_fiscal=tem_nota_fiscal,
    )


def test_rn008_d003_recebe_limite_inteiro_com_d004_recusada():
    r003, r004 = calcular(
        documento(_transporte(1, "d-003", "100.00"), _transporte(2, "d-004", "100.01")),
        politica_aplicavel(),
    )
    assert r003.valor_reembolsavel == Decimal("80.00")
    assert r003.status == Status.LIMITADO
    assert r004.motivo == Motivo.NOTA_FISCAL_AUSENTE


def test_rn008_estorno_d009_nao_altera_outras_de_transporte():
    corrida = _transporte(1, "d-100", "80.00", data="2026-07-11", tem_nota_fiscal=True)
    estorno = _transporte(2, "d-009", "-45.00", data="2026-07-11")
    sem_estorno = calcular(documento(corrida), politica_aplicavel())[0]
    com_estorno, r009 = calcular(documento(corrida, estorno), politica_aplicavel())
    assert r009.motivo == Motivo.VALOR_NEGATIVO
    assert com_estorno == sem_estorno
    assert com_estorno.valor_reembolsavel == Decimal("80.00")


def test_rn008_limite_vem_do_documento():
    politica = politica_aplicavel(
        documento={
            "moeda_base": "BRL",
            "padrao": {"alimentacao": {"limite": 70.00, "periodicidade": "dia"}},
            "centros_custo": {},
            "nota_fiscal_obrigatoria_acima_de": 100.00,
        }
    )
    primeira, segunda = calcular(
        documento(
            despesa(1, data="2026-07-03", valor="50.00"),
            despesa(2, data="2026-07-03", valor="50.00"),
        ),
        politica,
    )
    assert primeira.valor_reembolsavel == Decimal("50.00")
    assert primeira.status == Status.APROVADO
    assert segunda.valor_reembolsavel == Decimal("20.00")
    assert segunda.status == Status.LIMITADO
    assert "R$ 70,00" in segunda.justificativa


@pytest.mark.parametrize("periodicidade", ["dia", "diaria"])
def test_rn008_dia_e_diaria_sao_limite_por_data(periodicidade):
    politica = politica_aplicavel(
        documento={
            "moeda_base": "BRL",
            "padrao": {"alimentacao": {"limite": 60, "periodicidade": periodicidade}},
            "centros_custo": {},
            "nota_fiscal_obrigatoria_acima_de": 100,
        }
    )
    resultados = calcular(
        documento(
            despesa(1, data="2026-07-03", valor="40.00"),
            despesa(2, data="2026-07-03", valor="40.00"),
            despesa(3, data="2026-07-04", valor="40.00"),
        ),
        politica,
    )
    assert [r.valor_reembolsavel for r in resultados] == [
        Decimal("40.00"),
        Decimal("20.00"),
        Decimal("40.00"),
    ]


@pytest.mark.parametrize(
    ("centro_custo", "categoria", "valor", "esperado"),
    [
        ("CC-COMERCIAL", "hospedagem", "1200.00", "400.00"),
        ("CC-COMERCIAL", "representacao", "340.00", "300.00"),
        ("CC-COMERCIAL", "alimentacao", "95.00", "90.00"),
        ("CC-ADM", "hospedagem", "300.00", "250.00"),
        ("CC-ADM", "alimentacao", "50.00", "45.00"),
        ("CC-SUPORTE-N2", "hospedagem", "310.00", "250.00"),
    ],
    ids=["e-007", "e-001", "e-008", "cc-adm_hospedagem_herdada", "cc-adm_alimentacao", "f-002"],
)
def test_rn008_limite_da_tabela_efetiva(centro_custo, categoria, valor, esperado):
    item = calcular(
        documento(despesa(1, categoria=categoria, valor=valor)), politica_aplicavel(centro_custo)
    )[0]
    assert item.status == Status.LIMITADO
    assert item.motivo == Motivo.LIMITE_DIARIO
    assert item.valor_reembolsavel == Decimal(esperado)


def test_rn008_e007_hospedagem_de_varias_noites_vale_uma_diaria():
    e007 = despesa(1, id="e-007", data="2026-07-22", categoria="hospedagem", valor="1200.00")
    item = calcular(documento(e007), politica_aplicavel("CC-COMERCIAL"))[0]
    assert item.valor_reembolsavel == Decimal("400.00")
    assert "R$ 400,00" in item.justificativa


def test_rn008_representacao_nao_divide_limite_com_alimentacao():
    jantar, representacao = calcular(
        documento(
            despesa(1, data="2026-07-13", categoria="alimentacao", valor="90.00"),
            despesa(2, data="2026-07-13", categoria="representacao", valor="300.00"),
        ),
        politica_aplicavel("CC-COMERCIAL"),
    )
    assert jantar.status == Status.APROVADO
    assert representacao.status == Status.APROVADO
    assert representacao.valor_reembolsavel == Decimal("300.00")


@pytest.mark.parametrize(
    ("centro_custo", "categoria", "valor", "origem"),
    [
        (
            "CC-ADM",
            "hospedagem",
            "300.00",
            "centro de custo CC-ADM usando limite herdado da política padrão",
        ),
        ("CC-ADM", "alimentacao", "50.00", "centro de custo CC-ADM"),
        (" cc-comercial ", "alimentacao", "95.00", "centro de custo CC-COMERCIAL"),
        (
            "CC-SUPORTE-N2",
            "hospedagem",
            "310.00",
            "política padrão; centro de custo CC-SUPORTE-N2 não cadastrado",
        ),
        (
            " CC-Suporte-N2 ",
            "hospedagem",
            "310.00",
            "política padrão; centro de custo CC-Suporte-N2 não cadastrado",
        ),
        (None, "alimentacao", "61.00", "política padrão"),
    ],
    ids=[
        "herdada",
        "centro",
        "centro_com_outra_grafia",
        "nao_cadastrado",
        "nao_cadastrado_com_espacos",
        "padrao",
    ],
)
def test_rn008_justificativa_cita_a_origem_do_limite(centro_custo, categoria, valor, origem):
    item = calcular(
        documento(despesa(1, categoria=categoria, valor=valor)), politica_aplicavel(centro_custo)
    )[0]
    assert item.status == Status.LIMITADO
    assert f"({origem})" in item.justificativa
    assert "RN-008" in item.justificativa
