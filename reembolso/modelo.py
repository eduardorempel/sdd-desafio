"""Estruturas de dados do motor (plan §3)."""

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import StrEnum


class Status(StrEnum):
    """Status de um item da saída (spec §4)."""

    APROVADO = "aprovado"
    LIMITADO = "limitado"
    RECUSADO = "recusado"


class Motivo(StrEnum):
    """Códigos de motivo da saída (spec §4, tabela de motivos)."""

    DADOS_INVALIDOS = "DADOS_INVALIDOS"
    VALOR_NEGATIVO = "VALOR_NEGATIVO"
    FORA_DO_PERIODO = "FORA_DO_PERIODO"
    CATEGORIA_NAO_REEMBOLSAVEL = "CATEGORIA_NAO_REEMBOLSAVEL"
    DUPLICATA = "DUPLICATA"
    NOTA_FISCAL_AUSENTE = "NOTA_FISCAL_AUSENTE"
    LIMITE_DIARIO = "LIMITE_DIARIO"


@dataclass(frozen=True)
class Despesa:
    """Despesa que passou pela etapa 1 (RN-013), já normalizada e arredondada."""

    posicao: int
    id: str
    data: date
    categoria: str
    fornecedor: str
    tem_nota_fiscal: bool
    valor_informado: Decimal
    valor_considerado: Decimal


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


@dataclass(frozen=True)
class Resultado:
    id: str | None
    valor_informado: Decimal | None
    valor_considerado: Decimal | None
    valor_reembolsavel: Decimal
    status: Status
    motivo: Motivo | None
    justificativa: str
