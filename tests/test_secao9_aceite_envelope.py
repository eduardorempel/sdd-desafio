"""Aceite da seção 9 da spec para os dois documentos do envelope, pela CLI."""

import json
import os
import re
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import pytest

from reembolso.saida import serializar

RAIZ = Path(__file__).parent.parent
ENVELOPE = RAIZ / "exemplos" / "envelope"
POLITICA = ENVELOPE / "politica-v4.json"
CAMBIO = ENVELOPE / "cambio.json"
COMERCIAL = ENVELOPE / "despesas-envelope.json"
DESCONHECIDO = ENVELOPE / "despesas-envelope-cc-desconhecido.json"

# Tabelas da seção 9 da spec: id, valor_considerado, valor_reembolsavel, status, motivo.
TABELA_COMERCIAL = [
    ("e-001", "340.00", "300.00", "limitado", "LIMITE_DIARIO"),
    ("e-002", "130.46", "90.00", "limitado", "LIMITE_DIARIO"),
    ("e-003", "85.26", "85.26", "aprovado", None),
    ("e-004", "178.80", "90.00", "limitado", "LIMITE_DIARIO"),
    ("e-005", "220.00", "0.00", "recusado", "NOTA_FISCAL_AUSENTE"),
    ("e-006", None, "0.00", "recusado", "COTACAO_INDISPONIVEL"),
    ("e-007", "1200.00", "400.00", "limitado", "LIMITE_DIARIO"),
    ("e-008", "95.00", "90.00", "limitado", "LIMITE_DIARIO"),
    ("e-009", "120.00", "0.00", "recusado", "CATEGORIA_NAO_REEMBOLSAVEL"),
    ("e-010", "88.00", "88.00", "aprovado", None),
]
TABELA_DESCONHECIDO = [
    ("f-001", "58.00", "58.00", "aprovado", None),
    ("f-002", "310.00", "250.00", "limitado", "LIMITE_DIARIO"),
    ("f-003", "190.00", "0.00", "recusado", "CATEGORIA_NAO_REEMBOLSAVEL"),
    ("f-004", "65.76", "65.76", "aprovado", None),
]
DOCUMENTOS = [
    pytest.param(COMERCIAL, TABELA_COMERCIAL, "1143.26", id="despesas-envelope"),
    pytest.param(DESCONHECIDO, TABELA_DESCONHECIDO, "373.76", id="cc-desconhecido"),
]

JUSTIFICATIVA_E002 = (
    "Limite diário de alimentação de R$ 90,00 (centro de custo CC-COMERCIAL) aplicado; "
    "excedente de R$ 40,46 cortado (RN-008, RN-010)."
)
NAO_CADASTRADO = "política padrão; centro de custo CC-SUPORTE-N2 não cadastrado"


