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
  - **Commit:** f207780

- [x] **T-003** — Normalização de texto em `normalizacao.py`: remove espaços das
  pontas, passa para minúsculas e remove acentos. Mantém espaços internos.
  - **Atende:** RN-002, AMB-013, DT-007
  - **Aceite:** `ALIMENTACAO`, ` Alimentação ` e `alimentacao` → `alimentacao`;
    `Bistro Central` = `bistro central`; espaços internos mantidos; `ç` → `c`.
  - **Teste:** `tests/test_rn002_normalizacao.py`
  - **Commit:** 1e0e792

- [x] **T-004** — Arredondamento para centavos com a metade se afastando do zero
  em `normalizacao.py`. `-0.00` vira `0.00`.
  - **Atende:** RN-003, AMB-012, DT-001
  - **Aceite:** 33,333 → 33,33; 10,005 → 10,01; −10,005 → −10,01; −0,004 → 0,00,
    sem sinal.
  - **Teste:** `tests/test_rn003_arredondamento.py`
  - **Commit:** 1f7df07

## Fase 2 — Entrada (RN-013)

- [x] **T-005** — Parse do JSON em `entrada.py` com números lidos como `Decimal`.
  JSON ilegível, `NaN` e `Infinity` levantam `EntradaInvalida`.
  - **Atende:** RN-013 (erro geral: documento ilegível), DT-001, DT-003
  - **Aceite:** documento não JSON, com `NaN` ou com `Infinity` → `EntradaInvalida`;
    `33.333` é lido como `Decimal("33.333")`.
  - **Teste:** `tests/test_rn013_dados_invalidos.py::test_rn013_json_invalido_erro_geral`,
    `::test_rn013_nan_erro_geral`, `::test_rn013_infinity_erro_geral`,
    `::test_dt001_float_lido_como_decimal`
  - **Commit:** fb3fd8d

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
  - **Commit:** ab4c408

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
  - **Commit:** 0662169

- [x] **T-008** — Montagem da `Despesa` válida: posição (a partir de 1), categoria
  e fornecedor normalizados, `valor_informado` sem arredondamento e
  `valor_considerado` arredondado.
  - **Atende:** RN-002, RN-003, spec §4 (posição)
  - **Aceite:** a despesa de entrada ` Alimentação `/33,333 na posição 2 vira
    `Despesa(posicao=2, categoria="alimentacao", valor_informado=33.333,
    valor_considerado=33.33)`.
  - **Teste:** `tests/test_rn013_dados_invalidos.py::test_rn013_despesa_valida_normalizada_e_arredondada`
  - **Commit:** 0420f1f

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
  - **Commit:** 12a6a4a

- [x] **T-010** — Etapa de valor negativo.
  - **Atende:** RN-005, AMB-011
  - **Aceite:** d-009 (−45,00) → recusado, 0,00, `VALOR_NEGATIVO`; 0,00 → aprovado,
    0,00; −0,004 → aprovado, 0,00.
  - **Teste:** `tests/test_rn005_valor_negativo.py`
  - **Commit:** a9752c2

- [x] **T-011** — Etapa de período, com as bordas incluídas. `competencia` não é
  usada.
  - **Atende:** RN-004, AMB-009
  - **Aceite:** d-008 (2026-04-15) → `FORA_DO_PERIODO`; data igual a `inicio` e
    d-014 (igual a `fim`) → aceitas; `competencia` divergente das datas não muda o
    resultado.
  - **Teste:** `tests/test_rn004_periodo.py`
  - **Commit:** 9556082

- [x] **T-012** — Etapa de categoria + `CATEGORIAS_REEMBOLSAVEIS` em `politica.py`.
  - **Atende:** RN-001, AMB-014
  - **Aceite:** d-005 (`coworking`) → recusado, 0,00, `CATEGORIA_NAO_REEMBOLSAVEL`;
    `ALIMENTACAO` → aceita.
  - **Teste:** `tests/test_rn001_categoria.py`
  - **Commit:** 619aec1

- [x] **T-013** — Etapa de duplicatas (mesma data, categoria normalizada,
  fornecedor normalizado e `valor_considerado`). É mantida a de menor posição
  entre as que têm nota; se nenhuma tiver nota, a de menor posição.
  - **Atende:** RN-006, AMB-010
  - **Aceite:** d-006/d-007 → d-006 mantida, d-007 `DUPLICATA` com justificativa
    citando d-006; grupo em que só a 2ª tem nota → 2ª mantida; `Bistro Central` e
    `BISTRO CENTRAL ` → duplicatas; `id` e `descricao` diferentes não impedem a
    duplicata; despesa já recusada em etapa anterior não entra no grupo.
  - **Teste:** `tests/test_rn006_duplicatas.py`
  - **Commit:** 713e334

