"""Leitura e validação da entrada (etapas 1 e 2 da spec §8; RN-013)."""

import json
import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

_FORMATO_DATA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")


class EntradaInvalida(Exception):
    """Erro geral da RN-013: o documento inteiro é rejeitado e não há saída."""


@dataclass(frozen=True)
class Cabecalho:
    """Partes do documento validadas no nível geral (RN-013)."""

    colaborador: dict
    periodo: dict
    inicio: date
    fim: date
    itens: list[dict]


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


def texto_preenchido(valor: object) -> bool:
    """Texto com ao menos um caractere que não é espaço (RN-013)."""
    return isinstance(valor, str) and valor.strip() != ""


def data_valida(valor: object) -> date | None:
    """Data exatamente em `AAAA-MM-DD` e existente no calendário (RN-013, DT-002)."""
    if not isinstance(valor, str) or not _FORMATO_DATA.fullmatch(valor):
        return None
    try:
        return date.fromisoformat(valor)
    except ValueError:
        return None


def validar_documento(dados: object) -> Cabecalho:
    """Verifica os casos de erro geral da RN-013 e levanta `EntradaInvalida`.

    Campos informativos e desconhecidos não são lidos.
    """
    if not isinstance(dados, dict):
        raise EntradaInvalida("documento não é um objeto com colaborador, periodo e despesas")

    colaborador = dados.get("colaborador")
    if not isinstance(colaborador, dict):
        raise EntradaInvalida("colaborador ausente ou não é objeto")
    periodo = dados.get("periodo")
    if not isinstance(periodo, dict):
        raise EntradaInvalida("periodo ausente ou não é objeto")

    if not texto_preenchido(colaborador.get("id")):
        raise EntradaInvalida("colaborador.id ausente, vazio ou não é texto")

    inicio = data_valida(periodo.get("inicio"))
    if inicio is None:
        raise EntradaInvalida("periodo.inicio ausente ou não é data válida (AAAA-MM-DD)")
    fim = data_valida(periodo.get("fim"))
    if fim is None:
        raise EntradaInvalida("periodo.fim ausente ou não é data válida (AAAA-MM-DD)")
    if inicio > fim:
        raise EntradaInvalida("periodo.inicio é posterior a periodo.fim")

    itens = dados.get("despesas")
    if not isinstance(itens, list):
        raise EntradaInvalida("despesas ausente ou não é lista")
    for posicao, item in enumerate(itens, start=1):
        if not isinstance(item, dict):
            raise EntradaInvalida(f"item {posicao} de despesas não é objeto")

    return Cabecalho(colaborador, periodo, inicio, fim, itens)
