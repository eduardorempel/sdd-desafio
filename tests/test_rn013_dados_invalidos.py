import json
from datetime import date
from decimal import Decimal

import pytest

from reembolso.entrada import (
    EntradaInvalida,
    ler_despesa,
    ler_documento,
    ler_json,
    validar_despesa,
    validar_documento,
)
from reembolso.modelo import Despesa, Invalida


def test_rn013_json_invalido_erro_geral():
    with pytest.raises(EntradaInvalida):
        ler_json('{"colaborador": ')


def test_rn013_nan_erro_geral():
    with pytest.raises(EntradaInvalida):
        ler_json('{"valor": NaN}')


@pytest.mark.parametrize("literal", ["Infinity", "-Infinity"])
def test_rn013_infinity_erro_geral(literal):
    with pytest.raises(EntradaInvalida):
        ler_json(f'{{"valor": {literal}}}')


def test_dt001_float_lido_como_decimal():
    valor = ler_json('{"valor": 33.333}')["valor"]
    assert isinstance(valor, Decimal)
    assert valor == Decimal("33.333")


def test_dt001_metade_nao_sofre_erro_de_float():
    assert ler_json('{"valor": 10.005}')["valor"] == Decimal("10.005")


_REMOVER = object()


def _documento(**alteracoes):
    doc = {
        "colaborador": {"id": "c-0417", "nome": "Marina Volpi"},
        "periodo": {"competencia": "2026-07", "inicio": "2026-07-01", "fim": "2026-07-31"},
        "despesas": [],
    }
    for caminho, valor in alteracoes.items():
        alvo = doc
        *pais, campo = caminho.split("__")
        for pai in pais:
            alvo = alvo[pai]
        if valor is _REMOVER:
            del alvo[campo]
        else:
            alvo[campo] = valor
    return doc


@pytest.mark.parametrize(
    "alteracoes",
    [
        {"periodo__fim": _REMOVER},
        {"periodo__inicio": _REMOVER},
        {"periodo__inicio": "2026-02-30"},
        {"periodo__inicio": "2026-7-1"},
        {"periodo__fim": 20260731},
        {"periodo__inicio": "2026-08-01"},
        {"colaborador__id": "  "},
        {"colaborador__id": 417},
        {"colaborador__id": _REMOVER},
        {"colaborador": _REMOVER},
        {"colaborador": "c-0417"},
        {"periodo": _REMOVER},
        {"periodo": ["2026-07-01", "2026-07-31"]},
        {"despesas": _REMOVER},
        {"despesas": {"id": "d-001"}},
        {"despesas": [{"id": "d-001"}, "d-002"]},
        {"colaborador__centro_custo": 42},
        {"colaborador__centro_custo": None},
    ],
    ids=[
        "sem_periodo_fim",
        "sem_periodo_inicio",
        "periodo_inicio_inexistente",
        "periodo_inicio_fora_do_formato",
        "periodo_fim_nao_texto",
        "inicio_posterior_ao_fim",
        "colaborador_id_so_espacos",
        "colaborador_id_numerico",
        "sem_colaborador_id",
        "sem_colaborador",
        "colaborador_nao_objeto",
        "sem_periodo",
        "periodo_nao_objeto",
        "sem_despesas",
        "despesas_nao_lista",
        "item_nao_objeto",
        "centro_custo_numerico",
        "centro_custo_nulo",
    ],
)
def test_rn013_erro_geral_documento_invalido(alteracoes):
    with pytest.raises(EntradaInvalida):
        validar_documento(_documento(**alteracoes))


def test_rn013_erro_geral_documento_nao_objeto():
    with pytest.raises(EntradaInvalida):
        validar_documento([])


def test_rn013_erro_geral_nao_ocorre_com_competencia_malformada():
    cabecalho = validar_documento(_documento(periodo__competencia="julho"))
    assert cabecalho.inicio == date(2026, 7, 1)
    assert cabecalho.fim == date(2026, 7, 31)


def test_rn013_erro_geral_nao_ocorre_com_despesas_vazia():
    assert validar_documento(_documento(despesas=[])).itens == []


def test_rn013_erro_geral_nao_ocorre_com_campos_informativos_e_desconhecidos():
    doc = _documento(colaborador__nome=123, extra={"x": 1})
    validar_documento(doc)


def test_rn013_erro_geral_nao_ocorre_com_centro_custo_texto_ausente_ou_vazio():
    assert validar_documento(_documento(colaborador__centro_custo="  ")).centro_custo == "  "
    assert validar_documento(_documento()).centro_custo is None


def test_rn013_centro_custo_chega_ao_documento_como_veio():
    texto = json.dumps(_documento(colaborador__centro_custo=" cc-comercial "))
    assert ler_documento(texto).centro_custo == " cc-comercial "


def test_rn013_erro_geral_nao_ocorre_com_inicio_igual_ao_fim():
    validar_documento(_documento(periodo__inicio="2026-07-31"))


def _despesa(**alteracoes):
    item = {
        "id": "d-001",
        "data": "2026-07-03",
        "categoria": "alimentacao",
        "descricao": "Almoco",
        "fornecedor": "Restaurante Tavola",
        "valor": Decimal("50.00"),
        "tem_nota_fiscal": True,
    }
    for campo, valor in alteracoes.items():
        if valor is _REMOVER:
            del item[campo]
        else:
            item[campo] = valor
    return item


