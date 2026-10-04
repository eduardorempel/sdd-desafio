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

✻ Baked for 19s · done sábado, 17:36

> /export                                                                       
  ⎿  Conversation exported to:
     C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\01-analise-inicial.md

> Antes de alterar qualquer arquivo, leia:                                      
  - DESAFIO.md                                                                  
  - RUBRICA.md                                                                  
  - FAQ.md                                                                      
  - CLAUDE.md                                                                   
  - exemplos/despesas-exemplo.json                                              
  - specs/001-motor-reembolso/spec.md                                           
    QQuero começar a especificação do motor de reembolso.Neste momento NÃO      
  altere nenhum arquivo.Analise a política de reembolso junto com o JSON de     
  exemplo e                                                                     
    identifique todas as ambiguidades que precisam ser resolvidas. Para cada    
  ambiguidade, explique o que não está claro, mostre qual caso do JSON          
  evidencia o problema, apresente as possíveis interpretações e diga qual você  
  recomenda, justificando brevemente. Não tome decisões por mim e não escreva a 
  spec ainda; quero revisar essas decisões primeiro                             

  Read 2 files (ctrl+o to expand)

● Li os seis arquivos e cruzei a política com cada item do
  despesas-exemplo.json. Encontrei 15 ambiguidades, e uma 16ª questão que
  atravessa todas: a ordem de aplicação das regras. Classifiquei cada uma pelos
  três tipos da RUBRICA.md:27: [U] unidade de aplicação, [F] fronteira, [D] dado
  ausente. Não alterei nenhum arquivo, e as recomendações abaixo são só
  sugestões.

  ---

  AMB-01 [U] Limite diário: soma do dia ou valor de cada despesa?

  - Não está claro: se "R$ 60 por dia" limita a soma das despesas da categoria
    no dia ou cada despesa separadamente.
  - Evidência: d-001 (72,50) e d-002 (38,00), as duas de alimentação em 03/07.
  - Interpretações:
    - (a) Limite sobre a soma do dia: paga 60,00 no total.
    - (b) Limite por despesa: paga 60,00 + 38,00 = 98,00.
  - Recomendo (a). O texto diz "por dia", e a leitura (b) deixaria o limite ser
    contornado dividindo a conta.

  AMB-02 [U] Como dividir o limite do dia entre as despesas

  - Não está claro: a saída é por item. Se o dia estoura o limite, falta definir
    quanto cabe a cada despesa.
  - Evidência: d-001 e d-002.
  - Interpretações:
    - (a) Ordem da entrada: d-001 recebe 60,00 e d-002 recebe 0,00.
    - (b) Proporcional: cada item recebe 60/110,50 do seu valor (39,37 e 20,63).
    - (c) Maior valor primeiro.
  - Recomendo (a). É determinística, fácil de verificar à mão e simples de
    explicar na justificativa ("limite diário já consumido por d-001").

  AMB-03 [U] O que significa "reembolsadas parcialmente"

  - Não está claro: se paga até o limite e corta o excedente, ou se recusa o
    item inteiro.
  - Evidência: d-014 (61,00, só R$ 1 acima do limite) e d-001.
  - Interpretações:
    - (a) Paga até o limite e corta o excedente: d-014 recebe 60,00.
    - (b) Recusa o item inteiro: d-014 recebe 0,00.
  - Recomendo (a). "Parcialmente" só faz sentido se alguma parte for paga.

  AMB-04 [F] "Acima de R$ 100": o valor de exatamente R$ 100,00 está incluído?

  - Evidência: d-003 (100,00 sem nota) e d-004 (100,01 sem nota). O par está no
    arquivo justamente para testar essa fronteira.
  - Interpretações:
    - (a) Exige nota só quando o valor é maior que 100,00. d-003 não exige nota,
      d-004 exige.
    - (b) Exige nota a partir de 100,00, inclusive.
  - Recomendo (a). É a leitura literal de "acima de".

  AMB-05 [U] Nota fiscal: sobre qual valor a regra incide, e o que acontece 
  quando ela falta

  - Não está claro:
    - Base do valor: a regra pode olhar o valor original do item, o valor depois
      do limite ou o total do dia.
    - Consequência: sem nota, a despesa pode ser recusada inteira ou paga até
      R$ 100.
  - Evidência:
    - d-004 (100,01): depois do limite de 80 viraria 80,00, abaixo de 100, e
      deixaria de exigir nota.
    - d-003 + d-004 somam 200,01 no dia.
    - d-013 (690,00, sem nota).
  - Interpretações:
    - Base: (a) valor original do item, (b) valor depois do limite, (c) total do
      dia.
    - Consequência: (x) recusa o item inteiro, (y) paga até 100,00.
  - Recomendo base (a) e consequência (x). A nota comprova o gasto efetivamente
    feito, não o valor pago no reembolso. "Obrigatória" indica que, sem ela, a
    despesa não é aceita.

  AMB-06 [D] O que caracteriza estar "em viagem"

  - Não está claro: a entrada não tem campo que indique viagem.
  - Evidência:
    - d-003 "Corrida aeroporto".
    - d-010 "Hotel Rio".
    - d-011 "Café da manhã hotel".
  - Interpretações:
    - (a) Nunca aplicar a ampliação, por falta de dado. A regra 6 fica declarada
      como inaplicável.
    - (b) Considerar em viagem os dias cobertos por uma hospedagem: da data da
      hospedagem até a data mais o número de diárias. Para d-010 com 2 diárias,
      isso dá de 14/07 a 16/07.
    - (c) Procurar palavras na descrição, como "aeroporto" ou "hotel".
    - (d) Aceitar um campo opcional novo na entrada.
  - Recomendo (b). Usa só dado estruturado que já existe e é verificável. A (c)
    é frágil. A (d) muda o formato de entrada, que o desafio pede para
    respeitar, e os casos ocultos do avaliador não trariam esse campo. Depende
    de AMB-08.

  AMB-07 [U] A ampliação de 50% vale para quais categorias?

  - Não está claro: se vale para as três categorias, incluindo hospedagem.
  - Evidência: d-010. Se a própria hospedagem caracteriza a viagem e a ampliação
    valesse para ela, o limite efetivo seria sempre 375,00, e os 250,00 nunca
    se aplicariam.
  - Interpretações:
    - (a) As três categorias.
    - (b) Só alimentação e transporte urbano. Com isso, os limites em viagem
      ficam em 90,00 e 120,00.
  - Recomendo (b). Evita a circularidade e mantém o limite de hospedagem com
    sentido.

  AMB-08 [D] Quantas diárias tem uma despesa de hospedagem?

  - Não está claro: o limite é "por diária", mas não há campo com o número de
    diárias. A informação só aparece no texto livre da descrição.
  - Evidência:
    - d-010: 480,00, "2 diarias" (240 por diária, dentro do limite).
    - d-013: 690,00, "3 noites" (230 por noite).
  - Interpretações:
    - (a) Cada registro vale 1 diária: d-010 recebe 250,00.
    - (b) Extrair o número da descrição: d-010 recebe 480,00.
    - (c) Campo opcional de diárias na entrada, valendo 1 quando ausente.
  - Recomendo (b), restrita. Aceitar só o padrão "N diária(s)/noite(s)" e,
    quando não houver número, considerar 1 diária e dizer isso na justificativa.
    A (a) é conservadora, mas pune um caso legítimo visível no próprio dado.
  - Ponto fraco a avaliar: usar texto livre como dado é frágil. Talvez você
    prefira a (a) justamente por isso.

  AMB-09 [D/F] O que é "lançada dentro do período de competência"

  - Não está claro:
    - Datas: a entrada só traz a data da despesa, sem data de lançamento.
    - Bordas: não se sabe se o primeiro e o último dia do período contam.
    - Conflito: não há regra para o caso de competencia e inicio/fim
      discordarem.
  - Evidência:
    - d-008 (15/04, "lançado com atraso").
    - d-014 (31/07, último dia do período).
  - Interpretações:
    - (a) A data da despesa precisa estar entre inicio e fim, com as bordas
      incluídas. d-008 é recusada.
    - (b) Aceitar despesas atrasadas dentro de uma tolerância, por exemplo 90
      dias.
  - Recomendo (a), com inicio/fim prevalecendo sobre competencia. Não há data de
    lançamento, e qualquer tolerância seria inventada.

  AMB-10 [U] Duplicatas: o que conta como duplicata e como tratar

  - Evidência: d-006 e d-007 são idênticas (mesma data, categoria, fornecedor,
    valor e descrição) e só o id muda.
  - Interpretações sobre o que é duplicata:
    - (a) Mesma data, categoria, fornecedor e valor.
    - (b) A regra (a) mais a mesma descrição.
  - Interpretações sobre o tratamento:
    - (x) Mantém a primeira e recusa as demais.
    - (y) Recusa todas.
    - (z) Só sinaliza e paga.
  - Recomendo (a) com (x). A descrição é texto livre e não deveria evitar a
    detecção. Recusar todas puniria a despesa legítima.
  - Impacto da ordem: se a duplicata sai antes do limite diário, paga 54,90. Se
    as duas entram no limite, paga 60,00. Ver AMB-16.

  AMB-11 [D] Valores negativos (estornos)

  - Não está claro: a política não fala de estorno.
  - Evidência: d-009 (−45,00, "Estorno de corrida cancelada"). A corrida
    original não está nesta entrada.
  - Interpretações:
    - (a) Ignorar: reembolso 0,00, sem afetar outros itens.
    - (b) Abater do limite de transporte do mesmo dia.
    - (c) Abater do total do período.
    - (d) Tratar como entrada inválida.
  - Recomendo (a). A despesa original não está no período, então não há o que
    compensar. Abater de despesas sem relação seria inventar uma regra.

  AMB-12 [F] Arredondamento

  - Não está claro: a política não define precisão nem regra de arredondamento.
  - Evidência: d-011 (33,333, com três casas decimais).
  - Interpretações:
    - (a) Arredondar o valor de entrada para centavos, com 0,005 arredondado
      para cima, antes de qualquer regra.
    - (b) Arredondar só na saída.
    - (c) Truncar.
  - Recomendo (a). Dinheiro trabalha com centavos, e arredondar antes deixa as
    comparações de fronteira, como em AMB-04, sem efeito de casas fracionárias.

  AMB-13 [F] Categoria escrita de outro jeito

  - Não está claro: se a categoria deve bater exatamente com o nome da política
    ou se variações de escrita são aceitas.
  - Evidência: d-014 ("ALIMENTACAO", em maiúsculas).
  - Interpretações:
    - (a) Ignorar maiúsculas, acentos e espaços nas pontas.
    - (b) Exigir o nome exato, o que recusa d-014 por categoria desconhecida.
  - Recomendo (a). É erro de digitação, não uma categoria diferente. Recusar
    seria punir a forma e não o conteúdo.

  AMB-14 [U] O que conta como categoria "fora da política"

  - Não está claro: se a lista de categorias reembolsáveis é fechada nas três da
    política ou se cabem categorias parecidas.
  - Evidência: d-005 (coworking).
  - Interpretações:
    - (a) Lista fechada: só alimentação, transporte urbano e hospedagem.
    - (b) Encaixar coworking em alguma categoria parecida.
  - Recomendo (a). É o que diz a regra 9, e encaixar por semelhança seria criar
    política.

  AMB-15 [U] Fim de semana e feriado

  - Não está claro: se "por dia" quer dizer qualquer dia do calendário ou só
    dias úteis.
  - Evidência: d-012 (sábado, "plantão").
  - Interpretações:
    - (a) Sem restrição: todo dia do calendário conta.
    - (b) Recusar despesas de fim de semana.
  - Recomendo (a). A política não restringe, e plantão é trabalho legítimo.

  AMB-16 Ordem de aplicação das regras

  Várias decisões acima mudam de resultado conforme a ordem, por exemplo
  d-006/d-007 em AMB-10 e d-004 em AMB-05. A ordem que recomendo:

  1. Normalizar: arredondar o valor e padronizar a categoria.
  2. Validar o item: valor negativo, data fora do período, categoria fora da
     política.
  3. Duplicatas.
  4. Nota fiscal, sobre o valor original.
  5. Limites diários e por diária, já com a ampliação de viagem. Só os itens que
     passaram pelas etapas anteriores consomem o limite do dia.

  Justificativa: uma despesa recusada não deveria ocupar o limite de uma despesa
  válida.

  ---

  Quando você tiver decidido, posso escrever a spec.md com essas seções AMB-xx e
  as regras RN correspondentes.

  Um detalhe do processo: o /export salvou o arquivo 01-analise-inicial.md na
  raiz do repositório, e o desafio pede que ele fique em docs/sessions/. Não
  mexi nele porque você pediu para não alterar nada.

