import copy
import json
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from fabrica import cambio, contexto, despesa, documento, politica_aplicavel

from reembolso.cambio import ler_cambio
from reembolso.entrada import EntradaInvalida, ler_despesa
from reembolso.etapas import conversao
from reembolso.modelo import Despesa, Motivo, Recusa, Status
from reembolso.motor import calcular

CAMBIO = Path(__file__).parent.parent / "exemplos" / "envelope" / "cambio.json"

_REMOVER = object()


def _cambio(**alteracoes):
    """Câmbio pequeno e válido; `alteracoes` usa `__` como separador de caminho."""
    doc = copy.deepcopy(
        {
            "moeda_base": "BRL",
            "fonte": "teste",
            "taxas": {
                "2026-07-13": {"USD": 5.42, "EUR": 5.91},
                "2026-07-14": {"USD": 5.44},
            },
        }
    )
    for caminho, valor in alteracoes.items():
        alvo = doc
        *pais, campo = caminho.split("__")
        for pai in pais:
            alvo = alvo[pai]
        if valor is _REMOVER:
            del alvo[campo]
        else:
            alvo[campo] = valor
    return json.dumps(doc)


def test_rn018_documento_cambio_exemplo_aceito():
    cambio = ler_cambio(CAMBIO.read_text(encoding="utf-8"), "BRL")
    assert cambio.moeda_base == "BRL"
    assert set(cambio.taxas) == {"USD", "EUR"}
    assert len({data for lista in cambio.taxas.values() for data, _ in lista}) == 12
    assert cambio.taxas["EUR"][1] == (date(2026, 7, 14), Decimal("5.93"))


def test_rn018_documento_taxas_ordenadas_por_data():
    texto = _cambio(taxas={"2026-07-14": {"USD": 5.44}, "2026-07-13": {"USD": 5.42}})
    datas = [data for data, _ in ler_cambio(texto, "BRL").taxas["USD"]]
    assert datas == [date(2026, 7, 13), date(2026, 7, 14)]


def test_rn018_documento_taxa_sem_arredondamento():
    texto = _cambio(taxas={"2026-07-13": {"USD": 5.4219}})
    assert ler_cambio(texto, "BRL").taxas["USD"][0][1] == Decimal("5.4219")


@pytest.mark.parametrize(
    "texto",
    ['{"moeda_base": ', '{"moeda_base": "BRL", "taxas": NaN}', '{"x": Infinity}'],
    ids=["json_ilegivel", "nan", "infinity"],
)
def test_rn018_documento_ilegivel_erro_geral(texto):
    with pytest.raises(EntradaInvalida, match="câmbio"):
        ler_cambio(texto, "BRL")


@pytest.mark.parametrize(
    "alteracoes",
    [
        {"moeda_base": _REMOVER},
        {"taxas": _REMOVER},
        {"moeda_base": 986},
        {"moeda_base": ""},
        {"taxas": [{"USD": 5.42}]},
        {"moeda_base": "USD"},
        {"taxas__2026-7-13": {"USD": 5.42}},
        {"taxas__2026-02-30": {"USD": 5.42}},
        {"taxas__2026-07-13": [5.42]},
        {"taxas__2026-07-13__USD": 0},
        {"taxas__2026-07-13__USD": -5.42},
        {"taxas__2026-07-13__USD": "5,42"},
        {"taxas__2026-07-13__USD": True},
        {"taxas__2026-07-13__ usd ": 5.43},
    ],
    ids=[
        "sem_moeda_base",
        "sem_taxas",
        "moeda_base_numero",
        "moeda_base_vazia",
        "taxas_nao_e_objeto",
        "moeda_base_diferente_da_politica",
        "data_fora_do_formato",
        "data_inexistente",
        "taxas_da_data_nao_e_objeto",
        "taxa_zero",
        "taxa_negativa",
        "taxa_texto",
        "taxa_booleana",
        "moedas_iguais_depois_da_normalizacao",
    ],
)
def test_rn018_documento_invalido_erro_geral(alteracoes):
    with pytest.raises(EntradaInvalida, match="câmbio"):
        ler_cambio(_cambio(**alteracoes), "BRL")


