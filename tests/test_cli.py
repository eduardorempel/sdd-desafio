import json
import os
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).parent.parent
EXEMPLO = RAIZ / "exemplos" / "despesas-exemplo.json"
POLITICA = RAIZ / "exemplos" / "envelope" / "politica-v4.json"
CAMBIO = RAIZ / "exemplos" / "envelope" / "cambio.json"

CONTEUDO_ANTERIOR = '{"conteudo": "anterior"}\n'


def _rodar(*args):
    return subprocess.run(
        [sys.executable, "-m", "reembolso", *map(str, args)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=RAIZ,
        # Mensagens têm acentos; sem isso, no Windows o stderr do filho sai em cp1252.
        env={**os.environ, "PYTHONUTF8": "1"},
    )


def _sem_periodo_fim(tmp_path):
    dados = json.loads(EXEMPLO.read_text(encoding="utf-8"))
    del dados["periodo"]["fim"]
    entrada = tmp_path / "entrada.json"
    entrada.write_text(json.dumps(dados), encoding="utf-8")
    return entrada


def test_cli_exemplo_gera_arquivo(tmp_path):
    saida = tmp_path / "resultado.json"
    processo = _rodar("calcular", "--input", EXEMPLO, "--politica", POLITICA, "--output", saida)
    assert processo.returncode == 0, processo.stderr
    resultado = json.loads(saida.read_text(encoding="utf-8"), parse_float=Decimal)
    assert len(resultado["itens"]) == 14
    assert resultado["total_reembolsavel"] == Decimal("351.43")


def test_dt006_erro_geral_nao_sobrescreve_saida(tmp_path):
    saida = tmp_path / "resultado.json"
    saida.write_text(CONTEUDO_ANTERIOR, encoding="utf-8")
    processo = _rodar(
        "calcular", "--input", _sem_periodo_fim(tmp_path), "--politica", POLITICA, "--output", saida
    )
    assert processo.returncode == 1
    assert saida.read_text(encoding="utf-8") == CONTEUDO_ANTERIOR


def test_dt006_erro_geral_nao_cria_saida(tmp_path):
    saida = tmp_path / "resultado.json"
    processo = _rodar(
        "calcular", "--input", _sem_periodo_fim(tmp_path), "--politica", POLITICA, "--output", saida
    )
    assert processo.returncode == 1
    assert not saida.exists()


def test_dt006_erro_geral_retorna_1_e_escreve_stderr(tmp_path):
    saida = tmp_path / "resultado.json"
    processo = _rodar(
        "calcular", "--input", _sem_periodo_fim(tmp_path), "--politica", POLITICA, "--output", saida
    )
    assert processo.returncode == 1
    assert "periodo.fim" in processo.stderr
    assert processo.stdout == ""


def test_dt006_entrada_inexistente_e_erro_geral(tmp_path):
    saida = tmp_path / "resultado.json"
    processo = _rodar(
        "calcular",
        "--input",
        tmp_path / "nao-existe.json",
        "--politica",
        POLITICA,
        "--output",
        saida,
    )
    assert processo.returncode == 1
    assert processo.stderr
    assert not saida.exists()


def test_dt006_json_com_nan_e_erro_geral(tmp_path):
    entrada = tmp_path / "entrada.json"
    entrada.write_text(EXEMPLO.read_text(encoding="utf-8").replace("72.50", "NaN"), "utf-8")
    saida = tmp_path / "resultado.json"
    processo = _rodar("calcular", "--input", entrada, "--politica", POLITICA, "--output", saida)
    assert processo.returncode == 1
    assert not saida.exists()


def test_dt006_argumentos_invalidos_retornam_2(tmp_path):
    saida = tmp_path / "resultado.json"
    assert _rodar("calcular", "--input", EXEMPLO).returncode == 2
    assert _rodar("calcular", "--politica", POLITICA, "--output", saida).returncode == 2
    desconhecido = _rodar(
        "calcular", "--input", EXEMPLO, "--politica", POLITICA, "--output", saida, "--extra", "x"
    )
    assert desconhecido.returncode == 2
    assert _rodar().returncode == 2
    assert _rodar("outro").returncode == 2
    assert not saida.exists()


def test_rn015_sem_politica_retorna_1_e_nao_cria_saida(tmp_path):
    saida = tmp_path / "resultado.json"
    processo = _rodar("calcular", "--input", EXEMPLO, "--output", saida)
    assert processo.returncode == 1
    assert "política" in processo.stderr
    assert not saida.exists()


def test_rn015_sem_politica_nao_sobrescreve_saida(tmp_path):
    saida = tmp_path / "resultado.json"
    saida.write_text(CONTEUDO_ANTERIOR, encoding="utf-8")
    processo = _rodar("calcular", "--input", EXEMPLO, "--output", saida)
    assert processo.returncode == 1
    assert saida.read_text(encoding="utf-8") == CONTEUDO_ANTERIOR


def test_rn015_politica_inexistente_e_erro_geral(tmp_path):
    saida = tmp_path / "resultado.json"
    saida.write_text(CONTEUDO_ANTERIOR, encoding="utf-8")
    processo = _rodar(
        "calcular",
        "--input",
        EXEMPLO,
        "--politica",
        tmp_path / "nao-existe.json",
        "--output",
        saida,
    )
    assert processo.returncode == 1
    assert processo.stderr
    assert saida.read_text(encoding="utf-8") == CONTEUDO_ANTERIOR


def test_rn015_politica_invalida_nao_sobrescreve_saida(tmp_path):
    dados = json.loads(POLITICA.read_text(encoding="utf-8"))
    dados["padrao"]["alimentacao"]["limite"] = -1
    politica = tmp_path / "politica.json"
    politica.write_text(json.dumps(dados), encoding="utf-8")
    saida = tmp_path / "resultado.json"
    saida.write_text(CONTEUDO_ANTERIOR, encoding="utf-8")
    processo = _rodar("calcular", "--input", EXEMPLO, "--politica", politica, "--output", saida)
    assert processo.returncode == 1
    assert "política" in processo.stderr
    assert saida.read_text(encoding="utf-8") == CONTEUDO_ANTERIOR


def _exemplo_com(tmp_path, **colaborador):
    dados = json.loads(EXEMPLO.read_text(encoding="utf-8"))
    for campo, valor in colaborador.items():
        if valor is None:
            dados["colaborador"].pop(campo, None)
        else:
            dados["colaborador"][campo] = valor
    entrada = tmp_path / "entrada.json"
    entrada.write_text(json.dumps(dados), encoding="utf-8")
    return entrada


def _cambio_com(tmp_path, **alteracoes):
    dados = json.loads(CAMBIO.read_text(encoding="utf-8"))
    dados.update(alteracoes)
    cambio = tmp_path / "cambio.json"
    cambio.write_text(json.dumps(dados), encoding="utf-8")
    return cambio


def _erro_geral_preserva_saida(tmp_path, *args):
    saida = tmp_path / "resultado.json"
    saida.write_text(CONTEUDO_ANTERIOR, encoding="utf-8")
    processo = _rodar("calcular", *args, "--output", saida)
    assert processo.returncode == 1, processo.stderr
    assert processo.stderr
    assert saida.read_text(encoding="utf-8") == CONTEUDO_ANTERIOR
    return processo


def test_rn016_sem_centro_custo_usa_politica_padrao(tmp_path):
    saida = tmp_path / "resultado.json"
    entrada = _exemplo_com(tmp_path, centro_custo=None)
    processo = _rodar("calcular", "--input", entrada, "--politica", POLITICA, "--output", saida)
    assert processo.returncode == 0, processo.stderr
    resultado = json.loads(saida.read_text(encoding="utf-8"), parse_float=Decimal)
    assert resultado["total_reembolsavel"] == Decimal("585.43")
    d002 = resultado["itens"][1]
    assert "(política padrão)" in d002["justificativa"]


def test_rn016_centro_custo_invalido_e_erro_geral(tmp_path):
    entrada = _exemplo_com(tmp_path, centro_custo=42)
    processo = _erro_geral_preserva_saida(tmp_path, "--input", entrada, "--politica", POLITICA)
    assert "centro_custo" in processo.stderr


def test_rn018_cambio_invalido_nao_sobrescreve_saida(tmp_path):
    inexistente = tmp_path / "nao-existe.json"
    _erro_geral_preserva_saida(
        tmp_path, "--input", EXEMPLO, "--politica", POLITICA, "--cambio", inexistente
    )
    taxa_zero = _cambio_com(tmp_path, taxas={"2026-07-13": {"USD": 0}})
    processo = _erro_geral_preserva_saida(
        tmp_path, "--input", EXEMPLO, "--politica", POLITICA, "--cambio", taxa_zero
    )
    assert "câmbio" in processo.stderr


def test_rn018_moedas_base_divergentes_e_erro_geral(tmp_path):
    cambio = _cambio_com(tmp_path, moeda_base="USD")
    processo = _erro_geral_preserva_saida(
        tmp_path, "--input", EXEMPLO, "--politica", POLITICA, "--cambio", cambio
    )
    assert "moeda_base" in processo.stderr


def test_rn018_sem_cambio_despesa_estrangeira_cotacao_indisponivel(tmp_path):
    dados = json.loads(EXEMPLO.read_text(encoding="utf-8"))
    dados["despesas"][0]["moeda"] = "USD"
    entrada = tmp_path / "entrada.json"
    entrada.write_text(json.dumps(dados), encoding="utf-8")
    saida = tmp_path / "resultado.json"
    processo = _rodar("calcular", "--input", entrada, "--politica", POLITICA, "--output", saida)
    assert processo.returncode == 0, processo.stderr
    itens = json.loads(saida.read_text(encoding="utf-8"), parse_float=Decimal)["itens"]
    assert itens[0]["motivo"] == "COTACAO_INDISPONIVEL"
    assert itens[0]["valor_considerado"] is None
    assert itens[1]["valor_reembolsavel"] == Decimal("38.00")


def test_rn018_com_cambio_converte_pela_cli(tmp_path):
    dados = json.loads(EXEMPLO.read_text(encoding="utf-8"))
    dados["despesas"][0].update({"moeda": "EUR", "data": "2026-07-14", "valor": 10.00})
    entrada = tmp_path / "entrada.json"
    entrada.write_text(json.dumps(dados), encoding="utf-8")
    saida = tmp_path / "resultado.json"
    processo = _rodar(
        "calcular",
        "--input",
        entrada,
        "--politica",
        POLITICA,
        "--cambio",
        CAMBIO,
        "--output",
        saida,
    )
    assert processo.returncode == 0, processo.stderr
    item = json.loads(saida.read_text(encoding="utf-8"), parse_float=Decimal)["itens"][0]
    assert item["taxa_cambio"] == Decimal("5.93")
    assert item["valor_considerado"] == Decimal("59.30")
