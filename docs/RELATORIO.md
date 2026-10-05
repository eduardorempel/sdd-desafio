# Relatório — Desafio SDD

**Aluno:** Eduardo · **Repositório:** https://github.com/eduardorempel/sdd-desafio · **Data:** 2026-10-04

> **Autoria deste relatório:** rascunhado pelo Claude a partir do repositório e
> dos exports em `docs/sessions/`, e revisado por mim.

> Todas as afirmações abaixo apontam para um arquivo, um hash de commit ou uma
> linha de sessão exportada (`docs/sessions/NN-...md:linha`). Onde algo não dá
> para provar pelo repositório, isso está dito explicitamente.

---

## Resumo em números

| Item | Valor | Evidência |
|---|---|---|
| Ambiguidades registradas na spec | 40 (AMB-001 a AMB-040): 17 da v3, 23 da v4 | `spec.md` §6 |
| Regras de negócio | 18 (RN-001 a RN-018): 14 da v3, 4 novas da v4 | `spec.md` §5 |
| Entradas no `DECISIONS.md` | 3 (D-001, D-002, D-003) | `DECISIONS.md` |
| Tasks | 41 (T-001 a T-041), todas `[x]`, cada uma com o hash do commit | `tasks.md` |
| Casos de borda da §7 | 37 na v3 → 71 na v4 | `f1ca50c`, `f218cbb` |
| Testes antes do envelope | **245 passando** | `05-implementacao-bloco.md:2795`; reexecutado no commit `d8fa815` |
| Testes no final | **487 passando**, `ruff check` e `ruff format --check` limpos | `python -m pytest` em `d1e5af3`; `08-implementacao-envelope-v4.md:3414` |
| CLI nos três exemplos da §9 | 351,43 · 1.143,26 · 373,76, iguais à spec | execução real da CLI; `08:3416-3417` |

---

## 1. Como a v3 foi desambiguada

**Quem encontrou as ambiguidades.** Pedi ao Claude que cruzasse a política com o
`despesas-exemplo.json`, propusesse interpretações e recomendasse uma, **sem
decidir por mim e sem escrever a spec** (`02-especificacao.md:91-98`). Ele
listou "15 ambiguidades, e uma 16ª questão que atravessa todas: a ordem de
aplicação das regras", classificadas pelos três tipos da rubrica, U, F e D
(`02:103-106`).

**Quem decidiu.**
- Não aprovei tudo de uma vez: "não quero aprovar tudo automaticamente… quero
  revisar especificamente AMB-06, AMB-07 e AMB-08" (`02:343-346`). Esse pedido
  mudou duas recomendações (ver Discernimento, caso 1).
- Fechei AMB-06/07/08 do meu jeito e aprovei as outras (`02:551-556`).
- O Claude ainda apontou conflitos entre decisões já aprovadas (`02:627-673`).
  Resolvi esses conflitos (`02:688-694`) antes de liberar a escrita.

**A 17ª ambiguidade veio do planejamento.** Ao desenhar a validação para o
`plan.md`, o Claude listou 8 lacunas e disse: "Não decidi nenhum. Pela regra do
CLAUDE.md, cada um precisa de uma decisão na spec, ou o código vai decidir em
silêncio" (`03-planejamento.md:188-192`).
- Decidi as 8 (`03:221-236`), mais os pontos C–F (`03:323-335`) e o tratamento de
  `NaN`/campos desconhecidos (`03:516-517`).
- No item "elemento da lista que não é objeto = erro geral", mantive minha
  decisão mesmo com o Claude dizendo que ela "contraria a leitura natural da
  regra" (`03:260-267`). Ela foi escrita na RN-013 com justificativa.
- Tudo isso virou a spec 1.1, registrada na **D-001** (`2d52dd2`) antes de
  qualquer código.

**Exemplo de requisito antes/depois (RN-007, nota fiscal).** A primeira versão
(`90eefaa`) já resolvia a fronteira (AMB-004) e a base de comparação (AMB-005):

> Despesa com `valor_considerado` estritamente maior que 100,00 e sem nota fiscal
> é recusada inteira com `NOTA_FISCAL_AUSENTE`. A verificação usa o valor da
> própria despesa, e não a soma do dia nem o valor após o limite. Despesa de
> exatamente 100,00 não exige nota.