- [x] **T-014** — Etapa de nota fiscal + `LIMIAR_NOTA_FISCAL` em `politica.py`.
  - **Atende:** RN-007, AMB-004, AMB-005
  - **Aceite:** d-003 (100,00, sem nota) → passa; d-004 (100,01, sem nota) e d-013
    (690,00, sem nota) → recusado, 0,00, `NOTA_FISCAL_AUSENTE`; 150,00 com nota →
    passa.
  - **Teste:** `tests/test_rn007_nota_fiscal.py`
  - **Commit:** fa72946

- [x] **T-015** — Etapa de limites por data e categoria, com o limite consumido na
  ordem das posições e o excedente cortado + `LIMITE_POR_DATA` em `politica.py`.
  - **Atende:** RN-008, RN-009, RN-010, AMB-001, AMB-002, AMB-003, AMB-008
  - **Aceite:** d-001 + d-002 → 60,00 + 0,00; d-010 (480,00) → 250,00, `limitado`;
    d-014 (61,00) → 60,00, `limitado`; duas hospedagens 200,00 + 150,00 na mesma
    data → 200,00 + 50,00; d-003 → 80,00 com d-004 recusada na mesma data; estorno
    d-009 não altera o reembolso das outras despesas de transporte.
  - **Teste:** `tests/test_rn008_limites.py`, `tests/test_rn009_distribuicao.py`,
    `tests/test_rn010_parcial.py`
  - **Commit:** 7b9463a

- [x] **T-016** — Justificativa de `LIMITE_DIARIO` com o limite, o valor já
  consumido no dia e os `id` das despesas que o consumiram.
  - **Atende:** spec §4 (justificativa), RN-009
  - **Aceite:** a justificativa de d-002 cita R$ 60,00, d-001 e RN-009.
  - **Teste:** `tests/test_rn009_distribuicao.py::test_rn009_justificativa_cita_despesa_que_consumiu`
  - **Commit:** 43332ec

- [x] **T-017** — Testes das regras que determinam o que **não** fazer: viagem e
  dias do calendário (`test(T-017)`).
  - **Atende:** RN-011, RN-012, AMB-006, AMB-007, AMB-015
  - **Aceite:** d-003 ("Corrida aeroporto", 100,00) → limite de 80,00, 80,00;
    nenhuma despesa recebe limite acima da tabela da RN-008; d-012 (sábado,
    47,20) → aprovado, 47,20.
  - **Teste:** `tests/test_rn011_viagem.py`, `tests/test_rn012_calendario.py`
  - **Commit:** 5bf6028

## Fase 4 — Saída e CLI

- [x] **T-018** — `saida.py` + encoder JSON: `valor_considerado`,
  `valor_reembolsavel` e `total_reembolsavel` com duas casas; `valor_informado`
  sem quantizar; `null` onde a spec pede nulo; `Decimal` dentro de `colaborador`
  e `periodo`; UTF-8 com `ensure_ascii=False`.
  - **Atende:** spec §4 (saída), RN-003, DT-005
  - **Aceite:** 60 → `60.00`; `valor_informado` 33.333 → `33.333`; `null` em
    `motivo` de item aprovado e em `valor_considerado` de `DADOS_INVALIDOS`;
    `total_reembolsavel` é a soma dos itens; `colaborador` com número é
    serializado sem erro.
  - **Teste:** `tests/test_saida_serializacao.py`
  - **Commit:** 9560e22

- [x] **T-019** — CLI `calcular --input --output`: em erro geral, mensagem em
  stderr, código 1 e arquivo de saída não criado nem sobrescrito; sucesso retorna
  0; argumentos inválidos retornam 2.
  - **Atende:** RN-013 (erro geral, "não gera saída"), DT-006
  - **Aceite:** com um arquivo de saída já existente e uma entrada sem
    `periodo.fim`, o arquivo continua igual e o código é 1; o exemplo gera o
    arquivo e retorna 0.
  - **Teste:** `tests/test_cli.py::test_dt006_erro_geral_nao_sobrescreve_saida`,
    `::test_dt006_erro_geral_retorna_1_e_escreve_stderr`, `::test_cli_exemplo_gera_arquivo`
  - **Commit:** deb2843

## Fase 5 — Casos de borda e aceite

- [x] **T-020** — Aceite completo com `exemplos/despesas-exemplo.json`
  (`test(T-020)`).
  - **Atende:** spec §9
  - **Aceite:** as 14 linhas (`valor_reembolsavel`, `status`, `motivo`) batem com
    a tabela da §9; `total_reembolsavel` = 585,43; um item por despesa, na mesma
    ordem da entrada.
  - **Teste:** `tests/test_secao9_aceite_exemplo.py`
  - **Commit:** 9f0e7b1

- [x] **T-021** — Texto exato das justificativas dos exemplos da §4 e verificação
  de que todo item cita uma RN.
  - **Atende:** spec §4 (exemplo), spec §9 (justificativa cita RN)
  - **Aceite:** d-001, d-002 e d-004 têm exatamente as justificativas da §4; todo
    item casa com `RN-\d{3}`.
  - **Teste:** `tests/test_secao9_aceite_exemplo.py::test_justificativas_exemplo_secao4`,
    `::test_todo_item_cita_rn`
  - **Commit:** a9ec241

