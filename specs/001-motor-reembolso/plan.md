# Plano Técnico — Motor de Cálculo de Reembolso

**Versão:** 1.0 · **Baseado na spec:** 1.1 (inclui D-001)

> Aqui mora o COMO. Este arquivo pode e deve falar de linguagem, biblioteca e
> arquitetura. O que ele **não** pode é introduzir regra de negócio nova — se
> apareceu uma, ela pertence à `spec.md`.

---

## 1. Stack

| Escolha | O quê | Por quê | O que descartei e por quê |
|---|---|---|---|
| Linguagem | Python 3.12+ | `decimal` e `json` na biblioteca padrão; nenhuma dependência de runtime; rápido de escrever em 2 dias | Node/TS: sem decimal nativo, e `JSON.parse` converte `33.333` em float antes de qualquer código nosso rodar. Go: cerimônia demais para um CLI deste tamanho |
| Testes | pytest | `parametrize` com `ids` legíveis cobre a tabela da seção 7 da spec linha a linha | `unittest`: verboso e com parametrização pobre |
| Parsing/validação | `json` da stdlib + validação manual | A RN-013 recusa uma despesa e segue com as outras; validação escrita à mão expressa isso direto | pydantic/jsonschema: falham o documento inteiro por padrão; adaptar ao "erro por despesa" custa mais do que escrever ~50 linhas |
| Aritmética monetária | `decimal.Decimal`, lido direto do JSON com `parse_float=Decimal` | Float no parse transforma `10.005` em `10.00499…`, que arredonda para 10,00 e quebra a RN-003. O tipo certo precisa existir desde a leitura | float (erro de representação); inteiro em centavos (exigiria arredondar já no parse, e `valor_informado` precisa do valor sem arredondamento) |
| CLI | `argparse` | Biblioteca padrão; há um único subcomando | click/typer: dependência sem ganho |
| Lint/format | ruff | Uma ferramenta para lint e formatação | flake8 + black |

**Comandos:**

- Rodar: `python -m reembolso calcular --input despesas.json --output resultado.json`
- Testes: `python -m pytest`
- Lint/format: `ruff check .` · `ruff format .`

## 2. Arquitetura

```
arquivo JSON
   │
   ▼
cli ──► entrada ──────────► motor ─────────────────────► saida ──► arquivo JSON
(I/O)   parse + validação   etapas 3–8 da seção 8        serialização
        (etapas 1–2)        (núcleo puro)                + total
```

| Módulo | Responsabilidade | Regras |
|---|---|---|
| `cli.py` / `__main__.py` | Argumentos, leitura e escrita de arquivo, mensagem de erro, código de saída | — |
| `entrada.py` | JSON → `Documento`. Detecta erro geral (exceção `EntradaInvalida`) e erro por despesa (`DADOS_INVALIDOS`). Constrói `Despesa` já normalizada e arredondada | RN-013, AMB-017 |
| `normalizacao.py` | Normalização de texto e arredondamento | RN-002, RN-003 |
| `politica.py` | Dados da política: categorias, limites, limiar da nota fiscal | RN-001, RN-007, RN-008 |
| `etapas.py` | Uma função por etapa da seção 8 da spec | RN-001, RN-004 a RN-010 |
| `motor.py` | Lista ordenada de etapas e execução | Seção 8 |
| `justificativas.py` | Templates de texto das justificativas e formatação `R$ 0,00` | Seção 4 (justificativa) |
| `saida.py` | `Resultado` → estrutura JSON, `null`, duas casas, total | Seção 4 (saída), RN-003 |
| `modelo.py` | Dataclasses e enums | — |

**Fronteiras:**

- Só `cli.py` toca disco, stdout e stderr.
- `entrada.py` recebe texto e devolve objetos; não abre arquivo.
- `motor.py`, `etapas.py`, `normalizacao.py` e `politica.py` não conhecem JSON
  nem arquivo. Recebem e devolvem objetos do `modelo.py`.

Essa divisão permite testar toda regra de negócio sem I/O, e uma mudança de
política tende a tocar só `politica.py` e `etapas.py`.

## 3. Modelo de dados

Todas as estruturas são `@dataclass(frozen=True)`.

