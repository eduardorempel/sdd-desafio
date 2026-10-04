"""Leitura e validação da entrada (etapas 1 e 2 da spec §8; RN-013)."""

import json
from decimal import Decimal


class EntradaInvalida(Exception):
    """Erro geral da RN-013: o documento inteiro é rejeitado e não há saída."""


def _rejeitar_constante(nome: str):
    raise EntradaInvalida(f"documento não é JSON válido: literal {nome} não é permitido")


def ler_json(texto: str) -> object:
    """Converte o texto em objetos Python, com números não inteiros como Decimal (DT-001).

    `NaN`, `Infinity` e `-Infinity` são rejeitados (DT-003).
    """
    try:
        return json.loads(texto, parse_float=Decimal, parse_constant=_rejeitar_constante)
    except json.JSONDecodeError as erro:
        raise EntradaInvalida(f"documento não é JSON válido: {erro}") from erro