- [x] **T-022** — Tabela da §7 como teste parametrizado, com uma linha por caso e
  o nome do caso como `id` (`test(T-022)`).
  - **Atende:** spec §7 (todas as RN citadas na tabela)
  - **Aceite:** os 37 casos da §7 passam e aparecem no relatório do pytest com o
    nome da spec.
  - **Teste:** `tests/test_secao7_casos_de_borda.py`
  - **Commit:** f1ca50c

- [x] **T-023** — Invariantes: determinismo e descrição informativa
  (`test(T-023)`).
  - **Atende:** RN-014, spec §9, AMB-006, AMB-008, AMB-010
  - **Aceite:** duas execuções produzem saídas idênticas byte a byte; trocar todas
    as descrições do exemplo não altera `valor_reembolsavel`, `status` nem `motivo`.
  - **Teste:** `tests/test_rn014_descricao.py`,
    `tests/test_secao9_aceite_exemplo.py::test_determinismo`
  - **Commit:** 24e7e64

- [x] **T-024** — Teste de rastreabilidade: lê a `spec.md`, extrai os `RN-\d{3}` e
  falha se algum não tiver arquivo `test_rnNNN_*.py`. Fica por último porque só
  passa quando todas as RN têm teste.
  - **Atende:** plan §6
  - **Aceite:** RN-001 a RN-014 têm arquivo de teste; remover um deles faz o teste
    falhar.
  - **Teste:** `tests/test_rastreabilidade.py`
  - **Commit:** 6cbdd95

## Fase 6 — Finalização

- [x] **T-025** — README: requisitos, instalação, como rodar a CLI e como rodar os
  testes e o lint (`docs(T-025)`).
  - **Atende:** DESAFIO (entrega), RUBRICA §5
  - **Aceite:** num clone limpo, seguir o README gera `resultado.json` a partir do
    exemplo e `python -m pytest` passa.
  - **Teste:** manual (roteiro do próprio README); `tests/test_cli.py::test_cli_exemplo_gera_arquivo`
    cobre o mesmo comando
  - **Commit:** 8bb0338

---

## Fase 7 — Envelope (Dia 2)

**Baseado em:** spec 2.1 (D-002, D-003) · plan 2.0. Nomes de módulo, função,
tipo e argumento de CLI citados abaixo seguem o plan 2.0 (seções 2 a 4 e DT-004
a DT-014).

Sequência pensada para a suíte ficar verde em todo commit:

- T-026 a T-030 criam os documentos novos e o campo `moeda`, sem mudar o
  resultado de nenhuma despesa.
- T-031 a T-037 levam as regras para a política externa e o câmbio. Até a
  T-038, o fluxo real (CLI e testes de exemplo) usa a **política padrão** da
  v4, que tem os mesmos valores da v3, e por isso os testes de aceite da v3
  continuam passando. As regras novas são testadas passando a política
  aplicável explicitamente ao motor.
- T-038 liga a seleção por centro de custo e o câmbio no fluxo real e atualiza,
  no mesmo commit, os testes da v3 cujo resultado muda.
- T-039 a T-041 fecham a §7, a §9 e a rastreabilidade.

Com a T-031, as constantes de `politica.py` deixam de existir (fim da regra
"constantes sem task própria" do topo deste arquivo).

### 7.1 — Modelo e documentos de entrada

- [x] **T-026** — `modelo.py`: motivo `COTACAO_INDISPONIVEL`; `Despesa` ganha
  `moeda`, `taxa_cambio` e `data_cotacao`; `Resultado` ganha `moeda`,
  `taxa_cambio` e `data_cotacao`. Valores padrão (`BRL`, nulo, nulo) mantêm as
  despesas da v3 como estão.
  - **Atende:** spec §4 (tabela de motivos, campos de saída), RN-018, AMB-025, AMB-033
  - **Aceite:** os oito motivos têm exatamente os códigos da spec;
    `COTACAO_INDISPONIVEL` existe; a suíte da v3 continua passando sem alteração.
  - **Teste:** `tests/test_modelo.py::test_motivos_iguais_aos_codigos_da_spec`
    (atualizado para oito motivos)
  - **Commit:**

