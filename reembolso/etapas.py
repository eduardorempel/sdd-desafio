"""Uma função por etapa da seção 8 da spec (etapas 3 a 8)."""

from reembolso import justificativas
from reembolso.modelo import Despesa, Documento, Motivo, Recusa


def valor_negativo(despesa: Despesa, _documento: Documento) -> Recusa | None:
    """RN-005: valor considerado menor que zero é recusado; zero é válido."""
    if despesa.valor_considerado < 0:
        return Recusa(
            Motivo.VALOR_NEGATIVO, justificativas.valor_negativo(despesa.valor_considerado)
        )
    return None


def periodo(despesa: Despesa, documento: Documento) -> Recusa | None:
    """RN-004: a data deve estar entre início e fim, bordas incluídas; competência não é usada."""
    if documento.inicio <= despesa.data <= documento.fim:
        return None
    return Recusa(
        Motivo.FORA_DO_PERIODO,
        justificativas.fora_do_periodo(despesa.data, documento.inicio, documento.fim),
    )
