# Tasks — Motor de Cálculo de Reembolso

> Cada task é pequena o bastante para virar **um commit**. Se você não consegue
> descrever o critério de aceite como "o teste X passa", a task está grande demais.
>
> Marque `[x]` conforme conclui — ao longo do caminho, não tudo no fim. O histórico
> de quando cada task foi marcada é lido na correção.

**Baseado em:** spec 1.1 · plan 1.0

**Formato do commit:** `feat(T-003): <descrição>` · `test(T-003): <descrição>`

- Cada task entrega código **e** o teste dela no mesmo commit (`feat`). Tasks que
  só acrescentam teste usam `test`.
- As constantes de `politica.py` não têm task própria: cada uma entra junto com a
  etapa que a usa (T-012, T-014, T-015), para nunca ser commitada sem teste.
- Os testes de regra conferem `status`, `motivo` e valores. Na justificativa,
  conferem só a RN citada e os `id` citados (DT-008). O texto exato é conferido
  apenas para os exemplos da seção 4 da spec (T-021).

---

## Fase 1 — Fundação

- [x] **T-001** — Esqueleto do projeto: pacote `reembolso`, `pyproject` com pytest
  e ruff, ponto de entrada `python -m reembolso`. Preenche Stack e comandos no
  `CLAUDE.md`.
  - **Atende:** plan §1
  - **Aceite:** `python -m pytest` e `ruff check .` passam.
  - **Teste:** `tests/test_estrutura.py::test_pacote_importa`
  - **Commit:** 33ec69e

- [x] **T-002** — `modelo.py`: dataclasses `Documento`, `Despesa`, `Invalida`,
  `Resultado` e enums `Status` e `Motivo`, com valores iguais aos textos da spec.
  - **Atende:** spec §4 (status e motivos), plan §3
  - **Aceite:** os sete motivos e os três status têm exatamente os textos da spec.
  - **Teste:** `tests/test_modelo.py::test_motivos_iguais_aos_codigos_da_spec`,
    `::test_status_iguais_aos_textos_da_spec`
  - **Commit:**

- [x] **T-003** — Normalização de texto em `normalizacao.py`: remove espaços das
  pontas, passa para minúsculas e remove acentos. Mantém espaços internos.
  - **Atende:** RN-002, AMB-013, DT-007
  - **Aceite:** `ALIMENTACAO`, ` Alimentação ` e `alimentacao` → `alimentacao`;
    `Bistro Central` = `bistro central`; espaços internos mantidos; `ç` → `c`.
  - **Teste:** `tests/test_rn002_normalizacao.py`
  - **Commit:**

- [x] **T-004** — Arredondamento para centavos com a metade se afastando do zero
  em `normalizacao.py`. `-0.00` vira `0.00`.
  - **Atende:** RN-003, AMB-012, DT-001
  - **Aceite:** 33,333 → 33,33; 10,005 → 10,01; −10,005 → −10,01; −0,004 → 0,00,
    sem sinal.
  - **Teste:** `tests/test_rn003_arredondamento.py`
  - **Commit:**

## Fase 2 — Entrada (RN-013)

- [x] **T-005** — Parse do JSON em `entrada.py` com números lidos como `Decimal`.
  JSON ilegível, `NaN` e `Infinity` levantam `EntradaInvalida`.
  - **Atende:** RN-013 (erro geral: documento ilegível), DT-001, DT-003
  - **Aceite:** documento não JSON, com `NaN` ou com `Infinity` → `EntradaInvalida`;
    `33.333` é lido como `Decimal("33.333")`.
  - **Teste:** `tests/test_rn013_dados_invalidos.py::test_rn013_json_invalido_erro_geral`,
    `::test_rn013_nan_erro_geral`, `::test_rn013_infinity_erro_geral`,
    `::test_dt001_float_lido_como_decimal`
  - **Commit:**

