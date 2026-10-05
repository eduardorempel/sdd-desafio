from decimal import Decimal

from fabrica import despesa, documento, politica_aplicavel

from reembolso.modelo import Motivo, Status
from reembolso.motor import calcular


def test_rn009_d001_d002_consumo_pela_posicao():
    d001, d002 = calcular(
        documento(
            despesa(1, id="d-001", data="2026-07-03", valor="72.50"),
            despesa(2, id="d-002", data="2026-07-03", valor="38.00"),
        ),
        politica_aplicavel(),
    )
    assert d001.valor_reembolsavel == Decimal("60.00")
    assert d001.status == Status.LIMITADO
    assert d002.valor_reembolsavel == Decimal("0.00")
    assert d002.status == Status.LIMITADO
    assert d002.motivo == Motivo.LIMITE_DIARIO


def test_rn009_ordem_da_posicao_e_nao_do_valor():
    menor, maior = calcular(
        documento(
            despesa(1, data="2026-07-03", valor="38.00"),
            despesa(2, data="2026-07-03", valor="72.50"),
        ),
        politica_aplicavel(),
    )
    assert menor.valor_reembolsavel == Decimal("38.00")
    assert menor.status == Status.APROVADO
    assert maior.valor_reembolsavel == Decimal("22.00")
    assert maior.status == Status.LIMITADO


def test_rn009_duas_hospedagens_na_mesma_data():
    primeira, segunda = calcular(
        documento(
            despesa(1, data="2026-07-14", categoria="hospedagem", valor="200.00"),
            despesa(2, data="2026-07-14", categoria="hospedagem", valor="150.00"),
        ),
        politica_aplicavel(),
    )
    assert primeira.valor_reembolsavel == Decimal("200.00")
    assert primeira.status == Status.APROVADO
    assert segunda.valor_reembolsavel == Decimal("50.00")
    assert segunda.status == Status.LIMITADO


def test_rn009_justificativa_cita_despesa_que_consumiu():
    _, d002 = calcular(
        documento(
            despesa(1, id="d-001", data="2026-07-03", valor="72.50"),
            despesa(2, id="d-002", data="2026-07-03", valor="38.00"),
        ),
        politica_aplicavel(),
    )
    assert "R$ 60,00" in d002.justificativa
    assert "d-001" in d002.justificativa
    assert "RN-009" in d002.justificativa


def test_rn009_justificativa_cita_valor_consumido_e_todas_as_consumidoras():
    *_, terceira = calcular(
        documento(
            despesa(1, id="h-1", data="2026-07-14", categoria="hospedagem", valor="100.00"),
            despesa(2, id="h-2", data="2026-07-14", categoria="hospedagem", valor="100.00"),
            despesa(3, id="h-3", data="2026-07-14", categoria="hospedagem", valor="150.00"),
        ),
        politica_aplicavel(),
    )
    assert terceira.valor_reembolsavel == Decimal("50.00")
    assert "R$ 250,00" in terceira.justificativa
    assert "R$ 200,00" in terceira.justificativa
    assert "h-1" in terceira.justificativa
    assert "h-2" in terceira.justificativa
    assert "RN-009" in terceira.justificativa
    assert "RN-010" in terceira.justificativa


def test_rn009_justificativa_nao_cita_despesa_que_nao_consumiu():
    *_, terceira = calcular(
        documento(
            despesa(1, id="a-1", data="2026-07-03", valor="60.00"),
            despesa(2, id="a-2", data="2026-07-03", valor="5.00"),
            despesa(3, id="a-3", data="2026-07-03", valor="5.00"),
        ),
        politica_aplicavel(),
    )
    assert "a-1" in terceira.justificativa
    assert "a-2" not in terceira.justificativa


def test_rn009_despesa_zero_depois_do_limite_consumido_e_aprovada():
    _, zero = calcular(
        documento(
            despesa(1, data="2026-07-03", valor="60.00"),
            despesa(2, data="2026-07-03", valor="0.00"),
        ),
        politica_aplicavel(),
    )
    assert zero.status == Status.APROVADO
    assert zero.valor_reembolsavel == Decimal("0.00")


def test_rn009_d001_d002_no_centro_eng_plataforma():
    d001, d002 = calcular(
        documento(
            despesa(1, id="d-001", data="2026-07-03", valor="72.50"),
            despesa(2, id="d-002", data="2026-07-03", valor="38.00"),
        ),
        politica_aplicavel("CC-ENG-PLATAFORMA"),
    )
    assert d001.valor_reembolsavel == Decimal("72.50")
    assert d001.status == Status.APROVADO
    assert d002.valor_reembolsavel == Decimal("2.50")
    assert d002.status == Status.LIMITADO
    assert "R$ 75,00" in d002.justificativa
    assert "R$ 72,50" in d002.justificativa
    assert "d-001" in d002.justificativa
    assert "(centro de custo CC-ENG-PLATAFORMA)" in d002.justificativa
    assert "RN-009" in d002.justificativa


def test_rn009_justificativa_de_limite_ja_consumido_cita_a_origem():
    *_, terceira = calcular(
        documento(
            despesa(1, id="a-1", data="2026-07-03", valor="45.00"),
            despesa(2, id="a-2", data="2026-07-03", valor="5.00"),
        ),
        politica_aplicavel("CC-ADM"),
    )
    assert terceira.valor_reembolsavel == Decimal("0.00")
    assert "(centro de custo CC-ADM)" in terceira.justificativa
    assert "a-1" in terceira.justificativa