A versão final (spec 2.1) só mudou por causa da v4 (AMB-028):

> Despesa com `valor_considerado` (em reais, depois da conversão) estritamente
> maior que o limiar `nota_fiscal_obrigatoria_acima_de` do documento de política
> (100,00 na v4) e sem nota fiscal é recusada inteira […]. Despesa de valor
> exatamente igual ao limiar não exige nota.

O aceite da RN-007 sempre foi um caso do próprio exemplo: d-003 (100,00) não
exige nota e d-004 (100,01) é recusado. Na v4 entraram e-005 (40 USD × 5,50 =
220,00, recusado) e e-003 (85,26, não exige).

Um requisito que **estava errado** na primeira versão: a spec 1.0 dizia que
`valor_informado` sai "exatamente como veio na entrada" e também que "todos os
valores de saída têm duas casas" (RN-003). As duas frases se contradizem em
d-011 (33,333). O Claude achou isso ao planejar (`03:251-253`). A correção está
na D-001: `valor_informado` passou a ser o valor numérico, e a RN-003 passou a
valer só para os três campos monetários calculados.

## 2. Spec como fonte da verdade

O `CLAUDE.md` define a regra: "Quando o código e a spec discordarem, a spec está
certa e o código é o bug". Explicação de regra no chat é bug de spec. Na prática:

- **Toda mudança de spec antes de código.** D-001, D-002 e D-003 registram
  "**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`), antes de qualquer código".
  As datas dos commits confirmam: `2d52dd2` (spec 1.1) vem antes de `33ec69e`
  (T-001), e `20aee1d` e `e1f79c3` (spec 2.0 e 2.1) vêm antes de `18b151f`
  (T-026).
- **O Claude parou quando eu dei uma regra só no chat.**
  - Contexto: decidi a grafia do centro de custo não cadastrado no chat
    (`07-planejamento-envelope-v4.md:851-859`) e pedi para atualizar o
    `tasks.md`.
  - Resposta dele: "a regra nova … não está na spec nem na D-003. Pelo CLAUDE.md,
    ela precisa entrar primeiro na spec e no DECISIONS.md. Por isso, agora
    atualizo tasks.md só com o que já está na D-003" (`07:875-878`).
  - A regra virou AMB-040 e entrou na D-003, e só depois chegou às tasks.
- **Na implementação, a ordem era parar se faltasse decisão.** Escrevi "Não
  altere regras de negócio da spec por conta própria. Se encontrar uma decisão
  de negócio que não esteja definida na spec, PARE" (`05:32-34`). Na Fase 7:
  "se achar alguma decisao de negocio faltando para e me avisa" (`08:19-20`).
- **A spec não cita solução técnica.** O cabeçalho da `spec.md` proíbe citar
  linguagem, biblioteca, classe ou pasta. Os nomes técnicos ficam no `plan.md`.

## 3. Como saíram o plan e as tasks

- **`plan.md` 1.0** (`9b66b4a`): stack Python 3.12 sem dependências de runtime,
  com `Decimal` desde o parse. Cada decisão técnica tem uma alternativa
  descartada (DT-001 a DT-008). Exemplos: `float` e centavos inteiros
  descartados; `unidecode` descartado porque transliteraria além dos acentos;
  `pydantic`/`jsonschema` descartados.
- **A decisão que mais pesou no envelope.** O plano previa: "A política fica em
  dados, num só lugar (politica.py) … Essa é a decisão que mais pesa no envelope
  do dia 2, então vale registrar como DT" (`03:117-122`).
- **`tasks.md`**: T-001 a T-025 (`2d2c1f4`) e Fase 7 com T-026 a T-041
  (`cc21a10`). Cada task tem os campos **Atende** (RN/AMB/seção da spec),
  **Aceite** e **Teste** (nome do arquivo e da função). A Fase 7 foi planejada
  para a suíte ficar verde em todo commit (`tasks.md`, cabeçalho da Fase 7).

## 4. Rastreabilidade spec → task → commit → teste

- **Spec → task:** a tabela "Cobertura" no fim do `tasks.md` liga cada RN-001 a
  RN-018, cada AMB-001 a AMB-040 e as seções 4, 7, 8 e 9 às tasks e aos arquivos
  de teste.
