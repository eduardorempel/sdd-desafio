# Plano Técnico — Motor de Cálculo de Reembolso

**Versão:** 2.0 · **Baseado na spec:** 2.1 (inclui D-001, D-002 e D-003)

> Aqui mora o COMO. Este arquivo pode e deve falar de linguagem, biblioteca e
> arquitetura. O que ele **não** pode é introduzir regra de negócio nova — se
> apareceu uma, ela pertence à `spec.md`.

**O que mudou da 1.0 para a 2.0:** a política sai do código e vira documento
externo (RN-015), escolhido por centro de custo (RN-016); entram moeda (RN-017)
e câmbio (RN-018), com a conversão antes das regras; a CLI recebe os
documentos de política e de câmbio; a saída ganha `moeda`, `taxa_cambio` e
`data_cotacao`. Revistas: DT-004, DT-005, DT-006. Novas: DT-009 a DT-014.

---

## 1. Stack

| Escolha | O quê | Por quê | O que descartei e por quê |
|---|---|---|---|
| Linguagem | Python 3.12+ | `decimal` e `json` na biblioteca padrão; nenhuma dependência de runtime; rápido de escrever em 2 dias | Node/TS: sem decimal nativo, e `JSON.parse` converte `33.333` em float antes de qualquer código nosso rodar. Go: cerimônia demais para um CLI deste tamanho |
| Testes | pytest | `parametrize` com `ids` legíveis cobre a tabela da seção 7 da spec linha a linha | `unittest`: verboso e com parametrização pobre |
| Parsing/validação | `json` da stdlib + validação manual, para os três documentos | A RN-013 recusa uma despesa e segue com as outras; validação escrita à mão expressa isso direto. Política e câmbio reaproveitam os mesmos utilitários (DT-012) | pydantic/jsonschema: falham o documento inteiro por padrão; adaptar ao "erro por despesa" custa mais do que escrever ~50 linhas |
| Aritmética monetária | `decimal.Decimal`, lido direto do JSON com `parse_float=Decimal`, inclusive limites, limiar e taxas de câmbio | Float no parse transforma `10.005` em `10.00499…`, que arredonda para 10,00 e quebra a RN-003; o mesmo vale para `33.333 × 5.42` (AMB-027) | float (erro de representação); inteiro em centavos (exigiria arredondar já no parse, e `valor_informado` e `taxa_cambio` precisam sair sem arredondamento) |
| CLI | `argparse` | Biblioteca padrão; há um único subcomando | click/typer: dependência sem ganho |
| Lint/format | ruff | Uma ferramenta para lint e formatação | flake8 + black |

**Comandos:**

- Rodar: `python -m reembolso calcular --input despesas.json --politica politica.json [--cambio cambio.json] --output resultado.json`
- Testes: `python -m pytest`
- Lint/format: `ruff check .` · `ruff format .`

## 2. Arquitetura

```
despesas.json ─┐
politica.json ─┼─► cli ──► entrada / politica / cambio ──► motor ───────────► saida ──► resultado.json
cambio.json  ──┘   (I/O)   parse + validação dos 3 docs     etapas 3–9          serialização
  (opcional)               (etapas 1–2), política           da seção 8          + total
                           aplicável (RN-016)               (núcleo puro)
```

| Módulo | Responsabilidade | Regras |
|---|---|---|
| `cli.py` / `__main__.py` | Argumentos, leitura e escrita de arquivo, mensagem de erro, código de saída | — |
| `entrada.py` | JSON de despesas → `Documento`. Erro geral (`EntradaInvalida`) e erro por despesa (`DADOS_INVALIDOS`). Valida `centro_custo` e `moeda`. Também guarda os utilitários de parse estrito usados por `politica.py` e `cambio.py` (DT-012) | RN-013, RN-017, AMB-017, AMB-018, AMB-024 |
| `politica.py` | JSON de política → `Politica` (validação da RN-015) e escolha da `PoliticaAplicavel` pelo centro de custo, com herança por categoria | RN-015, RN-016, RN-002 (chaves e periodicidade) |
| `cambio.py` | JSON de câmbio → `Cambio` (validação da RN-018) e busca da taxa pela data da despesa ou a anterior mais próxima | RN-018 |
| `normalizacao.py` | Normalização de texto, de moeda e arredondamento | RN-002, RN-003, RN-017 |
| `etapas.py` | Uma função por etapa da seção 8 da spec, de 3 a 9 | RN-001, RN-003 a RN-010, RN-018 |
| `motor.py` | Lista ordenada de etapas e execução | Seção 8 |
| `justificativas.py` | Templates de texto das justificativas, formatação `R$ 0,00` e texto da origem da política | Seção 4 (justificativa), RN-016 |
| `saida.py` | `Resultado` → estrutura JSON, `null`, duas casas, total | Seção 4 (saída), RN-003 |
| `modelo.py` | Dataclasses e enums | — |

