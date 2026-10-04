"""Uma função por etapa da seção 8 da spec (etapas 3 a 8)."""

from collections import defaultdict

from reembolso import justificativas, politica
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


def categoria(despesa: Despesa, _documento: Documento) -> Recusa | None:
    """RN-001: só categorias da lista fechada, comparadas após normalização (RN-002)."""
    if despesa.categoria in politica.CATEGORIAS_REEMBOLSAVEIS:
        return None
    return Recusa(
        Motivo.CATEGORIA_NAO_REEMBOLSAVEL,
        justificativas.categoria_nao_reembolsavel(despesa.categoria),
    )


def duplicatas(vivas: list[Despesa], _documento: Documento) -> dict[int, Recusa]:
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


def nota_fiscal(despesa: Despesa, _documento: Documento) -> Recusa | None:
    """RN-007: valor da própria despesa acima do limiar e sem nota é recusado inteiro."""
    if despesa.valor_considerado > politica.LIMIAR_NOTA_FISCAL and not despesa.tem_nota_fiscal:
        return Recusa(
            Motivo.NOTA_FISCAL_AUSENTE,
            justificativas.nota_fiscal_ausente(politica.LIMIAR_NOTA_FISCAL),
        )
    return None
