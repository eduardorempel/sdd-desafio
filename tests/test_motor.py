from decimal import Decimal

from fabrica import cambio, despesa, documento, invalida, politica_aplicavel

from reembolso.etapas import Contexto
from reembolso.justificativas import reais
from reembolso.modelo import Corte, Motivo, Recusa, Status
from reembolso.motor import ETAPAS, Conversao, EmGrupo, PorItem, calcular


def _recusa_posicao(posicao):
    def regra(d, _doc):
        return Recusa(Motivo.VALOR_NEGATIVO, "teste (RN-005)") if d.posicao == posicao else None

    return regra


def _registra(vistas):
    def regra(vivas, _doc):
        vistas.extend(d.posicao for d in vivas)
        return {}

    return regra


def _corta_para(valor):
    def regra(vivas, _doc):
        return {
            d.posicao: Corte(Decimal(valor), Motivo.LIMITE_DIARIO, "corte (RN-008)") for d in vivas
        }

    return regra


def test_secao8_recusada_nao_chega_a_etapa_seguinte():
    vistas = []
    resultados = calcular(
        documento(despesa(1), despesa(2), despesa(3)),
        politica_aplicavel(),
        etapas=[PorItem(_recusa_posicao(2)), EmGrupo(_registra(vistas))],
    )
    assert vistas == [1, 3]
    assert resultados[1].status == Status.RECUSADO
    assert resultados[1].motivo == Motivo.VALOR_NEGATIVO
    assert resultados[1].valor_reembolsavel == Decimal("0.00")
    assert resultados[1].valor_considerado == Decimal("10.00")


def test_secao8_primeira_etapa_que_falha_define_o_motivo():
    def recusa_todas(_d, _doc):
        return Recusa(Motivo.FORA_DO_PERIODO, "teste (RN-004)")

    resultados = calcular(
        documento(despesa(1)),
        politica_aplicavel(),
        etapas=[PorItem(_recusa_posicao(1)), PorItem(recusa_todas)],
    )
    assert resultados[0].motivo == Motivo.VALOR_NEGATIVO


def test_secao8_invalida_vira_dados_invalidos():
    vistas = []
    resultados = calcular(
        documento(invalida(1, valor="50.00"), despesa(2)),
        politica_aplicavel(),
        etapas=[EmGrupo(_registra(vistas))],
    )
    item = resultados[0]
    assert vistas == [2]
    assert item.status == Status.RECUSADO
    assert item.motivo == Motivo.DADOS_INVALIDOS
    assert item.valor_reembolsavel == Decimal("0.00")
    assert item.valor_considerado is None
    assert item.valor_informado == Decimal("50.00")
    assert item.id == "d-x"
    assert "RN-013" in item.justificativa


def test_secao8_invalida_com_id_nulo():
    assert calcular(documento(invalida(1, id=None)), politica_aplicavel(), etapas=[])[0].id is None


def test_secao8_resultado_na_ordem_da_entrada():
    resultados = calcular(
        documento(despesa(1), invalida(2), despesa(3), despesa(4)),
        politica_aplicavel(),
        etapas=[PorItem(_recusa_posicao(3))],
    )
    assert [r.id for r in resultados] == ["d-001", "d-x", "d-003", "d-004"]


def test_secao8_sem_corte_e_aprovado_com_valor_considerado():
    item = calcular(documento(despesa(1, valor="33.333")), politica_aplicavel(), etapas=[])[0]
    assert item.status == Status.APROVADO
    assert item.motivo is None
    assert item.valor_reembolsavel == Decimal("33.33")
    assert "RN-" in item.justificativa


def test_secao8_corte_menor_que_considerado_e_limitado():
    item = calcular(
        documento(despesa(1)), politica_aplicavel(), etapas=[EmGrupo(_corta_para("5.00"))]
    )[0]
    assert item.status == Status.LIMITADO
    assert item.motivo == Motivo.LIMITE_DIARIO
    assert item.valor_reembolsavel == Decimal("5.00")
    assert item.justificativa == "corte (RN-008)"


def test_secao8_corte_igual_ao_considerado_e_aprovado():
    item = calcular(
        documento(despesa(1)), politica_aplicavel(), etapas=[EmGrupo(_corta_para("10.00"))]
    )[0]
    assert item.status == Status.APROVADO
    assert item.motivo is None


def test_secao8_documento_sem_despesas():
    assert calcular(documento(), politica_aplicavel(), etapas=[]) == []


def test_dt008_formata_reais():
    assert reais(Decimal("60")) == "R$ 60,00"
    assert reais(Decimal("12.5")) == "R$ 12,50"
    assert reais(Decimal("1234.56")) == "R$ 1.234,56"


def test_dt009_etapas_recebem_contexto():
    recebidos = []

    def por_item(d, ctx):
        recebidos.append(ctx)

    def em_grupo(vivas, ctx):
        recebidos.append(ctx)
        return {}

    doc = documento(despesa(1))
    politica = politica_aplicavel("CC-COMERCIAL")
    calcular(doc, politica, etapas=[PorItem(por_item), EmGrupo(em_grupo)])
    assert len(recebidos) == 2
    assert all(isinstance(ctx, Contexto) for ctx in recebidos)
    assert all(ctx.documento is doc for ctx in recebidos)
    assert all(ctx.politica is politica for ctx in recebidos)
    assert all(ctx.cambio is None for ctx in recebidos)


def test_dt010_conversao_e_a_primeira_etapa():
    assert isinstance(ETAPAS[0], Conversao)
    assert not any(isinstance(etapa, Conversao) for etapa in ETAPAS[1:])


def test_dt010_nenhuma_despesa_chega_a_etapa_4_sem_valor_considerado():
    vistas = []
    calcular(
        documento(
            despesa(1, data="2026-07-14", valor="22.00", moeda="EUR"),
            despesa(2, data="2026-07-21", valor="55.00", moeda="GBP"),
            despesa(3, data="2026-07-18", valor="47.20"),
        ),
        politica_aplicavel(),
        cambio(),
        etapas=[ETAPAS[0], EmGrupo(lambda vivas, _ctx: vistas.extend(vivas) or {})],
    )
    assert [d.posicao for d in vistas] == [1, 3]
    assert all(d.valor_considerado is not None for d in vistas)
    assert vistas[0].valor_considerado == Decimal("130.46")
