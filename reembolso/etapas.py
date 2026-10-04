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