✻ Crunched for 1m 46s · done 0:14

> Gostei da análise, mas não quero aprovar tudo automaticamente.                
                                                                                
  Antes de fechar as decisões, quero revisar especificamente                    
  AMB-06, AMB-07 e AMB-08.                                                      
                                                                                
  Na AMB-06, você recomenda inferir “em viagem” a partir de hospedagem,         
  mas a própria entrada não possui um campo estruturado indicando viagem.       
                                                                                
  Compare estas duas alternativas:                                              
                                                                                
  nunca aplicar a ampliação de 50% porque o dado “em viagem” não existe;        
  inferir viagem a partir de hospedagem.                                        
                                                                                
  Para cada alternativa, explique:                                              
  vantagens                                                                     
  riscos                                                                        
  impacto sobre os casos do JSON                                                
  qual delas é mais defensável para uma spec verificável                        
                                                                                
  Depois faça o mesmo tipo de comparação para:                                  
  AMB-07 ampliação de 50% valer para todas as categorias ou só                  
  alimentação/transporte                                                        
  AMB-08 inferir quantidade de diárias pelo texto livre ou tratar cada          
  hospedagem como 1 diária                                                      
                                                                                
  Não altere arquivos ainda                                                     

● Revendo as três com mais cuidado, mudei de recomendação em AMB-06 e AMB-08.
  Nas duas, o que pesou foi o critério de spec verificável que você destacou.
  Não alterei nenhum arquivo.

  ---

  AMB-06: "em viagem"

  Alternativa 1: nunca aplicar a ampliação

  Vantagens
  - A regra é trivial de verificar: o limite é sempre 60/80/250, sem nenhuma
    condição.
  - Não depende de outras decisões incertas.
  - É coerente com o critério da nota fiscal: o que não está comprovado não é
    pago.

  Riscos
  - A regra 6 da política fica sem efeito, e um colaborador realmente em viagem
    recebe menos do que o RH pretendia.
  - A spec precisa declarar isso de forma explícita, em "Fora de escopo" e em "O
    que fica em aberto". Se não declarar, parece que a regra foi esquecida.

  Alternativa 2: inferir viagem a partir de hospedagem

  Vantagens
  - Mantém a regra 6 viva usando só dados que já existem.
  - Hospedagem é um indício forte de viagem.

  Riscos
  - Deixa de pegar viagens óbvias. d-003 ("Corrida aeroporto") e d-004 ("Corrida
    hotel") são de 06/07, e não há hospedagem nesse dia. Pela regra, não
    estariam em viagem. A inferência erra justamente no caso mais evidente do
    arquivo.
  - Encadeia inferências. A janela de viagem depende do número de diárias
    (AMB-08), que por sua vez depende de texto livre ou de uma suposição.
  - Abre uma questão nova: uma hospedagem recusada, como d-013 sem nota, ainda
    caracteriza viagem? Se sim, um lançamento sem nota amplia os limites dos
    outros itens. Se não, a viagem existiu mas é ignorada.
  - Abre brecha para manipulação: lançar uma hospedagem barata amplia os limites
    de alimentação e transporte.

  Impacto no JSON

  ┌───────────────────┬───────────────┬─────────────────────────────────────┐
  │       Item        │    Alt. 1     │               Alt. 2                │
  ├───────────────────┼───────────────┼─────────────────────────────────────┤
  │ d-003 (06/07)     │ limite 80     │ limite 80 (sem hospedagem no dia)   │
  ├───────────────────┼───────────────┼─────────────────────────────────────┤
  │ d-011 (15/07,     │ 33,33         │ 33,33 (em viagem, mas já está       │
  │ 33,33)            │               │ abaixo de 60)                       │
  ├───────────────────┼───────────────┼─────────────────────────────────────┤
  │ dias 22 a 25/07   │ nenhuma       │ nenhuma despesa                     │
  │                   │ despesa       │                                     │
  └───────────────────┴───────────────┴─────────────────────────────────────┘

  No arquivo de exemplo, as duas alternativas dão exatamente o mesmo resultado.
  A diferença só aparece em casos ocultos.

  Mais defensável

  Alternativa 1. A Alternativa 2 tem riscos demais para um ganho que não aparece
  em nenhum caso do exemplo. A Alternativa 1 é verificável, honesta sobre a
  falta do dado e fácil de mudar se um dia surgir um campo de viagem.

  ---

  AMB-07: a ampliação vale para quais categorias

  Todas as categorias

  - Vantagem: é a leitura literal, porque o item 6 fala em "limites ampliados"
    sem restringir.
  - Risco: se a viagem for inferida pela hospedagem (AMB-06, alt. 2), toda
    hospedagem estará em viagem. O limite real passa a ser sempre 375, e os 250
    do item 3 nunca valem. Sem essa inferência, não há esse problema.

  Só alimentação e transporte

  - Vantagem: elimina a circularidade e preserva o limite de 250.
  - Risco: adiciona uma restrição que o RH não escreveu.

  Impacto no JSON

  Só d-010 é afetada, e apenas se a ampliação estiver ativa:
  - Contada como 1 diária: paga 375 com todas as categorias, ou 250 só com
    alimentação e transporte.
  - Contada como 2 diárias: paga 480 nos dois casos, porque fica abaixo do
    limite.

  d-013 é recusada de qualquer forma por falta de nota.

  Mais defensável

  Depende de AMB-06.
  - Com a alternativa 1: a pergunta perde o objeto. A spec deve registrar
    explicitamente que ela não se aplica enquanto não houver o dado de viagem,
    em vez de silenciar.
  - Com a alternativa 2: só alimentação e transporte, por causa da
    circularidade.

  ---

  AMB-08: número de diárias

  Ler o número no texto livre

  Vantagens
  - Reflete o que o dado mostra: d-010 é de fato de 2 diárias.
  - Paga corretamente casos legítimos.

  Riscos
  - Texto livre não é um formato garantido: a mesma informação pode vir como "2
    diarias", "3 noites", "duas diárias", "pernoite" ou "3 dias". Este último
    pode significar 2 noites.
  - Exige uma lista fechada de padrões aceitos: sem ela, a spec não é
    verificável.
  - Permite manipulação: escrever "5 diárias" quintuplica o limite, sem nada que
    confira.
  - Contradiz AMB-10: ali eu recomendei ignorar a descrição na detecção de
    duplicatas.

  Tratar cada registro como 1 diária

  Vantagens
  - Determinístico e verificável.
  - Usa só campos estruturados.
  - Deixa uma orientação clara de processo: estadias de várias noites são
    lançadas com um registro por diária.

  Riscos
  - Paga menos em casos legítimos.
  - O próprio exemplo mostra isso: d-010 recebe 250, embora o texto indique 240
    por diária.

  Impacto no JSON

  ┌─────────────────────────────────┬────────────┬──────────┐
  │              Item               │ Pelo texto │ 1 diária │
  ├─────────────────────────────────┼────────────┼──────────┤
  │ d-010 (480, 2 diárias)          │ 480,00     │ 250,00   │
  ├─────────────────────────────────┼────────────┼──────────┤
  │ d-013 (690, 3 noites, sem nota) │ 0,00       │ 0,00     │
  └─────────────────────────────────┴────────────┴──────────┘

  Mais defensável

  1 diária. Ela permite um princípio único e coerente em toda a spec: decisões 
  usam apenas campos estruturados; a descrição nunca altera um cálculo. Esse
  princípio sustenta AMB-06, AMB-08 e AMB-10 ao mesmo tempo, e é fácil de
  defender no relatório.

  O custo, o pagamento menor de d-010, fica registrado em "O que fica em
  aberto".

  ---

  Resumo das combinações

  ┌─────────────┬────────────┬──────────────┬────────┬────────┬────────────┐
  │             │            │              │        │        │ Diferenças │
  │ Combinação  │   AMB-06   │    AMB-07    │ AMB-08 │ d-010  │     no     │
  │             │            │              │        │        │  exemplo   │
  ├─────────────┼────────────┼──────────────┼────────┼────────┼────────────┤
  │ A           │ sem        │ não se       │ 1      │ 250,00 │ —          │
  │ (recomendo) │ ampliação  │ aplica       │ diária │        │            │
  ├─────────────┼────────────┼──────────────┼────────┼────────┼────────────┤
  │             │ inferir    │ só           │ pelo   │        │            │
  │ B           │ pela       │ alimentação  │ texto  │ 480,00 │ só d-010   │
  │             │ hospedagem │ e transporte │        │        │            │
  └─────────────┴────────────┴──────────────┴────────┴────────┴────────────┘

  No arquivo de exemplo, a única diferença concreta entre as combinações é d-010
  (250 ou 480). Na prática, você escolhe entre spec verificável e pagamento
  mais próximo da realidade do dado.

  Quais decisões você quer adotar para essas três? Com elas e as demais
  aprovadas, sigo para a escrita da spec.md.

✻ Churned for 54s · done 0:36

> Vamos ficar com:                                                              
  AMB-06 - não aplicar os 50% porque não existe esse dado de viagem na entrada  
  AMB-07- então essa regra fica sem aplicar por enquanto                        
  AMB-08 cada hospedagem vale 1 diária. Não usa a descrição pra calcular        
                                                                                
  As outras eu aprovo como você sugeriu                                         
                                                                                
  Só me faz um resumo final das 16 decisões e vê se alguma entra em conflito    
  com outra                                                                     
                                                                                
  Ainda não altera arquivo                                                      

● Resumo das 16 decisões

  ┌─────┬──────────────────┬────────────────────────────────────────────────┐
  │  #  │       Tema       │                    Decisão                     │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 01  │ Unidade do       │ Limite sobre a soma do dia, por categoria      │
  │     │ limite           │                                                │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 02  │ Divisão do       │ Pela ordem de entrada: a primeira despesa      │
  │     │ limite no dia    │ consome o limite primeiro                      │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 03  │ Reembolso        │ Paga até o limite e corta o excedente          │
  │     │ parcial          │                                                │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 04  │ Fronteira da     │ Exigida só quando o valor é maior que 100,00;  │
  │     │ nota fiscal      │ exatamente 100,00 não exige                    │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │     │ Base e efeito da │ Usa o valor do item, não o do dia nem o valor  │
  │ 05  │  nota            │ depois do limite; sem nota, a despesa é        │
  │     │                  │ recusada inteira                               │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 06  │ "Em viagem"      │ Ampliação de 50% nunca aplicada, porque a      │
  │     │                  │ entrada não tem o dado                         │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 07  │ Alcance da       │ Não se aplica enquanto valer a AMB-06          │
  │     │ ampliação        │                                                │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 08  │ Diárias de       │ Cada registro vale 1 diária; a descrição nunca │
  │     │ hospedagem       │  entra no cálculo                              │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │     │                  │ A data da despesa precisa estar entre inicio e │
  │ 09  │ Competência      │  fim, com as bordas incluídas; se houver       │
  │     │                  │ conflito, inicio/fim prevalecem sobre          │
  │     │                  │ competencia                                    │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 10  │ Duplicatas       │ Mesma data, categoria, fornecedor e valor;     │
  │     │                  │ mantém a primeira e recusa as demais           │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 11  │ Estorno (valor   │ Reembolso 0,00, sem abater de outros itens     │
  │     │ negativo)        │                                                │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 12  │ Arredondamento   │ Valor de entrada arredondado para centavos     │
  │     │                  │ (0,005 sobe) antes de qualquer regra           │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 13  │ Grafia da        │ Ignora maiúsculas, acentos e espaços nas       │
  │     │ categoria        │ pontas                                         │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 14  │ Categorias       │ Lista fechada: alimentação, transporte urbano  │
  │     │ aceitas          │ e hospedagem                                   │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │ 15  │ Fim de semana    │ Sem restrição: todo dia do calendário conta    │
  ├─────┼──────────────────┼────────────────────────────────────────────────┤
  │     │ Ordem de         │ Normalizar → validar (valor negativo, período, │
  │ 16  │ aplicação        │  categoria) → duplicatas → nota fiscal →       │
  │     │                  │ limites. Itens recusados não consomem limite   │
  └─────┴──────────────────┴────────────────────────────────────────────────┘

  Princípio que atravessa a spec: só campos estruturados decidem cálculos; a 
  descrição é apenas informativa.

  ---

  Conflitos encontrados

  Conflito 1: AMB-01 contra AMB-08 (hospedagem por dia ou por registro?)

  A AMB-01 soma os valores do dia por categoria. A AMB-08 diz que cada registro
  de hospedagem é 1 diária. Com dois registros de hospedagem na mesma data, as
  duas regras dão resultados diferentes:
  - Pela AMB-08: cada registro tem limite de 250, e o dia pode chegar a 500.
  - Pela AMB-01: a soma do dia fica limitada a 250.

  O arquivo de exemplo não tem esse caso, mas um caso oculto pode ter.

  Sugestão: somar também a hospedagem por dia, com limite de 250 por data. Com 1
  diária por registro, "por diária" e "por dia" passam a significar a mesma
  coisa, e a regra fica uniforme para as três categorias. Também faz sentido de
  negócio: uma pessoa só dorme em um lugar por noite.

  Conflito 2: AMB-10 contra AMB-05 e AMB-16 (duplicata que difere só na nota 
  fiscal)

  O critério de duplicata não olha tem_nota_fiscal, e as duplicatas são tratadas
  antes da nota. Exemplo:
  - d-x vale 150,00, sem nota, e é lançada primeiro.
  - d-y vale 150,00, com nota, mesmos data, categoria e fornecedor.

  d-x é mantida e depois recusada por falta de nota. d-y é recusada como
  duplicata. Nada é pago, mesmo havendo um comprovante válido.

  Incluir a nota no critério de duplicata não resolve: para valores de até 100,
  os dois itens seriam pagos, ou seja, pagamento em dobro.

  Sugestão: entre duplicatas, manter a que tem nota fiscal. Se as duas tiverem
  nota, ou nenhuma tiver, mantém a primeira na ordem de entrada.

  ---

  Pontos que não são conflito, mas precisam de redação precisa

  1. Valor considerado na AMB-05: a nota fiscal deve ser avaliada sobre o valor
     já arredondado (AMB-12). Assim, 100,004 vira 100,00 e não exige nota.
  2. Comparação de duplicatas na AMB-10: categoria e valor são comparados depois
     de normalizados. Falta decidir como comparar o fornecedor: texto exato ou
     com a mesma normalização da categoria (AMB-13)? Sugiro a mesma
     normalização, por coerência.
  3. "Ordem de entrada" nas AMB-02 e AMB-10: não é um campo, mas é
     determinística e verificável. Vale escrever na spec que essa ordem é a
     posição do item na lista de despesas.
  4. Lacuna pequena: valor zero. Nenhuma decisão cobre esse caso. Sugiro tratar
     como válido, com reembolso de 0,00 e uma justificativa.

  Fora isso, não encontrei conflitos. Com a ordem da AMB-16, as demais decisões
  se combinam sem contradição.

  Para fechar, preciso que você decida:
  1. A sugestão do conflito 1.
  2. A sugestão do conflito 2.
  3. A comparação de fornecedor (item 2 acima).
  4. O valor zero (item 4 acima).

  Depois disso, a spec.md pode ser escrita.

✻ Churned for 44s · done 0:43

> Fechou, vamos assim:                                                          
                                                                                
  1. hospedagem também soma por dia, com limite de 250 por data                 
  2. em duplicata, se uma tiver nota e a outra não, fica a que tem nota; se     
  empatar, fica a primeira                                                      
  3. fornecedor compara normalizado também                                      
  4. valor zero é válido e reembolsa 0                                          
                                                                                
  Atualiza o resumo final das decisões com isso e confirma se agora ficou tudo  
  coerente.                                                                     
                                                                                
  Ainda não altera arquivo.                                                     

● Resumo final: as 16 decisões

  #: 01
  Tema: Unidade do limite
  Decisão: Limite sobre a soma do dia, por categoria, para as três categorias:
  alimentação 60, transporte urbano 80, hospedagem 250
  ────────────────────────────────────────
  #: 02
  Tema: Divisão do limite no dia
  Decisão: Pela posição do item na lista de despesas: o primeiro consome o
  limite
  primeiro
  ────────────────────────────────────────
  #: 03
  Tema: Reembolso parcial
  Decisão: Paga até o limite e corta o excedente
  ────────────────────────────────────────
  #: 04
  Tema: Fronteira da nota fiscal
  Decisão: Exigida só quando o valor é maior que 100,00; exatamente 100,00 não
  exige
  ────────────────────────────────────────
  #: 05
  Tema: Base e efeito da nota
  Decisão: Usa o valor do item já arredondado, não o do dia nem o valor depois
  do
  limite; sem nota, a despesa é recusada inteira
  ────────────────────────────────────────
  #: 06
  Tema: "Em viagem"
  Decisão: Ampliação de 50% nunca aplicada, porque a entrada não tem o dado
  ────────────────────────────────────────
  #: 07
  Tema: Alcance da ampliação
  Decisão: Não se aplica enquanto valer a AMB-06
  ────────────────────────────────────────
  #: 08
  Tema: Diárias de hospedagem
  Decisão: Cada registro vale 1 diária; a descrição nunca entra no cálculo. Como

  há uma soma por data (AMB-01), o limite fica em 250 por data
  ────────────────────────────────────────
  #: 09
  Tema: Competência
  Decisão: A data da despesa precisa estar entre inicio e fim, com as bordas
  incluídas; se houver conflito, inicio/fim prevalecem sobre competencia
  ────────────────────────────────────────
  #: 10
  Tema: Duplicatas
  Decisão: Duplicata é ter a mesma data, categoria, fornecedor e valor,
  comparados depois de normalizados. Fica a despesa com nota fiscal; se as duas
   tiverem ou nenhuma tiver, fica a primeira. As demais são recusadas
  ────────────────────────────────────────
  #: 11
  Tema: Estorno (valor negativo)
  Decisão: Recusado, com reembolso 0,00 e sem abater de outros itens. Valor zero
   
  é válido e reembolsa 0,00
  ────────────────────────────────────────
  #: 12
  Tema: Arredondamento
  Decisão: Valor de entrada arredondado para centavos (0,005 sobe) antes de
  qualquer regra
  ────────────────────────────────────────
  #: 13
  Tema: Normalização de texto
  Decisão: Categoria e fornecedor: ignora maiúsculas, acentos e espaços nas
  pontas
  ────────────────────────────────────────
  #: 14
  Tema: Categorias aceitas
  Decisão: Lista fechada: alimentação, transporte urbano e hospedagem
  ────────────────────────────────────────
  #: 15
  Tema: Fim de semana
  Decisão: Sem restrição: todo dia do calendário conta
  ────────────────────────────────────────
  #: 16
  Tema: Ordem de aplicação
  Decisão: Normalizar → validar (valor negativo, período, categoria) →
  duplicatas
  → nota fiscal → limites. Itens recusados não consomem limite

  Princípio que atravessa a spec: só campos estruturados decidem cálculos; a 
  descrição é apenas informativa.

  ---

  Verificação de coerência

  Os dois conflitos estão resolvidos:
  - Hospedagem agora segue a mesma regra de soma por dia das outras categorias.
    Com 1 diária por registro, o limite por diária e o limite por dia coincidem.
  - Uma duplicata não pode mais anular um comprovante válido, nem gerar
    pagamento em dobro.

  As novas decisões não criam conflito:
  - Valor zero: passa pelas validações, consome 0 do limite, e dois zeros
    idênticos caem como duplicata sem efeito no valor.
  - Valor quase zero: como o arredondamento vem antes da validação, −0,004 vira
    0,00 e é tratado como zero, não como estorno. É coerente com a AMB-16, mas
    vale citar esse caso na tabela de casos de borda da spec.
  - Duplicata que fica com a nota fiscal: a escolha acontece na etapa de
    duplicatas, antes da etapa da nota fiscal. A despesa mantida conserva a sua
    posição original para a divisão do limite (AMB-02).

  Simulação no arquivo de exemplo: cada item recebe exatamente um resultado, sem
  ambiguidade.

  ┌───────┬───────────┬──────────────────────────────────────────────────────┐
  │ Item  │ Resultado │                        Motivo                        │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-001 │ 60,00     │ limite diário de alimentação                         │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-002 │ 0,00      │ limite do dia já consumido por d-001                 │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-003 │ 80,00     │ 100,00 não exige nota; limite de transporte          │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-004 │ 0,00      │ acima de 100 sem nota                                │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-005 │ 0,00      │ categoria fora da política                           │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-006 │ 54,90     │ dentro do limite                                     │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-007 │ 0,00      │ duplicata de d-006 (empate na nota, fica a primeira) │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-008 │ 0,00      │ fora do período                                      │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-009 │ 0,00      │ estorno                                              │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-010 │ 250,00    │ 1 diária, limite por data                            │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-011 │ 33,33     │ arredondado de 33,333                                │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-012 │ 47,20     │ fim de semana sem restrição                          │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-013 │ 0,00      │ acima de 100 sem nota                                │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ d-014 │ 60,00     │ categoria normalizada; 31/07 está dentro do período; │
  │       │           │  corta o excedente                                   │
  ├───────┼───────────┼──────────────────────────────────────────────────────┤
  │ Total │ 585,43    │                                                      │
  └───────┴───────────┴──────────────────────────────────────────────────────┘

  Esta tabela pode virar o critério de aceite de ponta a ponta da spec.

  Conclusão: está coerente. Não encontrei mais conflitos nem lacunas entre as
  decisões.

  O que ainda falta para a spec, e não é ambiguidade da política:
  - O formato da saída, que é seu de definir: campos por item, motivo da recusa
    e se há um total.
  - A lista de fora de escopo.
  - Como tratar uma entrada malformada, com campo faltando ou de tipo errado.

  Podemos fechar esses três quando você liberar a escrita da spec.md.

✻ Crunched for 26s · done 0:47

> Pode escrever a spec.md                                                       

● Write(specs\001-motor-reembolso\spec.md)
  ⎿  Added 486 lines, removed 38 lines
      1  # Spec — Motor de Cálculo de Reembolso
      2  
      3 -**Versão:** 1.0 · **Status:** rascunho · **Última alteração:** `
        -<data>`                                                         
      3 +**Versão:** 1.0 · **Status:** rascunho · **Última alteração:** 2
        +026-10-04                                                       
      4  
      5  > **Regra de ouro deste arquivo:** ele descreve o QUÊ e o PORQUÊ
         . Nenhuma linha
      6  > aqui pode citar linguagem, biblioteca, classe, função ou estru
         tura de pasta.
     ...
       13  
       14  ## 1. Problema
       15  
       16 -<Duas ou três frases. Quem sofre hoje, com o quê, e por quê is
          -so custa caro.>                                               
       16 +Hoje o financeiro confere manualmente, item por item, as despe
          +sas de cada                                                   
       17 +colaborador contra a política de reembolso. O processo é lento
          + e produz                                                     
       18 +resultados inconsistentes, porque a política é ambígua e cada 
          +pessoa a                                                      
       19 +interpreta de um jeito.                                       
       20  
       21  ## 2. Objetivo
       22  
       20 -<Uma frase. O que passa a ser verdade quando isto existir.>   
       23 +Dado o conjunto de despesas de um colaborador em um período, o
          + sistema calcula                                              
       24 +de forma determinística quanto é reembolsável em cada despesa 
          +e justifica cada                                              
       25 +decisão com base em regras escritas nesta spec.               
       26  
       27  ## 3. Fora de escopo
       28  
       24 -<Lista explícita. Este bloco vale ponto: ele impede o agente d
          -e inventar feature                                            
       25 -e impede você de mover a trave depois.>                       
       29 +- Não aplica a ampliação de limites para colaborador em viagem
          + (ver AMB-006).                                               
       30 +- Não processa mais de um colaborador ou mais de um período po
          +r execução.                                                   
       31 +- Não verifica a autenticidade da nota fiscal; considera apena
          +s a informação                                                
       32 +  "tem nota fiscal" declarada na entrada.                     
       33 +- Não detecta duplicatas entre execuções diferentes nem guarda
          + histórico.                                                   
       34 +- Não compensa estornos com despesas de outros períodos.      
       35 +- Não interpreta o texto da descrição para nenhum cálculo ou d
          +ecisão.                                                       
       36 +- Não converte moedas; todos os valores estão em reais.       
       37 +- Não aprova nem efetua pagamento; apenas calcula e justifica.
       38 +- Não reembolsa categorias além de alimentação, transporte urb
          +ano e hospedagem.                                             
       39  
       27 -- Não faz `<...>`                                             
       28 -- Não faz `<...>`                                             
       29 -                                                              
       40  ## 4. Entrada e saída
       41  
       32 -**Entrada:** conforme `exemplos/despesas-exemplo.json`. Campos
          - e significado:                                               
       42 +**Entrada:** um documento no formato de `exemplos/despesas-exe
          +mplo.json`.                                                   
       43  
       44  | Campo | Tipo | Significado | Obrigatório |
       45  |---|---|---|---|
       36 -| | | | |                                                     
       46 +| `colaborador.id` | texto | Identificador do colaborador | si
          +m |                                                           
       47 +| `colaborador.nome` | texto | Nome do colaborador (informativ
          +o) | não |                                                    
       48 +| `colaborador.centro_custo` | texto | Centro de custo (inform
          +ativo) | não |                                                
       49 +| `periodo.competencia` | texto `AAAA-MM` | Mês de competência
          + (informativo; ver AMB-009) | não |                           
       50 +| `periodo.inicio` | data `AAAA-MM-DD` | Primeiro dia do perío
          +do | sim |                                                    
       51 +| `periodo.fim` | data `AAAA-MM-DD` | Último dia do período | 
          +sim |                                                         
       52 +| `despesas` | lista | Despesas a avaliar; pode ser vazia | si
          +m |                                                           
       53 +| `despesas[].id` | texto | Identificador da despesa | sim |  
       54 +| `despesas[].data` | data `AAAA-MM-DD` | Data em que a despes
          +a ocorreu | sim |                                             
       55 +| `despesas[].categoria` | texto | Categoria da despesa | sim 
          +|                                                             
       56 +| `despesas[].descricao` | texto | Descrição livre (informativ
          +a; nunca usada em cálculo) | não |                            
       57 +| `despesas[].fornecedor` | texto | Nome do fornecedor | sim |
       58 +| `despesas[].valor` | número | Valor em reais; pode ter mais 
          +de duas casas decimais ou ser negativo | sim |                
       59 +| `despesas[].tem_nota_fiscal` | verdadeiro/falso | Se há nota
          + fiscal | sim |                                               
       60  
       38 -**Saída:** definida por mim. Estrutura e significado de cada c
          -ampo:                                                         
       61 +A **posição** de uma despesa é a sua ordem na lista `despesas`
          +, começando em 1.                                             
       62 +Ela é usada como critério de desempate (RN-006 e RN-009).     
       63  
       64 +**Saída:** um documento com a seguinte estrutura.             
       65 +                                                              
       66  | Campo | Tipo | Significado |
       67  |---|---|---|
       42 -| | | |                                                       
       68 +| `colaborador` | objeto | Cópia do objeto `colaborador` da en
          +trada |                                                       
       69 +| `periodo` | objeto | Cópia do objeto `periodo` da entrada | 
       70 +| `itens` | lista | Um item para cada despesa da entrada, na m
          +esma ordem |                                                  
       71 +| `itens[].id` | texto | `id` da despesa |                    
       72 +| `itens[].valor_informado` | número | `valor` exatamente como
          + veio na entrada; vazio se ausente ou inválido |              
       73 +| `itens[].valor_considerado` | número | Valor arredondado par
          +a centavos (RN-003); vazio se inválido |                      
       74 +| `itens[].valor_reembolsavel` | número | Valor a reembolsar, 
          +com duas casas decimais |                                     
       75 +| `itens[].status` | texto | `aprovado`, `limitado` ou `recusa
          +do` (definições abaixo) |                                     
       76 +| `itens[].motivo` | texto ou vazio | Código do motivo (tabela
          + abaixo); vazio quando `aprovado` |                           
       77 +| `itens[].justificativa` | texto | Explicação legível da deci
          +são, citando a regra (RN-xxx) |                               
       78 +| `total_reembolsavel` | número | Soma de `valor_reembolsavel`
          + de todos os itens |                                          
       79  
       44 -<Cole um exemplo de saída para uma entrada pequena. Vale mais 
          -que três parágrafos.>                                         
       80 +**Status:**                                                   
       81  
       82 +- `aprovado`: a despesa passou por todas as regras e `valor_re
          +embolsavel` é                                                 
       83 +  igual a `valor_considerado`.                                
       84 +- `limitado`: a despesa passou por todas as validações, mas o 
          +limite diário                                                 
       85 +  reduziu `valor_reembolsavel`, possivelmente a zero.         
       86 +- `recusado`: a despesa foi recusada em uma validação e `valor
          +_reembolsavel` é 0,00.                                        
       87 +                                                              
       88 +**Motivos:**                                                  
       89 +                                                              
       90 +| Código | Status | Regra |                                   
       91 +|---|---|---|                                                 
       92 +| `DADOS_INVALIDOS` | recusado | RN-013 |                     
       93 +| `VALOR_NEGATIVO` | recusado | RN-005 |                      
       94 +| `FORA_DO_PERIODO` | recusado | RN-004 |                     
       95 +| `CATEGORIA_NAO_REEMBOLSAVEL` | recusado | RN-001 |          
       96 +| `DUPLICATA` | recusado | RN-006 |                           
       97 +| `NOTA_FISCAL_AUSENTE` | recusado | RN-007 |                 
       98 +| `LIMITE_DIARIO` | limitado | RN-008, RN-009, RN-010 |       
       99 +                                                              
      100 +A justificativa deve citar o `id` da despesa mantida, no caso 
          +de `DUPLICATA`, e o                                           
      101 +limite com o valor já consumido no dia, no caso de `LIMITE_DIA
          +RIO`.                                                         
      102 +                                                              
      103 +**Exemplo** (entrada com período de 2026-07-01 a 2026-07-31): 
      104 +                                                              
      105 +Entrada (trecho):                                             
      106 +                                                              
      107 +```                                                           
      108 +{ "id": "d-001", "data": "2026-07-03", "categoria": "alimentac
          +ao", "fornecedor": "Restaurante Tavola", "valor": 72.50, "tem_
          +nota_fiscal": true }                                          
      109 +{ "id": "d-002", "data": "2026-07-03", "categoria": "alimentac
          +ao", "fornecedor": "Cantina do Porto",   "valor": 38.00, "tem_
          +nota_fiscal": true }                                          
      110 +{ "id": "d-004", "data": "2026-07-06", "categoria": "transport
          +e_urbano", "fornecedor": "TaxiApp",     "valor": 100.01, "tem_
          +nota_fiscal": false }                                         
      111 +```                                                           
      112 +                                                              
      113 +Saída (trecho):                                               
      114 +                                                              
      115 +```                                                           
      116 +"itens": [                                                    
      117 +  { "id": "d-001", "valor_informado": 72.50, "valor_considerad
          +o": 72.50, "valor_reembolsavel": 60.00,                       
      118 +    "status": "limitado", "motivo": "LIMITE_DIARIO",          
      119 +    "justificativa": "Limite diário de alimentação de R$ 60,00
          + aplicado; excedente de R$ 12,50 cortado (RN-008, RN-010)." },
      120 +  { "id": "d-002", "valor_informado": 38.00, "valor_considerad
          +o": 38.00, "valor_reembolsavel": 0.00,                        
      121 +    "status": "limitado", "motivo": "LIMITE_DIARIO",          
      122 +    "justificativa": "Limite diário de alimentação de R$ 60,00
          + já consumido por d-001 em 2026-07-03 (RN-008, RN-009)." },   
      123 +  { "id": "d-004", "valor_informado": 100.01, "valor_considera
          +do": 100.01, "valor_reembolsavel": 0.00,                      
      124 +    "status": "recusado", "motivo": "NOTA_FISCAL_AUSENTE",    
      125 +    "justificativa": "Valor acima de R$ 100,00 sem nota fiscal
          + (RN-007)." }                                                 
      126 +],                                                            
      127 +"total_reembolsavel": 60.00                                   
      128 +```                                                           
      129 +                                                              
      130  ## 5. Regras de negócio
      131  
       48 -Cada regra recebe um ID (`RN-001`, ...). As tasks vão referenc
          -iar esses IDs.                                                
      132 +### RN-001 — Categorias reembolsáveis                         
      133  
       50 -### RN-001 — <nome da regra>                                  
      134 +**Regra:** Só são reembolsáveis as categorias `alimentacao`, `
          +transporte_urbano`                                            
      135 +e `hospedagem`, comparadas depois da normalização (RN-002). Qu
          +alquer outra                                                  
      136 +categoria é recusada com `CATEGORIA_NAO_REEMBOLSAVEL`.        
      137 +**Origem:** política do RH, item 9 (AMB-014)                  
      138 +**Aceite:** d-005 (`coworking`, 89,00) → recusado, 0,00, `CATE
          +GORIA_NAO_REEMBOLSAVEL`.                                      
      139  
       52 -**Regra:** <enunciado sem ambiguidade>                        
       53 -**Origem:** política do RH, item `<n>`                        
       54 -**Aceite:** <como verificar que está implementada — normalment
          -e um caso concreto com números>                               
      140 +### RN-002 — Normalização de texto                            
      141  
       56 -### RN-002 — ...                                              
      142 +**Regra:** Antes de qualquer comparação, categoria e fornecedo
          +r são normalizados:                                           
      143 +espaços no início e no fim são removidos, letras maiúsculas vi
          +ram minúsculas e                                              
      144 +acentos são removidos. A normalização não altera mais nada; es
          +paços internos e                                              
      145 +outros caracteres são mantidos.                               
      146 +**Origem:** decisão desta spec (AMB-013)                      
      147 +**Aceite:** categoria `ALIMENTACAO`, ` Alimentação ` e `alimen
          +tacao` são tratadas                                           
      148 +como `alimentacao`. Fornecedores `Bistro Central` e `bistro ce
          +ntral` são iguais.                                            
      149  
      150 +### RN-003 — Arredondamento                                   
      151 +                                                              
      152 +**Regra:** O valor de cada despesa é arredondado para centavos
          + antes de qualquer                                            
      153 +outra regra, com arredondamento comercial: a metade se afasta 
          +do zero (0,005                                                
      154 +vira 0,01). Todas as regras seguintes usam o valor arredondado
      155 +(`valor_considerado`). Todos os valores de saída têm duas casa
          +s decimais.                                                   
      156 +**Origem:** decisão desta spec (AMB-012)                      
      157 +**Aceite:** d-011 (33,333) → `valor_considerado` 33,33. Valor 
          +10,005 → 10,01.                                               
      158 +Valor −0,004 → 0,00, tratado como valor zero (RN-005).        
      159 +                                                              
      160 +### RN-004 — Período de competência                           
      161 +                                                              
      162 +**Regra:** A despesa é aceita se sua `data` estiver entre `per
          +iodo.inicio` e                                                
      163 +`periodo.fim`, com as duas datas incluídas. Caso contrário, é 
          +recusada com                                                  
      164 +`FORA_DO_PERIODO`. O campo `periodo.competencia` é informativo
          + e não é usado                                                
      165 +nessa verificação.                                            
      166 +**Origem:** política do RH, item 7 (AMB-009)                  
      167 +**Aceite:** d-008 (2026-04-15, período de julho) → recusado, `
          +FORA_DO_PERIODO`.                                             
      168 +d-014 (2026-07-31, último dia) → aceito por esta regra.       
      169 +                                                              
      170 +### RN-005 — Valores negativos e zero                         
      171 +                                                              
      172 +**Regra:** Despesa com `valor_considerado` menor que zero é re
          +cusada com                                                    
      173 +`VALOR_NEGATIVO` e não abate o valor de nenhuma outra despesa.
          + Despesa com                                                  
      174 +`valor_considerado` igual a zero é válida e reembolsa 0,00 com
          + status `aprovado`.                                           
      175 +**Origem:** decisão desta spec (AMB-011)                      
      176 +**Aceite:** d-009 (−45,00) → recusado, 0,00, `VALOR_NEGATIVO`;
          + o reembolso das                                              
      177 +demais despesas de transporte urbano não muda. Despesa de 0,00
          + → aprovado, 0,00.                                            
      178 +                                                              
      179 +### RN-006 — Duplicatas                                       
      180 +                                                              
      181 +**Regra:** Duas ou mais despesas são duplicatas quando têm a m
          +esma `data`, a                                                
      182 +mesma categoria normalizada, o mesmo fornecedor normalizado e 
          +o mesmo                                                       
      183 +`valor_considerado`. Só despesas que passaram por RN-001, RN-0
          +04, RN-005 e RN-013                                           
      184 +participam dessa comparação. Em cada grupo de duplicatas, uma 
          +despesa é mantida:                                            
      185 +                                                              
      186 +1. se houver despesas com nota fiscal no grupo, fica a de meno
          +r posição entre elas;                                         
      187 +2. se nenhuma tiver nota fiscal, fica a de menor posição.     
      188 +                                                              
      189 +As demais são recusadas com `DUPLICATA`, e a justificativa cit
          +a o `id` da mantida.                                          
      190 +`id` e `descricao` não participam da comparação.              
      191 +**Origem:** política do RH, item 8 (AMB-010)                  
      192 +**Aceite:** d-006 e d-007 (2026-07-09, alimentação, Bistro Cen
          +tral, 54,90, ambas                                            
      193 +com nota) → d-006 mantida; d-007 recusada, `DUPLICATA`, citand
          +o d-006. Grupo em                                             
      194 +que só a segunda despesa tem nota → a segunda é mantida e a pr
          +imeira é recusada.                                            
      195 +                                                              
      196 +### RN-007 — Nota fiscal                                      
      197 +                                                              
      198 +**Regra:** Despesa com `valor_considerado` estritamente maior 
          +que 100,00 e sem                                              
      199 +nota fiscal é recusada inteira com `NOTA_FISCAL_AUSENTE`. A ve
          +rificação usa o                                               
      200 +valor da própria despesa, e não a soma do dia nem o valor após
          + o limite.                                                    
      201 +Despesa de exatamente 100,00 não exige nota.                  
      202 +**Origem:** política do RH, item 5 (AMB-004, AMB-005)         
      203 +**Aceite:** d-003 (100,00, sem nota) → não exige nota. d-004 (
          +100,01, sem nota)                                             
      204 +→ recusado, 0,00, `NOTA_FISCAL_AUSENTE`. d-013 (690,00, sem no
          +ta) → recusado.                                               
      205 +                                                              
      206 +### RN-008 — Limites diários por categoria                    
      207 +                                                              
      208 +**Regra:** Para cada combinação de data e categoria, a soma re
          +embolsada não                                                 
      209 +ultrapassa o limite:                                          
      210 +                                                              
      211 +| Categoria | Limite por data |                               
      212 +|---|---|                                                     
      213 +| `alimentacao` | R$ 60,00 |                                  
      214 +| `transporte_urbano` | R$ 80,00 |                            
      215 +| `hospedagem` | R$ 250,00 |                                  
      216 +                                                              
      217 +Cada despesa de hospedagem vale uma diária, qualquer que seja 
          +o texto da                                                    
      218 +descrição. Como o limite é por data, várias hospedagens na mes
          +ma data dividem                                               
      219 +o mesmo limite de R$ 250,00. Só despesas que passaram por toda
          +s as regras                                                   
      220 +anteriores consomem o limite.                                 
      221 +**Origem:** política do RH, itens 1, 2 e 3 (AMB-001, AMB-008) 
      222 +**Aceite:** d-010 (hospedagem, 480,00, descrição "2 diarias") 
          +→ 250,00, `limitado`.                                         
      223 +d-001 + d-002 (alimentação, 2026-07-03, 110,50 no total) → som
          +a reembolsada 60,00.                                          
      224 +                                                              
      225 +### RN-009 — Distribuição do limite entre despesas da mesma da
          +ta                                                            
      226 +                                                              
      227 +**Regra:** Quando várias despesas da mesma categoria e data di
          +sputam o limite,                                              
      228 +ele é consumido na ordem da posição: cada despesa recebe o men
          +or valor entre o                                              
      229 +seu `valor_considerado` e o saldo do limite que restou das ant
          +eriores.                                                      
      230 +**Origem:** decisão desta spec (AMB-002)                      
      231 +**Aceite:** d-001 (posição 1, 72,50) → 60,00; d-002 (posição 2
          +, 38,00) → 0,00,                                              
      232 +`limitado`, justificativa citando d-001.                      
      233 +                                                              
      234 +### RN-010 — Reembolso parcial                                
      235 +                                                              
      236 +**Regra:** Despesa que ultrapassa o saldo do limite é reembols
          +ada até o saldo; o                                            
      237 +excedente é cortado. A despesa não é recusada por ultrapassar 
          +o limite.                                                     
      238 +**Origem:** política do RH, item 4 (AMB-003)                  
      239 +**Aceite:** d-014 (alimentação, 61,00) → 60,00, `limitado`, `L
          +IMITE_DIARIO`.                                                
      240 +                                                              
      241 +### RN-011 — Ampliação para colaborador em viagem             
      242 +                                                              
      243 +**Regra:** A ampliação de 50% dos limites prevista pela políti
          +ca **não é                                                    
      244 +aplicada**. A entrada não traz nenhuma informação estruturada 
          +que indique viagem.                                           
      245 +**Origem:** política do RH, item 6 (AMB-006, AMB-007)         
      246 +**Aceite:** d-003 ("Corrida aeroporto", 100,00) → limite de 80
          +,00 aplicado,                                                 
      247 +reembolso 80,00. Nenhuma despesa do exemplo recebe limite acim
          +a da tabela da RN-008.                                        
      248 +                                                              
      249 +### RN-012 — Dias do calendário                               
      250 +                                                              
      251 +**Regra:** Todas as datas do calendário são tratadas da mesma 
          +forma; não há                                                 
      252 +distinção entre dias úteis, fins de semana e feriados.        
      253 +**Origem:** decisão desta spec (AMB-015)                      
      254 +**Aceite:** d-012 (sábado, 2026-07-18, alimentação, 47,20) → a
          +provado, 47,20.                                               
      255 +                                                              
      256 +### RN-013 — Dados inválidos                                  
      257 +                                                              
      258 +**Regra:**                                                    
      259 +                                                              
      260 +- **Erro geral:** se o documento de entrada não puder ser lido
          +, ou se faltar                                                
      261 +  `colaborador.id`, `periodo.inicio`, `periodo.fim` ou `despes
          +as`, ou se                                                    
      262 +  `periodo.inicio` for posterior a `periodo.fim`, o sistema en
          +cerra com mensagem                                            
      263 +  de erro e não gera saída.                                   
      264 +- **Erro em uma despesa:** se faltar um campo obrigatório da d
          +espesa, se a data                                             
      265 +  não for uma data válida, se o valor não for numérico ou se `
          +tem_nota_fiscal`                                              
      266 +  não for verdadeiro/falso, apenas essa despesa é recusada com
          + `DADOS_INVALIDOS`.                                           
      267 +  As demais são processadas normalmente.                      
      268 +                                                              
      269 +**Origem:** decisão desta spec                                
      270 +**Aceite:** despesa sem `tem_nota_fiscal` → recusado, `DADOS_I
          +NVALIDOS`, e as                                               
      271 +outras despesas do documento aparecem na saída normalmente. Do
          +cumento sem                                                   
      272 +`periodo.fim` → erro, sem arquivo de saída.                   
      273 +                                                              
      274 +### RN-014 — Descrição é informativa                          
      275 +                                                              
      276 +**Regra:** O campo `descricao` nunca altera nenhum cálculo ou 
          +decisão. Só campos                                            
      277 +estruturados (data, categoria, fornecedor, valor, nota fiscal,
          + período e                                                    
      278 +posição) determinam o resultado.                              
      279 +**Origem:** decisão desta spec (AMB-006, AMB-008, AMB-010)    
      280 +**Aceite:** trocar a descrição de qualquer despesa do exemplo 
          +não altera nenhum                                             
      281 +`valor_reembolsavel`, `status` ou `motivo`.                   
      282 +                                                              
      283  ---
      284  
      285  ## 6. Ambiguidades identificadas e decisões
      286  
       62 -> **Esta seção é o coração da spec e vale a maior parte dos 25
          - pontos do critério 1.**                                      
       63 -> Uma ambiguidade que você resolveu no código sem registrar aq
          -ui conta como                                                 
       64 -> não resolvida.                                              
      287 +### AMB-001 — Unidade do limite diário                        
      288  
       66 -### AMB-001 — <o que a política deixou em aberto>             
      289 +**Texto original do RH:** "Alimentação tem limite de R$ 60 por
          + dia."                                                        
      290 +**O que não está claro:** se o limite vale para a soma das des
          +pesas do dia ou                                               
      291 +para cada despesa separadamente.                              
      292 +**Decisão:** o limite vale para a soma das despesas da mesma c
          +ategoria na mesma                                             
      293 +data, para as três categorias.                                
      294 +**Justificativa:** o texto diz "por dia", e limitar por despes
          +a permitiria                                                  
      295 +contornar o limite dividindo a conta.                         
      296 +**Regra afetada:** RN-008                                     
      297  
       68 -**Texto original do RH:** "<citação literal>"                 
       69 -**O que não está claro:** <as duas ou mais leituras possíveis>
       70 -**Decisão:** <o que o sistema faz>                            
       71 -**Justificativa:** <por quê — uma linha; critério de negócio, 
          -não de conveniência técnica>                                  
       72 -**Regra afetada:** RN-00X                                     
      298 +### AMB-002 — Distribuição do limite entre despesas do mesmo d
          +ia                                                            
      299  
       74 -### AMB-002 — ...                                             
      300 +**Texto original do RH:** "Alimentação tem limite de R$ 60 por
          + dia." (itens 1–3)                                            
      301 +**O que não está claro:** quando a soma do dia ultrapassa o li
          +mite, quanto cabe a                                           
      302 +cada despesa. Pode ser pela ordem, proporcional ou do maior va
          +lor para o menor.                                             
      303 +**Decisão:** pela posição na entrada; a primeira consome o lim
          +ite primeiro.                                                 
      304 +**Justificativa:** é determinístico e verificável à mão, e a j
          +ustificativa de                                               
      305 +cada item fica simples de explicar.                           
      306 +**Regra afetada:** RN-009                                     
      307  
       76 -<A política tem no mínimo oito. Se você achou menos, releia   
       77 -`exemplos/despesas-exemplo.json` — cada item daquele arquivo e
          -xiste por um motivo.>                                         
      308 +### AMB-003 — Significado de "reembolsadas parcialmente"      
      309  
      310 +**Texto original do RH:** "Despesas acima do limite são reembo
          +lsadas parcialmente."                                         
      311 +**O que não está claro:** se paga até o limite e corta o exced
          +ente, ou se recusa                                            
      312 +a despesa inteira.                                            
      313 +**Decisão:** paga até o limite e corta o excedente.           
      314 +**Justificativa:** "parcialmente" só faz sentido se alguma par
          +te for paga.                                                  
      315 +**Regra afetada:** RN-010                                     
      316 +                                                              
      317 +### AMB-004 — Fronteira de "acima de R$ 100"                  
      318 +                                                              
      319 +**Texto original do RH:** "Nota fiscal é obrigatória acima de 
          +R$ 100."                                                      
      320 +**O que não está claro:** se uma despesa de exatamente R$ 100,
          +00 exige nota.                                                
      321 +**Decisão:** exige nota só quando o valor é estritamente maior
          + que 100,00.                                                  
      322 +**Justificativa:** é a leitura literal de "acima de".         
      323 +**Regra afetada:** RN-007                                     
      324 +                                                              
      325 +### AMB-005 — Base e consequência da exigência de nota fiscal 
      326 +                                                              
      327 +**Texto original do RH:** "Nota fiscal é obrigatória acima de 
          +R$ 100."                                                      
      328 +**O que não está claro:** se o valor comparado é o da despesa,
          + o total do dia ou                                            
      329 +o valor após o limite; e se a falta da nota recusa a despesa i
          +nteira ou paga até                                            
      330 +R$ 100,00.                                                    
      331 +**Decisão:** compara o valor da própria despesa, já arredondad
          +o; sem nota, a                                                
      332 +despesa é recusada inteira.                                   
      333 +**Justificativa:** a nota comprova o gasto efetivamente feito,
          + e "obrigatória"                                              
      334 +indica que sem ela a despesa não é aceita.                    
      335 +**Regra afetada:** RN-007                                     
      336 +                                                              
      337 +### AMB-006 — O que caracteriza "em viagem"                   
      338 +                                                              
      339 +**Texto original do RH:** "Colaborador em viagem tem limites a
          +mpliados em 50%."                                             
      340 +**O que não está claro:** a entrada não tem campo que indique 
          +viagem. Seria                                                 
      341 +preciso inferir pela hospedagem, pela descrição, ou não aplica
          +r.                                                            
      342 +**Decisão:** a ampliação não é aplicada.                      
      343 +**Justificativa:** inferir viagem falha em casos evidentes (d-
          +003, "Corrida                                                 
      344 +aeroporto", sem hospedagem no dia) e cria brechas; sem dado, n
          +ão há como verificar.                                         
      345 +**Regra afetada:** RN-011                                     
      346 +                                                              
      347 +### AMB-007 — Categorias alcançadas pela ampliação            
      348 +                                                              
      349 +**Texto original do RH:** "Colaborador em viagem tem limites a
          +mpliados em 50%."                                             
      350 +**O que não está claro:** se a ampliação vale para as três cat
          +egorias ou só para                                            
      351 +alimentação e transporte.                                     
      352 +**Decisão:** não se aplica enquanto valer a AMB-006; deve ser 
          +decidida se um dado                                           
      353 +de viagem passar a existir.                                   
      354 +**Justificativa:** sem ampliação, a pergunta não tem efeito; r
          +egistrar evita uma                                            
      355 +lacuna silenciosa.                                            
      356 +**Regra afetada:** RN-011                                     
      357 +                                                              
      358 +### AMB-008 — Número de diárias de uma hospedagem             
      359 +                                                              
      360 +**Texto original do RH:** "Hospedagem tem limite de R$ 250 por
          + diária."                                                     
      361 +**O que não está claro:** a entrada não tem número de diárias;
          + a informação só                                              
      362 +aparece no texto livre (d-010, "2 diarias"; d-013, "3 noites")
          +.                                                             
      363 +**Decisão:** cada despesa de hospedagem vale uma diária; a des
          +crição não é usada.                                           
      364 +**Justificativa:** texto livre não tem formato garantido e pod
          +e ser manipulado;                                             
      365 +estadias de várias noites devem ser lançadas com uma despesa p
          +or diária.                                                    
      366 +**Regra afetada:** RN-008, RN-014                             
      367 +                                                              
      368 +### AMB-009 — Significado de "dentro do período de competência
          +"                                                             
      369 +                                                              
      370 +**Texto original do RH:** "Despesas devem ser lançadas dentro 
          +do período de competência."                                   
      371 +**O que não está claro:** a entrada não tem data de lançamento
          +, só a data da                                                
      372 +despesa; não se sabe se as bordas do período contam nem qual c
          +ampo prevalece se                                             
      373 +`competencia` e `inicio`/`fim` discordarem.                   
      374 +**Decisão:** a data da despesa deve estar entre `inicio` e `fi
          +m`, com as bordas                                             
      375 +incluídas; `competencia` é apenas informativa.                
      376 +**Justificativa:** não há data de lançamento, e qualquer toler
          +ância para                                                    
      377 +despesas atrasadas seria inventada.                           
      378 +**Regra afetada:** RN-004                                     
      379 +                                                              
      380 +### AMB-010 — Definição e tratamento de duplicatas            
      381 +                                                              
      382 +**Texto original do RH:** "Duplicatas devem ser tratadas."    
      383 +**O que não está claro:** quais campos definem uma duplicata e
          + o que fazer com                                              
      384 +ela: recusar todas, manter uma ou apenas sinalizar.           
      385 +**Decisão:** mesma data, categoria, fornecedor e valor, compar
          +ados após                                                     
      386 +normalização; mantém a que tem nota fiscal e, em empate, a de 
          +menor posição; as                                             
      387 +demais são recusadas.                                         
      388 +**Justificativa:** recusar todas puniria a despesa legítima, e
          + preferir a com nota                                          
      389 +evita que uma duplicata anule um comprovante válido.          
      390 +**Regra afetada:** RN-006                                     
      391 +                                                              
      392 +### AMB-011 — Valores negativos e zero                        
      393 +                                                              
      394 +**Texto original do RH:** a política não menciona o caso.     
      395 +**O que não está claro:** um estorno (d-009, −45,00) pode ser 
          +ignorado, abatido                                             
      396 +de outras despesas ou tratado como erro; a política também não
          + fala de valor zero.                                          
      397 +**Decisão:** valor negativo é recusado sem abater nada; valor 
          +zero é válido e                                               
      398 +reembolsa 0,00.                                               
      399 +**Justificativa:** a despesa original do estorno não está no p
          +eríodo, então não                                             
      400 +há o que compensar.                                           
      401 +**Regra afetada:** RN-005                                     
      402 +                                                              
      403 +### AMB-012 — Arredondamento                                  
      404 +                                                              
      405 +**Texto original do RH:** a política não menciona o caso.     
      406 +**O que não está claro:** como tratar valores com mais de duas
          + casas decimais                                               
      407 +(d-011, 33,333) e quando arredondar.                          
      408 +**Decisão:** arredonda o valor de entrada para centavos, com a
          + metade se                                                    
      409 +afastando do zero, antes de qualquer regra.                   
      410 +**Justificativa:** dinheiro é pago em centavos, e arredondar a
          +ntes evita efeitos                                            
      411 +de casas fracionárias nas comparações de fronteira.           
      412 +**Regra afetada:** RN-003                                     
      413 +                                                              
      414 +### AMB-013 — Grafia de categoria e fornecedor                
      415 +                                                              
      416 +**Texto original do RH:** a política não menciona o caso.     
      417 +**O que não está claro:** se `ALIMENTACAO` (d-014) é a mesma c
          +ategoria que                                                  
      418 +`alimentacao`, e se fornecedores com grafias diferentes são o 
          +mesmo.                                                        
      419 +**Decisão:** ignora maiúsculas, acentos e espaços nas pontas, 
          +para categoria e                                              
      420 +fornecedor.                                                   
      421 +**Justificativa:** diferença de grafia é erro de digitação, nã
          +o uma categoria ou                                            
      422 +fornecedor diferente.                                         
      423 +**Regra afetada:** RN-002                                     
      424 +                                                              
      425 +### AMB-014 — Categorias "fora da política"                   
      426 +                                                              
      427 +**Texto original do RH:** "Categorias fora da política não são
          + reembolsáveis."                                              
      428 +**O que não está claro:** se a lista de categorias é fechada n
          +as três citadas ou                                            
      429 +se categorias parecidas (d-005, coworking) podem ser encaixada
          +s.                                                            
      430 +**Decisão:** lista fechada: alimentação, transporte urbano e h
          +ospedagem.                                                    
      431 +**Justificativa:** a política só cita essas três; encaixar por
          + semelhança seria                                             
      432 +criar política.                                               
      433 +**Regra afetada:** RN-001                                     
      434 +                                                              
      435 +### AMB-015 — Fins de semana e feriados                       
      436 +                                                              
      437 +**Texto original do RH:** "R$ 60 por dia" (itens 1–3)         
      438 +**O que não está claro:** se "dia" é qualquer dia do calendári
          +o ou só dia útil                                              
      439 +(d-012, sábado, "plantão").                                   
      440 +**Decisão:** qualquer dia do calendário, sem restrição.       
      441 +**Justificativa:** a política não restringe, e plantão é traba
          +lho legítimo.                                                 
      442 +**Regra afetada:** RN-012                                     
      443 +                                                              
      444 +### AMB-016 — Ordem de aplicação das regras                   
      445 +                                                              
      446 +**Texto original do RH:** a política não define ordem.        
      447 +**O que não está claro:** quando várias regras incidem na mesm
          +a despesa, a ordem                                            
      448 +muda o resultado (por exemplo, d-006/d-007 e d-004).          
      449 +**Decisão:** ver seção 8.                                     
      450 +**Justificativa:** uma despesa recusada não deve ocupar o limi
          +te de uma despesa                                             
      451 +válida.                                                       
      452 +**Regra afetada:** todas                                      
      453 +                                                              
      454  ---
      455  
      456  ## 7. Casos de borda
      457  
      458  | Caso | Entrada | Comportamento esperado | Regra |
      459  |---|---|---|---|
       85 -| | | | |                                                     
      460 +| Duas despesas no mesmo dia somam acima do limite | d-001 (72
          +,50) + d-002 (38,00), alimentação, mesma data | 60,00 + 0,00 |
          + RN-008, RN-009 |                                             
      461 +| Valor exatamente no limite da nota | d-003: 100,00, sem nota
          + | não exige nota; 80,00 pelo limite | RN-007, RN-008 |       
      462 +| Valor um centavo acima do limite da nota | d-004: 100,01, se
          +m nota | recusado, `NOTA_FISCAL_AUSENTE` | RN-007 |           
      463 +| Despesa recusada não consome limite | d-004 recusada na mesm
          +a data de d-003 | d-003 recebe o limite inteiro de 80,00 | RN-
          +008, seção 8 |                                                
      464 +| Categoria fora da lista | d-005: coworking | recusado, `CATE
          +GORIA_NAO_REEMBOLSAVEL` | RN-001 |                            
      465 +| Duplicata idêntica, ambas com nota | d-006 e d-007 | d-006: 
          +54,90; d-007: recusada, `DUPLICATA` | RN-006 |                
      466 +| Duplicata em que só a segunda tem nota | mesmas data, catego
          +ria, fornecedor e valor; só a 2ª com nota | 2ª mantida; 1ª rec
          +usada, `DUPLICATA` | RN-006 |                                 
      467 +| Duplicata com grafia diferente do fornecedor | `Bistro Centr
          +al` e `BISTRO CENTRAL ` | tratadas como duplicata | RN-002, RN
          +-006 |                                                        
      468 +| Despesa antes do período | d-008: 2026-04-15 | recusado, `FO
          +RA_DO_PERIODO` | RN-004 |                                     
      469 +| Despesa no último dia do período | d-014: 2026-07-31 | aceit
          +a pelo período | RN-004 |                                     
      470 +| Despesa no primeiro dia do período | data igual a `periodo.i
          +nicio` | aceita pelo período | RN-004 |                       
      471 +| Estorno | d-009: −45,00 | recusado, `VALOR_NEGATIVO`; não ab
          +ate outras | RN-005 |                                         
      472 +| Valor zero | 0,00 | aprovado, 0,00 | RN-005 |               
      473 +| Valor negativo que arredonda a zero | −0,004 | vira 0,00; ap
          +rovado, 0,00 | RN-003, RN-005 |                               
      474 +| Mais de duas casas decimais | d-011: 33,333 | considerado 33
          +,33; aprovado, 33,33 | RN-003 |                               
      475 +| Arredondamento na metade | 10,005 | considerado 10,01 | RN-0
          +03 |                                                          
      476 +| Hospedagem com várias diárias na descrição | d-010: 480,00, 
          +"2 diarias" | 1 diária; 250,00, `limitado` | RN-008, RN-014 | 
      477 +| Duas hospedagens na mesma data | 200,00 + 150,00, mesma data
          + | 200,00 + 50,00 | RN-008, RN-009 |                          
      478 +| Hospedagem sem nota acima de 100 | d-013: 690,00, sem nota |
          + recusado, `NOTA_FISCAL_AUSENTE` | RN-007 |                   
      479 +| Categoria em maiúsculas | d-014: `ALIMENTACAO`, 61,00 | trat
          +ada como alimentação; 60,00, `limitado` | RN-002, RN-010 |    
      480 +| Despesa em fim de semana | d-012: sábado | sem restrição; 47
          +,20 | RN-012 |                                                
      481 +| Indício de viagem na descrição | d-003: "Corrida aeroporto" 
          +| limite normal de 80,00 | RN-011, RN-014 |                   
      482 +| Campo obrigatório ausente em uma despesa | despesa sem `tem_
          +nota_fiscal` | recusado, `DADOS_INVALIDOS`; demais processadas
          + | RN-013 |                                                   
      483 +| Período ausente | documento sem `periodo.fim` | erro, sem sa
          +ída | RN-013 |                                                
      484 +| Lista de despesas vazia | `despesas: []` | saída com `itens`
          + vazio e total 0,00 | RN-013 |                                
      485  
      486  ## 8. Ordem de aplicação das regras
      487  
       89 -<Quando duas regras incidem sobre a mesma despesa, qual vale p
          -rimeiro? A ordem                                              
       90 -muda o resultado. Declarar isso separa spec boa de spec média.
          ->                                                             
      488 +Cada despesa passa pelas etapas abaixo, nesta ordem. Uma despe
          +sa recusada em uma                                            
      489 +etapa recebe o motivo dessa etapa e não participa das etapas s
          +eguintes, nem                                                 
      490 +consome limite.                                               
      491  
      492 +1. **Dados válidos** (RN-013) → `DADOS_INVALIDOS`             
      493 +2. **Normalização e arredondamento** (RN-002, RN-003)         
      494 +3. **Valor negativo** (RN-005) → `VALOR_NEGATIVO`             
      495 +4. **Período** (RN-004) → `FORA_DO_PERIODO`                   
      496 +5. **Categoria** (RN-001) → `CATEGORIA_NAO_REEMBOLSAVEL`      
      497 +6. **Duplicatas**, entre as despesas que passaram das etapas 1
          + a 5 (RN-006) → `DUPLICATA`                                   
      498 +7. **Nota fiscal** (RN-007) → `NOTA_FISCAL_AUSENTE`           
      499 +8. **Limites por data e categoria**, distribuídos pela posição
          +, entre as despesas                                           
      500 +   que passaram das etapas 1 a 7 (RN-008, RN-009, RN-010) → `L
          +IMITE_DIARIO`                                                 
      501 +                                                              
      502 +Se uma despesa falhar em mais de uma validação, o motivo regis
          +trado é o da                                                  
      503 +primeira etapa em que falhou.                                 
      504 +                                                              
      505  ## 9. Critérios de aceite
      506  
      507  O sistema está pronto quando:
      508  
       96 -- [ ] <critério verificável, sem ler código>                  
       97 -- [ ] <...>                                                   
      509 +- [ ] Processando `exemplos/despesas-exemplo.json`, a saída te
          +m exatamente:                                                 
      510  
      511 +  | Item | `valor_reembolsavel` | `status` | `motivo` |       
      512 +  |---|---|---|---|                                           
      513 +  | d-001 | 60,00 | limitado | `LIMITE_DIARIO` |              
      514 +  | d-002 | 0,00 | limitado | `LIMITE_DIARIO` |               
      515 +  | d-003 | 80,00 | limitado | `LIMITE_DIARIO` |              
      516 +  | d-004 | 0,00 | recusado | `NOTA_FISCAL_AUSENTE` |         
      517 +  | d-005 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOLSAVEL` |  
      518 +  | d-006 | 54,90 | aprovado | — |                            
      519 +  | d-007 | 0,00 | recusado | `DUPLICATA` |                   
      520 +  | d-008 | 0,00 | recusado | `FORA_DO_PERIODO` |             
      521 +  | d-009 | 0,00 | recusado | `VALOR_NEGATIVO` |              
      522 +  | d-010 | 250,00 | limitado | `LIMITE_DIARIO` |             
      523 +  | d-011 | 33,33 | aprovado | — |                            
      524 +  | d-012 | 47,20 | aprovado | — |                            
      525 +  | d-013 | 0,00 | recusado | `NOTA_FISCAL_AUSENTE` |         
      526 +  | d-014 | 60,00 | limitado | `LIMITE_DIARIO` |              
      527 +  | **total_reembolsavel** | **585,43** | | |                 
      528 +                                                              
      529 +- [ ] A saída tem um item para cada despesa da entrada, na mes
          +ma ordem.                                                     
      530 +- [ ] Todo item tem justificativa citando ao menos uma regra (
          +RN-xxx).                                                      
      531 +- [ ] Todos os casos da seção 7 produzem o comportamento descr
          +ito.                                                          
      532 +- [ ] Alterar apenas a descrição de qualquer despesa não alter
          +a a saída, exceto                                             
      533 +      o próprio campo de justificativa, se ele a citar.       
      534 +- [ ] Processar a mesma entrada duas vezes produz a mesma saíd
          +a.                                                            
      535 +                                                              
      536  ## 10. O que fica em aberto
      537  
      101 -<Perguntas que você não conseguiu responder e a decisão provis
          -ória que tomou.                                               
      102 -Honestidade aqui vale ponto — spec que finge não ter buraco é 
          -spec que esconde buraco.>                                     
      538 +- **Viagem (AMB-006, AMB-007):** a regra 6 da política fica se
          +m efeito até a                                                
      539 +  entrada trazer um dado de viagem. Colaboradores em viagem re
          +cebem menos do que                                            
      540 +  o RH provavelmente pretendia.                               
      541 +- **Hospedagem com várias diárias (AMB-008):** d-010 recebe 25
          +0,00, embora a                                                
      542 +  descrição indique duas diárias de 240,00. Decisão provisória
          +: o colaborador                                               
      543 +  deve lançar uma despesa por diária.                         
      544 +- **Despesas lançadas com atraso (AMB-009):** despesas legítim
          +as de períodos                                                
      545 +  anteriores, como d-008, são recusadas sem possibilidade de e
          +xceção.                                                       
      546 +- **Estorno de despesa já reembolsada (AMB-011):** se a despes
          +a original foi                                                
      547 +  reembolsada em outro período, o estorno não é compensado. De
          +cisão provisória:                                             
      548 +  fora de escopo.                                             
      549 +- **`id` repetido na entrada:** não é validado. Decisão provis
          +ória: as despesas                                             
      550 +  são processadas normalmente e distinguidas pela posição.    

● Escrevi a specs/001-motor-reembolso/spec.md com as 16 decisões que você
  aprovou. Elas viraram 14 regras de negócio (RN-001 a RN-014) e as 16
  ambiguidades registradas (AMB-001 a AMB-016). A spec também traz a ordem de
  aplicação, os casos de borda e o resultado esperado de cada item do exemplo,
  com total de 585,43. Não fiz commit.

  Você liberou a escrita sem decidirmos três pontos que eu tinha deixado em
  aberto, e mais alguns detalhes que surgiram ao escrever. Preenchi tudo com
  propostas minhas, que precisam da sua revisão:

  1. Formato da saída (seção 4):
     - Cada item traz valor_informado, valor_considerado, valor_reembolsavel,
       status, motivo e justificativa.
     - O status pode ser aprovado, limitado (cortado pelo limite, inclusive até
       zero, como d-002) ou recusado.
     - Há 7 códigos de motivo, como NOTA_FISCAL_AUSENTE e DUPLICATA, e um
       total_reembolsavel geral.
  2. Dados inválidos (RN-013):
     - Arquivo ilegível ou sem
       colaborador.id/periodo.inicio/periodo.fim/despesas encerra com erro e não
       gera saída. O mesmo vale para início depois do fim.
     - Uma despesa com campo faltando ou de tipo errado é recusada sozinha, com
       DADOS_INVALIDOS, e as demais seguem. Isso inclui despesa sem
       tem_nota_fiscal, que é recusada em vez de ser tratada como "sem nota".
  3. Fora de escopo (seção 3): 9 itens. Exemplos: não processa vários
     colaboradores, não valida se a nota é autêntica, não detecta duplicatas
     entre execuções e não converte moeda.
  4. Ordem entre as validações (seção 8): o resultado não muda, porque toda
     despesa recusada recebe 0,00, mas o motivo registrado muda. Defini a ordem
     dados inválidos → valor negativo → fora do período → categoria. Se uma
     despesa falhar em mais de uma, o motivo é o da primeira falha.
  5. id repetido na entrada: não é validado. Registrei isso como pendência na
     seção 10.

  Antes do commit, revise principalmente a seção 4 (formato da saída) e a
  RN-013. São as partes em que a decisão foi mais minha do que sua. Quando
  aprovar, o commit fica docs(spec): primeira versão da spec com 16 ambiguidades
  resolvidas.

  O export da sessão anterior continua em 01-analise-inicial.md, na raiz do
  repositório. O desafio pede que ele fique em docs/sessions/.

✻ Brewed for 2m 32s · done 0:59