- **Task → commit:**
  - Todos os 41 commits de implementação seguem `feat(T-NNN)`/`test(T-NNN)`, um
    por task.
  - Documentação usa `docs(spec)`, `docs(plan)`, `docs(tasks)` e
    `docs(sessions)`.
  - O hash de cada task está no próprio `tasks.md`, registrado em `7015605` e
    `0f6b03b`.
  - A única exceção é o commit inicial `d9423c6` (`chore:`).
- **Commit → teste:** há um arquivo `tests/test_rnNNN_*.py` por regra. Os
  arquivos `test_secao7_casos_de_borda.py`, `test_secao9_aceite_exemplo.py` e
  `test_secao9_aceite_envelope.py` usam os nomes da spec.
- **A rastreabilidade é testada.** `tests/test_rastreabilidade.py` lê a
  `spec.md` e falha se alguma RN não tiver arquivo de teste. Ele exige RN-001 a
  RN-018 e verifica que remover `test_rn018_cambio.py` faz o teste falhar
  (`48e3c54`).
- **Exemplo de ida e volta (RN-018):**
  - spec RN-018;
  - tasks T-029, T-034 e T-038;
  - commits `3acc4e8`, `88a9c2b` e `f9248fc`;
  - código `reembolso/cambio.py::Cambio.cotacao` e etapa `conversao` em
    `reembolso/etapas.py`;
  - testes em `tests/test_rn018_cambio.py`.

---

## 5. O envelope do Dia 2 (política v4)

### O que chegou

- Quatro arquivos em `exemplos/envelope/`: `politica-v4.json`, `cambio.json`,
  `despesas-envelope.json` e `despesas-envelope-cc-desconhecido.json`.
- Os temas: política externa por centro de custo, política padrão, categoria
  `representacao`, centro de custo que não reembolsa hospedagem, campo `moeda`
  e conversão cambial pela data da despesa (`06-envelope-spec-v4.md:13-58`).
- O texto narrativo da v4 não está no repositório. O Claude trabalhou pelos JSON
  e pela minha descrição (`06:72-74`).
- O item C (aprovação manual) ficou fora por ser opcional (spec §3).

### Ordem em que foi absorvido

| # | Passo | Evidência |
|---|---|---|
| 1 | Só análise de impacto: "NÃO altere spec.md / NÃO altere DECISIONS.md / NÃO crie tasks / NÃO implemente código / NÃO faça commit" | `06:15-22` |
| 2 | O Claude listou 19 ambiguidades novas (AMB-018 a AMB-036) com recomendação. Achado principal: o exemplo original é `CC-ENG-PLATAFORMA`, então o total da §9 cai de 585,43 para 351,43 | `06:76-81` |
| 3 | Confirmei as recomendações e fixei pontos específicos | `06:539-560` |
| 4 | spec 1.1 → 2.0 + **D-002** | `20aee1d` (17:24) |
| 5 | Ao escrever as tasks, o Claude achou 3 pontos não decididos. Decidi os três, e depois um quarto (AMB-040) → spec 2.1 + **D-003** | `07:630-659`, `07:851-859`, `e1f79c3` |
| 6 | plan 1.0 → 2.0 (DT-004 a DT-006 revistas, DT-009 a DT-014 novas) | `e2a2a45` |
| 7 | Fase 7 do `tasks.md` (T-026 a T-041) | `cc21a10` |
| 8 | Implementação, um commit por task | `18b151f` … `48e3c54` (22:57–23:14) |

### O que a arquitetura absorveu sem esforço

- **Ordem das regras como dado.** A nova etapa de conversão entrou como uma
  linha a mais no início de `ETAPAS` (`reembolso/motor.py:54`). As seis etapas
  da v3 continuaram iguais e na mesma ordem:
  ```python
  ETAPAS: list[Etapa] = [
      Conversao(regras.conversao),  # RN-018, RN-003 → COTACAO_INDISPONIVEL   ← nova
      PorItem(regras.valor_negativo),  # RN-005 → VALOR_NEGATIVO
      ...
  ```
- **Nota fiscal depois da conversão (AMB-028).** Saiu "de graça": como
  `valor_considerado` já está em reais quando a etapa de nota fiscal roda, só o
  limiar passou a vir do documento (DT-014).