- [x] **T-027** — Leitura e validação do documento de política (`politica.py`
  passa a ler `politica-v4.json` e devolver um objeto `Politica`). Chaves de
  categoria e de centro de custo e o valor de `periodicidade` normalizados pela
  RN-002; `moeda_base` normalizada pela RN-017. A grafia original de cada chave
  de centro de custo é guardada para as justificativas (AMB-038). Erro →
  `EntradaInvalida`. Ainda não é usado pelo motor.
  - **Atende:** RN-015, RN-002 (chaves e periodicidade do documento), RN-013
    (erro geral), AMB-031, AMB-034, AMB-036, AMB-038, AMB-039
  - **Aceite:** `politica-v4.json` → aceito, com `padrao` e três centros.
    Erro geral para: JSON ilegível, `NaN`, `Infinity`; sem `padrao`, sem
    `centros_custo`, sem `moeda_base` ou sem `nota_fiscal_obrigatoria_acima_de`;
    `padrao` que não é objeto; entrada de categoria que não é objeto; limite
    `-1`, `"60"` ou `true`; limiar negativo ou não numérico; `moeda_base` `USD`;
    `"periodicidade": "mes"`, `1` ou ausente; `Alimentação` e `alimentacao` na
    mesma tabela; `CC-ADM` e ` cc-adm ` em `centros_custo`. Sem erro:
    `moeda_base` `" brl "`; `centros_custo: {}`; limite `0`;
    `"periodicidade": "Dia"` e `" dia "` → `dia`; `"DIARIA"` → `diaria`; a chave
    `CC-COMERCIAL` mantém essa grafia para as justificativas;
    `"acrescimo_em_viagem_percentual": "x"`,
    `versao`, `vigencia` e `observacao` com qualquer valor.
  - **Teste:** `tests/test_rn015_politica.py`
  - **Commit:**

- [x] **T-028** — Política aplicável: `politica_aplicavel(politica, centro_custo)`
  devolve uma `PoliticaAplicavel` cujo `regra(categoria)` dá o limite (ou `None`
  se a categoria não consta) e a `Origem(tipo, codigo)` daquela categoria. O
  `tipo` é `PADRAO`, `CENTRO`, `HERDADA` ou `NAO_CADASTRADO`. Com o centro
  cadastrado, `codigo` é `Centro.codigo` (grafia da chave do documento de
  política). Sem cadastro, é o valor da entrada só com `strip()`, sem a
  normalização da RN-002. O texto da origem sai de `justificativas.origem`
  (DT-011). `Documento` ganha `centro_custo`, e na validação do documento de
  despesas `centro_custo` presente e não texto vira erro geral. Ainda não é
  usada pelo motor.
  - **Atende:** RN-016, RN-002 (centro de custo), RN-013 (erro geral do centro de
    custo), AMB-018, AMB-019, AMB-020, AMB-021, AMB-037, AMB-038, AMB-040,
    plan DT-011
  - **Aceite:** a seleção é conferida pelo `tipo`, pelo `codigo` e pelo limite;
    o texto de cada origem é conferido em `justificativas.origem`.
    Sem `centro_custo` ou `"  "` → padrão, origem "política padrão";
    `CC-COMERCIAL`, ` cc-comercial ` e `Cc-Comercial` → tabela do
    `CC-COMERCIAL`, origem "centro de custo CC-COMERCIAL" (grafia do documento
    de política); `CC-SUPORTE-N2` → padrão, origem "política padrão; centro de
    custo CC-SUPORTE-N2 não cadastrado"; `" CC-Suporte-N2 "` → padrão, origem
    "política padrão; centro de custo CC-Suporte-N2 não cadastrado" (só as pontas
    removidas, maiúsculas e minúsculas preservadas, e não `cc-suporte-n2`);
    `CC-ADM` → `hospedagem` 250,00 herdada
    da padrão, origem "centro de custo CC-ADM usando limite herdado da política
    padrão", e `alimentacao` 45,00, origem "centro de custo CC-ADM"; `CC-ADM` →
    `representacao`, ausente do centro e da padrão, origem "centro de custo CC-ADM";
    `CC-ENG-PLATAFORMA` → `hospedagem` 0,00 (não herda, porque consta);
    `CC-COMERCIAL` → `representacao` 300,00; padrão → sem `representacao`;
    `"centro_custo": 42` → `EntradaInvalida`.
  - **Teste:** `tests/test_rn016_politica_aplicavel.py` (seleção e
    `justificativas.origem`),
    `tests/test_rn013_dados_invalidos.py::test_rn013_erro_geral_*` (caso
    `centro_custo` numérico)
  - **Commit:**

- [x] **T-029** — Leitura e validação do documento de câmbio (`cambio.py` →
  objeto `Cambio`), opcional. Quando informado, é sempre validado. Códigos de
  moeda normalizados pela RN-017. Erro → `EntradaInvalida`. Ainda não é usado
  pelo motor.
  - **Atende:** RN-018 (documento de câmbio), RN-013 (erro geral), AMB-032
  - **Aceite:** `cambio.json` → aceito, com 12 datas. Erro geral para: JSON
    ilegível, `NaN`, `Infinity`; sem `moeda_base` ou sem `taxas`; `taxas` que não
    é objeto; `moeda_base` diferente da da política; chave `2026-7-13` ou
    `2026-02-30`; taxa `0`, `-5.42`, `"5,42"` ou `true`; `USD` e ` usd ` na mesma
    data. Sem erro: `fonte` e `observacao` com qualquer valor; `" usd "` lido como
    `USD`.
  - **Teste:** `tests/test_rn018_cambio.py::test_rn018_documento_*`
  - **Commit:**

