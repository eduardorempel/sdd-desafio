"""Documento de política (RN-015), política aplicável por centro de custo (RN-016) e
valores da política, como dados (plan §4)."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from reembolso.entrada import EntradaInvalida, ler_json, numero, texto_preenchido
from reembolso.normalizacao import normalizar_moeda, normalizar_texto

# RN-001: lista fechada de categorias reembolsáveis, já normalizadas (RN-002).
CATEGORIAS_REEMBOLSAVEIS = frozenset({"alimentacao", "transporte_urbano", "hospedagem"})

# RN-007: exige nota fiscal quando o valor considerado é estritamente maior que o limiar.
LIMIAR_NOTA_FISCAL = Decimal("100.00")

# RN-008: limite da soma reembolsada por combinação de data e categoria.
LIMITE_POR_DATA = {
    "alimentacao": Decimal("60.00"),
    "transporte_urbano": Decimal("80.00"),
    "hospedagem": Decimal("250.00"),
}

MOEDA_BASE = "BRL"
PERIODICIDADES = frozenset({"dia", "diaria"})


@dataclass(frozen=True)
class Centro:
    """Tabela de um centro de custo do documento de política."""

    codigo: str  # grafia da chave no documento (AMB-038)
    limites: dict[str, Decimal]  # categoria normalizada → limite


@dataclass(frozen=True)
class Politica:
    """Documento de política validado (RN-015)."""

    moeda_base: str
    limiar_nota_fiscal: Decimal
    padrao: dict[str, Decimal]  # categoria normalizada → limite
    centros: dict[str, Centro]  # chave normalizada → Centro


def _erro(mensagem: str) -> EntradaInvalida:
    return EntradaInvalida(f"documento de política inválido: {mensagem}")


def _objeto(valor: object, campo: str) -> dict:
    if not isinstance(valor, dict):
        raise _erro(f"{campo} ausente ou não é objeto")
    return valor


def _nao_negativo(valor: object, campo: str) -> Decimal:
    convertido = numero(valor)
    if convertido is None:
        raise _erro(f"{campo} ausente ou não é número")
    if convertido < 0:
        raise _erro(f"{campo} é negativo")
    return convertido


def _limite(entrada: object, campo: str) -> Decimal:
    """Uma entrada de categoria: limite ≥ 0 e periodicidade `dia` ou `diaria` (RN-015).

    A periodicidade não é guardada: as duas têm o mesmo efeito (AMB-036).
    """
    entrada = _objeto(entrada, campo)
    limite = _nao_negativo(entrada.get("limite"), f"{campo}.limite")
    periodicidade = entrada.get("periodicidade")
    if not isinstance(periodicidade, str):
        raise _erro(f"{campo}.periodicidade ausente ou não é texto")
    if normalizar_texto(periodicidade) not in PERIODICIDADES:
        raise _erro(f"{campo}.periodicidade {periodicidade!r} não é 'dia' nem 'diaria'")
    return limite


def _tabela(tabela: object, campo: str) -> dict[str, Decimal]:
    """Categorias com chave normalizada (RN-002); chaves que colidem são erro (RN-015)."""
    tabela = _objeto(tabela, campo)
    limites = {
        normalizar_texto(categoria): _limite(entrada, f"{campo}.{categoria}")
        for categoria, entrada in tabela.items()
    }
    if len(limites) != len(tabela):
        raise _erro(f"{campo} tem categorias iguais depois da normalização")
    return limites


def validar_politica(dados: object) -> Politica:
    """Verifica os casos de erro geral da RN-015 e levanta `EntradaInvalida`.

    `versao`, `vigencia`, `acrescimo_em_viagem_percentual`, `observacao` e campos não
    listados não são lidos.
    """
    dados = _objeto(dados, "documento")
    moeda_base = dados.get("moeda_base")
    if not texto_preenchido(moeda_base):
        raise _erro("moeda_base ausente, vazia ou não é texto")
    if normalizar_moeda(moeda_base) != MOEDA_BASE:
        raise _erro(f"moeda_base {moeda_base!r} não é {MOEDA_BASE}")
    limiar = _nao_negativo(
        dados.get("nota_fiscal_obrigatoria_acima_de"), "nota_fiscal_obrigatoria_acima_de"
    )
    padrao = _tabela(dados.get("padrao"), "padrao")
    centros_custo = _objeto(dados.get("centros_custo"), "centros_custo")
    centros = {
        normalizar_texto(codigo): Centro(codigo, _tabela(tabela, f"centros_custo.{codigo}"))
        for codigo, tabela in centros_custo.items()
    }
    if len(centros) != len(centros_custo):
        raise _erro("centros_custo tem centros iguais depois da normalização")
    return Politica(MOEDA_BASE, limiar, padrao, centros)


def ler_politica(texto: str) -> Politica:
    """Texto JSON → `Politica`. Levanta `EntradaInvalida` nos casos de erro geral (RN-015)."""
    try:
        dados = ler_json(texto)
    except EntradaInvalida as erro:
        raise _erro(str(erro)) from erro
    return validar_politica(dados)


class TipoOrigem(Enum):
    """De qual tabela veio a entrada de uma categoria (RN-016)."""

    PADRAO = "padrao"  # centro de custo ausente ou vazio
    CENTRO = "centro"  # centro cadastrado; categoria na tabela do centro ou em nenhuma
    HERDADA = "herdada"  # centro cadastrado; categoria só na padrão
    NAO_CADASTRADO = "nao_cadastrado"  # centro informado e não cadastrado


@dataclass(frozen=True)
class Origem:
    tipo: TipoOrigem
    codigo: str | None  # código a citar na justificativa (AMB-038, AMB-040)


@dataclass(frozen=True)
class PoliticaAplicavel:
    """Política escolhida para todas as despesas do documento (RN-016)."""

    limiar_nota_fiscal: Decimal
    padrao: dict[str, Decimal]
    centro: Centro | None = None
    nao_cadastrado: str | None = None  # código do centro informado e não cadastrado

    def regra(self, categoria: str) -> tuple[Decimal | None, Origem]:
        """Limite da categoria normalizada (`None` se não consta) e a origem dele."""
        if self.centro is not None:
            if categoria in self.centro.limites:
                return self.centro.limites[categoria], Origem(TipoOrigem.CENTRO, self.centro.codigo)
            if categoria in self.padrao:
                return self.padrao[categoria], Origem(TipoOrigem.HERDADA, self.centro.codigo)
            return None, Origem(TipoOrigem.CENTRO, self.centro.codigo)
        if self.nao_cadastrado is not None:
            return self.padrao.get(categoria), Origem(
                TipoOrigem.NAO_CADASTRADO, self.nao_cadastrado
            )
        return self.padrao.get(categoria), Origem(TipoOrigem.PADRAO, None)


def politica_aplicavel(politica: Politica, centro_custo: str | None) -> PoliticaAplicavel:
    """Escolhe a tabela pelo centro de custo comparado após a normalização (RN-016, RN-002).

    Centro cadastrado: categoria ausente herda da padrão (AMB-021). Não cadastrado: o
    código citado é o da entrada só sem os espaços das pontas (AMB-040).
    """
    base = {"limiar_nota_fiscal": politica.limiar_nota_fiscal, "padrao": politica.padrao}
    if centro_custo is None or not texto_preenchido(centro_custo):
        return PoliticaAplicavel(**base)
    centro = politica.centros.get(normalizar_texto(centro_custo))
    if centro is None:
        return PoliticaAplicavel(**base, nao_cadastrado=centro_custo.strip())
    return PoliticaAplicavel(**base, centro=centro)
