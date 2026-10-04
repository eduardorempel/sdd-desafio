import json
from decimal import Decimal
from pathlib import Path

import pytest

from reembolso.entrada import ler_documento
from reembolso.motor import calcular
from reembolso.saida import montar_saida, serializar

EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas-exemplo.json"

# Tabela da seção 9 da spec: id, valor_reembolsavel, status, motivo.
TABELA_SECAO9 = [
    ("d-001", "60.00", "limitado", "LIMITE_DIARIO"),
    ("d-002", "0.00", "limitado", "LIMITE_DIARIO"),
    ("d-003", "80.00", "limitado", "LIMITE_DIARIO"),
    ("d-004", "0.00", "recusado", "NOTA_FISCAL_AUSENTE"),
    ("d-005", "0.00", "recusado", "CATEGORIA_NAO_REEMBOLSAVEL"),
    ("d-006", "54.90", "aprovado", None),
    ("d-007", "0.00", "recusado", "DUPLICATA"),
    ("d-008", "0.00", "recusado", "FORA_DO_PERIODO"),
    ("d-009", "0.00", "recusado", "VALOR_NEGATIVO"),
    ("d-010", "250.00", "limitado", "LIMITE_DIARIO"),
    ("d-011", "33.33", "aprovado", None),
    ("d-012", "47.20", "aprovado", None),
    ("d-013", "0.00", "recusado", "NOTA_FISCAL_AUSENTE"),
    ("d-014", "60.00", "limitado", "LIMITE_DIARIO"),
]


def _processar(texto: str) -> str:
    documento = ler_documento(texto)
    return serializar(montar_saida(documento, calcular(documento)))


@pytest.fixture(scope="module")
def saida():
    return json.loads(_processar(EXEMPLO.read_text(encoding="utf-8")), parse_float=Decimal)


@pytest.mark.parametrize(
    ("posicao", "linha"), list(enumerate(TABELA_SECAO9)), ids=[li[0] for li in TABELA_SECAO9]
)
def test_secao9_linha_da_tabela(saida, posicao, linha):
    id_, valor, status, motivo = linha
    item = saida["itens"][posicao]
    assert item["id"] == id_
    assert item["valor_reembolsavel"] == Decimal(valor)
    assert item["status"] == status
    assert item["motivo"] == motivo


def test_secao9_total_reembolsavel(saida):
    assert saida["total_reembolsavel"] == Decimal("585.43")


def test_secao9_um_item_por_despesa_na_mesma_ordem(saida):
    entrada = json.loads(EXEMPLO.read_text(encoding="utf-8"))
    assert [i["id"] for i in saida["itens"]] == [d["id"] for d in entrada["despesas"]]


def test_secao9_colaborador_e_periodo_copiados(saida):
    entrada = json.loads(EXEMPLO.read_text(encoding="utf-8"))
    assert saida["colaborador"] == entrada["colaborador"]
    assert saida["periodo"] == entrada["periodo"]
