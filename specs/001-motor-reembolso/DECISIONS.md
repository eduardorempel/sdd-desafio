# Log de Decisões e Mudanças de Spec

> Uma entrada **toda vez** que a spec mudar. Este arquivo é a prova de que a spec
> foi tratada como artefato vivo e não como cerimônia de abertura.
>
> Spec que não muda em dois dias é spec que ninguém consultou. Mudança não é
> demérito — mudança não registrada é.

Ordem cronológica inversa: a mais recente primeiro.

---

## D-003 — Complemento da D-002: justificativa de herança, grafia do centro de custo e periodicidade · `2026-10-04`

**Gatilho:** ao escrever as tasks da Fase 7 (T-026 a T-041), o Claude apontou
três pontos que a spec 2.0 não decidia e dos quais dependem T-027, T-028, T-032,
T-033 e T-040. Ao ajustar as tasks, apontou um quarto ponto: a grafia do
centro de custo não cadastrado na justificativa. As decisões abaixo são minhas e
completam a v4/D-002.

**O que mudou na spec (2.0 → 2.1):**
- **RN-016:** a justificativa de categoria herdada da padrão cita os dois fatos:
  "centro de custo CC-ADM usando limite herdado da política padrão" (AMB-037).
  Com o centro cadastrado, o código citado é a grafia da chave no documento de
  política: `" cc-comercial "` aparece como `CC-COMERCIAL` (AMB-038). Com o
  centro não cadastrado, sem chave no documento, o código citado é o valor da
  entrada só sem os espaços das pontas, mantendo maiúsculas, minúsculas e
  acentos: `" CC-SUPORTE-N2 "` → `CC-SUPORTE-N2`. Não é a normalização da RN-002
  (AMB-040). A lista de textos de origem ficou explícita para cada caso.
- **RN-002 e RN-015:** `periodicidade` passa pela normalização antes da
  validação; `"Dia"` e `" dia "` são `dia`, e o mesmo vale para `diaria`.
  Depois da normalização, outro valor ou tipo diferente de texto é erro geral
  (AMB-039).
- **Seção 4:** a justificativa de `LIMITE_DIARIO` inclui o caso de limite
  herdado da padrão.
- **Seção 6:** novas AMB-037, AMB-038, AMB-039 e AMB-040.
- **Seção 7:** 3 casos novos (grafia do centro de custo na justificativa,
  grafia da periodicidade, centro de custo desconhecido com espaços nas
  pontas); o caso "Categoria ausente na tabela do centro" passa a conferir a
  justificativa de herança. Total de 68 → 71 casos.

**Por quê:**
- Citar só o centro esconde que o limite veio da padrão; citar só a padrão
  sugere que o centro não foi reconhecido.
- A grafia do documento de política é a canônica, e a mesma entrada com grafias
  diferentes deve gerar a mesma justificativa.
- Diferença de grafia não muda significado (mesmo raciocínio da AMB-013 e da
  AMB-020).
- Sem chave canônica, manter o código como foi digitado (só sem espaços nas
  pontas) ajuda a achar o erro de digitação que levou à política padrão.

**O que isso invalidou:** nada implementado ainda. Os totais da seção 9 não
mudam.

**Tasks afetadas:** T-027 (periodicidade normalizada), T-028 (origem com
herança e grafia canônica), T-032, T-033 e T-040 (texto das justificativas),
T-039 e o cabeçalho da Fase 7 (spec 2.0 → 2.1). `tasks.md` já reflete os três
primeiros pontos. Falta a AMB-040 em T-028, T-032 e T-033, e a T-039 passa de
70 para 71 casos.