- [x] **T-030** — Campo `moeda` da despesa: ausente → `BRL`; texto normalizado
  (pontas e maiúsculas); vazio ou não texto → `DADOS_INVALIDOS` com `moeda` nulo.
  Qualquer código não vazio é aceito. Revisa a T-007, onde `moeda` era ignorada.
  - **Atende:** RN-017, RN-013 (erro em uma despesa), AMB-024
  - **Aceite:** e-010 (sem `moeda`) → `BRL`; `" usd "` → `USD`; `"XYZ"` → aceito;
    `""`, `"   "` e `840` → `DADOS_INVALIDOS` e as demais despesas seguem.
    O teste da T-007 que tratava `"moeda": "USD"` como campo ignorado passa a
    usar `"projeto": "X"`.
  - **Teste:** `tests/test_rn017_moeda.py`,
    `tests/test_rn013_dados_invalidos.py::test_rn013_despesa_campo_desconhecido_e_ignorado`
  - **Commit:**

### 7.2 — Regras com política externa e câmbio

- [x] **T-031** — Política externa no motor e na CLI:
  `calcular(documento, politica, cambio=None, etapas=None)` monta um
  `Contexto(documento, politica, cambio)` e o passa a todas as etapas no lugar
  do `Documento` (troca mecânica de assinatura de todas as etapas, num único
  commit). As etapas de nota fiscal e de limites passam a ler o limiar e os
  limites da `PoliticaAplicavel`; `periodicidade` `dia` e `diaria` têm o mesmo
  efeito. As constantes de `politica.py` saem. `tests/fabrica.py` ganha
  `politica_aplicavel()`, que lê `politica-v4.json` e devolve a padrão por
  padrão. A CLI ganha `--politica`, **não** marcado como obrigatório no
  `argparse`: a falta dele é erro geral (código 1), assim como documento de
  política inexistente, ilegível ou inválido. Até a T-038, CLI e testes de
  exemplo usam a política padrão.
  - **Atende:** RN-015, RN-007 (limiar do documento), RN-008 (limites do
    documento), RN-013 (erro geral), AMB-031, AMB-036, plan DT-004, DT-006,
    DT-009, DT-014
  - **Aceite:** com a padrão da v4, toda a suíte da v3 passa (só as chamadas
    mudam para informar a política e as etapas recebem `Contexto`). Política com
    `alimentacao` 70,00 → duas despesas de 50,00 na mesma data → 50,00 + 20,00.
    Limiar 150,00 → 120,00 sem nota passa. CLI sem `--politica` → código 1,
    mensagem em stderr, arquivo de saída não criado e arquivo existente intacto
    (não é código 2). `--politica` apontando para arquivo inexistente ou com
    limite `-1` → código 1, arquivo de saída existente intacto.
  - **Teste:** `tests/test_rn007_nota_fiscal.py::test_rn007_limiar_vem_do_documento`,
    `tests/test_rn008_limites.py::test_rn008_limite_vem_do_documento`,
    `::test_rn008_dia_e_diaria_sao_limite_por_data`,
    `tests/test_motor.py::test_dt009_etapas_recebem_contexto`,
    `tests/test_cli.py::test_rn015_sem_politica_retorna_1_e_nao_cria_saida`,
    `::test_rn015_politica_inexistente_e_erro_geral`,
    `::test_rn015_politica_invalida_nao_sobrescreve_saida`
  - **Commit:**

- [x] **T-032** — Etapa de categoria pela política aplicável: reembolsável só se
  consta da tabela efetiva com limite maior que zero; limite 0,00 →
  `CATEGORIA_NAO_REEMBOLSAVEL`; `observacao` ignorada. A justificativa cita a
  origem da categoria (T-028). Revisa a T-012.
  - **Atende:** RN-001, RN-016, spec §4 (justificativa de categoria), AMB-014,
    AMB-021, AMB-022, AMB-023, AMB-037, AMB-038, AMB-040
  - **Aceite:** d-005 (`coworking`) → recusado, `CATEGORIA_NAO_REEMBOLSAVEL`.
    `CC-ENG-PLATAFORMA`: d-010 (hospedagem) → recusado, `CATEGORIA_NAO_REEMBOLSAVEL`;
    d-013 (hospedagem, 690,00, sem nota) → `CATEGORIA_NAO_REEMBOLSAVEL`, e não
    `NOTA_FISCAL_AUSENTE`. Padrão: f-003 (`representacao`) → recusado.
    `CC-COMERCIAL`: e-001 (`representacao`) → passa. `CC-ADM`: hospedagem →
    passa (herança). Limite 0 em qualquer categoria de qualquer tabela → recusado.
    A justificativa cita a RN-001 e a origem: d-010 → "centro de custo
    CC-ENG-PLATAFORMA"; ` cc-eng-plataforma ` → "centro de custo
    CC-ENG-PLATAFORMA"; f-003 → "política padrão; centro de custo CC-SUPORTE-N2
    não cadastrado"; `" CC-Suporte-N2 "` com `representacao` → "política padrão;
    centro de custo CC-Suporte-N2 não cadastrado"; `CC-ADM` com `representacao`
    → "centro de custo CC-ADM";
    política com `hospedagem` 0 na padrão e `CC-ADM` → "centro de custo CC-ADM
    usando limite herdado da política padrão".
  - **Teste:** `tests/test_rn001_categoria.py`
  - **Commit:**

