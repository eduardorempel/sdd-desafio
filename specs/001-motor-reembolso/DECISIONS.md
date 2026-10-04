# Log de Decisões e Mudanças de Spec

> Uma entrada **toda vez** que a spec mudar. Este arquivo é a prova de que a spec
> foi tratada como artefato vivo e não como cerimônia de abertura.
>
> Spec que não muda em dois dias é spec que ninguém consultou. Mudança não é
> demérito — mudança não registrada é.

Ordem cronológica inversa: a mais recente primeiro.

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