```
Documento
  colaborador: dict          # cópia como veio, para a saída
  periodo: dict              # cópia como veio, para a saída
  inicio: date
  fim: date
  despesas: list[Despesa | Invalida]   # na ordem da entrada

Despesa                      # passou pela etapa 1 (RN-013)
  posicao: int               # 1, 2, 3...
  id: str
  data: date
  categoria: str             # normalizada (RN-002)
  fornecedor: str            # normalizado (RN-002)
  tem_nota_fiscal: bool
  valor_informado: Decimal   # sem arredondamento
  valor_considerado: Decimal # arredondado (RN-003)

Invalida                     # recusada na etapa 1
  posicao: int
  id: str | None             # None se o id for inválido
  valor_informado: Decimal | None   # None se ausente ou não numérico
  detalhe: str               # qual campo falhou, para a justificativa

Resultado
  id: str | None
  valor_informado: Decimal | None
  valor_considerado: Decimal | None # None quando DADOS_INVALIDOS
  valor_reembolsavel: Decimal
  status: Status
  motivo: Motivo | None             # None quando APROVADO
  justificativa: str
```

- `Status`: `APROVADO`, `LIMITADO`, `RECUSADO`, com valores iguais aos textos
  da spec (`"aprovado"`...).
- `Motivo`: os sete códigos da tabela de motivos da spec, com valor igual ao
  código (`"DUPLICATA"`...).
- A saída mantém um `Resultado` por posição. A lista final é montada por ordem
  de posição, o que garante "um item por despesa, na mesma ordem".

## 4. Como a política é representada

Os valores da política ficam **em um único módulo, `politica.py`, como dados**:

```python
CATEGORIAS_REEMBOLSAVEIS = frozenset({"alimentacao", "transporte_urbano", "hospedagem"})
LIMITE_POR_DATA = {
    "alimentacao": Decimal("60.00"),
    "transporte_urbano": Decimal("80.00"),
    "hospedagem": Decimal("250.00"),
}
LIMIAR_NOTA_FISCAL = Decimal("100.00")   # exige nota se valor > limiar (RN-007)
```

Cada constante tem um comentário com a RN de origem.

A **ordem das regras** também é dado, em `motor.py`:

```python
ETAPAS = [
    PorItem(valor_negativo),      # RN-005 → VALOR_NEGATIVO
    PorItem(periodo),             # RN-004 → FORA_DO_PERIODO
    PorItem(categoria),           # RN-001 → CATEGORIA_NAO_REEMBOLSAVEL
    EmGrupo(duplicatas),          # RN-006 → DUPLICATA
    PorItem(nota_fiscal),         # RN-007 → NOTA_FISCAL_AUSENTE
    EmGrupo(limites_por_data),    # RN-008, RN-009, RN-010 → LIMITE_DIARIO
]
```

- **Etapa por item:** recebe uma `Despesa` e devolve `None` (passa) ou uma recusa
  com motivo e justificativa.
- **Etapa em grupo:** recebe todas as despesas ainda vivas, em ordem de posição,
  e decide sobre o conjunto. A de duplicatas devolve recusas. A de limites
  devolve o valor reembolsável de cada despesa.
- As etapas 1 e 2 (validação, normalização e arredondamento) acontecem em
  `entrada.py`, porque precisam do JSON bruto. As despesas `Invalida` não entram
  no motor.
- Uma despesa recusada sai da lista viva e não chega às etapas seguintes. É isso
  que impede uma despesa recusada de consumir limite (seção 8 da spec).
- Ao final, uma despesa que chegou à etapa 8 é `APROVADO` se
  `valor_reembolsavel == valor_considerado`, senão `LIMITADO`, exatamente como a
  seção 4 da spec define.

## 5. Decisões técnicas

### DT-001 — `Decimal` desde o parse do JSON

**Contexto:** a RN-003 exige arredondamento comercial (10,005 → 10,01), e d-011
tem três casas.
**Decisão:** `json.loads(texto, parse_float=Decimal)`. Inteiros (`parse_int`)
também são convertidos para `Decimal` na validação. O arredondamento usa
`quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`, que no `Decimal` afasta a
metade do zero, inclusive para negativos.
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
  rejeitado com teste explícito de tipo;
- datas validadas com regex `^\d{4}-\d{2}-\d{2}$` e depois `date.fromisoformat`.
  O regex é necessário porque `fromisoformat` aceita formatos além de `AAAA-MM-DD`;
- texto "vazio" = `str.strip() == ""`;
- campos informativos e desconhecidos não são lidos pela validação.
**Alternativa descartada:** pydantic, que falha o documento inteiro por padrão.
**Consequência:** cada caso da RN-013 vira um `if` com teste próprio. Mais código
explícito, mas cada linha aponta para um item da spec.