- [x] **T-006** — Validação do documento: `colaborador` e `periodo` são objetos,
  `colaborador.id` é texto não vazio, `inicio` e `fim` são datas válidas
  (`AAAA-MM-DD` e existentes no calendário), `inicio ≤ fim`, `despesas` é lista e
  todos os itens são objetos. Campos informativos e desconhecidos não são validados.
  - **Atende:** RN-013 (erro geral), AMB-017, DT-002
  - **Aceite:** documento sem `periodo.fim`, `periodo.inicio` = `2026-02-30`,
    `colaborador.id` `"  "` ou `417`, `inicio` posterior a `fim`, `despesas` que não
    é lista ou item que não é objeto → `EntradaInvalida`. `periodo.competencia` =
    `"julho"` e `despesas: []` → sem erro.
  - **Teste:** `tests/test_rn013_dados_invalidos.py::test_rn013_erro_geral_*`
  - **Commit:**

- [x] **T-007** — Validação de cada despesa: falha produz `Invalida` com
  `DADOS_INVALIDOS`. `id` é nulo quando o problema está no `id`; `valor_informado`
  é nulo quando o valor está ausente ou não é numérico; `bool` não é aceito como
  número.
  - **Atende:** RN-013 (erro em uma despesa), AMB-017, DT-002
  - **Aceite:** sem `tem_nota_fiscal`, `fornecedor` `"   "`, `id: 17` (id nulo),
    `data` `2026-7-3` e `2026-02-30`, `valor` `"72.50"` e `true`,
    `tem_nota_fiscal` que não é booleano → `DADOS_INVALIDOS`, e as demais despesas
    seguem. `valor` 50,00 com outro campo inválido → `valor_informado` 50,00.
    `"moeda": "USD"` e `descricao: 123` → ignorados.
  - **Teste:** `tests/test_rn013_dados_invalidos.py::test_rn013_despesa_*`
  - **Commit:**

- [x] **T-008** — Montagem da `Despesa` válida: posição (a partir de 1), categoria
  e fornecedor normalizados, `valor_informado` sem arredondamento e
  `valor_considerado` arredondado.
  - **Atende:** RN-002, RN-003, spec §4 (posição)
  - **Aceite:** a despesa de entrada ` Alimentação `/33,333 na posição 2 vira
    `Despesa(posicao=2, categoria="alimentacao", valor_informado=33.333,
    valor_considerado=33.33)`.
  - **Teste:** `tests/test_rn013_dados_invalidos.py::test_rn013_despesa_valida_normalizada_e_arredondada`
  - **Commit:**

## Fase 3 — Regras de negócio

- [x] **T-009** — `motor.py`: lista `ETAPAS` (inicialmente vazia), tipos `PorItem`
  e `EmGrupo`, lista de despesas vivas e status final (`aprovado` se
  `valor_reembolsavel == valor_considerado`, senão `limitado`). Uma `Invalida`
  vira `Resultado` recusado com `DADOS_INVALIDOS`. Cria `justificativas.py` com a
  formatação `R$ 0,00`.
  - **Atende:** spec §8, AMB-016, DT-004, DT-008
  - **Aceite:** despesa recusada em uma etapa não chega à seguinte; `Invalida` →
    recusado, 0,00, `valor_considerado` nulo; o resultado sai na ordem das posições.
  - **Teste:** `tests/test_motor.py::test_secao8_recusada_nao_chega_a_etapa_seguinte`,
    `::test_secao8_invalida_vira_dados_invalidos`, `::test_secao8_resultado_na_ordem_da_entrada`
  - **Commit:**

- [x] **T-010** — Etapa de valor negativo.
  - **Atende:** RN-005, AMB-011
  - **Aceite:** d-009 (−45,00) → recusado, 0,00, `VALOR_NEGATIVO`; 0,00 → aprovado,
    0,00; −0,004 → aprovado, 0,00.
  - **Teste:** `tests/test_rn005_valor_negativo.py`
  - **Commit:**

- [x] **T-011** — Etapa de período, com as bordas incluídas. `competencia` não é
  usada.
  - **Atende:** RN-004, AMB-009
  - **Aceite:** d-008 (2026-04-15) → `FORA_DO_PERIODO`; data igual a `inicio` e
    d-014 (igual a `fim`) → aceitas; `competencia` divergente das datas não muda o
    resultado.
  - **Teste:** `tests/test_rn004_periodo.py`
  - **Commit:**

