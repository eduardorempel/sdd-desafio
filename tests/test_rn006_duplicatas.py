from decimal import Decimal

from fabrica import despesa, documento, invalida

from reembolso.modelo import Motivo, Status
from reembolso.motor import calcular


def _bistro(posicao, id, **campos):
    base = {"data": "2026-07-09", "fornecedor": "Bistro Central", "valor": "54.90"}
    return despesa(posicao, id=id, **{**base, **campos})


def test_rn006_d006_d007_ambas_com_nota_mantem_a_primeira():
    d006, d007 = calcular(documento(_bistro(1, "d-006"), _bistro(2, "d-007")))
    assert d006.status == Status.APROVADO
    assert d006.valor_reembolsavel == Decimal("54.90")
    assert d007.status == Status.RECUSADO
    assert d007.motivo == Motivo.DUPLICATA
    assert d007.valor_reembolsavel == Decimal("0.00")
    assert "RN-006" in d007.justificativa
    assert "d-006" in d007.justificativa


def test_rn006_so_a_segunda_tem_nota_mantem_a_segunda():
    primeira, segunda = calcular(
        documento(_bistro(1, "d-a", tem_nota_fiscal=False), _bistro(2, "d-b", tem_nota_fiscal=True))
    )
    assert primeira.motivo == Motivo.DUPLICATA
    assert "d-b" in primeira.justificativa
    assert segunda.status == Status.APROVADO


def test_rn006_nenhuma_com_nota_mantem_a_primeira():
    primeira, segunda = calcular(
        documento(
            _bistro(1, "d-a", tem_nota_fiscal=False), _bistro(2, "d-b", tem_nota_fiscal=False)
        )
    )
    assert primeira.status == Status.APROVADO
    assert segunda.motivo == Motivo.DUPLICATA


def test_rn006_entre_varias_com_nota_mantem_a_de_menor_posicao():
    resultados = calcular(
        documento(
            _bistro(1, "d-a", tem_nota_fiscal=False),
            _bistro(2, "d-b", tem_nota_fiscal=True),
            _bistro(3, "d-c", tem_nota_fiscal=True),
        )
    )
    assert [r.motivo for r in resultados] == [Motivo.DUPLICATA, None, Motivo.DUPLICATA]
    assert all("d-b" in r.justificativa for r in (resultados[0], resultados[2]))
    assert not any("d-a" in r.justificativa or "d-c" in r.justificativa for r in resultados)


def test_rn006_fornecedor_com_grafia_diferente_e_duplicata():
    _, segunda = calcular(
        documento(_bistro(1, "d-a"), _bistro(2, "d-b", fornecedor="BISTRO CENTRAL "))
    )
    assert segunda.motivo == Motivo.DUPLICATA


def test_rn006_valor_comparado_apos_arredondamento():
    _, segunda = calcular(documento(_bistro(1, "d-a"), _bistro(2, "d-b", valor="54.899")))
    assert segunda.motivo == Motivo.DUPLICATA


def test_rn006_id_e_descricao_nao_participam():
    # O modelo não carrega descrição (RN-014); ids diferentes não impedem a duplicata.
    _, segunda = calcular(documento(_bistro(1, "x-1"), _bistro(2, "y-2")))
    assert segunda.motivo == Motivo.DUPLICATA


def test_rn006_qualquer_campo_diferente_nao_e_duplicata():
    resultados = calcular(
        documento(
            _bistro(1, "d-a"),
            _bistro(2, "d-b", data="2026-07-10"),
            _bistro(3, "d-c", fornecedor="Bistro Centro"),
            _bistro(4, "d-d", valor="54.91"),
            _bistro(5, "d-e", categoria="transporte_urbano"),
        )
    )
    assert all(r.motivo != Motivo.DUPLICATA for r in resultados)


def test_rn006_despesa_recusada_antes_nao_entra_no_grupo():
    # A primeira tem dados inválidos (RN-013) e não participa; a segunda fica sozinha no grupo.
    resultados = calcular(documento(invalida(1, id="d-a", valor="54.90"), _bistro(2, "d-b")))
    assert resultados[0].motivo == Motivo.DADOS_INVALIDOS
    assert resultados[1].status == Status.APROVADO
