import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

from reembolso.entrada import ler_documento
from reembolso.modelo import Despesa
from reembolso.motor import calcular
from reembolso.politica import LIMITE_POR_DATA

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
    item = calcular(ler_documento(_documento_com(d003)))[0]
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
    _, r_jantar = calcular(ler_documento(_documento_com(hotel, jantar)))
    assert r_jantar.valor_reembolsavel == Decimal("60.00")


def test_rn011_exemplo_nenhuma_despesa_acima_da_tabela_da_rn008():
    documento = ler_documento(EXEMPLO.read_text(encoding="utf-8"))
    resultados = calcular(documento)
    soma: dict[tuple, Decimal] = defaultdict(Decimal)
    for despesa, resultado in zip(documento.despesas, resultados, strict=True):
        assert isinstance(despesa, Despesa)
        soma[(despesa.data, despesa.categoria)] += resultado.valor_reembolsavel
    for (_, categoria), total in soma.items():
        if categoria in LIMITE_POR_DATA:
            assert total <= LIMITE_POR_DATA[categoria]
