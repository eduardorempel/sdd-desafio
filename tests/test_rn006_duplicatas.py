from decimal import Decimal

from fabrica import cambio, despesa, documento, invalida, politica_aplicavel

from reembolso.modelo import Motivo, Status
from reembolso.motor import calcular


def _bistro(posicao, id, **campos):
    base = {"data": "2026-07-09", "fornecedor": "Bistro Central", "valor": "54.90"}
    return despesa(posicao, id=id, **{**base, **campos})


def test_rn006_d006_d007_ambas_com_nota_mantem_a_primeira():
    d006, d007 = calcular(documento(_bistro(1, "d-006"), _bistro(2, "d-007")), politica_aplicavel())
    assert d006.status == Status.APROVADO
    assert d006.valor_reembolsavel == Decimal("54.90")
    assert d007.status == Status.RECUSADO
    assert d007.motivo == Motivo.DUPLICATA
    assert d007.valor_reembolsavel == Decimal("0.00")
    assert "RN-006" in d007.justificativa
    assert "d-006" in d007.justificativa


def test_rn006_so_a_segunda_tem_nota_mantem_a_segunda():
    primeira, segunda = calcular(
        documento(
            _bistro(1, "d-a", tem_nota_fiscal=False), _bistro(2, "d-b", tem_nota_fiscal=True)
        ),
        politica_aplicavel(),
    )
    assert primeira.motivo == Motivo.DUPLICATA
    assert "d-b" in primeira.justificativa
    assert segunda.status == Status.APROVADO


def test_rn006_nenhuma_com_nota_mantem_a_primeira():
    primeira, segunda = calcular(
        documento(
            _bistro(1, "d-a", tem_nota_fiscal=False), _bistro(2, "d-b", tem_nota_fiscal=False)
        ),
        politica_aplicavel(),
    )
    assert primeira.status == Status.APROVADO
    assert segunda.motivo == Motivo.DUPLICATA


def test_rn006_entre_varias_com_nota_mantem_a_de_menor_posicao():
    resultados = calcular(
        documento(
            _bistro(1, "d-a", tem_nota_fiscal=False),
            _bistro(2, "d-b", tem_nota_fiscal=True),
            _bistro(3, "d-c", tem_nota_fiscal=True),
        ),
        politica_aplicavel(),
    )
    assert [r.motivo for r in resultados] == [Motivo.DUPLICATA, None, Motivo.DUPLICATA]
    assert all("d-b" in r.justificativa for r in (resultados[0], resultados[2]))
    assert not any("d-a" in r.justificativa or "d-c" in r.justificativa for r in resultados)


def test_rn006_fornecedor_com_grafia_diferente_e_duplicata():
    _, segunda = calcular(
        documento(_bistro(1, "d-a"), _bistro(2, "d-b", fornecedor="BISTRO CENTRAL ")),
        politica_aplicavel(),
    )
    assert segunda.motivo == Motivo.DUPLICATA


def test_rn006_valor_comparado_apos_arredondamento():
    _, segunda = calcular(
        documento(_bistro(1, "d-a"), _bistro(2, "d-b", valor="54.899")), politica_aplicavel()
    )
    assert segunda.motivo == Motivo.DUPLICATA


def test_rn006_id_e_descricao_nao_participam():
    # O modelo não carrega descrição (RN-014); ids diferentes não impedem a duplicata.
    _, segunda = calcular(documento(_bistro(1, "x-1"), _bistro(2, "y-2")), politica_aplicavel())
    assert segunda.motivo == Motivo.DUPLICATA


def test_rn006_qualquer_campo_diferente_nao_e_duplicata():
    resultados = calcular(
        documento(
            _bistro(1, "d-a"),
            _bistro(2, "d-b", data="2026-07-10"),
            _bistro(3, "d-c", fornecedor="Bistro Centro"),
            _bistro(4, "d-d", valor="54.91"),
            _bistro(5, "d-e", categoria="transporte_urbano"),
        ),
        politica_aplicavel(),
    )
    assert all(r.motivo != Motivo.DUPLICATA for r in resultados)


def test_rn006_despesa_recusada_antes_nao_entra_no_grupo():
    # A primeira tem dados inválidos (RN-013) e não participa; a segunda fica sozinha no grupo.
    resultados = calcular(
        documento(invalida(1, id="d-a", valor="54.90"), _bistro(2, "d-b")), politica_aplicavel()
    )
    assert resultados[0].motivo == Motivo.DADOS_INVALIDOS
    assert resultados[1].status == Status.APROVADO


def _taberna(posicao, id, valor="22.00", moeda="EUR"):
    return despesa(
        posicao, id=id, data="2026-07-14", fornecedor="Taberna do Chiado", valor=valor, moeda=moeda
    )


def _calcular(*despesas):
    return calcular(documento(*despesas), politica_aplicavel("CC-COMERCIAL"), cambio())


def test_rn006_mesma_moeda_estrangeira_e_duplicata():
    _, segunda = _calcular(_taberna(1, "e-a"), _taberna(2, "e-b"))
    assert segunda.status == Status.RECUSADO
    assert segunda.motivo == Motivo.DUPLICATA
    assert "e-a" in segunda.justificativa


def test_rn006_mesmo_valor_em_reais_e_moedas_diferentes_nao_e_duplicata():
    eur, brl = _calcular(_taberna(1, "e-a"), _taberna(2, "e-b", valor="130.46", moeda="BRL"))
    assert eur.valor_considerado == brl.valor_considerado == Decimal("130.46")
    assert brl.motivo != Motivo.DUPLICATA


def test_rn006_mesmo_valor_original_e_moedas_diferentes_nao_e_duplicata():
    _, usd = _calcular(_taberna(1, "e-a"), _taberna(2, "e-b", moeda="USD"))
    assert usd.motivo != Motivo.DUPLICATA


def test_rn006_valor_original_comparado_arredondado_na_moeda_original():
    # 22,004 EUR e 22,00 EUR dão 130,49 e 130,46 em reais, mas são o mesmo valor original.
    primeira, segunda = _calcular(_taberna(1, "e-a", valor="22.004"), _taberna(2, "e-b"))
    assert primeira.valor_considerado != Decimal("130.46")
    assert segunda.motivo == Motivo.DUPLICATA


def test_rn006_cotacao_indisponivel_nao_entra_no_grupo():
    resultados = _calcular(_taberna(1, "g-a", moeda="GBP"), _taberna(2, "g-b", moeda="GBP"))
    assert [r.motivo for r in resultados] == [Motivo.COTACAO_INDISPONIVEL] * 2
