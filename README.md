# Motor de Cálculo de Reembolso

CLI que lê um JSON com as despesas de um colaborador em um período e gera um
JSON com o valor reembolsável, o status e a justificativa de cada despesa,
seguindo as regras da spec.

Este repositório é a entrega do desafio de Spec Driven Development
(enunciado em [`DESAFIO.md`](DESAFIO.md)).

| Documento | Conteúdo |
|---|---|
| [`specs/001-motor-reembolso/spec.md`](specs/001-motor-reembolso/spec.md) | O quê: regras de negócio (RN-001 a RN-018), ambiguidades, casos de borda, aceite |
| [`specs/001-motor-reembolso/plan.md`](specs/001-motor-reembolso/plan.md) | O como: stack, arquitetura, decisões técnicas |
| [`specs/001-motor-reembolso/tasks.md`](specs/001-motor-reembolso/tasks.md) | Em que ordem: tasks T-001 a T-041, cada uma com o seu commit |
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
python -m reembolso calcular --input exemplos/despesas-exemplo.json \
  --politica exemplos/envelope/politica-v4.json --output resultado.json

python -m reembolso calcular --input exemplos/envelope/despesas-envelope.json \
  --politica exemplos/envelope/politica-v4.json --cambio exemplos/envelope/cambio.json \
  --output resultado.json
```

- `--input`: documento de despesas no formato de
  [`exemplos/despesas-exemplo.json`](exemplos/despesas-exemplo.json) ou
  [`exemplos/envelope/despesas-envelope.json`](exemplos/envelope/despesas-envelope.json)
  (spec §4).
- `--politica`: documento de política, obrigatório, no formato de
  [`exemplos/envelope/politica-v4.json`](exemplos/envelope/politica-v4.json) (RN-015). A
  tabela aplicada é escolhida pelo `colaborador.centro_custo` (RN-016).
- `--cambio`: documento de câmbio no formato de
  [`exemplos/envelope/cambio.json`](exemplos/envelope/cambio.json); só é necessário com
  despesa em moeda estrangeira (RN-018). Sem ele, essas despesas saem recusadas com
  `COTACAO_INDISPONIVEL`.
- `--output`: arquivo de resultado, em UTF-8. Para o primeiro comando, o
  `total_reembolsavel` é `351.43`.

Códigos de saída:

| Código | Situação |
|---|---|
| 0 | Sucesso; o arquivo de saída foi gravado |
| 1 | Erro geral (RN-013, RN-015, RN-018): documento de despesas, de política ou de câmbio ilegível ou inválido, política não informada etc.; mensagem em stderr, e o arquivo de saída não é criado nem sobrescrito |
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
  normalizacao.py    normalização de texto (RN-002), moeda (RN-017) e arredondamento (RN-003)
  politica.py        documento de política (RN-015) e política aplicável (RN-016)
  cambio.py          documento de câmbio e busca da cotação (RN-018)
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
