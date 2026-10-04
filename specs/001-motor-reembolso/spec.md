# Spec — Motor de Cálculo de Reembolso

**Versão:** 2.0 · **Status:** rascunho · **Última alteração:** 2026-10-04

> **Regra de ouro deste arquivo:** ele descreve o QUÊ e o PORQUÊ. Nenhuma linha
> aqui pode citar linguagem, biblioteca, classe, função ou estrutura de pasta.
> Se apareceu solução, o lugar dela é o `plan.md`.
>
> **Teste de aceitação da própria spec:** uma pessoa que nunca viu o projeto
> consegue, lendo só este arquivo, verificar se o sistema está correto?

---

## 1. Problema

Hoje o financeiro confere manualmente, item por item, as despesas de cada
colaborador contra a política de reembolso. O processo é lento e produz
resultados inconsistentes, porque a política é ambígua e cada pessoa a
interpreta de um jeito.

## 2. Objetivo

Dado o conjunto de despesas de um colaborador em um período, o sistema calcula
de forma determinística quanto é reembolsável em cada despesa e justifica cada
decisão com base em regras escritas nesta spec.

## 3. Fora de escopo

- Não aplica a ampliação de limites para colaborador em viagem (ver AMB-006, AMB-035).
- Não processa mais de um colaborador ou mais de um período por execução.
- Não verifica a autenticidade da nota fiscal; considera apenas a informação
  "tem nota fiscal" declarada na entrada.
- Não detecta duplicatas entre execuções diferentes nem guarda histórico.
- Não compensa estornos com despesas de outros períodos.
- Não interpreta o texto da descrição para nenhum cálculo ou decisão.
- Não aplica IOF, spread ou tarifa na conversão de moeda; usa só a taxa do
  documento de câmbio (RN-018).
- Não escolhe política por vigência; aplica o documento de política informado,
  qualquer que seja o período (AMB-034).
- Não trata aprovação manual de despesas (item C da política v4, opcional).
- Não aprova nem efetua pagamento; apenas calcula e justifica.
- Não reembolsa categorias que não constam da política aplicável (RN-001).

## 4. Entrada e saída

**Entrada:** três documentos.

- **Despesas:** obrigatório, no formato de `exemplos/despesas-exemplo.json` ou
  `exemplos/envelope/despesas-envelope.json` (campos abaixo).
- **Política:** obrigatório, no formato de `exemplos/envelope/politica-v4.json`
  (RN-015).
- **Câmbio:** no formato de `exemplos/envelope/cambio.json`; só é necessário
  quando houver despesa em moeda estrangeira (RN-018).

Campos do documento de despesas:

| Campo | Tipo | Significado | Obrigatório |
|---|---|---|---|
| `colaborador.id` | texto | Identificador do colaborador | sim |
| `colaborador.nome` | texto | Nome do colaborador (informativo) | não |
| `colaborador.centro_custo` | texto | Centro de custo; escolhe a política aplicável (RN-016) | não |
| `periodo.competencia` | texto `AAAA-MM` | Mês de competência (informativo; ver AMB-009) | não |
| `periodo.inicio` | data `AAAA-MM-DD` | Primeiro dia do período | sim |
| `periodo.fim` | data `AAAA-MM-DD` | Último dia do período | sim |
| `despesas` | lista | Despesas a avaliar; pode ser vazia | sim |
| `despesas[].id` | texto | Identificador da despesa | sim |
| `despesas[].data` | data `AAAA-MM-DD` | Data em que a despesa ocorreu | sim |
| `despesas[].categoria` | texto | Categoria da despesa | sim |
| `despesas[].descricao` | texto | Descrição livre (informativa; nunca usada em cálculo) | não |
| `despesas[].fornecedor` | texto | Nome do fornecedor | sim |
| `despesas[].valor` | número | Valor na moeda da despesa; pode ter mais de duas casas decimais ou ser negativo | sim |
| `despesas[].moeda` | texto | Código da moeda da despesa; `BRL` se ausente (RN-017) | não |
| `despesas[].tem_nota_fiscal` | verdadeiro/falso | Se há nota fiscal | sim |

A **posição** de uma despesa é a sua ordem na lista `despesas`, começando em 1.
Ela é usada como critério de desempate (RN-006 e RN-009).

Campos marcados como informativos e campos que não constam desta tabela não são
validados e nunca participam de cálculo ou decisão (RN-013).

**Saída:** um documento com a seguinte estrutura.

| Campo | Tipo | Significado |
|---|---|---|
| `colaborador` | objeto | Cópia do objeto `colaborador` da entrada |
| `periodo` | objeto | Cópia do objeto `periodo` da entrada |
| `itens` | lista | Um item para cada despesa da entrada, na mesma ordem |
| `itens[].id` | texto ou nulo | `id` da despesa; nulo se ausente, vazio ou com tipo inválido |
| `itens[].valor_informado` | número ou nulo | Valor numérico de `valor` na entrada, na moeda da despesa, sem arredondamento; nulo se ausente ou não numérico. Só o valor importa, não a grafia: `72.5` e `72.50` são o mesmo valor |
| `itens[].moeda` | texto ou nulo | Moeda da despesa após a normalização (RN-017); nulo sempre que o motivo for `DADOS_INVALIDOS` |
| `itens[].taxa_cambio` | número ou nulo | Taxa usada na conversão, como está no documento de câmbio; nulo quando a moeda é `BRL` ou não houve conversão |
| `itens[].data_cotacao` | data ou nulo | Data da taxa usada (RN-018); nulo quando `taxa_cambio` é nulo |
| `itens[].valor_considerado` | número ou nulo | Valor em reais, convertido e arredondado para centavos (RN-003, RN-018); nulo sempre que o motivo for `DADOS_INVALIDOS` ou `COTACAO_INDISPONIVEL` |
| `itens[].valor_reembolsavel` | número | Valor a reembolsar, em reais, com duas casas decimais |
| `itens[].status` | texto | `aprovado`, `limitado` ou `recusado` (definições abaixo) |
| `itens[].motivo` | texto ou nulo | Código do motivo (tabela abaixo); nulo quando `aprovado` |
| `itens[].justificativa` | texto | Explicação legível da decisão, citando a regra (RN-xxx) |
| `total_reembolsavel` | número | Soma de `valor_reembolsavel` de todos os itens, em reais |

**Status:**

- `aprovado`: a despesa passou por todas as regras e `valor_reembolsavel` é
  igual a `valor_considerado`.
- `limitado`: a despesa passou por todas as validações, mas o limite diário
  reduziu `valor_reembolsavel`, possivelmente a zero.
- `recusado`: a despesa foi recusada em uma validação e `valor_reembolsavel` é 0,00.

**Motivos:**

| Código | Status | Regra |
|---|---|---|
| `DADOS_INVALIDOS` | recusado | RN-013, RN-017 |
| `COTACAO_INDISPONIVEL` | recusado | RN-018 |
| `VALOR_NEGATIVO` | recusado | RN-005 |
| `FORA_DO_PERIODO` | recusado | RN-004 |
| `CATEGORIA_NAO_REEMBOLSAVEL` | recusado | RN-001, RN-016 |
| `DUPLICATA` | recusado | RN-006 |
| `NOTA_FISCAL_AUSENTE` | recusado | RN-007 |
| `LIMITE_DIARIO` | limitado | RN-008, RN-009, RN-010 |

A justificativa deve citar:

- no caso de `DUPLICATA`, o `id` da despesa mantida;
- no caso de `LIMITE_DIARIO`, o limite, o valor já consumido no dia e a
  política de onde o limite veio (centro de custo ou política padrão, RN-016);
- no caso de `CATEGORIA_NAO_REEMBOLSAVEL`, a política aplicada;
- no caso de `COTACAO_INDISPONIVEL`, a moeda e a data da despesa.

**Exemplo 1** (`exemplos/despesas-exemplo.json`, centro de custo
`CC-ENG-PLATAFORMA`, período de 2026-07-01 a 2026-07-31):

Entrada (trecho):

```
{ "id": "d-001", "data": "2026-07-03", "categoria": "alimentacao", "fornecedor": "Restaurante Tavola", "valor": 72.50, "tem_nota_fiscal": true }
{ "id": "d-002", "data": "2026-07-03", "categoria": "alimentacao", "fornecedor": "Cantina do Porto",   "valor": 38.00, "tem_nota_fiscal": true }
{ "id": "d-004", "data": "2026-07-06", "categoria": "transporte_urbano", "fornecedor": "TaxiApp",     "valor": 100.01, "tem_nota_fiscal": false }
```

Saída (trecho):