- [x] **T-012** — Etapa de categoria + `CATEGORIAS_REEMBOLSAVEIS` em `politica.py`.
  - **Atende:** RN-001, AMB-014
  - **Aceite:** d-005 (`coworking`) → recusado, 0,00, `CATEGORIA_NAO_REEMBOLSAVEL`;
    `ALIMENTACAO` → aceita.
  - **Teste:** `tests/test_rn001_categoria.py`
  - **Commit:**

- [ ] **T-013** — Etapa de duplicatas (mesma data, categoria normalizada,
  fornecedor normalizado e `valor_considerado`). É mantida a de menor posição
  entre as que têm nota; se nenhuma tiver nota, a de menor posição.
  - **Atende:** RN-006, AMB-010
  - **Aceite:** d-006/d-007 → d-006 mantida, d-007 `DUPLICATA` com justificativa
    citando d-006; grupo em que só a 2ª tem nota → 2ª mantida; `Bistro Central` e
    `BISTRO CENTRAL ` → duplicatas; `id` e `descricao` diferentes não impedem a
    duplicata; despesa já recusada em etapa anterior não entra no grupo.
  - **Teste:** `tests/test_rn006_duplicatas.py`
  - **Commit:**

- [ ] **T-014** — Etapa de nota fiscal + `LIMIAR_NOTA_FISCAL` em `politica.py`.
  - **Atende:** RN-007, AMB-004, AMB-005
  - **Aceite:** d-003 (100,00, sem nota) → passa; d-004 (100,01, sem nota) e d-013
    (690,00, sem nota) → recusado, 0,00, `NOTA_FISCAL_AUSENTE`; 150,00 com nota →
    passa.
  - **Teste:** `tests/test_rn007_nota_fiscal.py`
  - **Commit:**

- [ ] **T-015** — Etapa de limites por data e categoria, com o limite consumido na
  ordem das posições e o excedente cortado + `LIMITE_POR_DATA` em `politica.py`.
  - **Atende:** RN-008, RN-009, RN-010, AMB-001, AMB-002, AMB-003, AMB-008
  - **Aceite:** d-001 + d-002 → 60,00 + 0,00; d-010 (480,00) → 250,00, `limitado`;
    d-014 (61,00) → 60,00, `limitado`; duas hospedagens 200,00 + 150,00 na mesma
    data → 200,00 + 50,00; d-003 → 80,00 com d-004 recusada na mesma data; estorno
    d-009 não altera o reembolso das outras despesas de transporte.
  - **Teste:** `tests/test_rn008_limites.py`, `tests/test_rn009_distribuicao.py`,
    `tests/test_rn010_parcial.py`
  - **Commit:**

- [ ] **T-016** — Justificativa de `LIMITE_DIARIO` com o limite, o valor já
  consumido no dia e os `id` das despesas que o consumiram.
  - **Atende:** spec §4 (justificativa), RN-009
  - **Aceite:** a justificativa de d-002 cita R$ 60,00, d-001 e RN-009.
  - **Teste:** `tests/test_rn009_distribuicao.py::test_rn009_justificativa_cita_despesa_que_consumiu`
  - **Commit:**

- [ ] **T-017** — Testes das regras que determinam o que **não** fazer: viagem e
  dias do calendário (`test(T-017)`).
  - **Atende:** RN-011, RN-012, AMB-006, AMB-007, AMB-015
  - **Aceite:** d-003 ("Corrida aeroporto", 100,00) → limite de 80,00, 80,00;
    nenhuma despesa recebe limite acima da tabela da RN-008; d-012 (sábado,
    47,20) → aprovado, 47,20.
  - **Teste:** `tests/test_rn011_viagem.py`, `tests/test_rn012_calendario.py`
  - **Commit:**

## Fase 4 — Saída e CLI

