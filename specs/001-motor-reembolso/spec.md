# Spec — Motor de Cálculo de Reembolso

**Versão:** 1.0 · **Status:** rascunho · **Última alteração:** 2026-10-04

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

- Não aplica a ampliação de limites para colaborador em viagem (ver AMB-006).
- Não processa mais de um colaborador ou mais de um período por execução.
- Não verifica a autenticidade da nota fiscal; considera apenas a informação
  "tem nota fiscal" declarada na entrada.
- Não detecta duplicatas entre execuções diferentes nem guarda histórico.
- Não compensa estornos com despesas de outros períodos.
- Não interpreta o texto da descrição para nenhum cálculo ou decisão.
- Não converte moedas; todos os valores estão em reais.
- Não aprova nem efetua pagamento; apenas calcula e justifica.
- Não reembolsa categorias além de alimentação, transporte urbano e hospedagem.

## 4. Entrada e saída

**Entrada:** um documento no formato de `exemplos/despesas-exemplo.json`.

| Campo | Tipo | Significado | Obrigatório |
|---|---|---|---|
| `colaborador.id` | texto | Identificador do colaborador | sim |
| `colaborador.nome` | texto | Nome do colaborador (informativo) | não |
| `colaborador.centro_custo` | texto | Centro de custo (informativo) | não |
| `periodo.competencia` | texto `AAAA-MM` | Mês de competência (informativo; ver AMB-009) | não |
| `periodo.inicio` | data `AAAA-MM-DD` | Primeiro dia do período | sim |
| `periodo.fim` | data `AAAA-MM-DD` | Último dia do período | sim |
| `despesas` | lista | Despesas a avaliar; pode ser vazia | sim |
| `despesas[].id` | texto | Identificador da despesa | sim |
| `despesas[].data` | data `AAAA-MM-DD` | Data em que a despesa ocorreu | sim |
| `despesas[].categoria` | texto | Categoria da despesa | sim |
| `despesas[].descricao` | texto | Descrição livre (informativa; nunca usada em cálculo) | não |
| `despesas[].fornecedor` | texto | Nome do fornecedor | sim |
| `despesas[].valor` | número | Valor em reais; pode ter mais de duas casas decimais ou ser negativo | sim |
| `despesas[].tem_nota_fiscal` | verdadeiro/falso | Se há nota fiscal | sim |

A **posição** de uma despesa é a sua ordem na lista `despesas`, começando em 1.
Ela é usada como critério de desempate (RN-006 e RN-009).

**Saída:** um documento com a seguinte estrutura.

| Campo | Tipo | Significado |
|---|---|---|
| `colaborador` | objeto | Cópia do objeto `colaborador` da entrada |
| `periodo` | objeto | Cópia do objeto `periodo` da entrada |
| `itens` | lista | Um item para cada despesa da entrada, na mesma ordem |
| `itens[].id` | texto | `id` da despesa |
| `itens[].valor_informado` | número | `valor` exatamente como veio na entrada; vazio se ausente ou inválido |
| `itens[].valor_considerado` | número | Valor arredondado para centavos (RN-003); vazio se inválido |
| `itens[].valor_reembolsavel` | número | Valor a reembolsar, com duas casas decimais |
| `itens[].status` | texto | `aprovado`, `limitado` ou `recusado` (definições abaixo) |
| `itens[].motivo` | texto ou vazio | Código do motivo (tabela abaixo); vazio quando `aprovado` |
| `itens[].justificativa` | texto | Explicação legível da decisão, citando a regra (RN-xxx) |
| `total_reembolsavel` | número | Soma de `valor_reembolsavel` de todos os itens |

**Status:**

- `aprovado`: a despesa passou por todas as regras e `valor_reembolsavel` é
  igual a `valor_considerado`.
- `limitado`: a despesa passou por todas as validações, mas o limite diário
  reduziu `valor_reembolsavel`, possivelmente a zero.
- `recusado`: a despesa foi recusada em uma validação e `valor_reembolsavel` é 0,00.

**Motivos:**

| Código | Status | Regra |
|---|---|---|
| `DADOS_INVALIDOS` | recusado | RN-013 |
| `VALOR_NEGATIVO` | recusado | RN-005 |
| `FORA_DO_PERIODO` | recusado | RN-004 |
| `CATEGORIA_NAO_REEMBOLSAVEL` | recusado | RN-001 |
| `DUPLICATA` | recusado | RN-006 |
| `NOTA_FISCAL_AUSENTE` | recusado | RN-007 |
| `LIMITE_DIARIO` | limitado | RN-008, RN-009, RN-010 |

