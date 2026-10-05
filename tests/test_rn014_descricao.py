import json
from decimal import Decimal
from pathlib import Path

import pytest
from fabrica import politica_aplicavel

from reembolso.entrada import ler_documento
from reembolso.motor import calcular
from reembolso.saida import montar_saida, serializar

EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas-exemplo.json"

REMOVER = object()


def _decisoes(dados: dict) -> list[tuple]:
    texto = serializar(dados)
    documento = ler_documento(texto)
    saida = montar_saida(documento, calcular(documento, politica_aplicavel()))
    return [(i["valor_reembolsavel"], i["status"], i["motivo"]) for i in saida["itens"]]


def _com_descricoes(trocar) -> dict:
    dados = json.loads(EXEMPLO.read_text(encoding="utf-8"), parse_float=Decimal)
    for posicao, despesa in enumerate(dados["despesas"]):
        nova = trocar(posicao, despesa)
        if nova is REMOVER:
            despesa.pop("descricao", None)
        else:
            despesa["descricao"] = nova
    return dados


@pytest.mark.parametrize(
    "trocar",
    [
        lambda p, _d: f"Descrição trocada {p}",
        lambda _p, _d: "Hotel - 3 diarias em viagem a trabalho, corrida aeroporto",
        lambda _p, d: d["descricao"].upper(),
        lambda _p, _d: "",
        lambda p, _d: p,
        lambda _p, _d: REMOVER,
    ],
    ids=[
        "texto_qualquer",
        "indicios_de_viagem_e_diarias",
        "maiusculas",
        "vazia",
        "numero",
        "ausente",
    ],
)
def test_rn014_trocar_descricoes_nao_altera_decisoes(trocar):
    original = _decisoes(_com_descricoes(lambda _p, d: d["descricao"]))
    assert _decisoes(_com_descricoes(trocar)) == original


def test_rn014_descricao_diferente_nao_impede_duplicata():
    # Trocar só a descrição de d-007 não desfaz a duplicata com d-006 (RN-006).
    def trocar(_posicao, despesa):
        return "Outra descrição" if despesa["id"] == "d-007" else despesa["descricao"]

    decisoes = _decisoes(_com_descricoes(trocar))
    assert decisoes[6][2] == "DUPLICATA"