```
"itens": [
  { "id": "d-001", "valor_informado": 72.50, "moeda": "BRL", "taxa_cambio": null, "data_cotacao": null,
    "valor_considerado": 72.50, "valor_reembolsavel": 72.50,
    "status": "aprovado", "motivo": null,
    "justificativa": "Despesa aprovada: passou por todas as regras e é reembolsada integralmente (RN-001, RN-004 a RN-008)." },
  { "id": "d-002", "valor_informado": 38.00, "moeda": "BRL", "taxa_cambio": null, "data_cotacao": null,
    "valor_considerado": 38.00, "valor_reembolsavel": 2.50,
    "status": "limitado", "motivo": "LIMITE_DIARIO",
    "justificativa": "Limite diário de alimentação de R$ 75,00 (centro de custo CC-ENG-PLATAFORMA), com R$ 72,50 já consumido por d-001 em 2026-07-03; excedente de R$ 35,50 cortado (RN-008, RN-009, RN-010)." },
  { "id": "d-004", "valor_informado": 100.01, "moeda": "BRL", "taxa_cambio": null, "data_cotacao": null,
    "valor_considerado": 100.01, "valor_reembolsavel": 0.00,
    "status": "recusado", "motivo": "NOTA_FISCAL_AUSENTE",
    "justificativa": "Valor acima de R$ 100,00 sem nota fiscal (RN-007)." }
],
"total_reembolsavel": 75.00
```

**Exemplo 2** (`exemplos/envelope/despesas-envelope.json`, centro de custo
`CC-COMERCIAL`, despesa em euro):

Entrada (trecho):

```
{ "id": "e-002", "data": "2026-07-14", "categoria": "alimentacao", "fornecedor": "Taberna do Chiado", "valor": 22.00, "moeda": "EUR", "tem_nota_fiscal": true }
```

Saída (trecho):

```
{ "id": "e-002", "valor_informado": 22.00, "moeda": "EUR", "taxa_cambio": 5.93, "data_cotacao": "2026-07-14",
  "valor_considerado": 130.46, "valor_reembolsavel": 90.00,
  "status": "limitado", "motivo": "LIMITE_DIARIO",
  "justificativa": "Limite diário de alimentação de R$ 90,00 (centro de custo CC-COMERCIAL) aplicado; excedente de R$ 40,46 cortado (RN-008, RN-010)." }
```

## 5. Regras de negócio

### RN-001 — Categorias reembolsáveis

**Regra:** Uma categoria é reembolsável quando consta da política aplicável
(RN-016) com limite maior que zero, comparada depois da normalização (RN-002).
É recusada com `CATEGORIA_NAO_REEMBOLSAVEL` a despesa cuja categoria:

- não consta nem da tabela do centro de custo nem da política padrão; ou
- consta com limite 0,00. Limite zero significa "não reembolsável naquele centro
  de custo". O texto de `observacao` do documento de política não é usado.

Categorias não são encaixadas por semelhança.
**Origem:** política do RH, item 9; política v4 (AMB-014, AMB-021, AMB-022, AMB-023)
**Aceite:** d-005 (`coworking`, 89,00) → recusado, 0,00, `CATEGORIA_NAO_REEMBOLSAVEL`.
d-010 e d-013 (hospedagem, `CC-ENG-PLATAFORMA`, limite 0,00) → recusados,
`CATEGORIA_NAO_REEMBOLSAVEL`. f-003 (`representacao`, política padrão) →
recusado. e-001 (`representacao`, `CC-COMERCIAL`) → reembolsável.

### RN-002 — Normalização de texto

**Regra:** Antes de qualquer comparação, categoria, fornecedor e centro de custo
são normalizados: espaços no início e no fim são removidos, letras maiúsculas
viram minúsculas e acentos são removidos. A normalização não altera mais nada;
espaços internos e outros caracteres são mantidos. As chaves de categoria e de
centro de custo do documento de política passam pela mesma normalização.
**Origem:** decisão desta spec (AMB-013, AMB-020)
**Aceite:** categoria `ALIMENTACAO`, ` Alimentação ` e `alimentacao` são tratadas
como `alimentacao`. Fornecedores `Bistro Central` e `bistro central` são iguais.
Centro de custo ` cc-comercial ` é o mesmo que `CC-COMERCIAL`.

### RN-003 — Arredondamento

**Regra:** O valor de cada despesa é convertido para reais (RN-018) e só então
arredondado para centavos, **uma única vez**, com arredondamento comercial: a
metade se afasta do zero (0,005 vira 0,01). O valor informado e a taxa não são
arredondados antes da multiplicação. Em `BRL`, a conversão não altera o valor.
Todas as regras seguintes usam o valor resultante (`valor_considerado`). Na
saída, `valor_considerado`, `valor_reembolsavel` e `total_reembolsavel` têm duas
casas decimais; `valor_informado` e `taxa_cambio` não são arredondados.
**Origem:** decisão desta spec (AMB-012, AMB-027)
**Aceite:** d-011 (33,333) → `valor_considerado` 33,33. Valor 10,005 → 10,01.
Valor −0,004 → 0,00, tratado como valor zero (RN-005). 33,333 USD em 2026-07-13
(taxa 5,42) → 180,66486 → 180,66 (e não 180,65, que sairia de 33,33 × 5,42).

### RN-004 — Período de competência

**Regra:** A despesa é aceita se sua `data` estiver entre `periodo.inicio` e
`periodo.fim`, com as duas datas incluídas. Caso contrário, é recusada com
`FORA_DO_PERIODO`. O campo `periodo.competencia` é informativo e não é usado
nessa verificação.
**Origem:** política do RH, item 7 (AMB-009)
**Aceite:** d-008 (2026-04-15, período de julho) → recusado, `FORA_DO_PERIODO`.
d-014 (2026-07-31, último dia) → aceito por esta regra.

### RN-005 — Valores negativos e zero

**Regra:** Despesa com `valor_considerado` menor que zero é recusada com
`VALOR_NEGATIVO` e não abate o valor de nenhuma outra despesa. Despesa com
`valor_considerado` igual a zero é válida e reembolsa 0,00 com status `aprovado`.
**Origem:** decisão desta spec (AMB-011)
**Aceite:** d-009 (−45,00) → recusado, 0,00, `VALOR_NEGATIVO`; o reembolso das
demais despesas de transporte urbano não muda. Despesa de 0,00 → aprovado, 0,00.

### RN-006 — Duplicatas

**Regra:** Duas ou mais despesas são duplicatas quando têm a mesma `data`, a
mesma categoria normalizada, o mesmo fornecedor normalizado, a mesma moeda
(RN-017) e o mesmo valor informado arredondado para centavos na moeda original
(com o arredondamento da RN-003). Em `BRL`, esse valor é o próprio
`valor_considerado`. Só despesas que passaram por RN-001, RN-004, RN-005,
RN-013 e RN-018 participam dessa comparação. Em cada grupo de duplicatas, uma
despesa é mantida:

1. se houver despesas com nota fiscal no grupo, fica a de menor posição entre elas;
2. se nenhuma tiver nota fiscal, fica a de menor posição.

As demais são recusadas com `DUPLICATA`, e a justificativa cita o `id` da mantida.
`id` e `descricao` não participam da comparação.
**Origem:** política do RH, item 8 (AMB-010, AMB-030)
**Aceite:** d-006 e d-007 (2026-07-09, alimentação, Bistro Central, 54,90, ambas
com nota) → d-006 mantida; d-007 recusada, `DUPLICATA`, citando d-006. Grupo em
que só a segunda despesa tem nota → a segunda é mantida e a primeira é recusada.
Duas despesas de 22,00 EUR com a mesma data, categoria e fornecedor → duplicatas.
22,00 EUR e 130,46 BRL com a mesma data, categoria e fornecedor → não são
duplicatas.

### RN-007 — Nota fiscal

**Regra:** Despesa com `valor_considerado` (em reais, depois da conversão)
estritamente maior que o limiar `nota_fiscal_obrigatoria_acima_de` do documento
de política (100,00 na v4) e sem nota fiscal é recusada inteira com
`NOTA_FISCAL_AUSENTE`. A verificação usa o valor da própria despesa, e não a
soma do dia nem o valor após o limite. Despesa de valor exatamente igual ao
limiar não exige nota.
**Origem:** política do RH, item 5; política v4 (AMB-004, AMB-005, AMB-028)
**Aceite:** d-003 (100,00, sem nota) → não exige nota. d-004 (100,01, sem nota)
→ recusado, 0,00, `NOTA_FISCAL_AUSENTE`. e-005 (40,00 USD × 5,50 = 220,00, sem
nota) → recusado, `NOTA_FISCAL_AUSENTE`. e-003 (14,50 EUR × 5,88 = 85,26, sem
nota) → não exige nota.

### RN-008 — Limites diários por categoria

