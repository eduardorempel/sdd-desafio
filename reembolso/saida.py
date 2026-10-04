"""Montagem e serialização do documento de saída (spec §4, RN-003, DT-005)."""

import json
from decimal import Decimal

from reembolso.modelo import Documento, Resultado
from reembolso.normalizacao import CENTAVO


def _dinheiro(valor: Decimal | None) -> Decimal | None:
    """Duas casas decimais (RN-003). Os valores já chegam arredondados."""
    return None if valor is None else valor.quantize(CENTAVO)


def _item(resultado: Resultado) -> dict:
    return {
        "id": resultado.id,
        "valor_informado": resultado.valor_informado,
        "valor_considerado": _dinheiro(resultado.valor_considerado),
        "valor_reembolsavel": _dinheiro(resultado.valor_reembolsavel),
        "status": resultado.status.value,
        "motivo": None if resultado.motivo is None else resultado.motivo.value,
        "justificativa": resultado.justificativa,
    }


def montar_saida(documento: Documento, resultados: list[Resultado]) -> dict:
    """Estrutura da saída da spec §4, com `None` onde a spec pede nulo."""
    total = sum((r.valor_reembolsavel for r in resultados), Decimal("0.00"))
    return {
        "colaborador": documento.colaborador,
        "periodo": documento.periodo,
        "itens": [_item(r) for r in resultados],
        "total_reembolsavel": _dinheiro(total),
    }


def _escrever(valor: object, nivel: int) -> str:
    if isinstance(valor, Decimal):
        # Literal numérico JSON com as casas do próprio Decimal (DT-005).
        return str(valor)
    recuo, recuo_interno = "  " * nivel, "  " * (nivel + 1)
    if isinstance(valor, dict):
        if not valor:
            return "{}"
        campos = [
            f"{recuo_interno}{json.dumps(str(chave), ensure_ascii=False)}: "
            f"{_escrever(item, nivel + 1)}"
            for chave, item in valor.items()
        ]
        return "{\n" + ",\n".join(campos) + f"\n{recuo}}}"
    if isinstance(valor, list):
        if not valor:
            return "[]"
        itens = [f"{recuo_interno}{_escrever(item, nivel + 1)}" for item in valor]
        return "[\n" + ",\n".join(itens) + f"\n{recuo}]"
    return json.dumps(valor, ensure_ascii=False)


def serializar(saida: dict) -> str:
    """JSON com recuo de 2 espaços, sem escapar acentos, com `Decimal` como número."""
    return _escrever(saida, 0) + "\n"