### DT-003 — `NaN` e `Infinity` como documento ilegível

**Contexto:** a RN-013 (D-001) trata `NaN`/`Infinity` como JSON inválido, mas o
`json` do Python aceita esses literais por padrão.
**Decisão:** `parse_constant` levanta `EntradaInvalida`, o que vira erro geral.
**Alternativa descartada:** aceitar e rejeitar depois como valor não numérico.
Isso contradiria a spec.
**Consequência:** o parser fica estrito como a norma JSON.

### DT-004 — Política em módulo Python, pipeline como lista

**Contexto:** a mudança de requisito do dia 2 é desconhecida. É provável que ela
mexa em limites, categorias, ordem das regras ou crie uma regra nova.
**Decisão:** valores da política em `politica.py` e ordem das etapas em
`ETAPAS` (seção 4 deste plano).
**Alternativa descartada:** arquivo de configuração externo (JSON/YAML). Ele
exigiria validar a própria configuração e documentar um formato a mais, sem
ganho enquanto quem muda a política é quem muda o código.
**Consequência:** trocar um valor é uma linha. Uma regra nova é uma função mais
uma linha em `ETAPAS`. Se a política precisar variar por execução (por exemplo,
um dado de viagem na entrada), `politica.py` vira um objeto passado ao motor, e
isso é uma refatoração local.

### DT-005 — Serialização da saída

**Contexto:** a saída exige duas casas em `valor_considerado`,
`valor_reembolsavel` e `total_reembolsavel` (RN-003), `null` nos campos sem
valor (D-001), e `colaborador`/`periodo` copiados como vieram, que podem conter
`Decimal` do parse.
**Decisão:** `saida.py` monta a estrutura com `None` onde a spec pede nulo. Um
encoder próprio escreve todo `Decimal` como literal numérico JSON:
- os três campos monetários saem quantizados em duas casas (`60.00`);
- `valor_informado` sai com `str(Decimal)`, sem quantizar (`33.333`);
- zero negativo (`-0.00`, resultado de arredondar `-0.004`) é normalizado para
  `0.00` antes de qualquer etapa, para que a RN-005 o veja como zero.
JSON escrito em UTF-8, com `ensure_ascii=False` e `indent=2`.
**Alternativa descartada:** converter para float na saída, que perde as duas
casas (`60.0`); ou emitir string (`"60.00"`), que contradiz o tipo "número" da
spec.
**Consequência:** um ponto único de formatação, testado isoladamente.

### DT-006 — Erro geral na CLI

**Contexto:** a RN-013 diz que, em erro geral, o sistema "encerra com mensagem
de erro e não gera saída". A forma de encerrar é técnica.
**Decisão:**
- a mensagem vai para **stderr**;
- o código de saída é **1**;
- o arquivo de saída **não é criado nem sobrescrito**. A CLI só abre o arquivo
  de saída depois que leitura, validação e cálculo terminaram sem erro. Se um
  arquivo com esse nome já existir, ele fica intacto.
Sucesso retorna 0. Argumentos inválidos de linha de comando retornam 2 (padrão
do `argparse`).
**Alternativa descartada:** gravar um JSON de erro no arquivo de saída. Contradiz
"não gera saída".
**Consequência:** quem chama a CLI distingue sucesso de erro só pelo código de
saída.

### DT-007 — Normalização de texto

**Contexto:** a RN-002 manda remover espaços das pontas, maiúsculas e acentos.
**Decisão:** `strip()`, depois `casefold()`/`lower()`, depois
`unicodedata.normalize("NFD", s)` removendo caracteres de categoria `Mn`
(marcas combinantes). Nada mais é alterado: espaços internos ficam.
**Alternativa descartada:** biblioteca `unidecode`, que translitera além de
acentos e mudaria texto que a spec manda preservar.
**Consequência:** `Alimentação` → `alimentacao`, `ç` → `c`.

### DT-008 — Justificativas por template

**Contexto:** a seção 9 da spec exige saída determinística e justificativas que
citem a RN, o `id` da despesa mantida (duplicata) e o limite já consumido.
**Decisão:** uma função por motivo em `justificativas.py`, com o mesmo texto dos
exemplos da seção 4 da spec. Valores formatados como `R$ 60,00`.
**Alternativa descartada:** montar o texto dentro de cada etapa, que espalharia
a formatação.
**Consequência:** os testes de regra verificam `status`, `motivo` e valores, e
checam na justificativa só a presença da RN e dos `id` citados. Isso evita testes
frágeis a mudanças de redação.

