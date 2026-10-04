"""Interface de linha de comando. Único módulo que toca disco, stdout e stderr (plan §2)."""

import argparse
import sys
from pathlib import Path

from reembolso.entrada import EntradaInvalida, ler_documento
from reembolso.motor import calcular
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
    calcular_.add_argument("--output", required=True, type=Path, help="JSON de resultado")
    return parser


def _calcular(entrada: Path) -> str:
    try:
        texto = entrada.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as erro:
        raise EntradaInvalida(f"não foi possível ler {entrada}: {erro}") from erro
    documento = ler_documento(texto)
    return serializar(montar_saida(documento, calcular(documento)))


def main(argv: list[str] | None = None) -> int:
    """Sucesso: 0. Erro geral da RN-013: mensagem em stderr, 1, sem saída (DT-006).

    Argumentos inválidos: 2, pelo argparse.
    """
    args = _parser().parse_args(argv)
    try:
        texto = _calcular(args.input)
    except EntradaInvalida as erro:
        print(f"erro: {erro}", file=sys.stderr)
        return 1
    # O arquivo de saída só é aberto depois que leitura, validação e cálculo terminaram.
    with args.output.open("w", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write(texto)
    return 0
