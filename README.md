# Motor de Cálculo de Reembolso

CLI que lê um JSON com as despesas de um colaborador em um período e gera um
JSON com o valor reembolsável, o status e a justificativa de cada despesa,
seguindo as regras da spec.

Este repositório é a entrega do desafio de Spec Driven Development
(enunciado em [`DESAFIO.md`](DESAFIO.md)).

| Documento | Conteúdo |
|---|---|
| [`specs/001-motor-reembolso/spec.md`](specs/001-motor-reembolso/spec.md) | O quê: regras de negócio (RN-001 a RN-014), ambiguidades, casos de borda, aceite |
| [`specs/001-motor-reembolso/plan.md`](specs/001-motor-reembolso/plan.md) | O como: stack, arquitetura, decisões técnicas |
| [`specs/001-motor-reembolso/tasks.md`](specs/001-motor-reembolso/tasks.md) | Em que ordem: tasks T-001 a T-025, cada uma com o seu commit |
| [`specs/001-motor-reembolso/DECISIONS.md`](specs/001-motor-reembolso/DECISIONS.md) | Log de mudanças da spec |

## Requisitos

- Python 3.12 ou mais recente
- Nenhuma dependência para rodar; `pytest` e `ruff` para desenvolvimento

## Instalação

```bash
python -m venv .venv
.venv/bin/python -m pip install -e ".[dev]"        # Linux/macOS
.venv/Scripts/python -m pip install -e ".[dev]"    # Windows
```

Os comandos abaixo supõem o ambiente virtual ativado
(`source .venv/bin/activate` ou `.venv\Scripts\activate`).

## Como rodar

```bash
python -m reembolso calcular --input exemplos/despesas-exemplo.json --output resultado.json
```

- `--input`: documento de despesas no formato de
  [`exemplos/despesas-exemplo.json`](exemplos/despesas-exemplo.json) (spec §4).
- `--output`: arquivo de resultado, em UTF-8. Para o exemplo, o
  `total_reembolsavel` é `585.43`.

Códigos de saída:

| Código | Situação |
|---|---|
| 0 | Sucesso; o arquivo de saída foi gravado |
| 1 | Erro geral da RN-013 (documento ilegível, sem período válido etc.); mensagem em stderr, e o arquivo de saída não é criado nem sobrescrito |
| 2 | Argumentos de linha de comando inválidos |

Uma despesa com dados inválidos não interrompe a execução: ela sai recusada
com `DADOS_INVALIDOS` e as demais são calculadas normalmente.

## Como testar

```bash
python -m pytest
```

Os testes seguem a spec: um arquivo `tests/test_rnNNN_*.py` por regra de
negócio, `tests/test_secao7_casos_de_borda.py` com um caso por linha da tabela
da seção 7, `tests/test_secao9_aceite_exemplo.py` com o aceite do exemplo e
`tests/test_rastreabilidade.py`, que falha se alguma RN da spec ficar sem
arquivo de teste.

## Lint e formatação

```bash
ruff check .
ruff format .
```

## Estrutura

```
reembolso/
  cli.py             argumentos, leitura e escrita de arquivo, códigos de saída
  entrada.py         JSON → Documento; validação da RN-013 (etapas 1 e 2)
  normalizacao.py    normalização de texto (RN-002) e arredondamento (RN-003)
  politica.py        categorias, limites e limiar da nota fiscal, como dados
  etapas.py          uma função por etapa da seção 8 da spec
  motor.py           ordem das etapas (ETAPAS) e execução
  justificativas.py  textos das justificativas
  saida.py           Resultado → JSON
  modelo.py          dataclasses e enums
tests/
exemplos/
specs/001-motor-reembolso/
docs/sessions/       exports das sessões com o Claude Code
```