- [x] **T-033** — Etapa de limites pela tabela efetiva, incluindo
  `representacao` como categoria independente, e justificativa de
  `LIMITE_DIARIO` citando a origem do limite. O acréscimo em viagem do documento
  não é aplicado. Revisa a T-015 e a T-016.
  - **Atende:** RN-008, RN-009, RN-010, RN-011, RN-016, spec §4 (justificativa
    de limite), AMB-008, AMB-021, AMB-023, AMB-035, AMB-036, AMB-037, AMB-038,
    AMB-040
  - **Aceite:** `CC-COMERCIAL`: e-007 (hospedagem, 1.200,00, "3 noites") →
    400,00, `limitado`; e-001 (`representacao`, 340,00) → 300,00, `limitado`;
    e-008 (alimentação, 95,00) → 90,00, `limitado`; alimentação e representação
    na mesma data não dividem limite. `CC-ADM`: hospedagem 300,00 → 250,00,
    `limitado`. `CC-ENG-PLATAFORMA`: d-001 + d-002 → 72,50 + 2,50. Padrão:
    f-002 (310,00) → 250,00. `acrescimo_em_viagem_percentual` 50 → nenhum limite
    acima da tabela. A justificativa cita o limite, o valor consumido, os `id`
    que consumiram e a origem: `CC-ADM` com hospedagem 300,00 → "centro de custo
    CC-ADM usando limite herdado da política padrão"; `CC-ADM` com alimentação
    acima de 45,00 → "centro de custo CC-ADM"; ` cc-comercial ` com alimentação
    de 95,00 → 90,00, `limitado`, citando "centro de custo CC-COMERCIAL"; f-002
    → "política padrão; centro de custo CC-SUPORTE-N2 não cadastrado";
    `" CC-Suporte-N2 "` com hospedagem de 310,00 → 250,00, `limitado`, citando
    "política padrão; centro de custo CC-Suporte-N2 não cadastrado".
  - **Teste:** `tests/test_rn008_limites.py`, `tests/test_rn009_distribuicao.py`,
    `tests/test_rn010_parcial.py`, `tests/test_rn011_viagem.py`
  - **Commit:**

- [x] **T-034** — Etapa de conversão (etapa 3 da §8, antes de valor negativo):
  novo tipo de etapa `Conversao` em `motor.py`, primeiro item de `ETAPAS`, que
  devolve a `Despesa` com `valor_considerado`, `taxa_cambio` e `data_cotacao`
  preenchidos (ela substitui a da lista viva) ou uma recusa.
  - **BRL:** `entrada.py` continua preenchendo `valor_considerado =
    arredondar(valor_informado)`, como na v3; a etapa deixa passar sem consultar
    o câmbio.
  - **Outra moeda:** `entrada.py` deixa `valor_considerado = None`; a etapa
    chama `Cambio.cotacao(moeda, data)`, que busca a maior data ≤ data da
    despesa (`bisect_right`), e arredonda o produto uma única vez.
  - Sem taxa, ou `cambio=None` → `COTACAO_INDISPONIVEL`, com `valor_considerado`
    nulo e justificativa `justificativas.cotacao_indisponivel(moeda, data)`.

  A linha da §7 "campo desconhecido" (que usava `moeda: USD`) passa a usar
  `projeto`.
  - **Atende:** RN-018, RN-003, RN-012, spec §8 (etapa 3), spec §4
    (justificativa de cotação), AMB-025, AMB-026, AMB-027, AMB-029, plan DT-010
  - **Aceite:** e-002 (22,00 EUR, 2026-07-14) → taxa 5,93, `data_cotacao`
    2026-07-14, 130,46. e-004 (30,00 EUR, sábado 2026-07-18) → taxa 5,96 de
    2026-07-17, 178,80. f-004 (12,00 USD, 2026-07-21) → 65,76. 33,333 USD em
    2026-07-13 → 180,66. e-006 (55,00 GBP) → recusado, `COTACAO_INDISPONIVEL`,
    `valor_considerado` nulo, justificativa citando `GBP` e a data. USD em
    2026-07-10 → `COTACAO_INDISPONIVEL`. USD sem câmbio → `COTACAO_INDISPONIVEL`
    e as despesas em BRL seguem. BRL em sábado → sem taxa, processada.
    −10,00 GBP → `COTACAO_INDISPONIVEL`; −10,00 USD em 2026-07-13 → −54,20,
    `VALOR_NEGATIVO`. USD sem cotação e fora do período → `COTACAO_INDISPONIVEL`.
    Despesa BRL construída pela entrada chega à etapa 4 com o mesmo
    `valor_considerado` da v3; nenhuma despesa chega à etapa 4 com
    `valor_considerado` nulo.
  - **Teste:** `tests/test_rn018_cambio.py::test_rn018_conversao_*`,
    `::test_rn018_cotacao_usa_data_anterior_mais_proxima`,
    `tests/test_motor.py::test_dt010_conversao_e_a_primeira_etapa`,
    `tests/test_rn003_arredondamento.py::test_rn003_arredonda_uma_vez_depois_da_conversao`,
    `tests/test_secao7_casos_de_borda.py` (linha "Campo desconhecido")
  - **Commit:**