- **Limites e categoria.** As três etapas mudaram só na origem do dado. Em vez da
  constante, usam `politica.regra(categoria)`; "a lógica da 1.0 fica igual"
  (DT-014).
- **Duplicatas com moeda.** Só a chave do agrupamento mudou (DT-013):
  - antes: `(data, categoria, fornecedor, valor_considerado)`;
  - depois: `(data, categoria, fornecedor, moeda, arredondar(valor_informado))`;
  - em BRL os dois dão o mesmo resultado (`a3cb4fe`).
- **BRL não passa pelo câmbio.** `entrada.py` já preenchia `valor_considerado`
  arredondado para despesas em BRL. O documento de câmbio só é consultado para
  outra moeda (DT-010).

### O que teve que mudar de verdade

- **Política embutida → documento externo.**
  - Antes do envelope, `reembolso/politica.py` em `d8fa815` era só isto:
    ```python
    CATEGORIAS_REEMBOLSAVEIS = frozenset({"alimentacao", "transporte_urbano", "hospedagem"})
    LIMIAR_NOTA_FISCAL = Decimal("100.00")
    LIMITE_POR_DATA = {"alimentacao": Decimal("60.00"), ...}
    ```
  - Agora o módulo lê e valida o documento (`ler_politica`, `validar_politica`)
    e escolhe a `PoliticaAplicavel` pelo centro de custo (`politica_aplicavel`).
  - **Autocrítica:** o plan 1.0 tinha **descartado** a configuração externa
    "porque config externa exigiria validar a própria config (YAGNI)"
    (`03:119-121`). Foi exatamente o que a v4 pediu.
  - O que salvou foi a política já estar isolada num módulo só. Nenhuma etapa
    tinha número mágico.
- **Centro de custo escolhe a política (RN-016).**
  - `colaborador.centro_custo` era informativo e passou a decidir. Ausente ou
    desconhecido usa a padrão; categoria ausente no centro herda da padrão.
  - A justificativa cita a origem: "centro de custo CC-ADM usando limite herdado
    da política padrão", ou "política padrão; centro de custo CC-SUPORTE-N2 não
    cadastrado".
  - Isso exigiu um tipo novo, `Origem`/`TipoOrigem` (DT-011).
- **`Contexto` em todas as etapas (DT-009).**
  - As etapas recebiam o `Documento` e passaram a receber
    `Contexto(documento, politica, cambio)`.
  - A troca foi mecânica, mas atingiu todas as etapas e os testes que chamam
    etapas diretamente: `0bea107` tocou 23 arquivos, +394/−135.
  - Era o risco classificado como "Alta" no plan 2.0.
- **Moeda e câmbio.**
  - `reembolso/cambio.py` é novo: busca da cotação na data ou na anterior mais
    próxima com `bisect_right`.
  - Campo `moeda` na despesa: BRL por padrão, normalizado (RN-017).
  - Motivo novo `COTACAO_INDISPONIVEL`, que recusa só aquela despesa.
  - Exemplo: e-004 (30,00 EUR num sábado) usa a taxa da sexta, 5,96, e dá
    178,80.
- **Saída e CLI.**
  - Campos novos `moeda`, `taxa_cambio` e `data_cotacao` (`dda18f4`).
  - Argumentos `--politica` (obrigatório pela spec; a falta é erro geral, código
    1) e `--cambio` (opcional) (`f9248fc`).
- **Testes da v3 que mudaram de resultado, com motivo documentado.**
  - O total do exemplo original caiu de 585,43 para 351,43. d-001, d-002,
    d-010, d-013 e d-014 mudaram, e d-013 trocou de motivo, de
    `NOTA_FISCAL_AUSENTE` para `CATEGORIA_NAO_REEMBOLSAVEL`.
  - Tudo isso está previsto na D-002 ("O que isso invalidou").
  - Os testes foram atualizados no mesmo commit que ligou a política real
    (`f9248fc`).
  - O caso da §7 "`moeda: USD` ignorado" contradizia a v4 e foi reescrito para
    `projeto`.

### Números da absorção (`d8fa815` → `48e3c54`)

