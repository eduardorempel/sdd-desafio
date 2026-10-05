import json
from datetime import date
from decimal import Decimal

from fabrica import cambio, despesa, documento, invalida, politica_aplicavel

from reembolso.modelo import Motivo, Resultado, Status
from reembolso.motor import calcular
from reembolso.saida import montar_saida, serializar


def _resultado(**campos):
    base = {
        "id": "d-001",
        "valor_informado": Decimal("60"),
        "valor_considerado": Decimal("60.00"),
        "valor_reembolsavel": Decimal("60.00"),
        "status": Status.APROVADO,
        "motivo": None,
        "justificativa": "ok (RN-008)",
    }
    return Resultado(**{**base, **campos})


def _texto(*resultados, doc=None):
    return serializar(montar_saida(doc or documento(), list(resultados)))


def test_dt005_valores_monetarios_com_duas_casas():
    texto = _texto(
        _resultado(
            valor_considerado=Decimal("60"),
            valor_reembolsavel=Decimal("60"),
        )
    )
    assert '"valor_considerado": 60.00' in texto
    assert '"valor_reembolsavel": 60.00' in texto
    assert '"total_reembolsavel": 60.00' in texto


def test_dt005_valor_informado_sem_quantizar():
    texto = _texto(_resultado(valor_informado=Decimal("33.333")))
    assert '"valor_informado": 33.333' in texto


def test_dt005_valor_informado_inteiro_sai_como_numero():
    assert '"valor_informado": 60,' in _texto(_resultado(valor_informado=Decimal("60")))


def test_dt005_motivo_nulo_em_item_aprovado():
    item = json.loads(_texto(_resultado()))["itens"][0]
    assert item["status"] == "aprovado"
    assert item["motivo"] is None


def test_dt005_nulos_em_dados_invalidos():
    resultados = calcular(documento(invalida(1, id=None, valor=None)), politica_aplicavel())
    item = json.loads(_texto(*resultados))["itens"][0]
    assert item["id"] is None
    assert item["valor_informado"] is None
    assert item["valor_considerado"] is None
    assert item["moeda"] is None
    assert item["taxa_cambio"] is None
    assert item["data_cotacao"] is None
    assert item["valor_reembolsavel"] == 0
    assert item["motivo"] == Motivo.DADOS_INVALIDOS.value


def test_dt005_total_e_a_soma_dos_itens():
    resultados = calcular(
        documento(
            despesa(1, valor="33.333"),
            despesa(2, valor="10.005", data="2026-07-11"),
            despesa(3, valor="-45.00", data="2026-07-12"),
        ),
        politica_aplicavel(),
    )
    saida = json.loads(_texto(*resultados), parse_float=Decimal)
    assert saida["total_reembolsavel"] == Decimal("43.34")
    assert saida["total_reembolsavel"] == sum(i["valor_reembolsavel"] for i in saida["itens"])


def test_dt005_sem_itens_total_zero():
    texto = _texto()
    assert '"itens": []' in texto
    assert '"total_reembolsavel": 0.00' in texto


def test_dt005_colaborador_e_periodo_copiados_com_numeros():
    doc = documento()
    doc.colaborador.update({"nome": "Conceição", "nivel": 3, "fator": Decimal("1.50")})
    saida = json.loads(_texto(doc=doc), parse_float=Decimal)
    assert saida["colaborador"] == {
        "id": "c-0417",
        "nome": "Conceição",
        "nivel": 3,
        "fator": Decimal("1.50"),
    }
    assert saida["periodo"] == doc.periodo


def test_dt005_utf8_sem_escapar_acentos():
    texto = _texto(_resultado(justificativa="Limite diário de alimentação (RN-008)"))
    assert "Limite diário de alimentação" in texto
    assert "\\u" not in texto


def test_dt005_campos_do_item_na_ordem_da_spec():
    item = json.loads(_texto(_resultado()))["itens"][0]
    assert list(item) == [
        "id",
        "valor_informado",
        "moeda",
        "taxa_cambio",
        "data_cotacao",
        "valor_considerado",
        "valor_reembolsavel",
        "status",
        "motivo",
        "justificativa",
    ]


def test_dt005_saida_e_json_valido_com_recuo():
    texto = _texto(_resultado(), _resultado(id="d-002"))
    assert json.loads(texto)["itens"][1]["id"] == "d-002"
    assert texto.startswith('{\n  "colaborador": {\n    "id": "c-0417"')


def test_dt005_moeda_e_cotacao_em_brl():
    resultados = calcular(documento(despesa(1, valor="47.20")), politica_aplicavel())
    texto = _texto(*resultados)
    item = json.loads(texto)["itens"][0]
    assert item["moeda"] == "BRL"
    assert item["taxa_cambio"] is None
    assert item["data_cotacao"] is None


def test_dt005_taxa_cambio_sem_quantizar():
    e002 = despesa(1, id="e-002", data="2026-07-14", valor="22.00", moeda="EUR")
    resultados = calcular(documento(e002), politica_aplicavel("CC-COMERCIAL"), cambio())
    texto = _texto(*resultados)
    assert '"valor_informado": 22.00' in texto
    assert '"moeda": "EUR"' in texto
    assert '"taxa_cambio": 5.93' in texto
    assert '"data_cotacao": "2026-07-14"' in texto
    assert '"valor_considerado": 130.46' in texto
    assert '"taxa_cambio": 5.4219' in _texto(
        _resultado(moeda="USD", taxa_cambio=Decimal("5.4219"), data_cotacao=date(2026, 7, 13))
    )


def test_dt005_nulos_em_cotacao_indisponivel():
    e006 = despesa(1, id="e-006", data="2026-07-21", valor="55.00", moeda="GBP")
    resultados = calcular(documento(e006), politica_aplicavel("CC-COMERCIAL"), cambio())
    item = json.loads(_texto(*resultados))["itens"][0]
    assert item["moeda"] == "GBP"
    assert item["motivo"] == Motivo.COTACAO_INDISPONIVEL.value
    assert item["valor_considerado"] is None
    assert item["taxa_cambio"] is None
    assert item["data_cotacao"] is None
    assert item["valor_reembolsavel"] == 0