**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`), antes de qualquer código.

---

## D-002 — Política v4: política externa por centro de custo, representação e câmbio · `2026-10-04`

**Gatilho:** envelope lacrado do Dia 2 (Política de Reembolso v4), com
`politica-v4.json`, `cambio.json` e dois documentos de despesas de exemplo
(`despesas-envelope.json`, `despesas-envelope-cc-desconhecido.json`). Antes de
mexer na spec, o Claude fez uma análise de impacto e listou 19 ambiguidades
novas (AMB-018 a AMB-036). As decisões foram revisadas e confirmadas por mim
antes da edição.

**O que mudou na spec (1.1 → 2.0):**
- **Entrada:** passam a ser três documentos. Despesas; política, obrigatória
  (RN-015); câmbio, só necessário com moeda estrangeira (RN-018).
  `colaborador.centro_custo` deixa de ser informativo e escolhe a política
  (RN-016). Novo campo opcional `despesas[].moeda` (RN-017).
- **Saída:**
  - `valor_informado` fica na moeda original;
  - novos campos `moeda`, `taxa_cambio` e `data_cotacao`;
  - `valor_considerado` é em reais e fica nulo também em `COTACAO_INDISPONIVEL`;
  - novo motivo `COTACAO_INDISPONIVEL`;
  - as justificativas de limite e de categoria citam o centro de custo ou a
    política padrão;
  - exemplo da seção 4 refeito para `CC-ENG-PLATAFORMA` e novo exemplo em EUR.
- **Regras alteradas:**
  - RN-001: categorias da política aplicável; limite 0 = não reembolsável;
  - RN-002: normalização vale também para o centro de custo e para as chaves do
    documento de política;
  - RN-003: converte primeiro e arredonda uma vez só em reais;
  - RN-006: duplicata exige mesma moeda e mesmo valor original;
  - RN-007: limiar vem do documento e é comparado com o valor convertido;
  - RN-008: limites vêm da política aplicável; `dia` e `diaria` = limite por data;
  - RN-011: percentual de viagem está no documento, mas continua sem ser aplicado;
  - RN-013: novos erros gerais (centro de custo com tipo errado, documento de
    política ou de câmbio inválido) e `moeda` inválida → `DADOS_INVALIDOS`;
  - RN-014: moeda e centro de custo entram na lista de campos estruturados.
- **Regras novas:** RN-015 (documento de política), RN-016 (política aplicável
  por centro de custo: ausente ou desconhecido → padrão; categoria ausente no
  centro → herda da padrão), RN-017 (moeda), RN-018 (conversão pela data da
  despesa, com a última cotação anterior disponível; sem cotação → recusa só
  aquela despesa).
- **Seção 6:** AMB-018 a AMB-036 novas; AMB-005, 006, 008, 010, 012 e 014
  revistas.
- **Seção 7:** casos que dependiam da tabela fixa foram reescritos para o
  centro de custo do exemplo; o caso "`moeda: USD` ignorado" virou `projeto`;
  31 casos novos de centro de custo, moeda, câmbio e documentos.
- **Seção 8:** nova etapa 3, conversão e arredondamento, antes de valor
  negativo. As etapas seguintes foram renumeradas (4 a 9) sem mudar de ordem.
- **Seção 9:** o exemplo original passa a ser avaliado com a v4 (é
  `CC-ENG-PLATAFORMA`): total de **585,43 → 351,43**. Novos critérios para os
  dois documentos do envelope (1.143,26 e 373,76).
- **Seção 3:** sai "não converte moedas" e a lista fixa de categorias; entram
  vigência e aprovação manual (item C) como fora de escopo.

**Por quê:**
- A v4 tira os valores da política do código e os põe em documento externo,
  com limites por centro de custo e uma política padrão.
- A herança por categoria se apoia no limite 0 explícito do
  `CC-ENG-PLATAFORMA`, que seria desnecessário se a ausência já recusasse.
- Converter e arredondar uma vez evita erro de arredondamento duplo, e todas as
  regras passam a usar um único valor em reais.
- O limiar da nota fiscal está na moeda base; compará-lo na moeda original o
  faria variar com o câmbio.
- Falta de cotação é falta de dado de referência, não da despesa; não deve
  impedir o cálculo das outras.
- Viagem continua sem acréscimo: não existe campo estruturado que a indique.
- Item C (aprovação manual) é opcional e ficou fora.

**O que isso invalidou:**
- Critério de aceite da seção 9: 5 dos 14 itens mudam (d-001, d-002, d-010,
  d-013, d-014 e o total). d-013 muda de motivo (`NOTA_FISCAL_AUSENTE` →
  `CATEGORIA_NAO_REEMBOLSAVEL`) porque a etapa de categoria vem antes da de
  nota fiscal.
- Justificativas exatas da seção 4 (passam a citar R$ 75,00 e o centro de custo).
- Código: a política fixa em `politica.py`, a etapa de categoria, a de nota
  fiscal, a de limite, as justificativas, a leitura da entrada (centro de
  custo, moeda), a CLI (novos documentos) e a serialização da saída (campos
  novos).
- Testes: aceite da seção 9, justificativas exatas, casos de borda da seção 7
  (o de `moeda: USD` agora contradiz a spec), testes de RN-001, RN-007, RN-008,
  RN-009, RN-010 e RN-013 que assumem a tabela fixa, e a verificação de
  rastreabilidade (RN-015 a RN-018 ainda não têm arquivo de teste).

**Tasks afetadas:** T-007, T-012, T-014, T-015, T-016, T-018, T-019, T-020,
T-021, T-022, T-024. As tasks novas ainda não foram criadas; entram na Fase 7
de `tasks.md` a partir de T-026.

**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`), antes de qualquer código.