def test_rn018_documento_que_nao_e_objeto_erro_geral():
    with pytest.raises(EntradaInvalida):
        ler_cambio("[]", "BRL")


def test_rn018_documento_campos_informativos_nao_validados():
    ler_cambio(_cambio(fonte=1, observacao=["x"], extra=None), "BRL")


def test_rn018_documento_codigo_de_moeda_normalizado():
    cambio = ler_cambio(_cambio(taxas={"2026-07-13": {" usd ": 5.42}}), "BRL")
    assert set(cambio.taxas) == {"USD"}


def test_rn018_documento_moeda_base_comparada_apos_normalizacao():
    assert ler_cambio(_cambio(moeda_base=" brl "), "BRL").moeda_base == "BRL"


@pytest.mark.parametrize(
    ("moeda", "data", "taxa", "data_cotacao"),
    [
        ("EUR", "2026-07-14", "5.93", "2026-07-14"),
        ("EUR", "2026-07-18", "5.96", "2026-07-17"),
        ("EUR", "2026-07-19", "5.96", "2026-07-17"),
        ("USD", "2026-07-20", "5.50", "2026-07-20"),
        ("USD", "2026-07-31", "5.51", "2026-07-28"),
    ],
    ids=["data_exata", "sabado", "domingo", "segunda", "lacuna_no_fim_do_mes"],
)
def test_rn018_cotacao_usa_data_anterior_mais_proxima(moeda, data, taxa, data_cotacao):
    assert cambio().cotacao(moeda, date.fromisoformat(data)) == (
        Decimal(taxa),
        date.fromisoformat(data_cotacao),
    )


@pytest.mark.parametrize(
    ("moeda", "data"),
    [("USD", "2026-07-10"), ("GBP", "2026-07-21"), ("USD", "2026-07-12")],
    ids=["antes_da_primeira_data", "moeda_sem_cotacao", "vespera_da_primeira_data"],
)
def test_rn018_cotacao_indisponivel(moeda, data):
    assert cambio().cotacao(moeda, date.fromisoformat(data)) is None


def _converter(moeda, valor, data, cambio_=None):
    d = despesa(1, data=data, valor=valor, moeda=moeda)
    return conversao(d, contexto(cambio=cambio_))


@pytest.mark.parametrize(
    ("moeda", "valor", "data", "taxa", "data_cotacao", "considerado"),
    [
        ("EUR", "22.00", "2026-07-14", "5.93", "2026-07-14", "130.46"),
        ("EUR", "30.00", "2026-07-18", "5.96", "2026-07-17", "178.80"),
        ("USD", "12.00", "2026-07-21", "5.48", "2026-07-21", "65.76"),
        ("USD", "33.333", "2026-07-13", "5.42", "2026-07-13", "180.66"),
    ],
    ids=["e-002", "e-004_sabado", "f-004", "arredondamento_cambial"],
)
def test_rn018_conversao_pela_data_da_despesa(moeda, valor, data, taxa, data_cotacao, considerado):
    convertida = _converter(moeda, valor, data, cambio())
    assert isinstance(convertida, Despesa)
    assert convertida.valor_considerado == Decimal(considerado)
    assert convertida.taxa_cambio == Decimal(taxa)
    assert convertida.data_cotacao == date.fromisoformat(data_cotacao)
    assert convertida.valor_informado == Decimal(valor)


def test_rn018_conversao_e002_no_resultado():
    e002 = despesa(1, id="e-002", data="2026-07-14", valor="22.00", moeda="EUR")
    item = calcular(documento(e002), politica_aplicavel("CC-COMERCIAL"), cambio())[0]
    assert item.valor_considerado == Decimal("130.46")
    assert item.taxa_cambio == Decimal("5.93")
    assert item.data_cotacao == date(2026, 7, 14)
    assert item.moeda == "EUR"
    assert item.valor_reembolsavel == Decimal("90.00")
    assert item.status == Status.LIMITADO