| Parte | Diff |
|---|---|
| spec, plan, tasks, DECISIONS (antes de qualquer código) | 4 arquivos, +1512/−230 |
| Código `reembolso/` | 10 arquivos, +481/−76 |
| Testes `tests/` | 26 arquivos, +2117/−132 |
| Testes | 245 → 487 |

- **Feito por mim vs reexecução das tasks.** Pelos exports, todo o conteúdo dessa
  absorção foi escrito pelo Claude a partir da spec atualizada: 16 tasks
  executadas em sequência numa única instrução (`08:6-26`, "19m 31s",
  `08:3457`).
- **Minha parte.**
  - Decisões: `06:539-560`, `07:646-657`, `07:851-859`, `07:1259`, `08:3459`.
  - Os commits sem trailer do Claude: `20aee1d`, `3ef0e3c`, `d1e5af3`.
  - O export das sessões.
- **Arquivos de código ou teste editados à mão: nenhum** que apareça nos exports.
- **Tempo.**
  - Tempo de processamento do Claude somado nas sessões 06, 07 e 08: cerca de
    44 min.
  - Relógio: da análise de impacto (concluída às 17:03, `06:537`) ao último
    commit (23:27).
  - Entre 18:54 e 22:30 não há atividade registrada nas sessões.

### Se eu tivesse escrito a spec sabendo da v4

- Teria tratado `centro_custo` e `moeda` como dados desde a 1.0, em vez de
  "informativos".
- Teria aceitado a política como entrada desde o início. A DT-004 da 1.0
  descartou isso por YAGNI e acabou custando a troca para `Contexto`.
- O que a spec me poupou: as regras da v3 (ordem das etapas, distribuição do
  limite por posição, arredondamento, duplicatas) não precisaram ser
  redescobertas. A D-002 lista exatamente quais RN mudaram, e a análise de
  impacto citou as que não mudavam (`06:85-147`).

---

## Delegação

| Atividade | Quem | Evidência |
|---|---|---|
| Identificar ambiguidades | Claude listou; eu pedi revisão de pontos específicos | `02:103-106`, `02:343-346` |
| Decidir ambiguidades | Eu (recomendações do Claude aceitas ou revistas) | `02:551-556`, `03:221-236`, `07:646-657` |
| Escrever spec, plan, tasks, DECISIONS | Claude, a partir das minhas decisões; eu travava cada passo com "não altere / não commite ainda" | `02:91-97`, `03:23-26`, `06:15-22` |
| Arquitetura | Claude propôs no `plan.md`; escolhi a stack ("Pode seguir com Python", `03:221`) | `9b66b4a` |
| Implementar e testar | Claude, uma task por commit | sessões 04, 05 e 08 |
| Commits de spec e sessões no Dia 1 | Eu (sem trailer `Co-Authored-By`) | `90eefaa`, `2d52dd2`, `9b66b4a`, `2d2c1f4`, `33ec69e` |
| Commits de implementação | Claude (com trailer `Co-Authored-By`) | `f207780` … `48e3c54` |
| Absorver o envelope | Claude executou; eu decidi as 23 ambiguidades novas | seção 5 acima |
| Este relatório | Rascunhado pelo Claude a partir do repositório e dos exports; revisado por mim | — |

**Onde deleguei e me arrependi.** Liberei a escrita da spec 1.0 com três pontos
ainda em aberto (formato da saída, fora de escopo, entrada malformada). O
próprio Claude avisou: "Preenchi tudo com propostas minhas, que precisam da sua
revisão" (`02:1706-1708`). Foi exatamente nessas partes que apareceram as
lacunas e as contradições corrigidas na D-001.

**Onde não deleguei e talvez devesse.** A sessão que gerou as tasks T-001 a
T-025 (`2d2c1f4`) não foi exportada (ver seção Sessões).

**Subagentes, skills, MCP, hooks.** Nenhum nas sessões do desafio. Os exports
mostram só Read, Search, Write, Update e shell. Para implementar, o Claude criou
um script local de commit (`/tmp/fechar.sh`, `05:116`).

## Discernimento

### Caso 1 — recomendação errada em AMB-06 e AMB-08, pega por mim

- **O que ele propôs:**
  - Para "em viagem" (AMB-06): "Recomendo (b)", inferir viagem a partir de
    hospedagem (`02:190-193`).
  - Para o número de diárias (AMB-08): "Recomendo (b), restrita", extrair o
    número de diárias do texto da descrição (`02:219-221`).