---

## D-001 — Validação de entrada, campos inesperados e valores nulos na saída · `2026-10-04`

**Gatilho:** ao desenhar a validação de entrada para o `plan.md`, o Claude
listou casos que a spec 1.0 não decidia (campo vazio, tipo errado, data em
formato diferente, item da lista que não é objeto, `NaN`, campos desconhecidos).
Também apontou duas contradições: `valor_informado` "exatamente como veio"
conflitava com "todos os valores de saída têm duas casas" (RN-003) no caso de
d-011 (33,333), e `valor_considerado` de uma despesa com `DADOS_INVALIDOS`
recebia respostas diferentes da seção 4 e da seção 8. Sem decisão, o código
resolveria esses casos em silêncio.

**O que mudou na spec (1.0 → 1.1):**
- **RN-013:** antes era uma frase por tipo de erro. Agora há listas explícitas:
  - **erro geral:** documento ilegível, incluindo `NaN`/`Infinity`; `colaborador`
    ou `periodo` que não são objeto; `colaborador.id` ausente, vazio ou que não é
    texto; datas do período fora de `AAAA-MM-DD` ou inexistentes; `despesas` que
    não é lista; item de `despesas` que não é objeto;
  - **`DADOS_INVALIDOS`:** campo obrigatório vazio ou só com espaços; `id`,
    `categoria` ou `fornecedor` que não são texto; data fora de `AAAA-MM-DD` ou
    inexistente;
  - **ignorados:** campos informativos com tipo ou formato errado, e campos
    desconhecidos.
- **Seção 4, saída:**
  - `itens[].id` fica nulo se o `id` for inválido;
  - `valor_informado` passa de "exatamente como veio" para "valor numérico, sem
    preservar grafia", nulo se ausente ou não numérico;
  - `valor_considerado` fica nulo sempre que o motivo for `DADOS_INVALIDOS`
    (antes, "vazio se inválido");
  - `motivo` passa de "texto ou vazio" para "texto ou nulo", nulo quando o
    status for `aprovado`. Na tabela da seção 9, o "—" dos itens aprovados
    virou "nulo".
- **Seção 4, entrada:** nota de que campos informativos e desconhecidos não são
  validados.
- **RN-003:** "todos os valores de saída têm duas casas" passa a valer só para
  `valor_considerado`, `valor_reembolsavel` e `total_reembolsavel`.
- **Seção 6:** nova AMB-017 (entrada malformada e campos inesperados).
- **Seção 7:** 12 casos de borda novos de RN-013.

**Por quê:**
- Uma despesa ruim não deve impedir o cálculo das outras.
- Sem colaborador, período ou lista legível não há o que calcular.
- Item que não é objeto não tem nem `id` para gerar uma linha de saída.
- `NaN`/`Infinity` não são JSON válido.
- Campos que não entram em cálculo não têm motivo para recusar nada.
- Todo campo de saída sem valor usa a mesma representação (nulo), em vez de
  "vazio", que podia ser lido como texto vazio ou campo omitido.

**O que isso invalidou:** nada implementado ainda. O critério de aceite da
seção 9 e o total de 585,43 não mudam: nenhuma despesa do exemplo é afetada.

**Tasks afetadas:** nenhuma; `tasks.md` ainda não foi escrito. As tasks de
validação de entrada e de saída devem cobrir os casos novos da seção 7.

**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`), antes de qualquer código.
