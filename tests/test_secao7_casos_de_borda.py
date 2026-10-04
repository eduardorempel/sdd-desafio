"""Tabela da seção 7 da spec: um caso por linha, com o nome da spec como `id`."""

import json
from decimal import Decimal

import pytest

from reembolso.entrada import EntradaInvalida, ler_documento
from reembolso.motor import calcular
from reembolso.saida import montar_saida, serializar

REMOVER = object()
ERRO = "erro geral, sem saída"


def _aplicar(base: dict, alteracoes: dict) -> dict:
    resultado = dict(base)
    for campo, valor in alteracoes.items():
        if valor is REMOVER:
            resultado.pop(campo, None)
        else:
            resultado[campo] = valor
    return resultado


def d(id="d-x", **campos):
    """Despesa válida de entrada; `campos` sobrescreve ou remove (REMOVER) campos."""
    base = {
        "id": id,
        "data": "2026-07-10",
        "categoria": "alimentacao",
        "descricao": "Despesa de teste",
        "fornecedor": f"Fornecedor {id}",
        "valor": Decimal("10.00"),
        "tem_nota_fiscal": True,
    }
    return _aplicar(base, campos)


def doc(*despesas, periodo=None, colaborador=None, **raiz):
    base = {
        "colaborador": _aplicar({"id": "c-0417", "nome": "Marina Volpi"}, colaborador or {}),
        "periodo": _aplicar(
            {"competencia": "2026-07", "inicio": "2026-07-01", "fim": "2026-07-31"}, periodo or {}
        ),
        "despesas": list(despesas),
    }
    return serializar(_aplicar(base, raiz))


def item(valor_reembolsavel, status, motivo=None, **outros):
    return {
        "valor_reembolsavel": valor_reembolsavel,
        "status": status,
        "motivo": motivo,
        **outros,
    }


def aprovado(valor, **outros):
    return item(valor, "aprovado", **outros)


def limitado(valor, **outros):
    return item(valor, "limitado", "LIMITE_DIARIO", **outros)


def recusado(motivo, **outros):
    return item("0.00", "recusado", motivo, **outros)


ALIM_0703 = {"data": "2026-07-03"}
TRANSP_0706 = {"data": "2026-07-06", "categoria": "transporte_urbano", "fornecedor": "TaxiApp"}
BISTRO = {"data": "2026-07-09", "fornecedor": "Bistro Central", "valor": Decimal("54.90")}
HOSP_0714 = {"data": "2026-07-14", "categoria": "hospedagem"}

