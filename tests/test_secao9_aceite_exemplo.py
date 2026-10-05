import json
import re
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import pytest
from fabrica import politica_aplicavel

from reembolso.entrada import ler_documento
from reembolso.motor import calcular
from reembolso.saida import montar_saida, serializar

EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas-exemplo.json"
POLITICA = Path(__file__).parent.parent / "exemplos" / "envelope" / "politica-v4.json"

# Tabela da seção 9 da spec: id, valor_reembolsavel, status, motivo.
TABELA_SECAO9 = [
    ("d-001", "72.50", "aprovado", None),
    ("d-002", "2.50", "limitado", "LIMITE_DIARIO"),
    ("d-003", "80.00", "limitado", "LIMITE_DIARIO"),
    ("d-004", "0.00", "recusado", "NOTA_FISCAL_AUSENTE"),
    ("d-005", "0.00", "recusado", "CATEGORIA_NAO_REEMBOLSAVEL"),
    ("d-006", "54.90", "aprovado", None),
    ("d-007", "0.00", "recusado", "DUPLICATA"),
    ("d-008", "0.00", "recusado", "FORA_DO_PERIODO"),
    ("d-009", "0.00", "recusado", "VALOR_NEGATIVO"),
    ("d-010", "0.00", "recusado", "CATEGORIA_NAO_REEMBOLSAVEL"),
    ("d-011", "33.33", "aprovado", None),
    ("d-012", "47.20", "aprovado", None),
    ("d-013", "0.00", "recusado", "CATEGORIA_NAO_REEMBOLSAVEL"),
    ("d-014", "61.00", "aprovado", None),
]


def _processar(texto: str) -> str:
    documento = ler_documento(texto)
    politica = politica_aplicavel(documento.centro_custo)
    return serializar(montar_saida(documento, calcular(documento, politica)))


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
    assert saida["total_reembolsavel"] == Decimal("351.43")


def test_secao9_um_item_por_despesa_na_mesma_ordem(saida):
    entrada = json.loads(EXEMPLO.read_text(encoding="utf-8"))
    assert [i["id"] for i in saida["itens"]] == [d["id"] for d in entrada["despesas"]]


def test_secao9_colaborador_e_periodo_copiados(saida):
    entrada = json.loads(EXEMPLO.read_text(encoding="utf-8"))
    assert saida["colaborador"] == entrada["colaborador"]
    assert saida["periodo"] == entrada["periodo"]


JUSTIFICATIVAS_SECAO4 = {
    "d-001": (
        "Despesa aprovada: passou por todas as regras e é reembolsada integralmente "
        "(RN-001, RN-004 a RN-008)."
    ),
    "d-002": (
        "Limite diário de alimentação de R$ 75,00 (centro de custo CC-ENG-PLATAFORMA), "
        "com R$ 72,50 já consumido por d-001 em 2026-07-03; excedente de R$ 35,50 cortado "
        "(RN-008, RN-009, RN-010)."
    ),
    "d-004": "Valor acima de R$ 100,00 sem nota fiscal (RN-007).",
}


@pytest.mark.parametrize("id_", list(JUSTIFICATIVAS_SECAO4))
def test_justificativas_exemplo_secao4(saida, id_):
    item = next(i for i in saida["itens"] if i["id"] == id_)
    assert item["justificativa"] == JUSTIFICATIVAS_SECAO4[id_]


def test_todo_item_cita_rn(saida):
    for item in saida["itens"]:
        assert re.search(r"RN-\d{3}", item["justificativa"]), item["id"]


def _rodar_cli(saida_path):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "reembolso",
            "calcular",
            "--input",
            EXEMPLO,
            "--politica",
            POLITICA,
            "--output",
            saida_path,
        ],
        capture_output=True,
        cwd=EXEMPLO.parent.parent,
        check=True,
    )


def test_determinismo(tmp_path):
    texto = EXEMPLO.read_text(encoding="utf-8")
    assert _processar(texto) == _processar(texto)
    # Processos separados: nenhuma ordem depende de hash ou estado do processo.
    primeira, segunda = tmp_path / "1.json", tmp_path / "2.json"
    _rodar_cli(primeira)
    _rodar_cli(segunda)
    assert primeira.read_bytes() == segunda.read_bytes()