## 6. Estratégia de testes

Estrutura:

```
tests/
  test_rn001_categoria.py ... test_rn014_descricao.py   # um arquivo por RN
  test_secao7_casos_de_borda.py                         # tabela da seção 7
  test_secao9_aceite_exemplo.py                         # exemplo completo
  test_cli.py                                           # ponta a ponta via subprocess
  test_saida_serializacao.py                            # DT-005
  test_rastreabilidade.py                               # toda RN tem teste
```

- **Nível:**
  - **unitário** (~70%): regras e normalização, sem I/O, com despesas montadas
    por um helper `despesa(**campos)`;
  - **integração** (~20%): `entrada` → `motor` → `saida` a partir de dicts;
  - **ponta a ponta** (~10%): CLI via `subprocess`, conferindo arquivo gerado,
    stderr e código de saída.
- **Cada `RN-NNN` da spec tem teste?** Há um arquivo `test_rnNNN_*.py` por regra,
  e o "Aceite" de cada RN vira pelo menos um teste nele. O
  `test_rastreabilidade.py` lê a `spec.md`, extrai os IDs `RN-\d{3}` e falha se
  algum não tiver arquivo de teste correspondente.
- **Casos de borda da seção 7 da spec:** um teste parametrizado com uma linha
  por caso da tabela. O `id` do parâmetro é o nome do caso na spec, então o
  relatório do pytest lista os casos com os mesmos nomes da spec.
- **Aceite da seção 9 da spec:** roda `exemplos/despesas-exemplo.json` e
  compara as 14 linhas (`valor_reembolsavel`, `status`, `motivo`) e o total
  585,43.
- **Invariantes da seção 9 da spec:**
  - determinismo: duas execuções produzem saídas idênticas byte a byte;
  - RN-014: trocar todas as descrições não altera `valor_reembolsavel`,
    `status` nem `motivo`;
  - "todo item tem justificativa citando RN-xxx", verificado por regex.
- **DT-006:** em erro geral, o teste cria antes um arquivo de saída com conteúdo
  conhecido e confirma que ele continua igual depois da execução.
- **Nomenclatura:** `test_rnNNN_<comportamento>`, por exemplo
  `test_rn007_valor_exatamente_100_nao_exige_nota`. Testes de decisão técnica
  usam `test_dtNNN_<comportamento>`.

## 7. Riscos

| Risco | Probabilidade | O que faço se acontecer |
|---|---|---|
| Float vazar em algum ponto (parse, soma, literal no código) e errar uma fronteira | Média | DT-001; constantes sempre como `Decimal("…")`; teste para 10,005 → 10,01 e para 100,00 vs 100,01 |
| Usar `round()` ou `ROUND_HALF_EVEN` por engano | Média | Uma única função de arredondamento em `normalizacao.py`, com teste de metade positiva e negativa |
| `-0.00` aparecer na saída ou não ser tratado como zero | Média | Normalização em `normalizacao.py` (DT-005) e caso da seção 7 (−0,004) |
| Serializador perder as duas casas (`60.0`) ou falhar com `Decimal` em `colaborador`/`periodo` | Alta se não testado | `test_saida_serializacao.py` cobre os dois casos |
| `bool` aceito como número em `valor` | Média | Teste explícito em RN-013 |
| `date.fromisoformat` aceitar formatos além de `AAAA-MM-DD` | Alta (Python 3.11+ aceita mais formatos) | Regex antes do parse (DT-002) |
| Acentos não removidos em todos os casos (letras compostas, `ç`) | Baixa | DT-007, com testes para `Alimentação`, `ç` e maiúsculas acentuadas |
| Mudança do dia 2 exigir reestruturação | Média | DT-004. Se a mudança não couber em `politica.py` ou `ETAPAS`, registrar o motivo no `DECISIONS.md` e na seção 5 deste plano |
| Justificativa divergir dos exemplos da spec e o teste não pegar | Baixa | Testes da seção 9 checam RN citada e `id`; os exemplos da seção 4 viram um teste de texto exato |
| Comportamento implementado sem regra na spec | Média | Toda dúvida de negócio que aparecer na implementação volta para a spec antes do código (regra do `CLAUDE.md`) |