def test_rn018_conversao_e006_moeda_sem_cotacao():
    e006 = despesa(
        1, id="e-006", data="2026-07-21", categoria="representacao", valor="55.00", moeda="GBP"
    )
    item = calcular(documento(e006), politica_aplicavel("CC-COMERCIAL"), cambio())[0]
    assert item.status == Status.RECUSADO
    assert item.motivo == Motivo.COTACAO_INDISPONIVEL
    assert item.valor_reembolsavel == Decimal("0.00")
    assert item.valor_considerado is None
    assert item.taxa_cambio is None
    assert item.data_cotacao is None
    assert item.moeda == "GBP"
    assert "GBP" in item.justificativa
    assert "2026-07-21" in item.justificativa
    assert "RN-018" in item.justificativa


def test_rn018_conversao_antes_da_primeira_cotacao_indisponivel():
    recusa = _converter("USD", "10.00", "2026-07-10", cambio())
    assert isinstance(recusa, Recusa)
    assert recusa.motivo == Motivo.COTACAO_INDISPONIVEL


def test_rn018_conversao_sem_documento_de_cambio():
    resultados = calcular(
        documento(
            despesa(1, data="2026-07-13", valor="10.00", moeda="USD"),
            despesa(2, data="2026-07-13", valor="20.00"),
        ),
        politica_aplicavel(),
    )
    assert resultados[0].motivo == Motivo.COTACAO_INDISPONIVEL
    assert resultados[0].valor_considerado is None
    assert resultados[1].status == Status.APROVADO
    assert resultados[1].valor_reembolsavel == Decimal("20.00")


def test_rn018_conversao_brl_nao_consulta_o_cambio():
    # Sábado, sem cotação no documento; em BRL o câmbio nem é consultado.
    brl = despesa(1, data="2026-07-18", valor="47.20")
    assert _converter("BRL", "47.20", "2026-07-18", cambio()) == brl
    assert _converter("BRL", "47.20", "2026-07-18") == brl
    item = calcular(documento(brl), politica_aplicavel())[0]
    assert item.status == Status.APROVADO
    assert item.taxa_cambio is None
    assert item.data_cotacao is None


def test_rn018_conversao_estorno_em_moeda_sem_cotacao():
    item = calcular(
        documento(despesa(1, data="2026-07-21", valor="-10.00", moeda="GBP")),
        politica_aplicavel(),
        cambio(),
    )[0]
    assert item.motivo == Motivo.COTACAO_INDISPONIVEL


def test_rn018_conversao_estorno_em_moeda_estrangeira():
    item = calcular(
        documento(despesa(1, data="2026-07-13", valor="-10.00", moeda="USD")),
        politica_aplicavel(),
        cambio(),
    )[0]
    assert item.valor_considerado == Decimal("-54.20")
    assert item.motivo == Motivo.VALOR_NEGATIVO


def test_rn018_conversao_vem_antes_do_periodo():
    item = calcular(
        documento(despesa(1, data="2026-06-10", valor="10.00", moeda="USD")),
        politica_aplicavel(),
        cambio(),
    )[0]
    assert item.motivo == Motivo.COTACAO_INDISPONIVEL


def test_rn018_conversao_despesa_brl_da_entrada_igual_a_v3():
    item = {
        "id": "d-011",
        "data": "2026-07-03",
        "categoria": "alimentacao",
        "fornecedor": "Padaria",
        "valor": Decimal("33.333"),
        "tem_nota_fiscal": True,
    }
    lida = ler_despesa(item, posicao=1)
    assert lida.valor_considerado == Decimal("33.33")
    assert conversao(lida, contexto()) is lida


def test_rn018_conversao_despesa_estrangeira_da_entrada_chega_sem_valor_considerado():
    item = {
        "id": "e-002",
        "data": "2026-07-14",
        "categoria": "alimentacao",
        "fornecedor": "Taberna",
        "valor": Decimal("22.00"),
        "moeda": "eur",
        "tem_nota_fiscal": True,
    }
    lida = ler_despesa(item, posicao=1)
    assert lida.valor_considerado is None
    assert conversao(lida, contexto(cambio=cambio())).valor_considerado == Decimal("130.46")