**Fronteiras:**

- Só `cli.py` toca disco, stdout e stderr.
- `entrada.py`, `politica.py` e `cambio.py` recebem texto e devolvem objetos;
  não abrem arquivo.
- `motor.py`, `etapas.py`, `normalizacao.py`, `justificativas.py` e a parte de
  seleção de `politica.py` não conhecem JSON nem arquivo. Recebem e devolvem
  objetos do `modelo.py`, de `politica.py` e de `cambio.py`.

Essa divisão permite testar toda regra de negócio sem I/O. Uma mudança de
valor da política agora é só uma mudança no documento de política, sem código.

## 3. Modelo de dados

Todas as estruturas são `@dataclass(frozen=True)`.

```
Documento
  colaborador: dict          # cópia como veio, para a saída
  periodo: dict              # cópia como veio, para a saída
  inicio: date
  fim: date
  centro_custo: str | None   # como veio (já validado como texto); None se ausente
  despesas: list[Despesa | Invalida]   # na ordem da entrada

Despesa                      # passou pela etapa 1 (RN-013, RN-017)
  posicao: int               # 1, 2, 3...
  id: str
  data: date
  categoria: str             # normalizada (RN-002)
  fornecedor: str            # normalizado (RN-002)
  tem_nota_fiscal: bool
  moeda: str                 # normalizada (RN-017); "BRL" se ausente
  valor_informado: Decimal   # na moeda da despesa, sem arredondamento
  valor_considerado: Decimal | None  # em reais (RN-003, RN-018); None até a etapa 3
                                     # nas despesas em moeda estrangeira (DT-010)
  taxa_cambio: Decimal | None        # como está no documento de câmbio; None em BRL
  data_cotacao: date | None          # data da taxa usada; None em BRL

Invalida                     # recusada na etapa 1
  posicao: int
  id: str | None             # None se o id for inválido
  valor_informado: Decimal | None   # None se ausente ou não numérico
  detalhe: str               # qual campo falhou, para a justificativa

Resultado
  id: str | None
  valor_informado: Decimal | None
  moeda: str | None                 # None quando DADOS_INVALIDOS
  taxa_cambio: Decimal | None
  data_cotacao: date | None
  valor_considerado: Decimal | None # None quando DADOS_INVALIDOS ou COTACAO_INDISPONIVEL
  valor_reembolsavel: Decimal
  status: Status
  motivo: Motivo | None             # None quando APROVADO
  justificativa: str
```

Política e câmbio (em `politica.py` e `cambio.py`):

```
Politica
  moeda_base: str                          # "BRL"
  limiar_nota_fiscal: Decimal
  padrao: dict[str, Decimal]               # categoria normalizada → limite
  centros: dict[str, Centro]               # chave normalizada → Centro

Centro
  codigo: str                              # grafia da chave no documento (AMB-038)
  limites: dict[str, Decimal]              # categoria normalizada → limite

Origem                                     # de onde veio a entrada de uma categoria (RN-016)
  tipo: TipoOrigem                         # PADRAO, CENTRO, HERDADA, NAO_CADASTRADO
  codigo: str | None                       # código a citar (AMB-038, AMB-040)

PoliticaAplicavel
  limiar_nota_fiscal: Decimal
  regra(categoria) -> (limite: Decimal | None, origem: Origem)
                                           # limite None = categoria não consta

Cambio
  moeda_base: str
  taxas: dict[str, list[tuple[date, Decimal]]]   # moeda → (data, taxa), ordenado por data
  cotacao(moeda, data) -> tuple[Decimal, date] | None
```

