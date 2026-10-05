"""Tabela da seção 7 da spec: um caso por linha, com o nome da spec como `id`."""

import json
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

import pytest

from reembolso.cli import main
from reembolso.saida import serializar

REMOVER = object()
ERRO = "erro geral, sem saída"
ENVELOPE = Path(__file__).parent.parent / "exemplos" / "envelope"
EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas-exemplo.json"


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


def _json(caminho: Path) -> dict:
    return json.loads(caminho.read_text(encoding="utf-8"), parse_float=Decimal)


def politica(**alteracoes) -> str:
    """`politica-v4.json`; `alteracoes` usa `__` como separador de caminho."""
    return serializar(_alterar(_json(ENVELOPE / "politica-v4.json"), alteracoes))


def cambio(**alteracoes) -> str:
    """`cambio.json`; `alteracoes` usa `__` como separador de caminho."""
    return serializar(_alterar(_json(ENVELOPE / "cambio.json"), alteracoes))


def _alterar(dados: dict, alteracoes: dict) -> dict:
    for caminho, valor in alteracoes.items():
        alvo = dados
        *pais, campo = caminho.split("__")
        for pai in pais:
            alvo = alvo[pai]
        if valor is REMOVER:
            del alvo[campo]
        else:
            alvo[campo] = valor
    return dados


@dataclass(frozen=True)
class Docs:
    """Os três documentos de uma execução; `None` = documento não informado."""

    despesas: str
    politica: str | None = None
    cambio: str | None = None


def docs(despesas: str, politica_: str | None = REMOVER, cambio_: str | None = REMOVER) -> Docs:
    """Por padrão, a política v4 e o câmbio do envelope."""
    return Docs(
        despesas,
        politica() if politica_ is REMOVER else politica_,
        cambio() if cambio_ is REMOVER else cambio_,
    )


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
ENG = {"centro_custo": "CC-ENG-PLATAFORMA"}
COMERCIAL = {"centro_custo": "CC-COMERCIAL"}
SUPORTE = {"centro_custo": "CC-SUPORTE-N2"}
ADM = {"centro_custo": "CC-ADM"}
E002 = {"data": "2026-07-14", "valor": Decimal("22.00"), "moeda": "EUR"}
USD_0713 = {"data": "2026-07-13", "moeda": "USD"}
TABELA_SECAO9 = [
    aprovado("72.50"),
    limitado("2.50"),
    limitado("80.00"),
    recusado("NOTA_FISCAL_AUSENTE"),
    recusado("CATEGORIA_NAO_REEMBOLSAVEL"),
    aprovado("54.90"),
    recusado("DUPLICATA"),
    recusado("FORA_DO_PERIODO"),
    recusado("VALOR_NEGATIVO"),
    recusado("CATEGORIA_NAO_REEMBOLSAVEL"),
    aprovado("33.33"),
    aprovado("47.20"),
    recusado("CATEGORIA_NAO_REEMBOLSAVEL"),
    aprovado("61.00"),
]

