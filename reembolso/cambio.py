"""Documento de câmbio (RN-018)."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from reembolso.entrada import EntradaInvalida, data_valida, ler_json, numero, texto_preenchido
from reembolso.normalizacao import normalizar_moeda


@dataclass(frozen=True)
class Cambio:
    """Documento de câmbio validado (RN-018)."""

    moeda_base: str
    taxas: dict[str, list[tuple[date, Decimal]]]  # moeda → (data, taxa), ordenado por data


def _erro(mensagem: str) -> EntradaInvalida:
    return EntradaInvalida(f"documento de câmbio inválido: {mensagem}")


def _taxas_da_data(chave: str, taxas: object) -> dict[str, Decimal]:
    """Taxas de uma data, com código normalizado (RN-017); taxa deve ser número > 0."""
    if not isinstance(taxas, dict):
        raise _erro(f"taxas.{chave} não é objeto")
    lidas = {}
    for moeda, taxa in taxas.items():
        convertida = numero(taxa)
        if convertida is None:
            raise _erro(f"taxas.{chave}.{moeda} não é número")
        if convertida <= 0:
            raise _erro(f"taxas.{chave}.{moeda} é menor ou igual a zero")
        lidas[normalizar_moeda(moeda)] = convertida
    if len(lidas) != len(taxas):
        raise _erro(f"taxas.{chave} tem moedas iguais depois da normalização")
    return lidas


def validar_cambio(dados: object, moeda_base_politica: str) -> Cambio:
    """Verifica os casos de erro geral da RN-018 e levanta `EntradaInvalida`.

    `fonte`, `observacao` e campos não listados não são lidos.
    """
    if not isinstance(dados, dict):
        raise _erro("documento não é objeto")
    moeda_base = dados.get("moeda_base")
    if not texto_preenchido(moeda_base):
        raise _erro("moeda_base ausente, vazia ou não é texto")
    if normalizar_moeda(moeda_base) != normalizar_moeda(moeda_base_politica):
        raise _erro(f"moeda_base {moeda_base!r} diferente da moeda_base da política")
    taxas = dados.get("taxas")
    if not isinstance(taxas, dict):
        raise _erro("taxas ausente ou não é objeto")

    por_moeda: dict[str, list[tuple[date, Decimal]]] = {}
    for chave, taxas_da_data in taxas.items():
        data = data_valida(chave)
        if data is None:
            raise _erro(f"chave {chave!r} de taxas não é data válida (AAAA-MM-DD)")
        for moeda, taxa in _taxas_da_data(chave, taxas_da_data).items():
            por_moeda.setdefault(moeda, []).append((data, taxa))
    return Cambio(
        normalizar_moeda(moeda_base),
        {moeda: sorted(lista) for moeda, lista in por_moeda.items()},
    )


def ler_cambio(texto: str, moeda_base_politica: str) -> Cambio:
    """Texto JSON → `Cambio`. Levanta `EntradaInvalida` nos casos de erro geral (RN-018)."""
    try:
        dados = ler_json(texto)
    except EntradaInvalida as erro:
        raise _erro(str(erro)) from erro
    return validar_cambio(dados, moeda_base_politica)
