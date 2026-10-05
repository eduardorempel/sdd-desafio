import json
import os
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).parent.parent
EXEMPLO = RAIZ / "exemplos" / "despesas-exemplo.json"
POLITICA = RAIZ / "exemplos" / "envelope" / "politica-v4.json"

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
    assert resultado["total_reembolsavel"] == Decimal("585.43")


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
    assert _rodar("calcular", "--input", EXEMPLO).returncode == 2
    assert _rodar().returncode == 2
    assert _rodar("outro").returncode == 2


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