- `Status`: `APROVADO`, `LIMITADO`, `RECUSADO`, com valores iguais aos textos
  da spec (`"aprovado"`...).
- `Motivo`: os oito códigos da tabela de motivos da spec, com valor igual ao
  código (`"COTACAO_INDISPONIVEL"`...).
- A periodicidade não é guardada: depois de validada (`dia` ou `diaria`), as
  duas têm o mesmo efeito (AMB-036).
- A saída mantém um `Resultado` por posição. A lista final é montada por ordem
  de posição, o que garante "um item por despesa, na mesma ordem".

## 4. Como a política é representada

Os valores da política **não estão mais no código**: vêm do documento de
política informado na execução (RN-015). `politica.py` só lê, valida e escolhe:

```python
politica = ler_politica(texto)                          # RN-015 → Politica
aplicavel = politica_aplicavel(politica, centro_custo)  # RN-016 → PoliticaAplicavel
```

Seleção (RN-016), com o centro de custo comparado após `normalizar_texto`:

| `centro_custo` | Categoria no centro | Categoria só na padrão | Categoria em nenhum |
|---|---|---|---|
| ausente ou vazio | — | limite da padrão, `PADRAO` | `None`, `PADRAO` |
| cadastrado | limite do centro, `CENTRO` | limite da padrão, `HERDADA` | `None`, `CENTRO` |
| não cadastrado | — | limite da padrão, `NAO_CADASTRADO` | `None`, `NAO_CADASTRADO` |

O texto da origem fica em `justificativas.py` (DT-011).

A **ordem das regras** continua sendo dado, em `motor.py`:

```python
ETAPAS = [
    Conversao(conversao),         # RN-018, RN-003 → COTACAO_INDISPONIVEL
    PorItem(valor_negativo),      # RN-005 → VALOR_NEGATIVO
    PorItem(periodo),             # RN-004 → FORA_DO_PERIODO
    PorItem(categoria),           # RN-001, RN-016 → CATEGORIA_NAO_REEMBOLSAVEL
    EmGrupo(duplicatas),          # RN-006 → DUPLICATA
    PorItem(nota_fiscal),         # RN-007 → NOTA_FISCAL_AUSENTE
    EmGrupo(limites_por_data),    # RN-008, RN-009, RN-010 → LIMITE_DIARIO
]
```

- **Etapa de conversão:** recebe uma `Despesa` e devolve a mesma despesa com
  `valor_considerado`, `taxa_cambio` e `data_cotacao` preenchidos, ou uma
  recusa. A despesa devolvida substitui a da lista viva.
- **Etapa por item:** recebe uma `Despesa` e devolve `None` (passa) ou uma recusa
  com motivo e justificativa.
- **Etapa em grupo:** recebe todas as despesas ainda vivas, em ordem de posição,
  e decide sobre o conjunto. A de duplicatas devolve recusas. A de limites
  devolve o valor reembolsável de cada despesa.
- Todas as etapas recebem um `Contexto` com o documento, a política aplicável e
  o câmbio (DT-009).
- As etapas 1 e 2 (validação e normalização) acontecem em `entrada.py`, porque
  precisam do JSON bruto. As despesas `Invalida` não entram no motor.
- Uma despesa recusada sai da lista viva e não chega às etapas seguintes. É isso
  que impede uma despesa recusada de consumir limite (seção 8 da spec).
- Ao final, uma despesa que chegou à etapa 9 é `APROVADO` se
  `valor_reembolsavel == valor_considerado`, senão `LIMITADO`, exatamente como a
  seção 4 da spec define.

## 5. Decisões técnicas

### DT-001 — `Decimal` desde o parse do JSON

**Contexto:** a RN-003 exige arredondamento comercial (10,005 → 10,01), e d-011
tem três casas.
**Decisão:** `json.loads(texto, parse_float=Decimal)`. Inteiros (`parse_int`)
também são convertidos para `Decimal` na validação. O arredondamento usa
`quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`, que no `Decimal` afasta a
metade do zero, inclusive para negativos. Vale para os três documentos.
**Alternativa descartada:** float com `round()`. O Python arredonda metade para
par, e o float já chega com erro de representação.
**Consequência:** nenhuma comparação de fronteira (100,00 vs 100,01) depende de
float. O serializador precisa saber escrever `Decimal` (DT-005).