- **Por que estava errado:**
  - A inferência de viagem erra o caso mais evidente do arquivo: "d-003
    ('Corrida aeroporto') e d-004 ('Corrida hotel') são de 06/07, e não há
    hospedagem nesse dia" (`02:400-403`).
  - Ler diárias da descrição "Permite manipulação: escrever '5 diárias'
    quintuplica o limite" e "Contradiz AMB-10: ali eu recomendei ignorar a
    descrição" (`02:487-490`).
- **Como detectei:** recusei a aprovação em bloco e questionei: "você recomenda
  inferir 'em viagem' a partir de hospedagem, mas a própria entrada não possui um
  campo estruturado indicando viagem" (`02:343-349`). Para ser honesto, não
  disse "está errado". Pedi vantagens, riscos e impacto no JSON, e ele mudou de
  posição: "mudei de recomendação em AMB-06 e AMB-08" (`02:370-371`).
- **O que fiz:**
  - Decidi não aplicar os 50% e contar cada hospedagem como 1 diária
    (`02:551-556`).
  - Isso virou o princípio da RN-014: só campos estruturados decidem cálculo.
  - Registrei os custos dessa escolha na §10 da spec: viagem sem acréscimo e
    e-007 com 400,00 apesar de "3 noites".

### Caso 2 — contagens erradas nos documentos, pegas pelo próprio Claude

- **D-002, primeira versão:** "7 dos 14 itens mudam" e "32 casos novos". O
  certo era 5 e 31; o próprio Claude corrigiu com `sed` (`06:2313-2318` →
  `06:2355-2362`).
- **D-003:** "68 → 71" virou "Recontei: são 2 casos novos … o total é 70"
  (`07:762-767`). Depois voltou a 71, legitimamente, com a AMB-040.
- **D-001:** "13 casos" virou "12 casos" (`03:828`, `03:874-883`).

Padrão: **contagens em texto livre erram com frequência**. Os totais
monetários, ao contrário, são conferidos por teste e pela execução real da CLI.

### Caso 3 — commit incompleto (T-025)

- **O que aconteceu:** o script de commit do Claude gravou a T-025 sem o
  `README.md`. O `git status` mostrava ` M README.md` depois do commit
  (`05:2694-2699`).
- **Diagnóstico dele:** "O commit da T-025 saiu só com o tasks.md (o README
  ficou fora do git add do meu script)" (`05:2713-2715`).
- **Correção:** amend local, sem push, que virou `8bb0338`.

### Caso 4 — o inverso: o Claude pegou um erro meu

- **Meu erro:** ao decidir a AMB-040, escrevi "use … o valor normalizado", mas
  meu exemplo mantinha maiúsculas.
- **O que ele apontou:** pela RN-002, "normalizado" daria `cc-suporte-n2`
  (`07:1237-1245`).
- **Resultado:** confirmei que era só tirar os espaços das pontas. A spec diz
  isso explicitamente: "não é a normalização da RN-002".

### Interpretação que ele fez sozinho e eu confirmei depois

- **O que ele fez:** na T-028, tratou `"centro_custo": null` como erro geral,
  pela leitura literal da RN-016 ("presente que não é texto"), e alterou um
  teste antigo que tratava `null` como informativo.
- **Como avisou:** "Se a intenção era tratar null como ausente, isso é decisão
  de negócio e precisa entrar na spec" (`08:3426-3430`).
- **O que fiz:** confirmei, "mantem centro_custo null como erro geral"
  (`08:3459`).
- **Por que conta:** é uma decisão que entrou no código antes da minha
  confirmação. O texto da spec já sustentava a leitura, mas ela foi feita por
  ele.

## Diligência

- **O que eu fazia de fato:**
  - travava cada etapa ("não altere arquivo", "não faça commit ainda");
  - exigia resumo do que mudou ("me mostra o que mudou", `03:933`);
  - na implementação, exigia teste + lint antes de marcar `[x]` e um commit por
    task.