CASOS = [
    pytest.param(
        doc(
            d("d-001", **ALIM_0703, valor=Decimal("72.50")),
            d("d-002", **ALIM_0703, valor=Decimal("38.00")),
        ),
        [limitado("60.00"), limitado("0.00")],
        id="Duas despesas no mesmo dia somam acima do limite",
    ),
    pytest.param(
        doc(d("d-003", **TRANSP_0706, valor=Decimal("100.00"), tem_nota_fiscal=False)),
        [limitado("80.00")],
        id="Valor exatamente no limite da nota",
    ),
    pytest.param(
        doc(d("d-004", **TRANSP_0706, valor=Decimal("100.01"), tem_nota_fiscal=False)),
        [recusado("NOTA_FISCAL_AUSENTE")],
        id="Valor um centavo acima do limite da nota",
    ),
    pytest.param(
        doc(
            d("d-003", **TRANSP_0706, valor=Decimal("100.00"), tem_nota_fiscal=False),
            d("d-004", **TRANSP_0706, valor=Decimal("100.01"), tem_nota_fiscal=False),
        ),
        [limitado("80.00"), recusado("NOTA_FISCAL_AUSENTE")],
        id="Despesa recusada não consome limite",
    ),
    pytest.param(
        doc(d("d-005", categoria="coworking", valor=Decimal("89.00"))),
        [recusado("CATEGORIA_NAO_REEMBOLSAVEL")],
        id="Categoria fora da lista",
    ),
    pytest.param(
        doc(d("d-006", **BISTRO), d("d-007", **BISTRO)),
        [aprovado("54.90"), recusado("DUPLICATA")],
        id="Duplicata idêntica, ambas com nota",
    ),
    pytest.param(
        doc(d("d-a", **BISTRO, tem_nota_fiscal=False), d("d-b", **BISTRO)),
        [recusado("DUPLICATA"), aprovado("54.90")],
        id="Duplicata em que só a segunda tem nota",
    ),
    pytest.param(
        doc(d("d-a", **BISTRO), d("d-b", **{**BISTRO, "fornecedor": "BISTRO CENTRAL "})),
        [aprovado("54.90"), recusado("DUPLICATA")],
        id="Duplicata com grafia diferente do fornecedor",
    ),
    pytest.param(
        doc(d("d-008", data="2026-04-15", valor=Decimal("41.00"))),
        [recusado("FORA_DO_PERIODO")],
        id="Despesa antes do período",
    ),
    pytest.param(
        doc(d("d-x", data="2026-07-31", valor=Decimal("41.00"))),
        [aprovado("41.00")],
        id="Despesa no último dia do período",
    ),
    pytest.param(
        doc(d("d-x", data="2026-07-01", valor=Decimal("41.00"))),
        [aprovado("41.00")],
        id="Despesa no primeiro dia do período",
    ),
    pytest.param(
        doc(
            d("d-100", **TRANSP_0706, valor=Decimal("80.00")),
            d("d-009", **TRANSP_0706, valor=Decimal("-45.00"), tem_nota_fiscal=False),
        ),
        [aprovado("80.00"), recusado("VALOR_NEGATIVO")],
        id="Estorno",
    ),
    pytest.param(
        doc(d("d-x", valor=Decimal("0.00"))),
        [aprovado("0.00", valor_considerado="0.00")],
        id="Valor zero",
    ),
    pytest.param(
        doc(d("d-x", valor=Decimal("-0.004"))),
        [aprovado("0.00", valor_considerado="0.00")],
        id="Valor negativo que arredonda a zero",
    ),
    pytest.param(
        doc(d("d-011", valor=Decimal("33.333"))),
        [aprovado("33.33", valor_informado="33.333", valor_considerado="33.33")],
        id="Mais de duas casas decimais",
    ),
    pytest.param(
        doc(d("d-x", valor=Decimal("10.005"))),
        [aprovado("10.01", valor_considerado="10.01")],
        id="Arredondamento na metade",
    ),
    pytest.param(
        doc(d("d-010", **HOSP_0714, descricao="Hotel Rio - 2 diarias", valor=Decimal("480.00"))),
        [limitado("250.00")],
        id="Hospedagem com várias diárias na descrição",
    ),
    pytest.param(
        doc(
            d("h-1", **HOSP_0714, valor=Decimal("200.00")),
            d("h-2", **HOSP_0714, valor=Decimal("150.00")),
        ),
        [aprovado("200.00"), limitado("50.00")],
        id="Duas hospedagens na mesma data",
    ),
    pytest.param(
        doc(d("d-013", **HOSP_0714, valor=Decimal("690.00"), tem_nota_fiscal=False)),
        [recusado("NOTA_FISCAL_AUSENTE")],
        id="Hospedagem sem nota acima de 100",
    ),
    pytest.param(
        doc(d("d-014", data="2026-07-31", categoria="ALIMENTACAO", valor=Decimal("61.00"))),
        [limitado("60.00")],
        id="Categoria em maiúsculas",
    ),
    pytest.param(
        doc(d("d-012", data="2026-07-18", valor=Decimal("47.20"))),
        [aprovado("47.20")],
        id="Despesa em fim de semana",
    ),
    pytest.param(
        doc(
            d(
                "d-003",
                **TRANSP_0706,
                descricao="Corrida aeroporto",
                valor=Decimal("100.00"),
                tem_nota_fiscal=False,
            )
        ),
        [limitado("80.00")],
        id="Indício de viagem na descrição",
    ),
    pytest.param(
        doc(d("d-a", tem_nota_fiscal=REMOVER), d("d-b")),
        [recusado("DADOS_INVALIDOS"), aprovado("10.00")],
        id="Campo obrigatório ausente em uma despesa",
    ),
    pytest.param(
        doc(d("d-x", fornecedor="   ")),
        [recusado("DADOS_INVALIDOS", valor_considerado=None)],
        id="Campo obrigatório só com espaços",
    ),
    pytest.param(
        doc(d(17)),
        [recusado("DADOS_INVALIDOS", id=None, valor_considerado=None)],
        id="`id` com tipo errado",
    ),
    pytest.param(
        doc(d("d-x", data="2026-7-3")),
        [recusado("DADOS_INVALIDOS")],
        id="Data fora do formato",
    ),
    pytest.param(
        doc(d("d-x", data="2026-02-30")),
        [recusado("DADOS_INVALIDOS")],
        id="Data inexistente",
    ),
    pytest.param(
        doc(d("d-x", valor="72.50")),
        [recusado("DADOS_INVALIDOS", valor_informado=None, valor_considerado=None)],
        id="Valor não numérico",
    ),
    pytest.param(
        doc(d("d-x", valor=Decimal("50.00"), tem_nota_fiscal=REMOVER)),
        [recusado("DADOS_INVALIDOS", valor_informado="50.00", valor_considerado=None)],
        id="Valor válido e outro campo inválido",
    ),
    pytest.param(
        doc(d("d-x", moeda="USD")),
        [aprovado("10.00")],
        id="Campo desconhecido",
    ),
    pytest.param(
        [doc(d("d-x", descricao=123)), doc(d("d-x"), periodo={"competencia": "julho"})],
        [aprovado("10.00")],
        id="Campo informativo malformado",
    ),
    pytest.param(doc(periodo={"fim": REMOVER}), ERRO, id="Período ausente"),
    pytest.param(doc(periodo={"inicio": "2026-02-30"}), ERRO, id="Data do período inválida"),
    pytest.param(
        [doc(colaborador={"id": "  "}), doc(colaborador={"id": 417})],
        ERRO,
        id="Colaborador sem identificação",
    ),
    pytest.param(
        [doc(despesas={"id": "d-x"}), doc(despesas=[d("d-x"), "d-y"])],
        ERRO,
        id="Lista de despesas malformada",
    ),
    pytest.param(
        [
            doc(d("d-x")).replace('"valor": 10.00', '"valor": NaN'),
            doc(d("d-x")).replace('"valor": 10.00', '"valor": Infinity'),
        ],
        ERRO,
        id="Documento com `NaN` ou `Infinity`",
    ),
    pytest.param(doc(), [], id="Lista de despesas vazia"),
]


def _processar(texto: str) -> dict:
    documento = ler_documento(texto)
    return json.loads(serializar(montar_saida(documento, calcular(documento))), parse_float=Decimal)


def _como_decimal(valor):
    return Decimal(valor) if isinstance(valor, str) else valor


def _verificar(texto: str, esperado):
    if esperado == ERRO:
        with pytest.raises(EntradaInvalida):
            ler_documento(texto)
        return
    saida = _processar(texto)
    itens = saida["itens"]
    assert len(itens) == len(esperado)
    for obtido, campos in zip(itens, esperado, strict=True):
        for campo, valor in campos.items():
            if campo in {"status", "motivo", "id"}:
                assert obtido[campo] == valor, campo
            else:
                assert obtido[campo] == _como_decimal(valor), campo
    total = sum((i["valor_reembolsavel"] for i in itens), Decimal("0"))
    assert saida["total_reembolsavel"] == total


def test_secao7_tem_37_casos():
    assert len(CASOS) == 37


@pytest.mark.parametrize(("entrada", "esperado"), CASOS)
def test_secao7_caso_de_borda(entrada, esperado):
    for texto in entrada if isinstance(entrada, list) else [entrada]:
        _verificar(texto, esperado)
