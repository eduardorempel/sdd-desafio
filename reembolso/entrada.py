"""Leitura e validação da entrada (etapas 1 e 2 da spec §8; RN-013)."""

import json
import re
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from reembolso.modelo import MOEDA_BASE, Despesa, Documento, Invalida
from reembolso.normalizacao import arredondar, normalizar_moeda, normalizar_texto

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
    centro_custo: str | None


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
    centro_custo = colaborador.get("centro_custo")
    if "centro_custo" in colaborador and not isinstance(centro_custo, str):
        raise EntradaInvalida("colaborador.centro_custo não é texto")

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

    return Cabecalho(colaborador, periodo, inicio, fim, itens, centro_custo)


def numero(valor: object) -> Decimal | None:
    """Valor numérico como Decimal; `bool` não é número (DT-002)."""
    if isinstance(valor, bool):
        return None
    if isinstance(valor, Decimal):
        return valor
    if isinstance(valor, int):
        return Decimal(valor)
    return None


def _problema_texto(item: dict, campo: str) -> str | None:
    if campo not in item:
        return f"{campo} ausente"
    if not isinstance(item[campo], str):
        return f"{campo} não é texto"
    if not texto_preenchido(item[campo]):
        return f"{campo} vazio"
    return None


def _problemas(item: dict) -> list[str]:
    """Lista os casos de erro em uma despesa previstos na RN-013, na ordem dos campos."""
    problemas = [_problema_texto(item, "id")]
    if "data" not in item:
        problemas.append("data ausente")
    elif data_valida(item["data"]) is None:
        problemas.append("data não é data válida (AAAA-MM-DD)")
    problemas.append(_problema_texto(item, "categoria"))
    problemas.append(_problema_texto(item, "fornecedor"))
    if "valor" not in item:
        problemas.append("valor ausente")
    elif numero(item["valor"]) is None:
        problemas.append("valor não é numérico")
    if "tem_nota_fiscal" not in item:
        problemas.append("tem_nota_fiscal ausente")
    elif not isinstance(item["tem_nota_fiscal"], bool):
        problemas.append("tem_nota_fiscal não é verdadeiro/falso")
    if "moeda" in item:
        problemas.append(_problema_texto(item, "moeda"))
    return [p for p in problemas if p is not None]


def validar_despesa(item: dict, posicao: int) -> Invalida | None:
    """Devolve `Invalida` se a despesa tiver erro da RN-013, ou `None` se for válida.

    `moeda` é opcional; presente, deve ser texto não vazio (RN-017). Campos informativos
    (`descricao`) e desconhecidos não são lidos.
    """
    problemas = _problemas(item)
    if not problemas:
        return None
    return Invalida(
        posicao=posicao,
        id=item["id"] if _problema_texto(item, "id") is None else None,
        valor_informado=numero(item.get("valor")),
        detalhe="; ".join(problemas),
    )


def ler_despesa(item: dict, posicao: int) -> Despesa | Invalida:
    """Etapas 1 e 2 da spec §8: valida (RN-013, RN-017), normaliza (RN-002, RN-017) e
    arredonda (RN-003). Sem `moeda`, a moeda é `BRL` (RN-017)."""
    invalida = validar_despesa(item, posicao)
    if invalida is not None:
        return invalida
    valor_informado = numero(item["valor"])
    moeda = normalizar_moeda(item.get("moeda", MOEDA_BASE))
    # Em BRL a conversão é a identidade (RN-003); as demais moedas são convertidas na
    # etapa 3, que preenche `valor_considerado` (DT-010).
    considerado = arredondar(valor_informado) if moeda == MOEDA_BASE else None
    return Despesa(
        posicao=posicao,
        id=item["id"],
        data=data_valida(item["data"]),
        categoria=normalizar_texto(item["categoria"]),
        fornecedor=normalizar_texto(item["fornecedor"]),
        tem_nota_fiscal=item["tem_nota_fiscal"],
        valor_informado=valor_informado,
        valor_considerado=considerado,
        moeda=moeda,
    )


def ler_documento(texto: str) -> Documento:
    """Texto JSON → `Documento`. Levanta `EntradaInvalida` nos casos de erro geral (RN-013)."""
    cabecalho = validar_documento(ler_json(texto))
    return Documento(
        colaborador=cabecalho.colaborador,
        periodo=cabecalho.periodo,
        inicio=cabecalho.inicio,
        fim=cabecalho.fim,
        despesas=[
            ler_despesa(item, posicao) for posicao, item in enumerate(cabecalho.itens, start=1)
        ],
        centro_custo=cabecalho.centro_custo,
    )