- **Quanto dos diffs eu li:** li por inteiro cerca de **35%** dos diffs. Nos
  outros, acompanhei pelos resumos do Claude, pelos testes e pelos resultados.
  Essa leitura não aparece nos exports: as sessões 05 e 08 têm uma única
  instrução minha e o resumo final do Claude (`05:6-39`, `08:6-26`). Nos diffs
  que não li inteiros, a verificação dependeu dos testes, do lint, do teste de
  rastreabilidade e da execução real da CLI contra os totais da §9.
- **Aceito sem verificar direito:**
  - O Claude commitou spec, plan, tasks e exemplos do envelope (`f92b75e`,
    `e1f79c3`, `e2a2a45`, `cc21a10`) sem eu pedir, antes da T-026 (`08:3419-3424`).
    Também ampliou o README além da T-038 e escreveu sozinho o texto da
    justificativa de `COTACAO_INDISPONIVEL`, que a spec só obriga a citar moeda e
    data (`08:3436-3448`).
  - Ele declarou tudo isso no resumo e eu aceitei.
- **Testes do mesmo agente que escreveu o código:** é o risco principal. O que
  reduz esse risco:
  - os valores esperados vêm da spec (tabelas da §9 e casos da §7), escritos e
    revisados antes do código;
  - o teste de rastreabilidade foi conferido por mutação: removido
    `test_rn018_cambio.py`, ele falha (`08:3384-3386`);
  - o Claude corrigiu testes mal escritos: `json.dumps(default=str)` serializava
    `Decimal` como texto (`05:658`, `08:3231`), e um nome de teste dizia o
    contrário do que testava (`05:2305`).

## Sessões exportadas

| Arquivo | Conteúdo |
|---|---|
| `01-analise-inicial.md` | Leitura do desafio e da rubrica |
| `02-especificacao.md` | Ambiguidades da v3, decisões, spec 1.0 (as linhas 1–77 repetem a sessão 01) |
| `03-planejamento.md` | Lacunas de validação, D-001/spec 1.1, plan 1.0 |
| `04-implementacao-t001.md` | T-001 |
| `05-implementacao-bloco.md` | T-002 a T-025, 245 testes |
| `06-envelope-spec-v4.md` | Análise de impacto da v4, spec 2.0, D-002 |
| `07-planejamento-envelope-v4.md` | D-003/spec 2.1, plan 2.0, Fase 7 |
| `08-implementacao-envelope-v4.md` | T-026 a T-041, 487 testes |

**Lacunas declaradas:**
- A sessão que gerou T-001 a T-025 (`2d2c1f4`, 12:13) **não foi exportada**.
- A sessão 07 foi salva em `reembolso/docs/sessions/` por ter rodado na
  subpasta, e foi movida em `0f6b03b`.

## Fechamento — aprendizados de SDD

1. **A ambiguidade aparece quando alguém tenta tornar a regra verificável.**
   Das 40 ambiguidades, várias só surgiram em etapas posteriores: no plano
   (AMB-017) e na escrita das tasks (AMB-037 a AMB-040). Escrever o "como"
   força o "o quê".
2. **Regra no chat precisa de uma barreira concreta.** A frase no `CLAUDE.md`
   fez o agente parar e devolver a regra para a spec (`07:875-878`). Sem ela, a
   AMB-040 teria ido direto para as tasks.
3. **Quando decido mal, é por decidir em bloco.** As piores partes da spec 1.0
   foram as que liberei sem decidir. A melhor correção (caso 1) veio de recusar
   a aprovação em bloco.
4. **O envelope custou na proporção do que estava no código e não na spec.** A
   v4 absorveu fácil tudo que já era regra escrita (ordem, distribuição,
   duplicatas). Resistiu onde o plano tinha feito uma aposta (política
   embutida, etapas sem `Contexto`).
5. **Para que tamanho vale:** para este motor, com regras pequenas mas cheias de
   bordas, a spec foi o que permitiu reexecutar 16 tasks em sequência sem eu
   tocar em código. Para um script descartável ou sem regra de negócio, o custo
   de três documentos e de um log de decisões não se pagaria.
6. **O desconfortável:** a verificação da implementação ficou quase toda
   terceirizada para testes escritos pelo mesmo agente: li por inteiro só cerca
   de 35% dos diffs. O que segurou a qualidade foi a spec ter os valores
   esperados antes do código, não a minha leitura de diff.
