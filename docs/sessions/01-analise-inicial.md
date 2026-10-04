 ▐▛███▛█   Claude Code v2.1.288
▝▜██████▀  Opus 5.5 · API Usage Billing
 ▝▝   ▝▝   C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio


> Analise brevemente a estrutura deste projeto e me diga qual parece ser o      
  objetivo do desafio                                                           

  Read 4 files, ran 1 shell command (ctrl+o to expand)

● Objetivo do desafio

  É um exercício de Spec Driven Development (SDD): o fechamento de uma trilha de
  cursos da Anthropic Academy, com 2 dias de duração, feito individualmente com
  o Claude Code. O que se avalia é o processo, não o código. O produto
  funcionando vale só 10 dos 100 pontos (DESAFIO.md:15).

  O produto (pretexto)

  Uma CLI de motor de reembolso de despesas, com stack livre:
  <comando> calcular --input despesas.json --output resultado.json
  Ela lê despesas no formato de exemplos/despesas-exemplo.json e devolve, para
  cada item, o valor reembolsável e a justificativa. O formato da saída é você
  quem define.

  O trabalho de verdade

  A política de reembolso do RH (DESAFIO.md:42-52) tem 9 itens e pelo menos 8 
  ambiguidades propositais, dos três tipos abaixo (RUBRICA.md:27):
  - unidade de aplicação: o limite de "R$ 60 por dia" vale por dia ou por
    despesa?
  - fronteira: uma despesa de exatamente R$ 100,00 está "acima de R$ 100"?
  - dado ausente: o que é estar "em viagem", se a entrada não tem esse campo?

  Para cada uma, é preciso registrar, decidir e justificar na spec.md. O arquivo
  de exemplo foi montado para expor essas ambiguidades: cada item dele existe
  por um motivo.

  Pontuação (RUBRICA.md)

  ┌─────────────────────────────────────────────────────────────────┬────────┐
  │                            Critério                             │ Pontos │
  ├─────────────────────────────────────────────────────────────────┼────────┤
  │ Qualidade da spec (ambiguidades resolvidas, sem detalhe de      │ 25     │
  │ implementação)                                                  │        │
  ├─────────────────────────────────────────────────────────────────┼────────┤
  │ Rastreabilidade spec → tasks → commits → testes                 │ 25     │
  ├─────────────────────────────────────────────────────────────────┼────────┤
  │ Absorver a mudança de requisito surpresa do Dia 2               │ 20     │
  ├─────────────────────────────────────────────────────────────────┼────────┤
  │ Relatório pelos 4 Ds, com pelo menos um erro real do Claude que │ 20     │
  │  você pegou                                                     │        │
  ├─────────────────────────────────────────────────────────────────┼────────┤
  │ Produto funciona                                                │ 10     │
  └─────────────────────────────────────────────────────────────────┴────────┘

  Regras do jogo

  1. Todo commit referencia uma task, no formato feat(T-003): ....
  2. Regra de negócio explicada no chat e ausente da spec é bug de spec, e custa
     −5 por ocorrência.
  3. Cada sessão é exportada com /export para docs/sessions/.

  Estado atual do repositório

  Só o template foi copiado (commit d9423c6). A spec.md, o plan.md, o tasks.md e
  o CLAUDE.md ainda estão com os placeholders <...>. Ainda não existem src/,
  tests/ nem docs/sessions/.

  O cronograma (DESAFIO.md:156) pede, como próximo passo, escrever a spec.md,
  depois o plan.md e o tasks.md, antes de qualquer código. Um bom ponto de
  partida é percorrer o despesas-exemplo.json item por item contra a política
  para levantar as ambiguidades.

  Antes de começar, o README recomenda testar o /export agora, para não
  descobrir no Dia 2 que não há registro das sessões.

✻ Baked for 19s · done 17:36