### DT-002 — Validação manual em dois níveis

**Contexto:** a RN-013 separa erro geral de erro em uma despesa.
**Decisão:** `entrada.py` valida o documento e, se algo falhar, levanta
`EntradaInvalida(mensagem)`. Em seguida valida cada despesa e produz `Despesa` ou
`Invalida`. Pontos de cuidado, todos derivados da RN-013:
- `bool` é subclasse de `int` em Python, então `"valor": true` precisa ser
  rejeitado com teste explícito de tipo; o mesmo vale para limite, limiar e
  taxa nos outros documentos;
- datas validadas com regex `^\d{4}-\d{2}-\d{2}$` e depois `date.fromisoformat`.
  O regex é necessário porque `fromisoformat` aceita formatos além de `AAAA-MM-DD`.
  Vale também para as chaves de `taxas` do câmbio;
- texto "vazio" = `str.strip() == ""`;
- `centro_custo` presente e não texto → `EntradaInvalida`; `moeda` presente e
  vazia ou não texto → `DADOS_INVALIDOS` (RN-017);
- campos informativos e desconhecidos não são lidos pela validação.
**Alternativa descartada:** pydantic, que falha o documento inteiro por padrão.
**Consequência:** cada caso da RN-013 vira um `if` com teste próprio. Mais código
explícito, mas cada linha aponta para um item da spec.

### DT-003 — `NaN` e `Infinity` como documento ilegível

**Contexto:** a RN-013 (D-001) trata `NaN`/`Infinity` como JSON inválido, mas o
`json` do Python aceita esses literais por padrão.
**Decisão:** `parse_constant` levanta `EntradaInvalida`, o que vira erro geral.
O mesmo parser estrito é usado na política e no câmbio (DT-012).
**Alternativa descartada:** aceitar e rejeitar depois como valor não numérico.
Isso contradiria a spec.
**Consequência:** o parser fica estrito como a norma JSON.

### DT-004 — Política em documento externo, pipeline como lista (revista na 2.0)

**Contexto:** na 1.0, os valores da política ficavam em `politica.py` como
constantes. A v4 (RN-015) passa a política para um documento externo, com
tabelas por centro de custo. A 1.0 já previa a saída: "`politica.py` vira um
objeto passado ao motor".
**Decisão:** `politica.py` deixa de ter constantes e passa a ler e validar o
documento (`ler_politica`) e a escolher a `PoliticaAplicavel`
(`politica_aplicavel`). A política aplicável é escolhida uma vez por execução,
antes do motor, e chega às etapas pelo `Contexto` (DT-009). Não existe política
embutida de reserva (AMB-031). A ordem das etapas continua em `ETAPAS`.
**Alternativa descartada:** manter as constantes como padrão quando não houver
documento. A spec proíbe (AMB-031) e criaria duas fontes da verdade.
**Consequência:** mudar um valor da política é editar o JSON; regra nova
continua sendo uma função mais uma linha em `ETAPAS`. Os testes de regra montam
a `PoliticaAplicavel` a partir de `exemplos/envelope/politica-v4.json` ou de
dicionários pequenos.

### DT-005 — Serialização da saída (revista na 2.0)

**Contexto:** a saída exige duas casas em `valor_considerado`,
`valor_reembolsavel` e `total_reembolsavel` (RN-003), `null` nos campos sem
valor (D-001), e `colaborador`/`periodo` copiados como vieram, que podem conter
`Decimal` do parse. A 2.0 acrescenta `moeda`, `taxa_cambio` e `data_cotacao`.
**Decisão:** `saida.py` monta a estrutura com `None` onde a spec pede nulo, com
os campos do item na ordem da tabela da seção 4 da spec: `id`,
`valor_informado`, `moeda`, `taxa_cambio`, `data_cotacao`, `valor_considerado`,
`valor_reembolsavel`, `status`, `motivo`, `justificativa`. Um encoder próprio
escreve todo `Decimal` como literal numérico JSON:
- os três campos monetários saem quantizados em duas casas (`60.00`);
- `valor_informado` e `taxa_cambio` saem com `str(Decimal)`, sem quantizar
  (`33.333`, `5.93`);