def _rodar(entrada: Path, saida: Path) -> bytes:
    processo = subprocess.run(
        [
            sys.executable,
            "-m",
            "reembolso",
            "calcular",
            "--input",
            entrada,
            "--politica",
            POLITICA,
            "--cambio",
            CAMBIO,
            "--output",
            saida,
        ],
        capture_output=True,
        cwd=RAIZ,
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    assert processo.returncode == 0, processo.stderr
    return saida.read_bytes()


def _saida(entrada: Path, pasta: Path) -> dict:
    return json.loads(_rodar(entrada, pasta / "resultado.json"), parse_float=Decimal)


@pytest.fixture(scope="module")
def saidas(tmp_path_factory):
    pasta = tmp_path_factory.mktemp("envelope")
    return {COMERCIAL: _saida(COMERCIAL, pasta), DESCONHECIDO: _saida(DESCONHECIDO, pasta)}


def _decimal(valor):
    return None if valor is None else Decimal(valor)


@pytest.mark.parametrize(("entrada", "tabela", "total"), DOCUMENTOS)
def test_secao9_envelope_linhas_da_tabela(saidas, entrada, tabela, total):
    itens = saidas[entrada]["itens"]
    assert len(itens) == len(tabela)
    for item, (id_, considerado, reembolsavel, status, motivo) in zip(itens, tabela, strict=True):
        assert item["id"] == id_
        assert item["valor_considerado"] == _decimal(considerado), id_
        assert item["valor_reembolsavel"] == Decimal(reembolsavel), id_
        assert item["status"] == status, id_
        assert item["motivo"] == motivo, id_


@pytest.mark.parametrize(("entrada", "tabela", "total"), DOCUMENTOS)
def test_secao9_envelope_total_reembolsavel(saidas, entrada, tabela, total):
    assert saidas[entrada]["total_reembolsavel"] == Decimal(total)


@pytest.mark.parametrize(("entrada", "tabela", "total"), DOCUMENTOS)
def test_secao9_envelope_um_item_por_despesa_na_mesma_ordem(saidas, entrada, tabela, total):
    despesas = json.loads(entrada.read_text(encoding="utf-8"))["despesas"]
    assert [i["id"] for i in saidas[entrada]["itens"]] == [d["id"] for d in despesas]


@pytest.mark.parametrize(("entrada", "tabela", "total"), DOCUMENTOS)
def test_secao9_envelope_todo_item_cita_rn(saidas, entrada, tabela, total):
    for item in saidas[entrada]["itens"]:
        assert re.search(r"RN-\d{3}", item["justificativa"]), item["id"]


def test_secao4_exemplo2_justificativa_e002(saidas):
    e002 = next(i for i in saidas[COMERCIAL]["itens"] if i["id"] == "e-002")
    assert e002["justificativa"] == JUSTIFICATIVA_E002
    assert e002["moeda"] == "EUR"
    assert e002["taxa_cambio"] == Decimal("5.93")
    assert e002["data_cotacao"] == "2026-07-14"
    assert e002["valor_informado"] == Decimal("22.00")


def test_rn016_envelope_comercial_cita_o_centro_sem_heranca(saidas):
    citados = [
        i
        for i in saidas[COMERCIAL]["itens"]
        if i["motivo"] in {"LIMITE_DIARIO", "CATEGORIA_NAO_REEMBOLSAVEL"}
    ]
    assert len(citados) == 6
    for item in citados:
        assert "(centro de custo CC-COMERCIAL)" in item["justificativa"], item["id"]
        assert "herdado" not in item["justificativa"], item["id"]


@pytest.mark.parametrize("id_", ["f-002", "f-003"])
def test_rn016_envelope_desconhecido_cita_centro_nao_cadastrado(saidas, id_):
    item = next(i for i in saidas[DESCONHECIDO]["itens"] if i["id"] == id_)
    assert NAO_CADASTRADO in item["justificativa"]


@pytest.mark.parametrize("entrada", [COMERCIAL, DESCONHECIDO], ids=["comercial", "desconhecido"])
def test_secao9_envelope_determinismo(tmp_path, entrada):
    assert _rodar(entrada, tmp_path / "1.json") == _rodar(entrada, tmp_path / "2.json")


@pytest.mark.parametrize("entrada", [COMERCIAL, DESCONHECIDO], ids=["comercial", "desconhecido"])
def test_rn014_envelope_descricao_nao_altera_decisoes(tmp_path, saidas, entrada):
    dados = json.loads(entrada.read_text(encoding="utf-8"), parse_float=Decimal)
    for posicao, despesa in enumerate(dados["despesas"]):
        despesa["descricao"] = f"Viagem a Londres, 3 noites, hotel {posicao}"
    trocada = tmp_path / "trocada.json"
    trocada.write_text(serializar(dados), encoding="utf-8")

    def decisoes(saida):
        return [(i["valor_reembolsavel"], i["status"], i["motivo"]) for i in saida["itens"]]

    assert decisoes(_saida(trocada, tmp_path)) == decisoes(saidas[entrada])