@pytest.mark.parametrize(
    "alteracoes",
    [
        {"tem_nota_fiscal": _REMOVER},
        {"tem_nota_fiscal": "sim"},
        {"tem_nota_fiscal": 1},
        {"fornecedor": "   "},
        {"fornecedor": _REMOVER},
        {"fornecedor": 42},
        {"categoria": ""},
        {"categoria": None},
        {"data": "2026-7-3"},
        {"data": "2026-02-30"},
        {"data": "20260703"},
        {"data": "2026-07-03T10:00"},
        {"data": _REMOVER},
        {"valor": "72.50"},
        {"valor": True},
        {"valor": None},
        {"valor": _REMOVER},
    ],
    ids=[
        "sem_tem_nota_fiscal",
        "tem_nota_fiscal_texto",
        "tem_nota_fiscal_numero",
        "fornecedor_so_espacos",
        "sem_fornecedor",
        "fornecedor_numerico",
        "categoria_vazia",
        "categoria_nula",
        "data_fora_do_formato",
        "data_inexistente",
        "data_sem_hifens",
        "data_com_hora",
        "sem_data",
        "valor_texto",
        "valor_booleano",
        "valor_nulo",
        "sem_valor",
    ],
)
def test_rn013_despesa_invalida_vira_dados_invalidos(alteracoes):
    invalida = validar_despesa(_despesa(**alteracoes), posicao=3)
    assert isinstance(invalida, Invalida)
    assert invalida.posicao == 3
    assert invalida.id == "d-001"
    assert invalida.detalhe


@pytest.mark.parametrize(
    "id_",
    [17, "", "   ", None, _REMOVER],
    ids=["numerico", "vazio", "so_espacos", "nulo", "ausente"],
)
def test_rn013_despesa_com_id_invalido_tem_id_nulo(id_):
    invalida = validar_despesa(_despesa(id=id_), posicao=1)
    assert isinstance(invalida, Invalida)
    assert invalida.id is None


@pytest.mark.parametrize(
    "valor", ["72.50", True, None, _REMOVER], ids=["texto", "booleano", "nulo", "ausente"]
)
def test_rn013_despesa_com_valor_nao_numerico_tem_valor_informado_nulo(valor):
    invalida = validar_despesa(_despesa(valor=valor), posicao=1)
    assert invalida.valor_informado is None


def test_rn013_despesa_com_valor_valido_e_outro_campo_invalido_mantem_valor_informado():
    invalida = validar_despesa(_despesa(tem_nota_fiscal=_REMOVER), posicao=1)
    assert invalida.valor_informado == Decimal("50.00")


def test_rn013_despesa_com_valor_inteiro_valido_mantem_valor_informado():
    invalida = validar_despesa(_despesa(valor=50, fornecedor=""), posicao=1)
    assert invalida.valor_informado == Decimal("50")


def test_rn013_despesa_detalhe_cita_o_campo():
    assert "tem_nota_fiscal" in validar_despesa(_despesa(tem_nota_fiscal=_REMOVER), 1).detalhe


def test_rn013_despesa_campo_desconhecido_e_ignorado():
    assert validar_despesa(_despesa(projeto="X"), posicao=1) is None


def test_rn013_despesa_descricao_malformada_e_ignorada():
    assert validar_despesa(_despesa(descricao=123), posicao=1) is None


def test_rn013_despesa_sem_descricao_e_valida():
    assert validar_despesa(_despesa(descricao=_REMOVER), posicao=1) is None


@pytest.mark.parametrize("valor", [Decimal("-45.00"), 0, 100], ids=["negativo", "zero", "inteiro"])
def test_rn013_despesa_com_valor_numerico_e_valida(valor):
    assert validar_despesa(_despesa(valor=valor), posicao=1) is None


def test_rn013_despesa_valida_normalizada_e_arredondada():
    item = _despesa(
        id="d-011",
        categoria=" Alimentação ",
        fornecedor=" Hotel Copa Sul ",
        valor=Decimal("33.333"),
    )
    assert ler_despesa(item, posicao=2) == Despesa(
        posicao=2,
        id="d-011",
        data=date(2026, 7, 3),
        categoria="alimentacao",
        fornecedor="hotel copa sul",
        tem_nota_fiscal=True,
        valor_informado=Decimal("33.333"),
        valor_considerado=Decimal("33.33"),
    )


def test_rn013_despesa_valida_com_valor_inteiro():
    despesa = ler_despesa(_despesa(valor=100), posicao=1)
    assert despesa.valor_informado == Decimal("100")
    assert despesa.valor_considerado == Decimal("100.00")


def test_rn013_despesa_invalida_nao_impede_as_demais():
    doc = _documento(
        despesas=[
            _despesa(id="d-001", valor=50),
            _despesa(id="d-002", valor=50, tem_nota_fiscal=_REMOVER),
            _despesa(id="d-003", valor=50),
        ]
    )
    texto = json.dumps(doc)
    despesas = ler_documento(texto).despesas
    assert [type(d) for d in despesas] == [Despesa, Invalida, Despesa]
    assert [d.posicao for d in despesas] == [1, 2, 3]
    assert [d.id for d in despesas] == ["d-001", "d-002", "d-003"]


def test_rn013_documento_lido_do_texto():
    doc = ler_documento(json.dumps(_documento()))
    assert doc.inicio == date(2026, 7, 1)
    assert doc.fim == date(2026, 7, 31)
    assert doc.colaborador["id"] == "c-0417"
    assert doc.despesas == []