A justificativa deve citar o `id` da despesa mantida, no caso de `DUPLICATA`, e o
limite com o valor já consumido no dia, no caso de `LIMITE_DIARIO`.

**Exemplo** (entrada com período de 2026-07-01 a 2026-07-31):

Entrada (trecho):

```
{ "id": "d-001", "data": "2026-07-03", "categoria": "alimentacao", "fornecedor": "Restaurante Tavola", "valor": 72.50, "tem_nota_fiscal": true }
{ "id": "d-002", "data": "2026-07-03", "categoria": "alimentacao", "fornecedor": "Cantina do Porto",   "valor": 38.00, "tem_nota_fiscal": true }
{ "id": "d-004", "data": "2026-07-06", "categoria": "transporte_urbano", "fornecedor": "TaxiApp",     "valor": 100.01, "tem_nota_fiscal": false }
```

Saída (trecho):

```
"itens": [
  { "id": "d-001", "valor_informado": 72.50, "valor_considerado": 72.50, "valor_reembolsavel": 60.00,
    "status": "limitado", "motivo": "LIMITE_DIARIO",
    "justificativa": "Limite diário de alimentação de R$ 60,00 aplicado; excedente de R$ 12,50 cortado (RN-008, RN-010)." },
  { "id": "d-002", "valor_informado": 38.00, "valor_considerado": 38.00, "valor_reembolsavel": 0.00,
    "status": "limitado", "motivo": "LIMITE_DIARIO",
    "justificativa": "Limite diário de alimentação de R$ 60,00 já consumido por d-001 em 2026-07-03 (RN-008, RN-009)." },
  { "id": "d-004", "valor_informado": 100.01, "valor_considerado": 100.01, "valor_reembolsavel": 0.00,
    "status": "recusado", "motivo": "NOTA_FISCAL_AUSENTE",
    "justificativa": "Valor acima de R$ 100,00 sem nota fiscal (RN-007)." }
],
"total_reembolsavel": 60.00
```

## 5. Regras de negócio

### RN-001 — Categorias reembolsáveis

**Regra:** Só são reembolsáveis as categorias `alimentacao`, `transporte_urbano`
e `hospedagem`, comparadas depois da normalização (RN-002). Qualquer outra
categoria é recusada com `CATEGORIA_NAO_REEMBOLSAVEL`.
**Origem:** política do RH, item 9 (AMB-014)
**Aceite:** d-005 (`coworking`, 89,00) → recusado, 0,00, `CATEGORIA_NAO_REEMBOLSAVEL`.

### RN-002 — Normalização de texto

**Regra:** Antes de qualquer comparação, categoria e fornecedor são normalizados:
espaços no início e no fim são removidos, letras maiúsculas viram minúsculas e
acentos são removidos. A normalização não altera mais nada; espaços internos e
outros caracteres são mantidos.
**Origem:** decisão desta spec (AMB-013)
**Aceite:** categoria `ALIMENTACAO`, ` Alimentação ` e `alimentacao` são tratadas
como `alimentacao`. Fornecedores `Bistro Central` e `bistro central` são iguais.

### RN-003 — Arredondamento

**Regra:** O valor de cada despesa é arredondado para centavos antes de qualquer
outra regra, com arredondamento comercial: a metade se afasta do zero (0,005
vira 0,01). Todas as regras seguintes usam o valor arredondado
(`valor_considerado`). Todos os valores de saída têm duas casas decimais.
**Origem:** decisão desta spec (AMB-012)
**Aceite:** d-011 (33,333) → `valor_considerado` 33,33. Valor 10,005 → 10,01.
Valor −0,004 → 0,00, tratado como valor zero (RN-005).

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
mesma categoria normalizada, o mesmo fornecedor normalizado e o mesmo
`valor_considerado`. Só despesas que passaram por RN-001, RN-004, RN-005 e RN-013
participam dessa comparação. Em cada grupo de duplicatas, uma despesa é mantida:

1. se houver despesas com nota fiscal no grupo, fica a de menor posição entre elas;
2. se nenhuma tiver nota fiscal, fica a de menor posição.

As demais são recusadas com `DUPLICATA`, e a justificativa cita o `id` da mantida.
`id` e `descricao` não participam da comparação.
**Origem:** política do RH, item 8 (AMB-010)
**Aceite:** d-006 e d-007 (2026-07-09, alimentação, Bistro Central, 54,90, ambas
com nota) → d-006 mantida; d-007 recusada, `DUPLICATA`, citando d-006. Grupo em
que só a segunda despesa tem nota → a segunda é mantida e a primeira é recusada.