- `data_cotacao` sai como texto `AAAA-MM-DD`;
- zero negativo (`-0.00`, resultado de arredondar `-0.004`) é normalizado para
  `0.00` antes de qualquer etapa, para que a RN-005 o veja como zero.
JSON escrito em UTF-8, com `ensure_ascii=False` e `indent=2`.
**Alternativa descartada:** converter para float na saída, que perde as duas
casas (`60.0`); ou emitir string (`"60.00"`), que contradiz o tipo "número" da
spec.
**Consequência:** um ponto único de formatação, testado isoladamente.

### DT-006 — Erro geral e argumentos na CLI (revista na 2.0)

**Contexto:** a RN-013 diz que, em erro geral, o sistema "encerra com mensagem
de erro e não gera saída". A forma de encerrar é técnica. A 2.0 acrescenta os
documentos de política (obrigatório) e de câmbio (opcional).
**Decisão:**
- argumentos: `calcular --input <despesas> --politica <política> [--cambio
  <câmbio>] --output <resultado>`;
- `--input` e `--output` são obrigatórios no `argparse`. Faltando um deles, ou
  com argumento desconhecido, o código é **2** (padrão do `argparse`);
- `--politica` **não** é marcado como obrigatório no `argparse`. A falta do
  documento de política é um erro geral da RN-013/RN-015, tratado pela CLI
  como os demais: código **1**;
- `--cambio` é opcional. Sem ele, o motor recebe `cambio=None`, e as despesas
  em moeda estrangeira são recusadas com `COTACAO_INDISPONIVEL` (RN-018); as
  despesas em BRL não precisam dele;
- erro geral em qualquer documento (arquivo inexistente ou ilegível, JSON
  inválido, estrutura inválida): mensagem em **stderr**, código **1**, e o
  arquivo de saída **não é criado nem sobrescrito**. A CLI só abre o arquivo de
  saída depois que leitura, validação e cálculo terminaram sem erro;
- ordem de leitura: despesas, política, câmbio. O câmbio precisa da política já
  lida para comparar `moeda_base`.
Sucesso retorna 0.
**Alternativa descartada:** `--politica` obrigatório no `argparse`, que daria
código 2 para um caso que a spec classifica como erro geral; ou gravar um JSON
de erro no arquivo de saída, que contradiz "não gera saída".
**Consequência:** quem chama a CLI distingue sucesso de erro só pelo código de
saída; 2 sempre significa linha de comando mal formada.

### DT-007 — Normalização de texto

**Contexto:** a RN-002 manda remover espaços das pontas, maiúsculas e acentos.
**Decisão:** `strip()`, depois `casefold()`/`lower()`, depois
`unicodedata.normalize("NFD", s)` removendo caracteres de categoria `Mn`
(marcas combinantes). Nada mais é alterado: espaços internos ficam. Aplicada a
categoria, fornecedor, centro de custo e, no documento de política, às chaves
de categoria e de centro e à `periodicidade` (AMB-020, AMB-039).
Moeda tem normalização própria, `normalizar_moeda`: `strip()` e `upper()`
(RN-017), usada na despesa, nas chaves do câmbio e em `moeda_base`.
**Alternativa descartada:** biblioteca `unidecode`, que translitera além de
acentos e mudaria texto que a spec manda preservar.
**Consequência:** `Alimentação` → `alimentacao`, `ç` → `c`, `" usd "` → `USD`.

### DT-008 — Justificativas por template

**Contexto:** a seção 9 da spec exige saída determinística e justificativas que
citem a RN, o `id` da despesa mantida (duplicata), o limite já consumido e,
desde a 2.0, a origem da política e a moeda/data sem cotação.
**Decisão:** uma função por motivo em `justificativas.py`, com o mesmo texto dos
exemplos da seção 4 da spec. Valores formatados como `R$ 60,00`. Novas:
`cotacao_indisponivel(moeda, data)` e `origem(Origem)` (DT-011).
**Alternativa descartada:** montar o texto dentro de cada etapa, que espalharia
a formatação.
**Consequência:** os testes de regra verificam `status`, `motivo` e valores, e
checam na justificativa só a presença da RN, dos `id` citados e do texto de
origem. Isso evita testes frágeis a mudanças de redação.

### DT-009 — `Contexto` das etapas