- [ ] **T-018** — `saida.py` + encoder JSON: `valor_considerado`,
  `valor_reembolsavel` e `total_reembolsavel` com duas casas; `valor_informado`
  sem quantizar; `null` onde a spec pede nulo; `Decimal` dentro de `colaborador`
  e `periodo`; UTF-8 com `ensure_ascii=False`.
  - **Atende:** spec §4 (saída), RN-003, DT-005
  - **Aceite:** 60 → `60.00`; `valor_informado` 33.333 → `33.333`; `null` em
    `motivo` de item aprovado e em `valor_considerado` de `DADOS_INVALIDOS`;
    `total_reembolsavel` é a soma dos itens; `colaborador` com número é
    serializado sem erro.
  - **Teste:** `tests/test_saida_serializacao.py`
  - **Commit:**

- [ ] **T-019** — CLI `calcular --input --output`: em erro geral, mensagem em
  stderr, código 1 e arquivo de saída não criado nem sobrescrito; sucesso retorna
  0; argumentos inválidos retornam 2.
  - **Atende:** RN-013 (erro geral, "não gera saída"), DT-006
  - **Aceite:** com um arquivo de saída já existente e uma entrada sem
    `periodo.fim`, o arquivo continua igual e o código é 1; o exemplo gera o
    arquivo e retorna 0.
  - **Teste:** `tests/test_cli.py::test_dt006_erro_geral_nao_sobrescreve_saida`,
    `::test_dt006_erro_geral_retorna_1_e_escreve_stderr`, `::test_cli_exemplo_gera_arquivo`
  - **Commit:**

## Fase 5 — Casos de borda e aceite

- [ ] **T-020** — Aceite completo com `exemplos/despesas-exemplo.json`
  (`test(T-020)`).
  - **Atende:** spec §9
  - **Aceite:** as 14 linhas (`valor_reembolsavel`, `status`, `motivo`) batem com
    a tabela da §9; `total_reembolsavel` = 585,43; um item por despesa, na mesma
    ordem da entrada.
  - **Teste:** `tests/test_secao9_aceite_exemplo.py`
  - **Commit:**

- [ ] **T-021** — Texto exato das justificativas dos exemplos da §4 e verificação
  de que todo item cita uma RN.
  - **Atende:** spec §4 (exemplo), spec §9 (justificativa cita RN)
  - **Aceite:** d-001, d-002 e d-004 têm exatamente as justificativas da §4; todo
    item casa com `RN-\d{3}`.
  - **Teste:** `tests/test_secao9_aceite_exemplo.py::test_justificativas_exemplo_secao4`,
    `::test_todo_item_cita_rn`
  - **Commit:**

- [ ] **T-022** — Tabela da §7 como teste parametrizado, com uma linha por caso e
  o nome do caso como `id` (`test(T-022)`).
  - **Atende:** spec §7 (todas as RN citadas na tabela)
  - **Aceite:** os 37 casos da §7 passam e aparecem no relatório do pytest com o
    nome da spec.
  - **Teste:** `tests/test_secao7_casos_de_borda.py`
  - **Commit:**

- [ ] **T-023** — Invariantes: determinismo e descrição informativa
  (`test(T-023)`).
  - **Atende:** RN-014, spec §9, AMB-006, AMB-008, AMB-010
  - **Aceite:** duas execuções produzem saídas idênticas byte a byte; trocar todas
    as descrições do exemplo não altera `valor_reembolsavel`, `status` nem `motivo`.
  - **Teste:** `tests/test_rn014_descricao.py`,
    `tests/test_secao9_aceite_exemplo.py::test_determinismo`
  - **Commit:**

- [ ] **T-024** — Teste de rastreabilidade: lê a `spec.md`, extrai os `RN-\d{3}` e
  falha se algum não tiver arquivo `test_rnNNN_*.py`. Fica por último porque só
  passa quando todas as RN têm teste.
  - **Atende:** plan §6
  - **Aceite:** RN-001 a RN-014 têm arquivo de teste; remover um deles faz o teste
    falhar.
  - **Teste:** `tests/test_rastreabilidade.py`
  - **Commit:**