- [ ] **T-035** — Nota fiscal comparada com o valor convertido para reais
  (`test(T-035)`; a T-034 já entrega `valor_considerado` em reais).
  - **Atende:** RN-007, AMB-028
  - **Aceite:** e-005 (40,00 USD × 5,50 = 220,00, sem nota) → recusado,
    `NOTA_FISCAL_AUSENTE`. e-003 (14,50 EUR × 5,88 = 85,26, sem nota) → passa.
    20,00 USD (abaixo de 100 na moeda original, acima em reais), sem nota →
    recusado.
  - **Teste:** `tests/test_rn007_nota_fiscal.py::test_rn007_compara_valor_convertido_*`
  - **Commit:**

- [ ] **T-036** — Duplicatas exigem a mesma moeda e o mesmo valor informado
  arredondado para centavos na moeda original (em `BRL`, o próprio
  `valor_considerado`). Despesas recusadas por `COTACAO_INDISPONIVEL` não entram
  no grupo. Revisa a T-013.
  - **Atende:** RN-006, AMB-010, AMB-030
  - **Aceite:** duas despesas de 22,00 EUR, mesmas data, categoria e fornecedor
    → a segunda é `DUPLICATA`, citando a primeira. 22,00 EUR e 130,46 BRL → não
    são duplicatas. 22,00 EUR e 22,00 USD → não são duplicatas. 22,004 EUR e
    22,00 EUR → duplicatas. Duas GBP iguais → ambas `COTACAO_INDISPONIVEL`,
    nenhuma `DUPLICATA`.
  - **Teste:** `tests/test_rn006_duplicatas.py`
  - **Commit:**

- [ ] **T-037** — Saída com os campos novos, na ordem da §4: `moeda`,
  `taxa_cambio` (como está no documento, sem quantizar) e `data_cotacao`
  (`AAAA-MM-DD`); `valor_considerado` nulo também em `COTACAO_INDISPONIVEL`;
  `moeda` nula em `DADOS_INVALIDOS`. Revisa a T-018.
  - **Atende:** spec §4 (saída), RN-003, RN-017, RN-018, AMB-033, DT-005
  - **Aceite:** item em BRL → `"moeda": "BRL"`, `taxa_cambio` e `data_cotacao`
    `null`. e-002 → `"taxa_cambio": 5.93`, `"data_cotacao": "2026-07-14"`,
    `"valor_considerado": 130.46`, `"valor_informado": 22.00`. e-006 →
    `"moeda": "GBP"`, `valor_considerado`, `taxa_cambio` e `data_cotacao` `null`.
    `DADOS_INVALIDOS` → `moeda` `null`. Campos do item na ordem da tabela da §4.
  - **Teste:** `tests/test_saida_serializacao.py::test_dt005_campos_do_item_na_ordem_da_spec`,
    `::test_dt005_moeda_e_cotacao_em_brl`, `::test_dt005_taxa_cambio_sem_quantizar`,
    `::test_dt005_nulos_em_cotacao_indisponivel`, `::test_dt005_nulos_em_dados_invalidos`
  - **Commit:**

### 7.3 — Integração, aceite e rastreabilidade