**Contexto:** na 1.0, as etapas recebiam a despesa e o `Documento`. Agora
categoria, nota fiscal e limites precisam da política aplicável, e a conversão
precisa do câmbio.
**Decisão:** `calcular(documento, politica, cambio=None, etapas=None)` monta um
`Contexto(documento, politica: PoliticaAplicavel, cambio: Cambio | None)` e o
passa a todas as etapas no lugar do `Documento`.
**Alternativa descartada:** variáveis globais ou parâmetros diferentes por
etapa, que quebrariam a assinatura uniforme de `PorItem`/`EmGrupo`.
**Consequência:** a troca de assinatura é mecânica e atinge todas as etapas e os
testes que chamam etapas diretamente; o `Contexto` absorve dados futuros sem
mudar assinaturas de novo.

### DT-010 — Conversão de moeda

**Contexto:** a RN-018 converte pela data da despesa, com a última taxa anterior
disponível, e a RN-003 manda arredondar uma única vez, em reais. A conversão é a
etapa 3 da seção 8, antes de valor negativo.
**Decisão:**
- **BRL:** `entrada.py` já preenche `valor_considerado = arredondar(valor_informado)`,
  como na 1.0; a etapa de conversão deixa a despesa passar sem consultar o
  câmbio. Em BRL a conversão é a identidade (RN-003), então o resultado é o
  mesmo de convertê-la na etapa 3.
- **Outra moeda:** `entrada.py` deixa `valor_considerado = None`; a etapa de
  conversão chama `cambio.cotacao(moeda, data)`. A busca usa a lista
  `(data, taxa)` da moeda, ordenada, e `bisect_right` para achar a maior data
  ≤ data da despesa. Achou: `valor_considerado = arredondar(valor_informado ×
  taxa)`, com `taxa_cambio` e `data_cotacao` preenchidos. Não achou, ou
  `cambio is None`: recusa `COTACAO_INDISPONIVEL`.
- Os dois fatores são `Decimal` sem arredondamento; o produto usa o contexto
  decimal padrão (28 dígitos), suficiente para os valores do domínio.
**Alternativa descartada:** converter em `entrada.py`, que obrigaria a entrada a
conhecer o câmbio e tiraria `COTACAO_INDISPONIVEL` da ordem da seção 8.
Converter todas as moedas na etapa 3, inclusive BRL, mudaria a construção da
`Despesa` e os testes da 1.0 sem ganho de comportamento.
**Consequência:** todas as etapas de 4 em diante veem `valor_considerado` em
reais e nunca `None`. Despesa estrangeira sem cotação e também fora do período
recebe `COTACAO_INDISPONIVEL` (custo aceito na AMB-029).

### DT-011 — Origem da política como dado

**Contexto:** as justificativas de `LIMITE_DIARIO` e
`CATEGORIA_NAO_REEMBOLSAVEL` citam a origem (RN-016, AMB-037, AMB-038, AMB-040).
**Decisão:** `politica_aplicavel` devolve, por categoria, uma `Origem(tipo,
codigo)`. `justificativas.origem` transforma em texto:
- `PADRAO` → "política padrão";
- `CENTRO` → "centro de custo `<codigo>`";
- `HERDADA` → "centro de custo `<codigo>` usando limite herdado da política padrão";
- `NAO_CADASTRADO` → "política padrão; centro de custo `<codigo>` não cadastrado".
Para centro cadastrado, `codigo` é `Centro.codigo`, a grafia da chave no
documento de política. Para não cadastrado, é o valor da entrada só com
`strip()`, **sem** `normalizar_texto`.
**Alternativa descartada:** a seleção devolver o texto pronto, que misturaria
formatação com a regra de seleção.
**Consequência:** a seleção é testada pelo `tipo` e pelo `codigo`; o texto é
testado uma vez em `justificativas.py`.

### DT-012 — Validação dos documentos de política e de câmbio

**Contexto:** RN-015 e RN-018 listam os erros gerais de cada documento.
**Decisão:** `politica.py` e `cambio.py` usam os utilitários de `entrada.py`
(`ler_json` estrito, `data_valida`, `texto_preenchido`, número que não é `bool`)
e levantam a mesma `EntradaInvalida`, com mensagem que cita o documento e o
campo. Pontos de cuidado:
- chaves normalizadas que colidem (`Alimentação`/`alimentacao`, `CC-ADM`/` cc-adm `,
  `USD`/` usd `) são detectadas comparando o tamanho do dicionário antes e depois
  da normalização, por tabela/data;
