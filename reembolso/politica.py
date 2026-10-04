"""Valores da política de reembolso, como dados (plan §4, DT-004)."""

from decimal import Decimal

# RN-001: lista fechada de categorias reembolsáveis, já normalizadas (RN-002).
CATEGORIAS_REEMBOLSAVEIS = frozenset({"alimentacao", "transporte_urbano", "hospedagem"})

# RN-007: exige nota fiscal quando o valor considerado é estritamente maior que o limiar.
LIMIAR_NOTA_FISCAL = Decimal("100.00")