**Regra:** Para cada combinação de data e categoria, a soma reembolsada não
ultrapassa o limite da categoria na política aplicável (RN-016). As
periodicidades `dia` e `diaria` do documento de política significam, as duas,
limite por data.

Cada despesa de hospedagem vale uma diária, qualquer que seja o texto da
descrição. Como o limite é por data, várias despesas da mesma categoria na
mesma data dividem o mesmo limite. Só despesas que passaram por todas as regras
anteriores consomem o limite.

Para conferência, a política v4 (`exemplos/envelope/politica-v4.json`) resulta
nos limites por data abaixo. Se o documento de política mudar, valem os valores
do documento.

| Categoria | Padrão | `CC-ENG-PLATAFORMA` | `CC-COMERCIAL` | `CC-ADM` |
|---|---|---|---|---|
| `alimentacao` | R$ 60,00 | R$ 75,00 | R$ 90,00 | R$ 45,00 |
| `transporte_urbano` | R$ 80,00 | R$ 80,00 | R$ 150,00 | R$ 60,00 |
| `hospedagem` | R$ 250,00 | não reembolsável (0,00) | R$ 400,00 | R$ 250,00 (herdado da padrão) |
| `representacao` | não consta | não consta | R$ 300,00 | não consta |

"Não consta" e "não reembolsável" levam à recusa pela RN-001.
**Origem:** política do RH, itens 1, 2 e 3; política v4 (AMB-001, AMB-008, AMB-023, AMB-036)
**Aceite:** e-007 (hospedagem, `CC-COMERCIAL`, 1.200,00, descrição "3 noites")
→ 400,00, `limitado`. d-001 + d-002 (alimentação, `CC-ENG-PLATAFORMA`,
2026-07-03, 110,50 no total) → soma reembolsada 75,00. e-001 (representação,
`CC-COMERCIAL`, 340,00) → 300,00, `limitado`.

### RN-009 — Distribuição do limite entre despesas da mesma data

**Regra:** Quando várias despesas da mesma categoria e data disputam o limite,
ele é consumido na ordem da posição: cada despesa recebe o menor valor entre o
seu `valor_considerado` e o saldo do limite que restou das anteriores.
**Origem:** decisão desta spec (AMB-002)
**Aceite:** d-001 (posição 1, 72,50) → 72,50; d-002 (posição 2, 38,00) → 2,50,
`limitado`, justificativa citando d-001.

### RN-010 — Reembolso parcial

**Regra:** Despesa que ultrapassa o saldo do limite é reembolsada até o saldo; o
excedente é cortado. A despesa não é recusada por ultrapassar o limite.
**Origem:** política do RH, item 4 (AMB-003)
**Aceite:** e-008 (alimentação, `CC-COMERCIAL`, 95,00) → 90,00, `limitado`,
`LIMITE_DIARIO`.

### RN-011 — Ampliação para colaborador em viagem

**Regra:** A ampliação dos limites prevista pela política
(`acrescimo_em_viagem_percentual`, 50% na v4) **não é aplicada**. A entrada não
traz nenhuma informação estruturada que indique viagem; moeda estrangeira e
descrição não são tratadas como indício de viagem.
**Origem:** política do RH, item 6; política v4 (AMB-006, AMB-007, AMB-035)
**Aceite:** d-003 ("Corrida aeroporto", 100,00) → limite de 80,00 aplicado,
reembolso 80,00. e-002 ("Almoco - Lisboa", EUR) → limite de 90,00 do
`CC-COMERCIAL`, sem acréscimo. Nenhuma despesa recebe limite acima do da
política aplicável.

### RN-012 — Dias do calendário

**Regra:** Todas as datas do calendário são tratadas da mesma forma; não há
distinção entre dias úteis, fins de semana e feriados. A falta de cotação em
fins de semana e feriados é tratada pela RN-018, sem calendário de feriados.
**Origem:** decisão desta spec (AMB-015)
**Aceite:** d-012 (sábado, 2026-07-18, alimentação, 47,20) → aprovado, 47,20.

### RN-013 — Dados inválidos

**Regra:**

Um campo de texto é considerado **vazio** quando não tem nenhum caractere ou só
tem espaços. Uma data é **válida** quando está exatamente no formato
`AAAA-MM-DD` e existe no calendário (2026-02-30 não é válida).

- **Erro geral:** o sistema encerra com mensagem de erro e não gera saída quando:
  - o documento de despesas não pode ser lido, o que inclui documento que não
    segue o formato JSON, como `NaN` ou `Infinity` em qualquer campo;
  - `colaborador` ou `periodo` estão ausentes ou não são objeto;
  - `colaborador.id` está ausente, vazio ou não é texto;
  - `colaborador.centro_custo` está presente e não é texto (RN-016);
  - `periodo.inicio` ou `periodo.fim` estão ausentes ou não são data válida;
  - `periodo.inicio` é posterior a `periodo.fim`;
  - `despesas` está ausente ou não é lista;
  - algum item de `despesas` não é objeto;
  - o documento de política está ausente ou é inválido (RN-015);
  - o documento de câmbio foi informado e é inválido (RN-018).
- **Erro em uma despesa:** apenas essa despesa é recusada com `DADOS_INVALIDOS`,
  e as demais são processadas normalmente, quando:
  - falta um campo obrigatório da despesa, ou um campo obrigatório de texto
    está vazio;
  - `id`, `categoria` ou `fornecedor` não são texto;
  - `data` não é data válida;
  - `valor` não é numérico;
  - `tem_nota_fiscal` não é verdadeiro/falso;
  - `moeda` está presente e é vazia ou não é texto (RN-017).

  Na saída, a despesa recusada por `DADOS_INVALIDOS` tem `valor_considerado` e
  `moeda` nulos, e também `id` nulo quando o problema está no `id`.
- **Campos informativos e desconhecidos:** `colaborador.nome`,
  `periodo.competencia` e `despesas[].descricao`, além de qualquer campo que não
  conste da tabela de entrada, não são validados e nunca participam de cálculo
  ou decisão. Tipo ou formato errado nesses campos não gera erro.

**Origem:** decisão desta spec (AMB-017, AMB-018, AMB-024, AMB-031, AMB-032)
**Aceite:** despesa sem `tem_nota_fiscal` → recusado, `DADOS_INVALIDOS`, e as
outras despesas do documento aparecem na saída normalmente. Documento sem
`periodo.fim` → erro, sem arquivo de saída. Despesa com `fornecedor` igual a
`"   "` → recusado, `DADOS_INVALIDOS`. Despesa com `id` numérico → recusado,
`DADOS_INVALIDOS`, `itens[].id` nulo. `periodo.inicio` igual a `2026-02-30` →
erro, sem arquivo de saída. Despesa com `"projeto": "X"` → campo ignorado.

### RN-014 — Descrição é informativa

**Regra:** O campo `descricao` nunca altera nenhum cálculo ou decisão. Só campos
estruturados (data, categoria, fornecedor, valor, moeda, nota fiscal, período,
centro de custo e posição) e os documentos de política e de câmbio determinam o
resultado.
**Origem:** decisão desta spec (AMB-006, AMB-008, AMB-010)
**Aceite:** trocar a descrição de qualquer despesa dos exemplos não altera nenhum
`valor_reembolsavel`, `status` ou `motivo`.

### RN-015 — Documento de política

**Regra:** Os valores da política vêm de um documento de política, obrigatório
em toda execução, no formato de `exemplos/envelope/politica-v4.json`:

| Campo | Tipo | Significado | Obrigatório |
|---|---|---|---|
| `moeda_base` | texto | Moeda dos limites e do limiar da nota fiscal; deve ser `BRL` após a normalização da RN-017 | sim |
| `padrao` | objeto | Tabela de categorias da política padrão | sim |
| `centros_custo` | objeto | Uma tabela de categorias por centro de custo; pode ser vazio | sim |
| `nota_fiscal_obrigatoria_acima_de` | número ≥ 0 | Limiar da RN-007 | sim |
| `<tabela>.<categoria>` | objeto | Entrada de uma categoria em uma tabela | — |
| `<tabela>.<categoria>.limite` | número ≥ 0 | Limite por data (RN-008); 0 significa não reembolsável (RN-001) | sim |
| `<tabela>.<categoria>.periodicidade` | `dia` ou `diaria` | Ambos significam limite por data (RN-008) | sim |

`versao`, `vigencia`, `acrescimo_em_viagem_percentual`, `observacao` e campos
não listados são informativos e não são validados.

O sistema encerra com erro geral, sem saída (RN-013), quando o documento de
política:

- está ausente ou não pode ser lido, o que inclui `NaN` ou `Infinity`;
- não tem algum campo obrigatório, ou tem campo obrigatório de tipo errado;
- tem `moeda_base` diferente de `BRL`;
- tem limite negativo, ou limite ou limiar que não é número;
- tem periodicidade diferente de `dia` e `diaria`;
- tem, depois da normalização da RN-002, duas categorias iguais na mesma tabela
  ou dois centros de custo iguais.

**Origem:** política v4 (AMB-031, AMB-036)
**Aceite:** `politica-v4.json` → aceito. Execução sem documento de política →
erro, sem saída. Limite `-1` → erro. `"periodicidade": "mes"` → erro. Documento
sem `padrao` → erro. `"acrescimo_em_viagem_percentual": "x"` → ignorado.

### RN-016 — Política aplicável por centro de custo

**Regra:** A política aplicável a todas as despesas do documento é escolhida
pelo `colaborador.centro_custo`, comparado após a normalização da RN-002:

1. centro de custo ausente ou vazio → política padrão;
2. centro de custo cadastrado no documento de política → tabela desse centro;
   para uma categoria que não consta da tabela do centro, vale a entrada da
   política padrão (herança por categoria);
3. centro de custo informado e não cadastrado → política padrão;
4. centro de custo presente que não é texto → erro geral (RN-013).

As justificativas de `LIMITE_DIARIO` e `CATEGORIA_NAO_REEMBOLSAVEL` citam a
política usada: "centro de custo `<código>`", "política padrão" ou, no caso 3,
"política padrão; centro de custo `<código>` não cadastrado".
**Origem:** política v4 (AMB-018, AMB-019, AMB-020, AMB-021)
**Aceite:** `exemplos/despesas-exemplo.json` (`CC-ENG-PLATAFORMA`) → limite de
alimentação de 75,00. `despesas-envelope-cc-desconhecido.json` (`CC-SUPORTE-N2`)
→ política padrão; f-002 (hospedagem, 310,00) → 250,00. Documento sem
`centro_custo` → política padrão. `CC-ADM` com hospedagem de 300,00 → limite
250,00 herdado da padrão; 250,00, `limitado`. `"centro_custo": 42` → erro, sem
saída.

### RN-017 — Moeda da despesa

**Regra:** O campo `moeda` é opcional. Ausente, a moeda é `BRL`. Presente, deve
ser texto não vazio, e é normalizado removendo espaços no início e no fim e
convertendo letras para maiúsculas. Presente e vazio, ou presente e de outro
tipo, a despesa é recusada com `DADOS_INVALIDOS`. Qualquer código não vazio é
aceito; um código sem cotação é tratado pela RN-018.
**Origem:** política v4 (AMB-024)
**Aceite:** e-010 (sem `moeda`) → `BRL`; 88,00, aprovado. `" usd "` → `USD`.
`""` → recusado, `DADOS_INVALIDOS`. `840` → recusado, `DADOS_INVALIDOS`.

### RN-018 — Conversão cambial pela data da despesa

**Regra:**

- Despesa em `BRL` não é convertida e não consulta o documento de câmbio.
- Despesa em outra moeda é convertida para reais multiplicando o valor
  informado pela taxa dessa moeda na `data` da despesa, segundo o documento de
  câmbio. Se não houver taxa dessa moeda nessa data (fim de semana, feriado ou
  lacuna do documento), usa-se a taxa da data anterior mais próxima que tenha
  essa moeda. O produto é arredondado uma única vez (RN-003).
- Se não houver taxa dessa moeda nem na data da despesa nem antes dela, ou se o
  documento de câmbio não foi informado, apenas essa despesa é recusada com
  `COTACAO_INDISPONIVEL`, e as demais são processadas normalmente.

O documento de câmbio só é necessário quando houver despesa em moeda
estrangeira; quando informado, ele é sempre validado. Formato de
`exemplos/envelope/cambio.json`:

| Campo | Tipo | Significado | Obrigatório |
|---|---|---|---|
| `moeda_base` | texto | Moeda para a qual as taxas convertem; deve ser igual à `moeda_base` da política | sim |
| `taxas` | objeto | Para cada data `AAAA-MM-DD`, um objeto de código de moeda → taxa | sim |
| `taxas.<data>.<moeda>` | número > 0 | Quantos reais vale uma unidade da moeda nessa data | — |

Os códigos de moeda passam pela normalização da RN-017. `fonte`, `observacao` e
campos não listados são informativos.

O sistema encerra com erro geral, sem saída (RN-013), quando o documento de
câmbio informado:

- não pode ser lido, o que inclui `NaN` ou `Infinity`;
- não tem `moeda_base` ou `taxas`, ou eles têm tipo errado;
- tem `moeda_base` diferente da `moeda_base` da política;
- tem chave de `taxas` que não é data válida;
- tem taxa que não é número ou que é menor ou igual a zero;
- tem, na mesma data, dois códigos de moeda iguais depois da normalização.

**Origem:** política v4 (AMB-025, AMB-026, AMB-029, AMB-032)
**Aceite:** e-002 (22,00 EUR, 2026-07-14, taxa 5,93) → 130,46. e-004 (30,00 EUR,
sábado 2026-07-18) → taxa de 2026-07-17 (5,96) → 178,80. e-006 (55,00 GBP) →
recusado, `COTACAO_INDISPONIVEL`, `valor_considerado` nulo. Despesa em USD em
2026-07-10, antes da primeira data do documento → recusado,
`COTACAO_INDISPONIVEL`. Despesa em USD sem documento de câmbio → recusado,
`COTACAO_INDISPONIVEL`; despesas em BRL do mesmo documento processadas
normalmente. Documento de câmbio com taxa 0 → erro, sem saída.

---

## 6. Ambiguidades identificadas e decisões

### AMB-001 — Unidade do limite diário

**Texto original do RH:** "Alimentação tem limite de R$ 60 por dia."
**O que não está claro:** se o limite vale para a soma das despesas do dia ou
para cada despesa separadamente.
**Decisão:** o limite vale para a soma das despesas da mesma categoria na mesma
data, para todas as categorias.
**Justificativa:** o texto diz "por dia", e limitar por despesa permitiria
contornar o limite dividindo a conta.
**Regra afetada:** RN-008

### AMB-002 — Distribuição do limite entre despesas do mesmo dia

**Texto original do RH:** "Alimentação tem limite de R$ 60 por dia." (itens 1–3)
**O que não está claro:** quando a soma do dia ultrapassa o limite, quanto cabe a
cada despesa. Pode ser pela ordem, proporcional ou do maior valor para o menor.
**Decisão:** pela posição na entrada; a primeira consome o limite primeiro.
**Justificativa:** é determinístico e verificável à mão, e a justificativa de
cada item fica simples de explicar.
**Regra afetada:** RN-009

### AMB-003 — Significado de "reembolsadas parcialmente"

**Texto original do RH:** "Despesas acima do limite são reembolsadas parcialmente."
**O que não está claro:** se paga até o limite e corta o excedente, ou se recusa
a despesa inteira.
**Decisão:** paga até o limite e corta o excedente.
**Justificativa:** "parcialmente" só faz sentido se alguma parte for paga.
**Regra afetada:** RN-010

### AMB-004 — Fronteira de "acima de R$ 100"

**Texto original do RH:** "Nota fiscal é obrigatória acima de R$ 100."
**O que não está claro:** se uma despesa de exatamente R$ 100,00 exige nota.
**Decisão:** exige nota só quando o valor é estritamente maior que 100,00.
**Justificativa:** é a leitura literal de "acima de".
**Regra afetada:** RN-007

### AMB-005 — Base e consequência da exigência de nota fiscal

**Texto original do RH:** "Nota fiscal é obrigatória acima de R$ 100."
**O que não está claro:** se o valor comparado é o da despesa, o total do dia ou
o valor após o limite; e se a falta da nota recusa a despesa inteira ou paga até
R$ 100,00.
**Decisão:** compara o valor da própria despesa, já arredondado; sem nota, a
despesa é recusada inteira. Na v4, o valor comparado é o convertido para reais
(AMB-028).
**Justificativa:** a nota comprova o gasto efetivamente feito, e "obrigatória"
indica que sem ela a despesa não é aceita.
**Regra afetada:** RN-007

### AMB-006 — O que caracteriza "em viagem"