- `moeda_base` da política: `normalizar_moeda` e igual a `BRL`; do câmbio:
  igual à da política após a mesma normalização;
- campos informativos (`versao`, `vigencia`, `acrescimo_em_viagem_percentual`,
  `observacao`, `fonte`) não são lidos.
**Alternativa descartada:** um módulo de validação genérico por esquema, que
seria maior que as duas validações juntas.
**Consequência:** a CLI trata os três documentos com o mesmo `except
EntradaInvalida`.

### DT-013 — Chave de duplicatas

**Contexto:** a RN-006 passou a exigir a mesma moeda e o mesmo valor original
arredondado na moeda original (AMB-030).
**Decisão:** a chave do grupo é `(data, categoria, fornecedor, moeda,
arredondar(valor_informado))`. Em BRL, `arredondar(valor_informado)` é o
próprio `valor_considerado`, então a regra da 1.0 é um caso particular.
**Alternativa descartada:** comparar `valor_considerado`, que juntaria 22,00 EUR
e 130,46 BRL.
**Consequência:** uma só fórmula para todas as moedas.

### DT-014 — Nota fiscal e limites lidos da política aplicável

**Contexto:** RN-007 e RN-008 passam a usar o limiar e os limites do documento;
RN-001 passa a recusar limite 0 (AMB-022).
**Decisão:**
- `categoria`: `limite is None or limite == 0` → `CATEGORIA_NAO_REEMBOLSAVEL`,
  com a origem na justificativa;
- `nota_fiscal`: `valor_considerado > politica.limiar_nota_fiscal` e sem nota →
  recusa. Como `valor_considerado` já está em reais, a AMB-028 sai de graça;
- `limites_por_data`: agrupa por `(data, categoria)` e usa `politica.regra(categoria)`;
  `representacao` não tem tratamento especial (AMB-023). O acréscimo em viagem
  não é lido (AMB-035).
**Alternativa descartada:** —
**Consequência:** as três etapas mudam só na origem do dado; a lógica da 1.0
fica igual.

## 6. Estratégia de testes

Estrutura:

```
tests/
  fabrica.py                                            # despesa(), documento(), politica_aplicavel()
  test_rn001_categoria.py ... test_rn018_cambio.py      # um arquivo por RN
  test_secao7_casos_de_borda.py                         # tabela da seção 7
  test_secao9_aceite_exemplo.py                         # exemplo original (CC-ENG-PLATAFORMA)
  test_secao9_aceite_envelope.py                        # dois documentos do envelope
  test_cli.py                                           # ponta a ponta via subprocess
  test_saida_serializacao.py                            # DT-005
  test_rastreabilidade.py                               # toda RN tem teste
```

- **Nível:**
  - **unitário** (~70%): regras, normalização, seleção da política, busca de
    cotação, sem I/O, com despesas montadas por `despesa(**campos)` e política
    por `politica_aplicavel(centro_custo=..., documento=...)`;
  - **integração** (~20%): `entrada` → `politica`/`cambio` → `motor` → `saida`
    a partir de texto;
  - **ponta a ponta** (~10%): CLI via `subprocess`, conferindo arquivo gerado,
    stderr e código de saída.
- **Política nos testes:** `fabrica.politica_aplicavel()` lê
  `exemplos/envelope/politica-v4.json` e devolve, por padrão, a política padrão,
  que tem os mesmos valores da v3. Testes de regra que dependem de centro de
  custo pedem o centro explicitamente. Testes de validação usam dicionários
  pequenos.
- **Cada `RN-NNN` da spec tem teste?** Há um arquivo `test_rnNNN_*.py` por regra,
  de RN-001 a RN-018, e o "Aceite" de cada RN vira pelo menos um teste nele. O
  `test_rastreabilidade.py` lê a `spec.md`, extrai os IDs `RN-\d{3}` e falha se
  algum não tiver arquivo de teste correspondente.
