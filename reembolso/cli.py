"""Interface de linha de comando. Único módulo que toca disco, stdout e stderr (plan §2)."""

import argparse
import sys
from pathlib import Path

from reembolso.entrada import EntradaInvalida, ler_documento
from reembolso.motor import calcular
from reembolso.politica import ler_politica, politica_aplicavel
from reembolso.saida import montar_saida, serializar


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m reembolso",
        description="Motor de cálculo de reembolso de despesas corporativas.",
    )
    subcomandos = parser.add_subparsers(dest="comando", required=True)
    calcular_ = subcomandos.add_parser(
        "calcular", help="calcula o reembolso de um documento de despesas"
    )
    calcular_.add_argument("--input", required=True, type=Path, help="JSON de despesas")
    # Não é obrigatório no argparse: a falta da política é erro geral, código 1 (DT-006).
    calcular_.add_argument("--politica", type=Path, help="JSON da política de reembolso")
    calcular_.add_argument("--output", required=True, type=Path, help="JSON de resultado")
    return parser


def _ler(caminho: Path) -> str:
    try:
        return caminho.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as erro:
        raise EntradaInvalida(f"não foi possível ler {caminho}: {erro}") from erro


def _calcular(entrada: Path, politica: Path | None) -> str:
    documento = ler_documento(_ler(entrada))
    if politica is None:
        raise EntradaInvalida("documento de política não informado (--politica)")
    # Até a T-038, o fluxo real usa a política padrão, sem escolher por centro de custo.
    aplicavel = politica_aplicavel(ler_politica(_ler(politica)), None)
    return serializar(montar_saida(documento, calcular(documento, aplicavel)))


def main(argv: list[str] | None = None) -> int:
    """Sucesso: 0. Erro geral (RN-013, RN-015): mensagem em stderr, 1, sem saída (DT-006).

    Argumentos inválidos: 2, pelo argparse.
    """
    args = _parser().parse_args(argv)
    try:
        texto = _calcular(args.input, args.politica)
    except EntradaInvalida as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 1
    # O arquivo de saída só é aberto depois que leitura, validação e cálculo terminaram.
    with args.output.open("w", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write(texto)
    return 0