- [ ] **T-038** — Fluxo real completo: a CLI ganha `--cambio` (opcional) e passa
  a escolher a política pelo `colaborador.centro_custo` (T-028). Ordem de
  leitura: despesas, política, câmbio (o câmbio compara `moeda_base` com a
  política). Sem `--cambio`, o motor recebe `cambio=None`. No mesmo
  commit, atualiza os testes da v3 cujo resultado muda com o
  `CC-ENG-PLATAFORMA`: tabela da §9 (total 585,43 → 351,43), justificativas
  exatas da §4 (Exemplo 1) e as linhas da §7 reescritas pela spec 2.0. Atualiza
  o comando de execução no README e no `CLAUDE.md`. Revisa as T-019, T-020,
  T-021, T-022 e T-025.
  - **Atende:** RN-016, RN-018 (câmbio opcional), RN-013 (erro geral dos
    documentos), spec §4 (Exemplo 1), spec §8 (validação antes das etapas),
    spec §9 (exemplo original), plan DT-006
  - **Aceite:** `exemplos/despesas-exemplo.json` + `politica-v4.json`, sem
    câmbio → as 14 linhas da §9 e total 351,43; d-001, d-002 e d-004 com
    exatamente as justificativas do Exemplo 1 da §4. Sem `centro_custo` →
    padrão. `"centro_custo": 42`, `--cambio` para arquivo inexistente, câmbio
    com taxa 0 ou câmbio com `moeda_base` diferente → código 1, arquivo de
    saída existente intacto. Despesa em USD sem `--cambio` →
    `COTACAO_INDISPONIVEL` e código 0. Argumento desconhecido ou `--input`
    ausente → código 2. Linhas da §7
    reescritas ("Duas despesas no mesmo dia...", "Hospedagem com várias
    diárias", "Duas hospedagens na mesma data", "Hospedagem sem nota acima de
    100", "Categoria em maiúsculas", "Campo desconhecido") batem com a spec 2.0.
  - **Teste:** `tests/test_secao9_aceite_exemplo.py`,
    `tests/test_secao7_casos_de_borda.py` (linhas reescritas),
    `tests/test_cli.py::test_cli_exemplo_gera_arquivo`,
    `::test_rn016_centro_custo_invalido_e_erro_geral`,
    `::test_rn018_cambio_invalido_nao_sobrescreve_saida`,
    `::test_rn018_moedas_base_divergentes_e_erro_geral`,
    `::test_rn018_sem_cambio_despesa_estrangeira_cotacao_indisponivel`,
    `::test_dt006_argumentos_invalidos_retornam_2` (com `--input` ausente e
    argumento desconhecido)
  - **Commit:**

- [ ] **T-039** — Casos novos da §7 da spec 2.1 na tabela parametrizada, com o
  nome do caso como `id` (`test(T-039)`).
  - **Atende:** spec §7 (casos de RN-001, RN-006, RN-007, RN-013, RN-015 a
    RN-018 e seção 8 incluídos nas specs 2.0 e 2.1), AMB-037, AMB-038, AMB-039,
    AMB-040
  - **Aceite:** os 71 casos da §7 passam e aparecem no relatório do pytest com o
    nome da spec; o teste de contagem passa de 37 para 71. Inclui "Grafia do
    centro de custo na justificativa", "Periodicidade com grafia diferente",
    "Centro de custo desconhecido com espaços nas pontas" (`" CC-Suporte-N2 "`
    → justificativa com "CC-Suporte-N2") e a justificativa de herança em
    "Categoria ausente na tabela do centro".
  - **Teste:** `tests/test_secao7_casos_de_borda.py::test_secao7_caso_de_borda`,
    `::test_secao7_tem_71_casos`
  - **Commit:**

- [ ] **T-040** — Aceite dos dois documentos do envelope pela CLI, com
  `politica-v4.json` e `cambio.json` (`test(T-040)`).
  - **Atende:** spec §9 (envelope), spec §4 (Exemplo 2), RN-014, RN-016,
    AMB-019, AMB-038
  - **Aceite:** `despesas-envelope.json` → as 10 linhas da §9
    (`valor_considerado`, `valor_reembolsavel`, `status`, `motivo`) e total
    1.143,26; e-002 com exatamente a justificativa do Exemplo 2 da §4; as
    justificativas de `LIMITE_DIARIO` e `CATEGORIA_NAO_REEMBOLSAVEL` citam
    "centro de custo CC-COMERCIAL", sem herança (todas as categorias reembolsadas
    do documento constam do centro).
    `despesas-envelope-cc-desconhecido.json` → as 4 linhas e total 373,76; as
    justificativas de f-002 e f-003 citam "política padrão; centro de custo
    CC-SUPORTE-N2 não cadastrado". Nos dois: um item por despesa, na ordem;
    todo item cita `RN-\d{3}`; duas execuções idênticas byte a byte; trocar as
    descrições não altera `valor_reembolsavel`, `status` nem `motivo`.
  - **Teste:** `tests/test_secao9_aceite_envelope.py`
  - **Commit:**

- [ ] **T-041** — Rastreabilidade: o teste exige `test_rnNNN_*.py` de RN-001 a
  RN-018; a tabela de Cobertura deste arquivo ganha RN-015 a RN-018, AMB-018 a
  AMB-036 e as tasks da Fase 7 nas linhas revistas. Fica por último porque só
  passa quando RN-015 a RN-018 têm teste.
  - **Atende:** plan §6, D-002 (rastreabilidade)
  - **Aceite:** a `spec.md` 2.0 tem RN-001 a RN-018 e todas têm arquivo de
    teste; remover `test_rn018_cambio.py` faz o teste falhar; toda RN e toda AMB
    da spec aparecem na Cobertura com task e teste.
  - **Teste:** `tests/test_rastreabilidade.py::test_rastreabilidade_spec_tem_rn001_a_rn018`,
    `::test_rastreabilidade_toda_rn_tem_arquivo_de_teste`
  - **Commit:**

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