- **Casos de borda da seção 7 da spec:** um teste parametrizado com uma linha
  por caso da tabela (71 na spec 2.1). O `id` do parâmetro é o nome do caso na
  spec.
- **Aceite da seção 9 da spec:**
  - `exemplos/despesas-exemplo.json` com a política v4 e sem câmbio: 14 linhas
    e total 351,43;
  - `despesas-envelope.json` com política e câmbio: 10 linhas e total 1.143,26;
  - `despesas-envelope-cc-desconhecido.json`: 4 linhas e total 373,76.
- **Invariantes da seção 9 da spec:**
  - determinismo: duas execuções produzem saídas idênticas byte a byte;
  - RN-014: trocar todas as descrições não altera `valor_reembolsavel`,
    `status` nem `motivo`;
  - "todo item tem justificativa citando RN-xxx", verificado por regex.
- **DT-006:** em erro geral (inclusive política ausente ou inválida e câmbio
  inválido), o teste cria antes um arquivo de saída com conteúdo conhecido e
  confirma que ele continua igual depois da execução e que o código é 1.
  Argumento desconhecido ou `--input` ausente → código 2.
- **Nomenclatura:** `test_rnNNN_<comportamento>`, por exemplo
  `test_rn018_sabado_usa_taxa_de_sexta`. Testes de decisão técnica usam
  `test_dtNNN_<comportamento>`.

## 7. Riscos

| Risco | Probabilidade | O que faço se acontecer |
|---|---|---|
| Float vazar em algum ponto (parse, soma, literal no código, taxa) e errar uma fronteira | Média | DT-001 nos três documentos; teste para 10,005 → 10,01, 100,00 vs 100,01 e 33,333 USD × 5,42 → 180,66 |
| Arredondar duas vezes na conversão | Média | DT-010: um único `arredondar` sobre o produto; teste 180,66 vs 180,65 |
| Busca de cotação pegar a data seguinte em vez da anterior | Média | `bisect_right` − 1 (DT-010); testes de sábado (e-004), de data antes da primeira cotação e de data exata |
| Usar `round()` ou `ROUND_HALF_EVEN` por engano | Média | Uma única função de arredondamento em `normalizacao.py`, com teste de metade positiva e negativa |
| `-0.00` aparecer na saída ou não ser tratado como zero | Média | Normalização em `normalizacao.py` (DT-005) e caso da seção 7 (−0,004) |
| Serializador perder as duas casas, quantizar `taxa_cambio` ou falhar com `Decimal` em `colaborador`/`periodo` | Alta se não testado | `test_saida_serializacao.py` cobre os casos |
| `bool` aceito como número em `valor`, limite, limiar ou taxa | Média | Teste explícito em RN-013, RN-015 e RN-018 |
| `date.fromisoformat` aceitar formatos além de `AAAA-MM-DD` (também nas chaves do câmbio) | Alta (Python 3.11+ aceita mais formatos) | Regex antes do parse (DT-002) |
| Centro não cadastrado sair normalizado (`cc-suporte-n2`) na justificativa | Média | DT-011: só `strip()`; caso da seção 7 com `" CC-Suporte-N2 "` |
| `--politica` marcado como obrigatório no `argparse` e devolver 2 em vez de 1 | Média | DT-006; teste de CLI sem `--politica` esperando 1 e saída intacta |
| Troca de assinatura das etapas (DT-009) quebrar muitos testes de uma vez | Alta | Fazer a troca num único commit, junto com a `fabrica.politica_aplicavel()` |
| Testes de aceite da v3 mudarem de resultado quando o centro de custo passar a valer | Certa | Atualizar a tabela da seção 9 (585,43 → 351,43) e as justificativas da seção 4 no mesmo commit em que a seleção por centro de custo entra no fluxo real |
| Acentos não removidos em todos os casos (letras compostas, `ç`) | Baixa | DT-007, com testes para `Alimentação`, `ç` e maiúsculas acentuadas |
| Justificativa divergir dos exemplos da spec e o teste não pegar | Baixa | Testes da seção 9 checam RN citada, `id` e origem; os exemplos da seção 4 viram um teste de texto exato |
| Comportamento implementado sem regra na spec | Média | Toda dúvida de negócio que aparecer na implementação volta para a spec antes do código (regra do `CLAUDE.md`) |