### RN-007 — Nota fiscal

**Regra:** Despesa com `valor_considerado` estritamente maior que 100,00 e sem
nota fiscal é recusada inteira com `NOTA_FISCAL_AUSENTE`. A verificação usa o
valor da própria despesa, e não a soma do dia nem o valor após o limite.
Despesa de exatamente 100,00 não exige nota.
**Origem:** política do RH, item 5 (AMB-004, AMB-005)
**Aceite:** d-003 (100,00, sem nota) → não exige nota. d-004 (100,01, sem nota)
→ recusado, 0,00, `NOTA_FISCAL_AUSENTE`. d-013 (690,00, sem nota) → recusado.

### RN-008 — Limites diários por categoria

**Regra:** Para cada combinação de data e categoria, a soma reembolsada não
ultrapassa o limite:

| Categoria | Limite por data |
|---|---|
| `alimentacao` | R$ 60,00 |
| `transporte_urbano` | R$ 80,00 |
| `hospedagem` | R$ 250,00 |

Cada despesa de hospedagem vale uma diária, qualquer que seja o texto da
descrição. Como o limite é por data, várias hospedagens na mesma data dividem
o mesmo limite de R$ 250,00. Só despesas que passaram por todas as regras
anteriores consomem o limite.
**Origem:** política do RH, itens 1, 2 e 3 (AMB-001, AMB-008)
**Aceite:** d-010 (hospedagem, 480,00, descrição "2 diarias") → 250,00, `limitado`.
d-001 + d-002 (alimentação, 2026-07-03, 110,50 no total) → soma reembolsada 60,00.

### RN-009 — Distribuição do limite entre despesas da mesma data

**Regra:** Quando várias despesas da mesma categoria e data disputam o limite,
ele é consumido na ordem da posição: cada despesa recebe o menor valor entre o
seu `valor_considerado` e o saldo do limite que restou das anteriores.
**Origem:** decisão desta spec (AMB-002)
**Aceite:** d-001 (posição 1, 72,50) → 60,00; d-002 (posição 2, 38,00) → 0,00,
`limitado`, justificativa citando d-001.

### RN-010 — Reembolso parcial

**Regra:** Despesa que ultrapassa o saldo do limite é reembolsada até o saldo; o
excedente é cortado. A despesa não é recusada por ultrapassar o limite.
**Origem:** política do RH, item 4 (AMB-003)
**Aceite:** d-014 (alimentação, 61,00) → 60,00, `limitado`, `LIMITE_DIARIO`.

### RN-011 — Ampliação para colaborador em viagem

**Regra:** A ampliação de 50% dos limites prevista pela política **não é
aplicada**. A entrada não traz nenhuma informação estruturada que indique viagem.
**Origem:** política do RH, item 6 (AMB-006, AMB-007)
**Aceite:** d-003 ("Corrida aeroporto", 100,00) → limite de 80,00 aplicado,
reembolso 80,00. Nenhuma despesa do exemplo recebe limite acima da tabela da RN-008.

### RN-012 — Dias do calendário

**Regra:** Todas as datas do calendário são tratadas da mesma forma; não há
distinção entre dias úteis, fins de semana e feriados.
**Origem:** decisão desta spec (AMB-015)
**Aceite:** d-012 (sábado, 2026-07-18, alimentação, 47,20) → aprovado, 47,20.

### RN-013 — Dados inválidos

**Regra:**

- **Erro geral:** se o documento de entrada não puder ser lido, ou se faltar
  `colaborador.id`, `periodo.inicio`, `periodo.fim` ou `despesas`, ou se
  `periodo.inicio` for posterior a `periodo.fim`, o sistema encerra com mensagem
  de erro e não gera saída.
- **Erro em uma despesa:** se faltar um campo obrigatório da despesa, se a data
  não for uma data válida, se o valor não for numérico ou se `tem_nota_fiscal`
  não for verdadeiro/falso, apenas essa despesa é recusada com `DADOS_INVALIDOS`.
  As demais são processadas normalmente.

**Origem:** decisão desta spec
**Aceite:** despesa sem `tem_nota_fiscal` → recusado, `DADOS_INVALIDOS`, e as
outras despesas do documento aparecem na saída normalmente. Documento sem
`periodo.fim` → erro, sem arquivo de saída.