## Fase 6 — Finalização

- [ ] **T-025** — README: requisitos, instalação, como rodar a CLI e como rodar os
  testes e o lint (`docs(T-025)`).
  - **Atende:** DESAFIO (entrega), RUBRICA §5
  - **Aceite:** num clone limpo, seguir o README gera `resultado.json` a partir do
    exemplo e `python -m pytest` passa.
  - **Teste:** manual (roteiro do próprio README); `tests/test_cli.py::test_cli_exemplo_gera_arquivo`
    cobre o mesmo comando
  - **Commit:**

---

## Fase 7 — Envelope (criar no Dia 2)

<Novas tasks a partir da mudança de requisito. Numeração continua de onde parou
(T-026) — não reinicie e não renumere as antigas: a numeração é o eixo da
rastreabilidade.>

---

## Cobertura

Preencha ao fechar cada fase. É a sua própria checagem de rastreabilidade — e é
exatamente a matriz que a correção vai montar.

| Regra da spec | Task | Teste |
|---|---|---|
| RN-001 | T-012 | `test_rn001_categoria.py` |
| RN-002 | T-003, T-008 | `test_rn002_normalizacao.py` |
| RN-003 | T-004, T-008, T-018 | `test_rn003_arredondamento.py`, `test_saida_serializacao.py` |
| RN-004 | T-011 | `test_rn004_periodo.py` |
| RN-005 | T-010 | `test_rn005_valor_negativo.py` |
| RN-006 | T-013 | `test_rn006_duplicatas.py` |
| RN-007 | T-014 | `test_rn007_nota_fiscal.py` |
| RN-008 | T-015 | `test_rn008_limites.py` |
| RN-009 | T-015, T-016 | `test_rn009_distribuicao.py` |
| RN-010 | T-015 | `test_rn010_parcial.py` |
| RN-011 | T-017 | `test_rn011_viagem.py` |
| RN-012 | T-017 | `test_rn012_calendario.py` |
| RN-013 | T-005, T-006, T-007, T-019 | `test_rn013_dados_invalidos.py`, `test_cli.py` |
| RN-014 | T-023 | `test_rn014_descricao.py` |
| AMB-001 | T-015 | `test_rn008_limites.py` |
| AMB-002 | T-015 | `test_rn009_distribuicao.py` |
| AMB-003 | T-015 | `test_rn010_parcial.py` |
| AMB-004 | T-014 | `test_rn007_nota_fiscal.py` |
| AMB-005 | T-014 | `test_rn007_nota_fiscal.py` |
| AMB-006 | T-017, T-023 | `test_rn011_viagem.py`, `test_rn014_descricao.py` |
| AMB-007 | T-017 | `test_rn011_viagem.py` |
| AMB-008 | T-015, T-023 | `test_rn008_limites.py`, `test_rn014_descricao.py` |
| AMB-009 | T-011 | `test_rn004_periodo.py` |
| AMB-010 | T-013, T-023 | `test_rn006_duplicatas.py`, `test_rn014_descricao.py` |
| AMB-011 | T-010, T-015 | `test_rn005_valor_negativo.py`, `test_rn008_limites.py` |
| AMB-012 | T-004 | `test_rn003_arredondamento.py` |
| AMB-013 | T-003 | `test_rn002_normalizacao.py` |
| AMB-014 | T-012 | `test_rn001_categoria.py` |
| AMB-015 | T-017 | `test_rn012_calendario.py` |
| AMB-016 | T-009 | `test_motor.py` |
| AMB-017 | T-006, T-007 | `test_rn013_dados_invalidos.py` |
| §4 Saída | T-002, T-018, T-021 | `test_modelo.py`, `test_saida_serializacao.py`, `test_secao9_aceite_exemplo.py` |
| §7 Casos de borda | T-022 | `test_secao7_casos_de_borda.py` |
| §8 Ordem das regras | T-009 | `test_motor.py` |
| §9 Critérios de aceite | T-020, T-021, T-023 | `test_secao9_aceite_exemplo.py` |
