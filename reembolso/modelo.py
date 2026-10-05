"""Estruturas de dados do motor (plan §3)."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum

MOEDA_BASE = "BRL"  # moeda dos limites e de `valor_considerado` (RN-015, RN-018)


class Status(StrEnum):
    """Status de um item da saída (spec §4)."""

    APROVADO = "aprovado"
    LIMITADO = "limitado"
    RECUSADO = "recusado"


class Motivo(StrEnum):
    """Códigos de motivo da saída (spec §4, tabela de motivos)."""

    DADOS_INVALIDOS = "DADOS_INVALIDOS"
    COTACAO_INDISPONIVEL = "COTACAO_INDISPONIVEL"
    VALOR_NEGATIVO = "VALOR_NEGATIVO"
    FORA_DO_PERIODO = "FORA_DO_PERIODO"
    CATEGORIA_NAO_REEMBOLSAVEL = "CATEGORIA_NAO_REEMBOLSAVEL"
    DUPLICATA = "DUPLICATA"
    NOTA_FISCAL_AUSENTE = "NOTA_FISCAL_AUSENTE"
    LIMITE_DIARIO = "LIMITE_DIARIO"


@dataclass(frozen=True)
class Despesa:
    """Despesa que passou pela etapa 1 (RN-013), já normalizada e arredondada.

    `valor_informado` está na moeda da despesa; `valor_considerado`, em reais (RN-018).
    """

    posicao: int
    id: str
    data: date
    categoria: str
    fornecedor: str
    tem_nota_fiscal: bool
    valor_informado: Decimal
    valor_considerado: Decimal | None  # None até a etapa 3 em moeda estrangeira (DT-010)
    moeda: str = MOEDA_BASE  # normalizada (RN-017)
    taxa_cambio: Decimal | None = None  # como está no documento de câmbio; None em BRL
    data_cotacao: date | None = None  # data da taxa usada; None em BRL


@dataclass(frozen=True)
class Invalida:
    """Despesa recusada na etapa 1 (RN-013)."""

    posicao: int
    id: str | None
    valor_informado: Decimal | None
    detalhe: str


@dataclass(frozen=True)
class Documento:
    colaborador: dict
    periodo: dict
    inicio: date
    fim: date
    despesas: list[Despesa | Invalida]
    centro_custo: str | None = None  # como veio (já validado como texto); None se ausente


@dataclass(frozen=True)
class Resultado:
    id: str | None
    valor_informado: Decimal | None
    valor_considerado: Decimal | None
    valor_reembolsavel: Decimal
    status: Status
    motivo: Motivo | None
    justificativa: str
    moeda: str | None = "BRL"
    taxa_cambio: Decimal | None = None
    data_cotacao: date | None = None


@dataclass(frozen=True)
class Recusa:
    """Decisão de uma etapa que recusa a despesa (spec §8)."""

    motivo: Motivo
    justificativa: str


@dataclass(frozen=True)
class Corte:
    """Decisão de uma etapa em grupo que reduz o valor reembolsável (spec §8, etapa 8)."""

    valor_reembolsavel: Decimal
    motivo: Motivo
    justificativa: str