CASOS = [
    pytest.param(
        doc(
            d("d-001", **ALIM_0703, valor=Decimal("72.50")),
            d("d-002", **ALIM_0703, valor=Decimal("38.00")),
            colaborador=ENG,
        ),
        [aprovado("72.50"), limitado("2.50")],
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
        id="Categoria fora da política",
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
        doc(
            d("e-007", **HOSP_0714, descricao="Hotel Londres - 3 noites", valor=Decimal("1200.00")),
            colaborador=COMERCIAL,
        ),
        [limitado("400.00")],
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
        doc(
            d("d-014", data="2026-07-31", categoria="ALIMENTACAO", valor=Decimal("61.00")),
            colaborador=ENG,
        ),
        [aprovado("61.00")],
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
        doc(d("e-002", **E002, descricao="Almoco - Lisboa"), colaborador=COMERCIAL),
        [limitado("90.00", valor_considerado="130.46")],
        id="Indício de viagem pela moeda",
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
        doc(d("d-x", projeto="X")),
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
    pytest.param(
        doc(d("d-x", valor=Decimal("61.00"))),
        [limitado("60.00", justificativa_cita="(política padrão)")],
        id="Centro de custo ausente",
    ),
    pytest.param(
        doc(d("f-002", **HOSP_0714, valor=Decimal("310.00")), colaborador=SUPORTE),
        [
            limitado(
                "250.00",
                justificativa_cita="política padrão; centro de custo CC-SUPORTE-N2 não cadastrado",
            )
        ],
        id="Centro de custo desconhecido",
    ),
    pytest.param(
        doc(
            d("f-002", **HOSP_0714, valor=Decimal("310.00")),
            colaborador={"centro_custo": " CC-Suporte-N2 "},
        ),
        [
            limitado(
                "250.00",
                justificativa_cita="política padrão; centro de custo CC-Suporte-N2 não cadastrado",
            )
        ],
        id="Centro de custo desconhecido com espaços nas pontas",
    ),
    pytest.param(
        doc(d("d-x", valor=Decimal("95.00")), colaborador={"centro_custo": " cc-comercial "}),
        [limitado("90.00")],
        id="Centro de custo com grafia diferente",
    ),
    pytest.param(
        doc(d("d-x"), colaborador={"centro_custo": 42}), ERRO, id="Centro de custo com tipo errado"
    ),
    pytest.param(
        doc(d("d-x", **HOSP_0714, valor=Decimal("300.00")), colaborador=ADM),
        [
            limitado(
                "250.00",
                justificativa_cita=(
                    "centro de custo CC-ADM usando limite herdado da política padrão"
                ),
            )
        ],
        id="Categoria ausente na tabela do centro",
    ),
    pytest.param(
        doc(d("d-x", valor=Decimal("95.00")), colaborador={"centro_custo": " cc-comercial "}),
        [limitado("90.00", justificativa_cita="(centro de custo CC-COMERCIAL)")],
        id="Grafia do centro de custo na justificativa",
    ),
    pytest.param(
        doc(d("d-010", **HOSP_0714, valor=Decimal("480.00")), colaborador=ENG),
        [recusado("CATEGORIA_NAO_REEMBOLSAVEL")],
        id="Categoria com limite zero",
    ),
    pytest.param(
        doc(
            d("d-013", **HOSP_0714, valor=Decimal("690.00"), tem_nota_fiscal=False),
            colaborador=ENG,
        ),
        [recusado("CATEGORIA_NAO_REEMBOLSAVEL")],
        id="Limite zero vem antes da nota fiscal",
    ),
    pytest.param(
        doc(d("f-003", categoria="representacao", valor=Decimal("190.00")), colaborador=SUPORTE),
        [recusado("CATEGORIA_NAO_REEMBOLSAVEL")],
        id="Representação em centro que não a tem",
    ),
    pytest.param(
        doc(d("e-001", categoria="representacao", valor=Decimal("340.00")), colaborador=COMERCIAL),
        [limitado("300.00")],
        id="Representação acima do limite",
    ),
    pytest.param(
        doc(d("e-010", valor=Decimal("88.00")), colaborador=COMERCIAL),
        [aprovado("88.00", moeda="BRL")],
        id="Moeda ausente",
    ),
    pytest.param(
        doc(d("d-x", **{**USD_0713, "moeda": " usd "})),
        [aprovado("54.20", moeda="USD", taxa_cambio="5.42")],
        id="Moeda em minúsculas",
    ),
    pytest.param(
        [doc(d("d-x", moeda=""), d("d-y")), doc(d("d-x", moeda=840), d("d-y"))],
        [recusado("DADOS_INVALIDOS", moeda=None), aprovado("10.00")],
        id="Moeda vazia ou de tipo errado",
    ),
    pytest.param(
        doc(d("e-002", **E002), colaborador=COMERCIAL),
        [
            limitado(
                "90.00", valor_considerado="130.46", taxa_cambio="5.93", data_cotacao="2026-07-14"
            )
        ],
        id="Moeda estrangeira com cotação na data",
    ),
    pytest.param(
        doc(d("e-006", data="2026-07-21", valor=Decimal("55.00"), moeda="GBP")),
        [recusado("COTACAO_INDISPONIVEL", valor_considerado=None, moeda="GBP")],
        id="Moeda sem cotação",
    ),
    pytest.param(
        doc(
            d("e-004", data="2026-07-18", valor=Decimal("30.00"), moeda="EUR"),
            colaborador=COMERCIAL,
        ),
        [
            limitado(
                "90.00", valor_considerado="178.80", taxa_cambio="5.96", data_cotacao="2026-07-17"
            )
        ],
        id="Data sem cotação (fim de semana)",
    ),
    pytest.param(
        doc(d("d-x", data="2026-07-10", moeda="USD")),
        [recusado("COTACAO_INDISPONIVEL")],
        id="Data anterior à primeira cotação",
    ),
    pytest.param(
        doc(d("d-x", data="2026-07-18")),
        [aprovado("10.00", taxa_cambio=None, data_cotacao=None)],
        id="Despesa em BRL em data sem cotação",
    ),
    pytest.param(
        doc(d("d-x", **USD_0713, valor=Decimal("33.333"))),
        [limitado("60.00", valor_considerado="180.66")],
        id="Arredondamento cambial",
    ),
    pytest.param(
        doc(
            d(
                "e-005",
                data="2026-07-20",
                categoria="transporte_urbano",
                valor=Decimal("40.00"),
                moeda="USD",
                tem_nota_fiscal=False,
            )
        ),
        [recusado("NOTA_FISCAL_AUSENTE", valor_considerado="220.00")],
        id="Nota fiscal após conversão",
    ),
    pytest.param(
        doc(
            d(
                "e-003",
                data="2026-07-15",
                valor=Decimal("14.50"),
                moeda="EUR",
                tem_nota_fiscal=False,
            ),
            colaborador=COMERCIAL,
        ),
        [aprovado("85.26")],
        id="Abaixo do limiar após conversão",
    ),
    pytest.param(
        doc(
            d("e-a", **E002, fornecedor="Taberna do Chiado"),
            d("e-b", **E002, fornecedor="Taberna do Chiado"),
            colaborador=COMERCIAL,
        ),
        [limitado("90.00"), recusado("DUPLICATA", justificativa_cita="e-a")],
        id="Duplicata na mesma moeda estrangeira",
    ),
    pytest.param(
        doc(
            d("e-a", **E002, fornecedor="Taberna do Chiado"),
            d(
                "e-b",
                **{**E002, "valor": Decimal("130.46"), "moeda": "BRL"},
                fornecedor="Taberna do Chiado",
            ),
            colaborador=COMERCIAL,
        ),
        [limitado("90.00"), limitado("0.00")],
        id="Mesmo valor em reais, moedas diferentes",
    ),
    pytest.param(
        doc(d("d-x", data="2026-07-21", valor=Decimal("-10.00"), moeda="GBP")),
        [recusado("COTACAO_INDISPONIVEL")],
        id="Estorno em moeda sem cotação",
    ),
    pytest.param(
        doc(d("d-x", **USD_0713, valor=Decimal("-10.00"))),
        [recusado("VALOR_NEGATIVO", valor_considerado="-54.20")],
        id="Estorno em moeda estrangeira",
    ),
    pytest.param(
        docs(doc(d("d-x", **USD_0713), d("d-y")), cambio_=None),
        [recusado("COTACAO_INDISPONIVEL"), aprovado("10.00")],
        id="Documento de câmbio ausente, despesa estrangeira",
    ),
    pytest.param(
        docs(EXEMPLO.read_text(encoding="utf-8"), cambio_=None),
        TABELA_SECAO9,
        id="Documento de câmbio ausente, tudo em reais",
    ),
    pytest.param(docs(doc(d("d-x")), politica_=None), ERRO, id="Documento de política ausente"),
    pytest.param(
        [
            docs(doc(d("d-x")), politica(padrao__alimentacao__limite=-1)),
            docs(doc(d("d-x")), politica(padrao=REMOVER)),
            docs(doc(d("d-x")), politica(padrao__alimentacao__periodicidade="mes")),
        ],
        ERRO,
        id="Documento de política inválido",
    ),
    pytest.param(
        [
            docs(
                doc(d("d-x", valor=Decimal("61.00"))),
                politica(padrao__alimentacao__periodicidade="Dia"),
            ),
            docs(
                doc(d("d-x", valor=Decimal("61.00"))),
                politica(padrao__alimentacao__periodicidade=" diaria "),
            ),
        ],
        [limitado("60.00")],
        id="Periodicidade com grafia diferente",
    ),
    pytest.param(
        [
            docs(doc(d("d-x")), cambio_=cambio(**{"taxas__2026-07-13__USD": 0})),
            docs(doc(d("d-x")), cambio_=cambio(**{"taxas__2026-07-13__USD": "5,42"})),
        ],
        ERRO,
        id="Documento de câmbio inválido",
    ),
    pytest.param(
        docs(doc(d("d-x")), cambio_=cambio(moeda_base="USD")), ERRO, id="Moedas base divergentes"
    ),
]


def _executar(pasta: Path, documentos: Docs) -> dict | None:
    """Roda a CLI (fluxo real); `None` em erro geral, depois de conferir código 1 e sem saída."""
    args = ["calcular"]
    for opcao, texto in [
        ("--input", documentos.despesas),
        ("--politica", documentos.politica),
        ("--cambio", documentos.cambio),
    ]:
        if texto is not None:
            arquivo = pasta / f"{opcao[2:]}.json"
            arquivo.write_text(texto, encoding="utf-8")
            args += [opcao, str(arquivo)]
    saida = pasta / "resultado.json"
    saida.unlink(missing_ok=True)
    codigo = main([*args, "--output", str(saida)])
    if codigo != 0:
        assert codigo == 1
        assert not saida.exists()
        return None
    return _json(saida)


_TEXTO = {"status", "motivo", "id", "moeda", "data_cotacao"}


def _verificar(pasta: Path, documentos: Docs, esperado):
    saida = _executar(pasta, documentos)
    if esperado == ERRO:
        assert saida is None
        return
    assert saida is not None
    itens = saida["itens"]
    assert len(itens) == len(esperado)
    for obtido, campos in zip(itens, esperado, strict=True):
        for campo, valor in campos.items():
            if campo == "justificativa_cita":
                assert valor in obtido["justificativa"]
            elif campo in _TEXTO or not isinstance(valor, str):
                assert obtido[campo] == valor, campo
            else:
                assert obtido[campo] == Decimal(valor), campo
    total = sum((i["valor_reembolsavel"] for i in itens), Decimal("0"))
    assert saida["total_reembolsavel"] == total


def test_secao7_tem_71_casos():
    assert len(CASOS) == 71


@pytest.mark.parametrize(("entrada", "esperado"), CASOS)
def test_secao7_caso_de_borda(tmp_path, entrada, esperado):
    for caso in entrada if isinstance(entrada, list) else [entrada]:
        _verificar(tmp_path, caso if isinstance(caso, Docs) else docs(caso), esperado)