**Texto original do RH:** "Colaborador em viagem tem limites ampliados em 50%."
**O que não está claro:** a entrada não tem campo que indique viagem. Seria
preciso inferir pela hospedagem, pela descrição, ou não aplicar.
**Decisão:** a ampliação não é aplicada. Mantida na v4 (AMB-035).
**Justificativa:** inferir viagem falha em casos evidentes (d-003, "Corrida
aeroporto", sem hospedagem no dia) e cria brechas; sem dado, não há como verificar.
**Regra afetada:** RN-011

### AMB-007 — Categorias alcançadas pela ampliação

**Texto original do RH:** "Colaborador em viagem tem limites ampliados em 50%."
**O que não está claro:** se a ampliação vale para todas as categorias ou só para
alimentação e transporte.
**Decisão:** não se aplica enquanto valer a AMB-006; deve ser decidida se um dado
de viagem passar a existir.
**Justificativa:** sem ampliação, a pergunta não tem efeito; registrar evita uma
lacuna silenciosa.
**Regra afetada:** RN-011

### AMB-008 — Número de diárias de uma hospedagem

**Texto original do RH:** "Hospedagem tem limite de R$ 250 por diária."
**O que não está claro:** a entrada não tem número de diárias; a informação só
aparece no texto livre (d-010, "2 diarias"; d-013, "3 noites"; e-007, "3 noites").
**Decisão:** cada despesa de hospedagem vale uma diária; a descrição não é usada.
Mantida na v4: a periodicidade `diaria` é tratada como limite por data (AMB-036).
**Justificativa:** texto livre não tem formato garantido e pode ser manipulado;
estadias de várias noites devem ser lançadas com uma despesa por diária.
**Regra afetada:** RN-008, RN-014

### AMB-009 — Significado de "dentro do período de competência"

**Texto original do RH:** "Despesas devem ser lançadas dentro do período de competência."
**O que não está claro:** a entrada não tem data de lançamento, só a data da
despesa; não se sabe se as bordas do período contam nem qual campo prevalece se
`competencia` e `inicio`/`fim` discordarem.
**Decisão:** a data da despesa deve estar entre `inicio` e `fim`, com as bordas
incluídas; `competencia` é apenas informativa.
**Justificativa:** não há data de lançamento, e qualquer tolerância para
despesas atrasadas seria inventada.
**Regra afetada:** RN-004

### AMB-010 — Definição e tratamento de duplicatas

**Texto original do RH:** "Duplicatas devem ser tratadas."
**O que não está claro:** quais campos definem uma duplicata e o que fazer com
ela: recusar todas, manter uma ou apenas sinalizar.
**Decisão:** mesma data, categoria, fornecedor e valor, comparados após
normalização; mantém a que tem nota fiscal e, em empate, a de menor posição; as
demais são recusadas. Na v4, também a mesma moeda, e o valor é o original
(AMB-030).
**Justificativa:** recusar todas puniria a despesa legítima, e preferir a com nota
evita que uma duplicata anule um comprovante válido.
**Regra afetada:** RN-006

### AMB-011 — Valores negativos e zero

**Texto original do RH:** a política não menciona o caso.
**O que não está claro:** um estorno (d-009, −45,00) pode ser ignorado, abatido
de outras despesas ou tratado como erro; a política também não fala de valor zero.
**Decisão:** valor negativo é recusado sem abater nada; valor zero é válido e
reembolsa 0,00.
**Justificativa:** a despesa original do estorno não está no período, então não
há o que compensar.
**Regra afetada:** RN-005

### AMB-012 — Arredondamento

**Texto original do RH:** a política não menciona o caso.
**O que não está claro:** como tratar valores com mais de duas casas decimais
(d-011, 33,333) e quando arredondar.
**Decisão:** arredonda para centavos, com a metade se afastando do zero, antes
de qualquer regra. Na v4, o arredondamento acontece depois da conversão para
reais, uma única vez (AMB-027).
**Justificativa:** dinheiro é pago em centavos, e arredondar antes evita efeitos
de casas fracionárias nas comparações de fronteira.
**Regra afetada:** RN-003

### AMB-013 — Grafia de categoria e fornecedor

**Texto original do RH:** a política não menciona o caso.
**O que não está claro:** se `ALIMENTACAO` (d-014) é a mesma categoria que
`alimentacao`, e se fornecedores com grafias diferentes são o mesmo.
**Decisão:** ignora maiúsculas, acentos e espaços nas pontas, para categoria e
fornecedor.
**Justificativa:** diferença de grafia é erro de digitação, não uma categoria ou
fornecedor diferente.
**Regra afetada:** RN-002

### AMB-014 — Categorias "fora da política"

**Texto original do RH:** "Categorias fora da política não são reembolsáveis."
**O que não está claro:** se a lista de categorias é fechada nas três citadas ou
se categorias parecidas (d-005, coworking) podem ser encaixadas.
**Decisão (revista na v4):** a lista continua fechada, mas passa a ser a das
categorias com limite maior que zero na política aplicável (RN-016), e não mais
uma lista fixa de três. Encaixar por semelhança continua proibido.
**Justificativa:** a política v4 lista as categorias por centro de custo
(incluindo `representacao`); encaixar por semelhança seria criar política.
**Regra afetada:** RN-001

### AMB-015 — Fins de semana e feriados

**Texto original do RH:** "R$ 60 por dia" (itens 1–3)
**O que não está claro:** se "dia" é qualquer dia do calendário ou só dia útil
(d-012, sábado, "plantão").
**Decisão:** qualquer dia do calendário, sem restrição.
**Justificativa:** a política não restringe, e plantão é trabalho legítimo.
**Regra afetada:** RN-012

### AMB-016 — Ordem de aplicação das regras

**Texto original do RH:** a política não define ordem.
**O que não está claro:** quando várias regras incidem na mesma despesa, a ordem
muda o resultado (por exemplo, d-006/d-007 e d-004).
**Decisão:** ver seção 8.
**Justificativa:** uma despesa recusada não deve ocupar o limite de uma despesa
válida.
**Regra afetada:** todas

### AMB-017 — Entrada malformada e campos inesperados

**Texto original do RH:** a política não menciona o caso.
**O que não está claro:** o que fazer com campo vazio ou de tipo errado, data
fora do formato, valor que não é número, item da lista que não é despesa, campo
informativo malformado e campo que a entrada não prevê; e quais desses casos
invalidam o documento inteiro ou só uma despesa.
**Decisão:** problemas na identificação do colaborador, no período, na lista de
despesas ou no formato do documento invalidam o documento inteiro; problemas em
campos obrigatórios de uma despesa recusam só essa despesa; campos informativos
e desconhecidos são ignorados. Detalhes na RN-013.
**Justificativa:** sem colaborador, período ou lista não há o que calcular; uma
despesa ruim não deve impedir o cálculo das outras; e campos que não entram em
cálculo não têm motivo para recusar nada.
**Regra afetada:** RN-013

### AMB-018 — Centro de custo ausente, vazio ou de tipo errado

**Texto original da política v4:** `politica-v4.json` tem uma tabela `padrao` e
tabelas em `centros_custo`, sem dizer quando a padrão vale.
**O que não está claro:** que política usar quando o centro de custo não vem, ou
vem com tipo errado.
**Decisão:** ausente ou vazio → política padrão; presente e não texto → erro
geral.
**Justificativa:** "não informado" é um caso legítimo, e é para isso que a
padrão existe; tipo errado é entrada malformada e afeta todas as despesas.
**Regra afetada:** RN-013, RN-016

### AMB-019 — Centro de custo desconhecido

**Texto original da política v4:** idem AMB-018.
**O que não está claro:** se a padrão vale também para um centro de custo que
não está cadastrado (`despesas-envelope-cc-desconhecido.json`, `CC-SUPORTE-N2`).
**Decisão:** usa a política padrão, e a justificativa diz que o centro de custo
não está cadastrado.
**Justificativa:** "padrão" sugere fallback, e o próprio envelope traz o caso
para ser processado. O risco de um erro de digitação cair na padrão sem aviso
é reduzido pela justificativa explícita e pela normalização (AMB-020).
**Regra afetada:** RN-016

### AMB-020 — Comparação do centro de custo

**Texto original da política v4:** a política não menciona o caso.
**O que não está claro:** se ` cc-comercial ` é o mesmo centro que `CC-COMERCIAL`.
**Decisão:** compara após a normalização da RN-002, dos dois lados; o mesmo vale
para as chaves de categoria do documento de política.
**Justificativa:** mesmo raciocínio da AMB-013; e, com a AMB-019, um erro de
grafia levaria à padrão sem aviso.
**Regra afetada:** RN-002, RN-016

### AMB-021 — Centro de custo cadastrado sem a categoria

**Texto original da política v4:** a tabela de `CC-ADM` não tem `hospedagem`.
**O que não está claro:** se a tabela do centro substitui a padrão inteira (a
categoria ausente não é reembolsável) ou só sobrescreve as categorias que lista
(a categoria ausente herda da padrão).
**Decisão:** herda da padrão, categoria por categoria. Categoria que não está
nem no centro nem na padrão não é reembolsável.
**Justificativa:** `CC-ENG-PLATAFORMA` precisou declarar hospedagem com limite 0
e "nao reembolsavel"; se a ausência já significasse isso, a declaração seria
desnecessária.
**Regra afetada:** RN-001, RN-016

### AMB-022 — Limite zero

**Texto original da política v4:** `CC-ENG-PLATAFORMA` → `hospedagem`:
`"limite": 0.00`, `"observacao": "nao reembolsavel"`.
**O que não está claro:** se a despesa é recusada ou "limitada a zero", e se o
texto de `observacao` tem efeito.
**Decisão:** limite 0,00 significa categoria não reembolsável naquele centro de
custo, em qualquer categoria; a despesa é recusada com
`CATEGORIA_NAO_REEMBOLSAVEL`. `observacao` é informativa.
**Justificativa:** `limitado` sugere que algo foi pago; dizer que o centro de
custo não cobre a categoria é mais claro. Como a etapa de categoria vem antes
da de nota fiscal, d-013 passa a ser recusada por categoria.
**Regra afetada:** RN-001

### AMB-023 — Categoria `representacao`

**Texto original da política v4:** `CC-COMERCIAL` → `representacao`:
`"limite": 300.00`, `"periodicidade": "dia"`. Não consta da padrão.
**O que não está claro:** se divide limite com alimentação (e-001 e f-003 são
jantares), se exige nota fiscal e se o limite é por data.
**Decisão:** categoria independente, com o mesmo tratamento das demais: limite
próprio por data, mesma regra de nota fiscal e de duplicatas. Só é reembolsável
onde a política aplicável a lista.
**Justificativa:** o documento dá a ela o mesmo formato das outras categorias;
qualquer tratamento especial seria inventado.
**Regra afetada:** RN-001, RN-008

### AMB-024 — Moeda ausente ou inválida

**Texto original da política v4:** `"moeda_base": "BRL"`; despesas com e sem
o campo `moeda` (e-010 não tem).
**O que não está claro:** o que fazer sem `moeda`, com `"usd"` minúsculo, com
texto vazio ou com número.
**Decisão:** ausente → `BRL`; texto é normalizado (espaços nas pontas e
maiúsculas); vazio ou não texto → `DADOS_INVALIDOS`.
**Justificativa:** mantém as entradas sem moeda (todo o exemplo original)
válidas, e a política declara `BRL` como moeda base.
**Regra afetada:** RN-013, RN-017

### AMB-025 — Moeda sem cotação

**Texto original da política v4:** `cambio.json` só tem USD e EUR.
**O que não está claro:** o que fazer com e-006 (GBP).
**Decisão:** recusa só aquela despesa, com o motivo novo `COTACAO_INDISPONIVEL`;
`valor_considerado` fica nulo.
**Justificativa:** o dado da despesa está certo, falta o dado de referência; uma
despesa não deve impedir o cálculo das outras (AMB-017). Distinguir "moeda
inexistente" de "moeda sem cotação" exigiria uma lista de códigos de moeda, que
seria escopo novo.
**Regra afetada:** RN-018

### AMB-026 — Data sem cotação

**Texto original da política v4:** `cambio.json`: "Cotacoes publicadas apenas em
dias uteis bancarios."
**O que não está claro:** que taxa usar em e-004 (sábado, 2026-07-18): a
anterior, a seguinte, nenhuma, ou a anterior com limite de dias.
**Decisão:** a taxa da data anterior mais próxima que tenha essa moeda, sem
limite de dias; sem nenhuma anterior, `COTACAO_INDISPONIVEL`. A data usada sai
em `data_cotacao`.
**Justificativa:** é a prática da PTAX (último fechamento disponível) e não usa
dado futuro; "dia útil anterior" exigiria calendário de feriados, contra a
RN-012.
**Regra afetada:** RN-018

### AMB-027 — Arredondamento na conversão

**Texto original da política v4:** a política não menciona o caso.
**O que não está claro:** se arredonda antes de converter, depois, ou nas duas
vezes (33,333 USD × 5,42 dá 180,66 com uma vez e 180,65 com duas).
**Decisão:** multiplica o valor informado pela taxa, sem arredondar nenhum dos
dois, e arredonda uma única vez em reais.
**Justificativa:** arredondar duas vezes acumula erro; mantém o princípio da
RN-003 de um único valor em centavos antes das regras.
**Regra afetada:** RN-003, RN-018

### AMB-028 — Nota fiscal depois da conversão

**Texto original da política v4:** `"nota_fiscal_obrigatoria_acima_de": 100.00`,
com `"moeda_base": "BRL"`.
**O que não está claro:** se o limiar vale na moeda original ou em reais (e-005:
40,00 USD, sem nota, vira 220,00).
**Decisão:** compara o valor já convertido para reais.
**Justificativa:** o limiar está na moeda base; comparar na moeda original faria
o limiar variar com o câmbio.
**Regra afetada:** RN-007

### AMB-029 — Posição da conversão na ordem das regras

**Texto original da política v4:** a política não define ordem.
**O que não está claro:** se a conversão vem logo depois da normalização ou
depois das etapas que não usam valor (período, categoria).
**Decisão:** logo depois da normalização e antes de valor negativo (seção 8).
**Justificativa:** todas as regras passam a usar um único valor em reais, e a
ordem das etapas existentes não muda. Custo aceito: despesa estrangeira sem
cotação e também fora do período ou de categoria não reembolsável recebe
`COTACAO_INDISPONIVEL`.
**Regra afetada:** RN-018, seção 8

### AMB-030 — Duplicatas com moeda estrangeira

**Texto original da política v4:** a política não menciona o caso.
**O que não está claro:** se 22,00 EUR e 130,46 BRL, mesma data e fornecedor,
são duplicatas.
**Decisão:** duplicata exige a mesma moeda e o mesmo valor original (arredondado
para centavos na moeda original), além dos critérios da AMB-010.
**Justificativa:** duplicata é o mesmo comprovante lançado duas vezes, e um
comprovante tem uma só moeda.
**Regra afetada:** RN-006

### AMB-031 — Documento de política ausente ou inválido

**Texto original da política v4:** a política passa a ser um documento externo.
**O que não está claro:** se o documento é obrigatório e o que fazer com limite
negativo, periodicidade desconhecida, falta de `padrao` etc.
**Decisão:** obrigatório; qualquer problema estrutural é erro geral, sem saída
(lista na RN-015). Não há política embutida como reserva.
**Justificativa:** afeta todas as despesas igualmente (AMB-017); uma reserva
embutida criaria duas fontes da verdade.
**Regra afetada:** RN-013, RN-015

### AMB-032 — Documento de câmbio ausente ou inválido

**Texto original da política v4:** câmbio em documento externo (`cambio.json`).
**O que não está claro:** se o documento é obrigatório quando todas as despesas
estão em reais, e o que fazer com taxa inválida ou moeda base divergente.
**Decisão:** só é necessário quando houver despesa em moeda estrangeira; sem
ele, essas despesas são recusadas com `COTACAO_INDISPONIVEL`. Informado e
malformado, ou com `moeda_base` diferente da política, é erro geral.
**Justificativa:** um documento só em reais não deve depender do câmbio; um
arquivo corrompido não deve ser tratado como "não há cotação".
**Regra afetada:** RN-013, RN-018

### AMB-033 — Rastreabilidade da conversão na saída

**Texto original da política v4:** a política não menciona o caso.
**O que não está claro:** a saída da v3 não mostra moeda, taxa nem data da
cotação, e não diz de qual política veio o limite.
**Decisão:** `valor_informado` fica na moeda original; novos campos `moeda`,
`taxa_cambio` e `data_cotacao`; justificativas de limite e de categoria citam o
centro de custo ou a política padrão.
**Justificativa:** sem isso, o resultado não pode ser conferido à mão (seção 2).
**Regra afetada:** seção 4, RN-016

### AMB-034 — Vigência da política

**Texto original da política v4:** `"vigencia": "2026-07-01"`.
**O que não está claro:** o que fazer com despesas anteriores à vigência.
**Decisão:** `versao` e `vigencia` são informativas; o documento informado vale
para toda a execução.
**Justificativa:** só existe um documento de política; escolher entre versões
seria escopo novo.
**Regra afetada:** RN-015

### AMB-035 — Acréscimo em viagem parametrizado

**Texto original da política v4:** `"acrescimo_em_viagem_percentual": 50`.
**O que não está claro:** se o percentual no documento obriga a aplicar a
ampliação (e-002 "Lisboa", e-006 e e-007 "Londres").
**Decisão:** continua sem aplicar; o campo é informativo.
**Justificativa:** continua não existindo dado estruturado de viagem; moeda
estrangeira não prova viagem (compra online em dólar, por exemplo).
**Regra afetada:** RN-011

### AMB-036 — Periodicidade `dia` e `diaria`

**Texto original da política v4:** alimentação, transporte e representação com
`"periodicidade": "dia"`; hospedagem com `"diaria"`.
**O que não está claro:** se os dois valores significam coisas diferentes.
**Decisão:** os dois significam limite por data e categoria (RN-008); cada
hospedagem vale uma diária (AMB-008). Outro valor → erro geral.
**Justificativa:** é a semântica atual da RN-008.
**Regra afetada:** RN-008, RN-015

---

## 7. Casos de borda

| Caso | Entrada | Comportamento esperado | Regra |
|---|---|---|---|
| Duas despesas no mesmo dia somam acima do limite | d-001 (72,50) + d-002 (38,00), alimentação, mesma data, `CC-ENG-PLATAFORMA` | 72,50 + 2,50 | RN-008, RN-009 |
| Valor exatamente no limite da nota | d-003: 100,00, sem nota | não exige nota; 80,00 pelo limite | RN-007, RN-008 |
| Valor um centavo acima do limite da nota | d-004: 100,01, sem nota | recusado, `NOTA_FISCAL_AUSENTE` | RN-007 |
| Despesa recusada não consome limite | d-004 recusada na mesma data de d-003 | d-003 recebe o limite inteiro de 80,00 | RN-008, seção 8 |
| Categoria fora da política | d-005: coworking | recusado, `CATEGORIA_NAO_REEMBOLSAVEL` | RN-001 |
| Duplicata idêntica, ambas com nota | d-006 e d-007 | d-006: 54,90; d-007: recusada, `DUPLICATA` | RN-006 |
| Duplicata em que só a segunda tem nota | mesmas data, categoria, fornecedor e valor; só a 2ª com nota | 2ª mantida; 1ª recusada, `DUPLICATA` | RN-006 |
| Duplicata com grafia diferente do fornecedor | `Bistro Central` e `BISTRO CENTRAL ` | tratadas como duplicata | RN-002, RN-006 |
| Despesa antes do período | d-008: 2026-04-15 | recusado, `FORA_DO_PERIODO` | RN-004 |
| Despesa no último dia do período | d-014: 2026-07-31 | aceita pelo período | RN-004 |
| Despesa no primeiro dia do período | data igual a `periodo.inicio` | aceita pelo período | RN-004 |
| Estorno | d-009: −45,00 | recusado, `VALOR_NEGATIVO`; não abate outras | RN-005 |
| Valor zero | 0,00 | aprovado, 0,00 | RN-005 |
| Valor negativo que arredonda a zero | −0,004 | vira 0,00; aprovado, 0,00 | RN-003, RN-005 |
| Mais de duas casas decimais | d-011: 33,333 | considerado 33,33; aprovado, 33,33 | RN-003 |
| Arredondamento na metade | 10,005 | considerado 10,01 | RN-003 |
| Hospedagem com várias diárias na descrição | e-007: 1.200,00, "3 noites", `CC-COMERCIAL` | 1 diária; 400,00, `limitado` | RN-008, RN-014 |
| Duas hospedagens na mesma data | 200,00 + 150,00, mesma data, política padrão | 200,00 + 50,00 | RN-008, RN-009 |
| Hospedagem sem nota acima de 100 | 690,00, sem nota, política padrão | recusado, `NOTA_FISCAL_AUSENTE` | RN-007 |
| Categoria em maiúsculas | d-014: `ALIMENTACAO`, 61,00, `CC-ENG-PLATAFORMA` | tratada como alimentação; 61,00, aprovado | RN-002, RN-008 |
| Despesa em fim de semana | d-012: sábado | sem restrição; 47,20 | RN-012 |
| Indício de viagem na descrição | d-003: "Corrida aeroporto" | limite normal de 80,00 | RN-011, RN-014 |
| Indício de viagem pela moeda | e-002: EUR, "Almoco - Lisboa" | limite normal de 90,00 do `CC-COMERCIAL` | RN-011 |
| Campo obrigatório ausente em uma despesa | despesa sem `tem_nota_fiscal` | recusado, `DADOS_INVALIDOS`; demais processadas | RN-013 |
| Campo obrigatório só com espaços | `fornecedor`: `"   "` | recusado, `DADOS_INVALIDOS`; `valor_considerado` nulo | RN-013 |
| `id` com tipo errado | `id`: 17 | recusado, `DADOS_INVALIDOS`; `id` e `valor_considerado` nulos | RN-013 |
| Data fora do formato | `data`: `2026-7-3` | recusado, `DADOS_INVALIDOS` | RN-013 |
| Data inexistente | `data`: `2026-02-30` | recusado, `DADOS_INVALIDOS` | RN-013 |
| Valor não numérico | `valor`: `"72.50"` | recusado, `DADOS_INVALIDOS`; `valor_informado` e `valor_considerado` nulos | RN-013 |
| Valor válido e outro campo inválido | `valor`: 50,00, sem `tem_nota_fiscal` | recusado, `DADOS_INVALIDOS`; `valor_informado` 50,00, `valor_considerado` nulo | RN-013 |
| Campo desconhecido | despesa com `"projeto": "X"` | campo ignorado; despesa processada normalmente | RN-013 |
| Campo informativo malformado | `descricao`: 123 ou `periodo.competencia`: `"julho"` | campo ignorado; sem erro | RN-013, RN-014 |
| Período ausente | documento sem `periodo.fim` | erro, sem saída | RN-013 |
| Data do período inválida | `periodo.inicio`: `2026-02-30` | erro, sem saída | RN-013 |
| Colaborador sem identificação | `colaborador.id`: `"  "` ou 417 | erro, sem saída | RN-013 |
| Lista de despesas malformada | `despesas` não é lista, ou um item não é objeto | erro, sem saída | RN-013 |
| Documento com `NaN` ou `Infinity` | `valor`: `NaN` | erro, sem saída | RN-013 |
| Lista de despesas vazia | `despesas: []` | saída com `itens` vazio e total 0,00 | RN-013 |
| Centro de custo ausente | documento sem `colaborador.centro_custo` | política padrão | RN-016 |
| Centro de custo desconhecido | `CC-SUPORTE-N2` | política padrão; justificativa cita que não está cadastrado | RN-016 |
| Centro de custo com grafia diferente | ` cc-comercial ` | tratado como `CC-COMERCIAL` | RN-002, RN-016 |
| Centro de custo com tipo errado | `centro_custo`: 42 | erro, sem saída | RN-013, RN-016 |
| Categoria ausente na tabela do centro | `CC-ADM`, hospedagem de 300,00 | herda 250,00 da padrão; 250,00, `limitado` | RN-016 |
| Categoria com limite zero | d-010: hospedagem, `CC-ENG-PLATAFORMA` | recusado, `CATEGORIA_NAO_REEMBOLSAVEL` | RN-001 |
| Limite zero vem antes da nota fiscal | d-013: hospedagem, 690,00, sem nota, `CC-ENG-PLATAFORMA` | recusado, `CATEGORIA_NAO_REEMBOLSAVEL` | RN-001, seção 8 |
| Representação em centro que não a tem | f-003: `representacao`, política padrão | recusado, `CATEGORIA_NAO_REEMBOLSAVEL` | RN-001 |
| Representação acima do limite | e-001: 340,00, `CC-COMERCIAL` | 300,00, `limitado` | RN-008, RN-010 |
| Moeda ausente | e-010: sem `moeda` | `BRL`; 88,00, aprovado | RN-017 |
| Moeda em minúsculas | `moeda`: `" usd "` | tratada como `USD` | RN-017 |
| Moeda vazia ou de tipo errado | `moeda`: `""` ou 840 | recusado, `DADOS_INVALIDOS` | RN-013, RN-017 |
| Moeda estrangeira com cotação na data | e-002: 22,00 EUR em 2026-07-14 | 130,46; 90,00, `limitado` | RN-018, RN-008 |
| Moeda sem cotação | e-006: 55,00 GBP | recusado, `COTACAO_INDISPONIVEL`; `valor_considerado` nulo | RN-018 |
| Data sem cotação (fim de semana) | e-004: 30,00 EUR em 2026-07-18 | taxa de 2026-07-17 (5,96); 178,80; 90,00, `limitado` | RN-018 |
| Data anterior à primeira cotação | USD em 2026-07-10 | recusado, `COTACAO_INDISPONIVEL` | RN-018 |
| Despesa em BRL em data sem cotação | BRL em sábado | sem consulta ao câmbio; processada normalmente | RN-018 |
| Arredondamento cambial | 33,333 USD em 2026-07-13 (5,42) | 180,66 (uma única vez) | RN-003, RN-018 |
| Nota fiscal após conversão | e-005: 40,00 USD × 5,50 = 220,00, sem nota | recusado, `NOTA_FISCAL_AUSENTE` | RN-007 |
| Abaixo do limiar após conversão | e-003: 14,50 EUR × 5,88 = 85,26, sem nota | não exige nota; 85,26, aprovado | RN-007 |
| Duplicata na mesma moeda estrangeira | duas despesas de 22,00 EUR, mesmas data, categoria e fornecedor | tratadas como duplicata | RN-006 |
| Mesmo valor em reais, moedas diferentes | 22,00 EUR e 130,46 BRL, mesmas data, categoria e fornecedor | não são duplicata | RN-006 |
| Estorno em moeda sem cotação | −10,00 GBP | recusado, `COTACAO_INDISPONIVEL` (conversão vem antes) | RN-018, seção 8 |
| Estorno em moeda estrangeira | −10,00 USD em 2026-07-13 | −54,20; recusado, `VALOR_NEGATIVO` | RN-005, RN-018 |
| Documento de câmbio ausente, despesa estrangeira | despesa em USD, sem câmbio | recusado, `COTACAO_INDISPONIVEL`; demais processadas | RN-018 |
| Documento de câmbio ausente, tudo em reais | `exemplos/despesas-exemplo.json`, sem câmbio | processado normalmente | RN-018 |
| Documento de política ausente | execução sem política | erro, sem saída | RN-015 |
| Documento de política inválido | limite `-1`, sem `padrao` ou `"periodicidade": "mes"` | erro, sem saída | RN-015 |
| Documento de câmbio inválido | taxa 0 ou `"5,42"` | erro, sem saída | RN-018 |
| Moedas base divergentes | câmbio com `moeda_base` diferente da política | erro, sem saída | RN-018 |

## 8. Ordem de aplicação das regras

Antes das etapas por despesa, o sistema valida o documento de despesas, o de
política e, se informado, o de câmbio (RN-013, RN-015, RN-018), e escolhe a
política aplicável (RN-016). Qualquer erro geral encerra a execução sem saída.

Cada despesa passa pelas etapas abaixo, nesta ordem. Uma despesa recusada em uma
etapa recebe o motivo dessa etapa e não participa das etapas seguintes, nem
consome limite.

1. **Dados válidos** (RN-013, RN-017) → `DADOS_INVALIDOS`
2. **Normalização** (RN-002, RN-017)
3. **Conversão e arredondamento** (RN-018, RN-003) → `COTACAO_INDISPONIVEL`
4. **Valor negativo** (RN-005) → `VALOR_NEGATIVO`
5. **Período** (RN-004) → `FORA_DO_PERIODO`
6. **Categoria** na política aplicável (RN-001, RN-016) → `CATEGORIA_NAO_REEMBOLSAVEL`
7. **Duplicatas**, entre as despesas que passaram das etapas 1 a 6 (RN-006) → `DUPLICATA`
8. **Nota fiscal** (RN-007) → `NOTA_FISCAL_AUSENTE`
9. **Limites por data e categoria**, distribuídos pela posição, entre as despesas
   que passaram das etapas 1 a 8 (RN-008, RN-009, RN-010) → `LIMITE_DIARIO`

Se uma despesa falhar em mais de uma validação, o motivo registrado é o da
primeira etapa em que falhou.

## 9. Critérios de aceite

O sistema está pronto quando:

- [ ] Processando `exemplos/despesas-exemplo.json` (`CC-ENG-PLATAFORMA`) com
  `exemplos/envelope/politica-v4.json` e sem documento de câmbio, a saída tem
  exatamente:

  | Item | `valor_reembolsavel` | `status` | `motivo` |
  |---|---|---|---|
  | d-001 | 72,50 | aprovado | nulo |
  | d-002 | 2,50 | limitado | `LIMITE_DIARIO` |
  | d-003 | 80,00 | limitado | `LIMITE_DIARIO` |
  | d-004 | 0,00 | recusado | `NOTA_FISCAL_AUSENTE` |
  | d-005 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOLSAVEL` |
  | d-006 | 54,90 | aprovado | nulo |
  | d-007 | 0,00 | recusado | `DUPLICATA` |
  | d-008 | 0,00 | recusado | `FORA_DO_PERIODO` |
  | d-009 | 0,00 | recusado | `VALOR_NEGATIVO` |
  | d-010 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOLSAVEL` |
  | d-011 | 33,33 | aprovado | nulo |
  | d-012 | 47,20 | aprovado | nulo |
  | d-013 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOLSAVEL` |
  | d-014 | 61,00 | aprovado | nulo |
  | **total_reembolsavel** | **351,43** | | |

- [ ] Processando `exemplos/envelope/despesas-envelope.json` (`CC-COMERCIAL`)
  com `exemplos/envelope/politica-v4.json` e `exemplos/envelope/cambio.json`, a
  saída tem exatamente:

  | Item | `valor_considerado` | `valor_reembolsavel` | `status` | `motivo` |
  |---|---|---|---|---|
  | e-001 | 340,00 | 300,00 | limitado | `LIMITE_DIARIO` |
  | e-002 | 130,46 | 90,00 | limitado | `LIMITE_DIARIO` |
  | e-003 | 85,26 | 85,26 | aprovado | nulo |
  | e-004 | 178,80 | 90,00 | limitado | `LIMITE_DIARIO` |
  | e-005 | 220,00 | 0,00 | recusado | `NOTA_FISCAL_AUSENTE` |
  | e-006 | nulo | 0,00 | recusado | `COTACAO_INDISPONIVEL` |
  | e-007 | 1.200,00 | 400,00 | limitado | `LIMITE_DIARIO` |
  | e-008 | 95,00 | 90,00 | limitado | `LIMITE_DIARIO` |
  | e-009 | 120,00 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOLSAVEL` |
  | e-010 | 88,00 | 88,00 | aprovado | nulo |
  | **total_reembolsavel** | | **1.143,26** | | |

- [ ] Processando `exemplos/envelope/despesas-envelope-cc-desconhecido.json`
  (`CC-SUPORTE-N2`) com a mesma política e o mesmo câmbio, a saída usa a
  política padrão e tem exatamente:

  | Item | `valor_considerado` | `valor_reembolsavel` | `status` | `motivo` |
  |---|---|---|---|---|
  | f-001 | 58,00 | 58,00 | aprovado | nulo |
  | f-002 | 310,00 | 250,00 | limitado | `LIMITE_DIARIO` |
  | f-003 | 190,00 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOLSAVEL` |
  | f-004 | 65,76 | 65,76 | aprovado | nulo |
  | **total_reembolsavel** | | **373,76** | | |

- [ ] A saída tem um item para cada despesa da entrada, na mesma ordem.
- [ ] Todo item tem justificativa citando ao menos uma regra (RN-xxx).
- [ ] Todos os casos da seção 7 produzem o comportamento descrito.
- [ ] Alterar apenas a descrição de qualquer despesa não altera a saída, exceto
      o próprio campo de justificativa, se ele a citar.
- [ ] Processar a mesma entrada duas vezes produz a mesma saída.

## 10. O que fica em aberto

- **Viagem (AMB-006, AMB-007, AMB-035):** a regra de viagem fica sem efeito até
  a entrada trazer um dado de viagem, mesmo com o percentual agora no documento
  de política. Colaboradores em viagem recebem menos do que o RH provavelmente
  pretendia.
- **Hospedagem com várias diárias (AMB-008):** e-007 recebe 400,00, embora a
  descrição indique três noites. Decisão provisória: o colaborador deve lançar
  uma despesa por diária.
- **Despesas lançadas com atraso (AMB-009):** despesas legítimas de períodos
  anteriores, como d-008, são recusadas sem possibilidade de exceção.
- **Estorno de despesa já reembolsada (AMB-011):** se a despesa original foi
  reembolsada em outro período, o estorno não é compensado. Decisão provisória:
  fora de escopo.
- **`id` repetido na entrada:** não é validado. Decisão provisória: as despesas
  são processadas normalmente e distinguidas pela posição.
- **Centro de custo desconhecido (AMB-019):** um erro de digitação que a
  normalização não corrige leva à política padrão; a justificativa avisa, mas o
  cálculo não para.
- **Herança da padrão (AMB-021):** a leitura de que `CC-ADM` herda hospedagem da
  padrão se apoia no limite 0 explícito do `CC-ENG-PLATAFORMA`; deve ser
  confirmada com o RH.
- **Lacunas no câmbio (AMB-026):** sem limite de dias para trás, uma despesa de
  2026-07-31 usaria a taxa de 2026-07-28, embora 29 a 31 sejam dias úteis sem
  cotação no documento. A data usada aparece em `data_cotacao`.
- **Vigência (AMB-034):** a política v4 é aplicada mesmo a períodos anteriores a
  2026-07-01.
- **Aprovação manual (item C da política v4):** opcional; não implementado.