### RN-014 — Descrição é informativa

**Regra:** O campo `descricao` nunca altera nenhum cálculo ou decisão. Só campos
estruturados (data, categoria, fornecedor, valor, nota fiscal, período e
posição) determinam o resultado.
**Origem:** decisão desta spec (AMB-006, AMB-008, AMB-010)
**Aceite:** trocar a descrição de qualquer despesa do exemplo não altera nenhum
`valor_reembolsavel`, `status` ou `motivo`.

---

## 6. Ambiguidades identificadas e decisões

### AMB-001 — Unidade do limite diário

**Texto original do RH:** "Alimentação tem limite de R$ 60 por dia."
**O que não está claro:** se o limite vale para a soma das despesas do dia ou
para cada despesa separadamente.
**Decisão:** o limite vale para a soma das despesas da mesma categoria na mesma
data, para as três categorias.
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
despesa é recusada inteira.
**Justificativa:** a nota comprova o gasto efetivamente feito, e "obrigatória"
indica que sem ela a despesa não é aceita.
**Regra afetada:** RN-007

### AMB-006 — O que caracteriza "em viagem"

**Texto original do RH:** "Colaborador em viagem tem limites ampliados em 50%."
**O que não está claro:** a entrada não tem campo que indique viagem. Seria
preciso inferir pela hospedagem, pela descrição, ou não aplicar.
**Decisão:** a ampliação não é aplicada.
**Justificativa:** inferir viagem falha em casos evidentes (d-003, "Corrida
aeroporto", sem hospedagem no dia) e cria brechas; sem dado, não há como verificar.
**Regra afetada:** RN-011

### AMB-007 — Categorias alcançadas pela ampliação

**Texto original do RH:** "Colaborador em viagem tem limites ampliados em 50%."
**O que não está claro:** se a ampliação vale para as três categorias ou só para
alimentação e transporte.
**Decisão:** não se aplica enquanto valer a AMB-006; deve ser decidida se um dado
de viagem passar a existir.
**Justificativa:** sem ampliação, a pergunta não tem efeito; registrar evita uma
lacuna silenciosa.
**Regra afetada:** RN-011

### AMB-008 — Número de diárias de uma hospedagem

**Texto original do RH:** "Hospedagem tem limite de R$ 250 por diária."
**O que não está claro:** a entrada não tem número de diárias; a informação só
aparece no texto livre (d-010, "2 diarias"; d-013, "3 noites").
**Decisão:** cada despesa de hospedagem vale uma diária; a descrição não é usada.
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
demais são recusadas.
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
**Decisão:** arredonda o valor de entrada para centavos, com a metade se
afastando do zero, antes de qualquer regra.
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
**Decisão:** lista fechada: alimentação, transporte urbano e hospedagem.
**Justificativa:** a política só cita essas três; encaixar por semelhança seria
criar política.
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

---

## 7. Casos de borda

| Caso | Entrada | Comportamento esperado | Regra |
|---|---|---|---|
| Duas despesas no mesmo dia somam acima do limite | d-001 (72,50) + d-002 (38,00), alimentação, mesma data | 60,00 + 0,00 | RN-008, RN-009 |
| Valor exatamente no limite da nota | d-003: 100,00, sem nota | não exige nota; 80,00 pelo limite | RN-007, RN-008 |
| Valor um centavo acima do limite da nota | d-004: 100,01, sem nota | recusado, `NOTA_FISCAL_AUSENTE` | RN-007 |
| Despesa recusada não consome limite | d-004 recusada na mesma data de d-003 | d-003 recebe o limite inteiro de 80,00 | RN-008, seção 8 |
| Categoria fora da lista | d-005: coworking | recusado, `CATEGORIA_NAO_REEMBOLSAVEL` | RN-001 |
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
| Hospedagem com várias diárias na descrição | d-010: 480,00, "2 diarias" | 1 diária; 250,00, `limitado` | RN-008, RN-014 |
| Duas hospedagens na mesma data | 200,00 + 150,00, mesma data | 200,00 + 50,00 | RN-008, RN-009 |
| Hospedagem sem nota acima de 100 | d-013: 690,00, sem nota | recusado, `NOTA_FISCAL_AUSENTE` | RN-007 |
| Categoria em maiúsculas | d-014: `ALIMENTACAO`, 61,00 | tratada como alimentação; 60,00, `limitado` | RN-002, RN-010 |
| Despesa em fim de semana | d-012: sábado | sem restrição; 47,20 | RN-012 |
| Indício de viagem na descrição | d-003: "Corrida aeroporto" | limite normal de 80,00 | RN-011, RN-014 |
| Campo obrigatório ausente em uma despesa | despesa sem `tem_nota_fiscal` | recusado, `DADOS_INVALIDOS`; demais processadas | RN-013 |
| Período ausente | documento sem `periodo.fim` | erro, sem saída | RN-013 |
| Lista de despesas vazia | `despesas: []` | saída com `itens` vazio e total 0,00 | RN-013 |

## 8. Ordem de aplicação das regras

Cada despesa passa pelas etapas abaixo, nesta ordem. Uma despesa recusada em uma
etapa recebe o motivo dessa etapa e não participa das etapas seguintes, nem
consome limite.

1. **Dados válidos** (RN-013) → `DADOS_INVALIDOS`
2. **Normalização e arredondamento** (RN-002, RN-003)
3. **Valor negativo** (RN-005) → `VALOR_NEGATIVO`
4. **Período** (RN-004) → `FORA_DO_PERIODO`
5. **Categoria** (RN-001) → `CATEGORIA_NAO_REEMBOLSAVEL`
6. **Duplicatas**, entre as despesas que passaram das etapas 1 a 5 (RN-006) → `DUPLICATA`
7. **Nota fiscal** (RN-007) → `NOTA_FISCAL_AUSENTE`
8. **Limites por data e categoria**, distribuídos pela posição, entre as despesas
   que passaram das etapas 1 a 7 (RN-008, RN-009, RN-010) → `LIMITE_DIARIO`

Se uma despesa falhar em mais de uma validação, o motivo registrado é o da
primeira etapa em que falhou.

## 9. Critérios de aceite

O sistema está pronto quando:

- [ ] Processando `exemplos/despesas-exemplo.json`, a saída tem exatamente:

  | Item | `valor_reembolsavel` | `status` | `motivo` |
  |---|---|---|---|
  | d-001 | 60,00 | limitado | `LIMITE_DIARIO` |
  | d-002 | 0,00 | limitado | `LIMITE_DIARIO` |
  | d-003 | 80,00 | limitado | `LIMITE_DIARIO` |
  | d-004 | 0,00 | recusado | `NOTA_FISCAL_AUSENTE` |
  | d-005 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOLSAVEL` |
  | d-006 | 54,90 | aprovado | — |
  | d-007 | 0,00 | recusado | `DUPLICATA` |
  | d-008 | 0,00 | recusado | `FORA_DO_PERIODO` |
  | d-009 | 0,00 | recusado | `VALOR_NEGATIVO` |
  | d-010 | 250,00 | limitado | `LIMITE_DIARIO` |
  | d-011 | 33,33 | aprovado | — |
  | d-012 | 47,20 | aprovado | — |
  | d-013 | 0,00 | recusado | `NOTA_FISCAL_AUSENTE` |
  | d-014 | 60,00 | limitado | `LIMITE_DIARIO` |
  | **total_reembolsavel** | **585,43** | | |

- [ ] A saída tem um item para cada despesa da entrada, na mesma ordem.
- [ ] Todo item tem justificativa citando ao menos uma regra (RN-xxx).
- [ ] Todos os casos da seção 7 produzem o comportamento descrito.
- [ ] Alterar apenas a descrição de qualquer despesa não altera a saída, exceto
      o próprio campo de justificativa, se ele a citar.
- [ ] Processar a mesma entrada duas vezes produz a mesma saída.

## 10. O que fica em aberto

- **Viagem (AMB-006, AMB-007):** a regra 6 da política fica sem efeito até a
  entrada trazer um dado de viagem. Colaboradores em viagem recebem menos do que
  o RH provavelmente pretendia.
- **Hospedagem com várias diárias (AMB-008):** d-010 recebe 250,00, embora a
  descrição indique duas diárias de 240,00. Decisão provisória: o colaborador
  deve lançar uma despesa por diária.
- **Despesas lançadas com atraso (AMB-009):** despesas legítimas de períodos
  anteriores, como d-008, são recusadas sem possibilidade de exceção.
- **Estorno de despesa já reembolsada (AMB-011):** se a despesa original foi
  reembolsada em outro período, o estorno não é compensado. Decisão provisória:
  fora de escopo.
- **`id` repetido na entrada:** não é validado. Decisão provisória: as despesas
  são processadas normalmente e distinguidas pela posição.
