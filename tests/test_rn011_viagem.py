import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from fabrica import despesa, documento, politica_aplicavel

from reembolso.entrada import ler_documento
from reembolso.modelo import Despesa
from reembolso.motor import calcular

EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas-exemplo.json"


def _documento_com(*despesas):
    return json.dumps(
        {
            "colaborador": {"id": "c-0417"},
            "periodo": {"inicio": "2026-07-01", "fim": "2026-07-31"},
            "despesas": list(despesas),
        }
    )


def test_rn011_d003_corrida_aeroporto_recebe_limite_normal():
    d003 = {
        "id": "d-003",
        "data": "2026-07-06",
        "categoria": "transporte_urbano",
        "descricao": "Corrida aeroporto",
        "fornecedor": "TaxiApp",
        "valor": 100.00,
        "tem_nota_fiscal": False,
    }
    item = calcular(ler_documento(_documento_com(d003)), politica_aplicavel())[0]
    assert item.valor_reembolsavel == Decimal("80.00")
    assert "R$ 80,00" in item.justificativa


def test_rn011_hospedagem_no_mesmo_dia_nao_amplia_limite():
    hotel = {
        "id": "h-1",
        "data": "2026-07-06",
        "categoria": "hospedagem",
        "descricao": "Hotel em viagem",
        "fornecedor": "Hotel",
        "valor": 200.00,
        "tem_nota_fiscal": True,
    }
    jantar = {
        "id": "a-1",
        "data": "2026-07-06",
        "categoria": "alimentacao",
        "descricao": "Jantar em viagem",
        "fornecedor": "Restaurante",
        "valor": 90.00,
        "tem_nota_fiscal": True,
    }
    _, r_jantar = calcular(ler_documento(_documento_com(hotel, jantar)), politica_aplicavel())
    assert r_jantar.valor_reembolsavel == Decimal("60.00")


def test_rn011_exemplo_nenhuma_despesa_acima_da_tabela_da_rn008():
    lido = ler_documento(EXEMPLO.read_text(encoding="utf-8"))
    resultados = calcular(lido, politica_aplicavel())
    soma: dict[tuple, Decimal] = defaultdict(Decimal)
    for lida, resultado in zip(lido.despesas, resultados, strict=True):
        assert isinstance(lida, Despesa)
        soma[(lida.data, lida.categoria)] += resultado.valor_reembolsavel
    politica = politica_aplicavel()
    for (_, categoria), total in soma.items():
        limite, _ = politica.regra(categoria)
        if limite is not None:
            assert total <= limite


def test_rn011_acrescimo_em_viagem_do_documento_nao_e_aplicado():
    politica = politica_aplicavel(
        "CC-COMERCIAL",
        documento={
            "moeda_base": "BRL",
            "padrao": {"alimentacao": {"limite": 60, "periodicidade": "dia"}},
            "centros_custo": {
                "CC-COMERCIAL": {
                    "alimentacao": {"limite": 90, "periodicidade": "dia"},
                    "hospedagem": {"limite": 400, "periodicidade": "diaria"},
                }
            },
            "nota_fiscal_obrigatoria_acima_de": 100,
            "acrescimo_em_viagem_percentual": 50,
        },
    )
    alimentacao, hospedagem = calcular(
        documento(
            despesa(1, data="2026-07-22", categoria="alimentacao", valor="200.00"),
            despesa(2, data="2026-07-22", categoria="hospedagem", valor="1200.00"),
        ),
        politica,
    )
    assert alimentacao.valor_reembolsavel == Decimal("90.00")
    assert hospedagem.valor_reembolsavel == Decimal("400.00")
