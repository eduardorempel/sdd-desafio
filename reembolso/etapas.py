"""Uma função por etapa da seção 8 da spec."""

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal

from reembolso import justificativas
from reembolso.cambio import Cambio
from reembolso.modelo import Corte, Despesa, Documento, Motivo, Recusa
from reembolso.politica import PoliticaAplicavel


@dataclass(frozen=True)
class Contexto:
    """O que toda etapa recebe além das despesas (DT-009)."""

    documento: Documento
    politica: PoliticaAplicavel
    cambio: Cambio | None = None


def valor_negativo(despesa: Despesa, _contexto: Contexto) -> Recusa | None:
    """RN-005: valor considerado menor que zero é recusado; zero é válido."""
    if despesa.valor_considerado < 0:
        return Recusa(
            Motivo.VALOR_NEGATIVO, justificativas.valor_negativo(despesa.valor_considerado)
        )
    return None


def periodo(despesa: Despesa, contexto: Contexto) -> Recusa | None:
    """RN-004: a data deve estar entre início e fim, bordas incluídas; competência não é usada."""
    documento = contexto.documento
    if documento.inicio <= despesa.data <= documento.fim:
        return None
    return Recusa(
        Motivo.FORA_DO_PERIODO,
        justificativas.fora_do_periodo(despesa.data, documento.inicio, documento.fim),
    )


def categoria(despesa: Despesa, contexto: Contexto) -> Recusa | None:
    """RN-001, RN-016: reembolsável só se consta da política aplicável com limite maior que zero.

    Comparada após normalização (RN-002); limite 0 é "não reembolsável" (AMB-022), e o texto
    de `observacao` não é usado.
    """
    limite, origem = contexto.politica.regra(despesa.categoria)
    if limite is not None and limite > 0:
        return None
    return Recusa(
        Motivo.CATEGORIA_NAO_REEMBOLSAVEL,
        justificativas.categoria_nao_reembolsavel(despesa.categoria, origem),
    )


def duplicatas(vivas: list[Despesa], _contexto: Contexto) -> dict[int, Recusa]:
    """RN-006: agrupa por data, categoria, fornecedor e valor considerado e mantém uma por grupo.

    Fica a de menor posição entre as que têm nota fiscal; se nenhuma tiver, a de menor
    posição. `vivas` chega em ordem de posição.
    """
    grupos: dict[tuple, list[Despesa]] = defaultdict(list)
    for despesa in vivas:
        chave = (despesa.data, despesa.categoria, despesa.fornecedor, despesa.valor_considerado)
        grupos[chave].append(despesa)

    recusas: dict[int, Recusa] = {}
    for grupo in grupos.values():
        com_nota = [d for d in grupo if d.tem_nota_fiscal]
        mantida = (com_nota or grupo)[0]
        for despesa in grupo:
            if despesa is not mantida:
                recusas[despesa.posicao] = Recusa(
                    Motivo.DUPLICATA, justificativas.duplicata(mantida.id)
                )
    return recusas


def nota_fiscal(despesa: Despesa, contexto: Contexto) -> Recusa | None:
    """RN-007: valor da própria despesa acima do limiar do documento e sem nota é recusado."""
    limiar = contexto.politica.limiar_nota_fiscal
    if despesa.valor_considerado > limiar and not despesa.tem_nota_fiscal:
        return Recusa(Motivo.NOTA_FISCAL_AUSENTE, justificativas.nota_fiscal_ausente(limiar))
    return None


def limites_por_data(vivas: list[Despesa], contexto: Contexto) -> dict[int, Corte]:
    """RN-008, RN-009, RN-010: limite por data e categoria, consumido na ordem da posição.

    O limite vem da tabela efetiva da política aplicável (RN-016), e a justificativa cita
    a origem dele; `dia` e `diaria` são, as duas, limite por data. `representacao` é uma
    categoria como as outras (AMB-023), e o acréscimo em viagem não é lido (AMB-035).
    Cada despesa recebe o menor valor entre o seu valor considerado e o saldo deixado
    pelas anteriores; o excedente é cortado. `vivas` chega em ordem de posição.
    """
    consumos: dict[tuple, Decimal] = defaultdict(Decimal)
    consumidoras: dict[tuple, list[str]] = defaultdict(list)
    cortes: dict[int, Corte] = {}
    for despesa in vivas:
        limite, origem = contexto.politica.regra(despesa.categoria)
        chave = (despesa.data, despesa.categoria)
        consumido = consumos[chave]
        reembolsavel = min(despesa.valor_considerado, limite - consumido)
        if reembolsavel < despesa.valor_considerado:
            cortes[despesa.posicao] = Corte(
                reembolsavel,
                Motivo.LIMITE_DIARIO,
                justificativas.limite_diario(
                    despesa.categoria,
                    limite,
                    origem,
                    despesa.data,
                    consumido,
                    list(consumidoras[chave]),
                    despesa.valor_considerado - reembolsavel,
                ),
            )
        if reembolsavel > 0:
            consumos[chave] = consumido + reembolsavel
            consumidoras[chave].append(despesa.id)
    return cortes
