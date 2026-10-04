 ▐▛███▛█   Claude Code v2.1.289
▝▜██████▀  Opus 5.5 · API Usage Billing
 ▝▝   ▝▝   C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio


> Leia:                                                                         
  -CLAUDE.md                                                                    
  - specs/001-motor-reembolso/spec.md                                           
    -specs/001-motor-reembolso/plan.md                                          
  - specs/001-motor-reembolso/tasks.md                                          
  - specs/001-motor-reembolso/DECISIONS.md                                      
                                                                                
  Começou o Envelope do Dia 2 com a Política de Reembolso v4.                   
                                                                                
  Antes de qualquer alteração de código, faça SOMENTE a análise de impacto e    
  ambiguidades.                                                                 
                                                                                
  Ainda NÃO altere spec.md                                                      
  NÃO altere DECISIONS.md                                                       
  NÃO crie tasks                                                                
  NÃO implemente código.                                                        
  NÃO faça commit.                                                              
                                                                                
  Analise a mudança da v4 e identifique:                                        
                                                                                
  1. quais regras atuais da spec v3 são invalidadas ou precisam mudar;          
                                                                                
  2. quais novas regras precisam existir para:                                  
      política externa por centro de custo;                                     
      política padrão;                                                          
      categoria representacao;                                                  
     centro de custo que não reembolsa hospedagem;                              
     campo moeda;                                                               
      conversão cambial pela data da despesa;                                   
  3. todas as ambiguidades novas;                                               
  4. para cada ambiguidade:                                                     
     o que não está claro;                                                      
      qual caso do envelope evidencia o problema;                               
     interpretações possíveis;                                                  
      sua recomendação;                                                         
      justificativa curta.                                                      
                                                                                
  Preste atenção especialmente em:                                              
   centro de custo ausente;                                                     
   centro de custo conhecido com categoria ausente na tabela;                   
  centro de custo desconhecido;                                                 
   data sem cotação;                                                            
   moeda sem cotação disponível;                                                
   moeda ausente;                                                               
   arredondamento cambial;                                                      
   nota fiscal após conversão;                                                  
   duplicatas com moeda estrangeira;                                            
   arquivos de política/câmbio inválidos ou ausentes.                           
                                                                                
  Não implemente o item C de aprovação manual agora, porque é opcional.         
                                                                                
  No final, apresente somente a análise para eu revisar as decisões antes de    
  atualizar a spec.                                                             

  Searched for 1 pattern, read 1 file, ran 4 shell commands (ctrl+o to expand)

● Já li a spec, o DECISIONS e os arquivos do envelope. Agora vou verificar o
  exemplo v3 e o plano para medir o impacto nos critérios de aceite atuais.

  Ran 2 shell commands (ctrl+o to expand)

● Análise de impacto: Política de Reembolso v4 (Envelope do Dia 2)

  Não alterei nenhum arquivo. Esta é só a análise.

  Fontes: politica-v4.json, cambio.json, despesas-envelope.json,
  despesas-envelope-cc-desconhecido.json e a spec 1.1. O texto narrativo da
  política v4 não está no repositório, então trabalhei pelos JSONs e pela sua
  descrição. O item C (aprovação manual) ficou de fora.

  O achado mais importante: o exemplo atual (despesas-exemplo.json) tem
  centro_custo: "CC-ENG-PLATAFORMA". Pela v4, esse centro de custo tem
  alimentação de 75,00 e não reembolsa hospedagem. Isso muda o total do critério
  de aceite da seção 9 de 585,43 para 351,43. As despesas d-001, d-002, d-010,
  d-013 e d-014 mudam, e a justificativa de exemplo da seção 4 ("R$ 60,00")
  também fica errada.

  ---

  1. Regras da spec atual que ficam inválidas ou precisam mudar

  Trecho: §3 Fora de escopo
  O que muda: Saem "Não converte moedas" e "Não reembolsa categorias além de
  alimentação, transporte urbano e hospedagem"
  ────────────────────────────────────────
  Trecho: §4 Entrada
  O que muda: centro_custo deixa de ser informativo e passa a decidir os
  limites.
  valor deixa de estar "em reais". Entra o campo moeda. Política e câmbio viram
   entradas externas
  ────────────────────────────────────────
  Trecho: §4 Saída
  O que muda: Muda o significado de valor_informado (moeda original) e de
  valor_considerado (BRL). Faltam campos de moeda e cotação. Entra pelo menos
  um motivo novo. O exemplo de d-001/d-002 cita R$ 60,00, mas o certo agora é
  R$ 75,00
  ────────────────────────────────────────
  Trecho: RN-001
  O que muda: A lista fechada de 3 categorias passa a ser "as categorias da
  política aplicável"
  ────────────────────────────────────────
  Trecho: RN-003
  O que muda: O arredondamento passa a acontecer depois da conversão de moeda
  ────────────────────────────────────────
  Trecho: RN-006
  O que muda: Precisa dizer qual valor e qual moeda entram na comparação de
  duplicatas
  ────────────────────────────────────────
  Trecho: RN-007
  O que muda: O limiar de 100,00 vem do arquivo de política. Precisa dizer que a

  comparação é feita no valor já convertido para BRL
  ────────────────────────────────────────
  Trecho: RN-008
  O que muda: A tabela fixa vira uma tabela por centro de custo, vinda do
  arquivo
  de política
  ────────────────────────────────────────
  Trecho: RN-011
  O que muda: O percentual de 50% vem do arquivo, mas continua sem ser aplicado
  ────────────────────────────────────────
  Trecho: RN-013
  O que muda: centro_custo sai da lista de campos informativos e moeda passa a
  ser validada. O aceite "moeda: USD → campo ignorado" e a linha correspondente
   da §7 ficam inválidos. Entram erros gerais para os arquivos de política e de
   câmbio
  ────────────────────────────────────────
  Trecho: RN-014
  O que muda: A lista de campos estruturados ganha moeda e centro de custo
  ────────────────────────────────────────
  Trecho: §8 Ordem
  O que muda: Entra uma etapa nova de conversão de moeda
  ────────────────────────────────────────
  Trecho: §9 Aceite
  O que muda: O total do exemplo vai a 351,43 (detalhe abaixo), e entram
  critérios para os dois arquivos do envelope
  ────────────────────────────────────────
  Trecho: AMB-014 / AMB-012 / AMB-005
  O que muda: Precisam ser substituídas ou revistas

  Não mudam: RN-002, RN-004, RN-005, RN-009, RN-010, RN-012, AMB-006, AMB-007 e
  AMB-008.

  O exemplo atual sob a v4 (CC-ENG-PLATAFORMA, aplicando as recomendações
  abaixo):
  - d-001: 72,50, aprovado.
  - d-002: 2,50, limitado.
  - d-010: recusado. Hoje sai 250,00.
  - d-013: recusado por CATEGORIA_NAO_REEMBOLSAVEL. Hoje é recusado por
    NOTA_FISCAL_AUSENTE.
  - d-014: 61,00, aprovado.
  - As demais não mudam. Total: 351,43.

  2. Regras novas necessárias (numeração sugerida)

  - RN-015 — Política externa: os limites, as categorias, o limiar da nota
    fiscal, a moeda base e o percentual de viagem vêm de um arquivo de política
    com uma seção padrao e uma seção centros_custo.
  - RN-016 — Escolha da política: a política usada é a do centro de custo do
    colaborador quando ele está cadastrado, e a padrao nos demais casos
    (AMB-018/019).
  - RN-017 — Política padrão: alimentação 60, transporte 80 e hospedagem 250. A
    padrão não tem representação.
  - RN-018 — Categorias por centro de custo: só são reembolsáveis as categorias
    que aparecem na política aplicável (AMB-021).
  - RN-019 — Limite zero: uma categoria com limite 0,00 é tratada como não
    reembolsável naquele centro de custo. Caso do CC-ENG-PLATAFORMA com
    hospedagem (AMB-022).
  - RN-020 — Representação: tem limite por data, igual às outras categorias, e
    só existe onde a política a lista. No envelope, só no CC-COMERCIAL, com
    300,00 (AMB-023).
  - RN-021 — Campo moeda: é opcional, tem BRL como padrão e passa por
    normalização (AMB-024).
  - RN-022 — Conversão: o valor em BRL é o valor informado vezes a cotação da
    moeda na data da despesa, com um único arredondamento (AMB-025 a 027).
  - RN-023 — Arquivos de política e de câmbio: quando são obrigatórios e o que
    acontece se estiverem ausentes ou inválidos (AMB-031/032).

  3 e 4. Ambiguidades novas

  AMB-018 — Centro de custo ausente, vazio ou com tipo errado

  - O que não está claro: a política diz qual tabela usar para cada centro de
    custo, mas não diz o que fazer quando ele não é informado.
  - Caso: nenhum no envelope. O campo era informativo e opcional na v3.
  - Interpretações:
    - (a) usar a política padrão;
    - (b) erro geral.
  - Recomendação:
    - ausente ou vazio → política padrão, e a justificativa diz isso;
    - tipo errado (número, objeto) → erro geral, como já acontece com
      colaborador.id.
  - Justificativa: "não informado" é um caso legítimo e é exatamente para isso
    que a padrão existe. Já um tipo errado é entrada malformada e afeta todas as
    despesas do documento.

  AMB-019 — Centro de custo desconhecido

  - O que não está claro: se a padrão vale só quando o centro de custo está
    ausente, ou também quando ele não está na tabela.
  - Caso: despesas-envelope-cc-desconhecido.json (CC-SUPORTE-N2).
  - Interpretações:
    - (a) usar a padrão;
    - (b) erro geral, sem saída;
    - (c) recusar todas as despesas.
  - Recomendação: (a). A justificativa precisa dizer "centro de custo
    CC-SUPORTE-N2 não cadastrado; política padrão aplicada".
  - Justificativa: o nome "padrão" sugere fallback, e o próprio arquivo do
    envelope parece feito para ser processado. O risco é um erro de digitação no
    centro de custo cair na padrão sem ninguém perceber. A justificativa
    explícita reduz esse risco.
  - Resultado com a recomendação:
    - f-001: 58,00, aprovado.
    - f-002: 250,00, limitado.
    - f-003: recusado, CATEGORIA_NAO_REEMBOLSAVEL.
    - f-004: 65,76, aprovado.
    - Total: 373,76.

  AMB-020 — Como comparar o centro de custo

  - O que não está claro: se "cc-comercial " é o mesmo que CC-COMERCIAL.
  - Caso: nenhum no envelope.
  - Interpretações:
    - (a) comparação exata;
    - (b) normalização da RN-002 nos dois lados.
  - Recomendação: (b). As chaves de categoria do arquivo de política também
    passam pela RN-002.
  - Justificativa: é o mesmo raciocínio da AMB-013. E, junto com a AMB-019, um
    erro de grafia mandaria o colaborador para a padrão sem aviso.

  AMB-021 — Centro de custo conhecido, mas sem a categoria na tabela

  - O que não está claro: se a tabela do centro de custo substitui a padrão
    inteira ou só sobrescreve as categorias que lista.
  - Caso: a tabela do CC-ADM não tem hospedagem. Nenhuma despesa do envelope cai
    nesse caso.
  - Interpretações:
    - (a) categoria ausente = não reembolsável naquele centro de custo;
    - (b) categoria ausente = usa o limite da padrão.
  - Recomendação: (b), mas confirmar com o RH.
  - Justificativa: o CC-ENG-PLATAFORMA precisou declarar hospedagem com limite 0
    e "nao reembolsavel". Se a ausência já significasse "não reembolsável",
    esse registro seria desnecessário. Isso indica que ausência quer dizer
    "herda da padrão". Como a padrão não tem representação, o CC-ADM continuaria
    sem representação.
  - Efeito no CC-ADM: com (a), hospedagem é recusada; com (b), tem limite de
    250,00.

  AMB-022 — Limite 0,00 ("não reembolsável")

  - O que não está claro: se a despesa é recusada ou "limitada a zero". Também
    não está claro se o texto de observacao tem algum efeito.
  - Caso: CC-ENG-PLATAFORMA com hospedagem, que afeta d-010 e d-013 do exemplo
    atual.
  - Interpretações:
    - (a) recusada na etapa de categoria, com CATEGORIA_NAO_REEMBOLSAVEL;
    - (b) limitado, LIMITE_DIARIO, 0,00;
    - (c) um motivo novo.
  - Recomendação: (a), aplicada a qualquer categoria com limite 0. A decisão vem
    do limite, não do texto da observacao, que é só informativa.
  - Justificativa: "limitado" sugere que algo foi pago, e é mais útil dizer ao
    colaborador que o centro de custo dele não cobre aquela categoria.
  - Efeito colateral: d-013 passa de NOTA_FISCAL_AUSENTE para
    CATEGORIA_NAO_REEMBOLSAVEL, porque a etapa de categoria vem antes da etapa
    de nota fiscal.

  AMB-023 — Como funciona a representação

  - O que não está claro: se a representação divide o limite com alimentação
    (e-001 e f-003 são jantares), se exige nota fiscal e se o limite é por data.
  - Casos: e-001 (340,00), e-006 (GBP) e f-003 (centro de custo sem
    representação).
  - Interpretações:
    - (a) categoria independente, com o mesmo tratamento das outras;
    - (b) categoria com regras próprias.
  - Recomendação: (a). Limite próprio por data, a mesma regra de nota fiscal,
    entra na verificação de duplicatas, e a descrição continua sem ser
    interpretada (RN-014).
  - Justificativa: o JSON dá a ela o mesmo formato das outras categorias (limite
    e periodicidade: dia). Qualquer outro tratamento seria inventado.
  - Resultado: e-001 → 300,00, limitado.

  AMB-024 — Moeda ausente ou inválida

  - O que não está claro: o que fazer sem o campo moeda, com "usd" minúsculo,
    com texto vazio ou com número.
  - Caso: e-010 não tem moeda, e o exemplo da v3 inteiro também não tem.
  - Interpretações:
    - (a) moeda ausente = BRL;
    - (b) moeda ausente = DADOS_INVALIDOS.
  - Recomendação:
    - ausente → BRL;
    - texto → remover espaços e passar para maiúsculas;
    - vazio ou outro tipo → DADOS_INVALIDOS.
  - Justificativa: mantém compatibilidade com as entradas da v3. A política
    declara BRL como moeda_base.
  - Resultado: e-010 → 88,00, aprovado.

  AMB-025 — Moeda sem cotação

  - O que não está claro: o que fazer quando a moeda não está no arquivo de
    câmbio.
  - Caso: e-006 está em GBP, e o câmbio só tem USD e EUR. Um código como "XYZ"
    cai no mesmo caso.
  - Interpretações:
    - (a) recusar com um motivo novo, COTACAO_INDISPONIVEL;
    - (b) DADOS_INVALIDOS;
    - (c) erro geral.
  - Recomendação: (a). valor_considerado fica nulo.
  - Justificativa: o dado da despesa está correto, o que falta é a cotação. Pela
    AMB-017, uma despesa com problema não deve impedir o cálculo das outras.
    Não dá para separar "moeda inexistente" de "moeda sem cotação" sem uma lista
    ISO, e isso seria escopo novo.

  AMB-026 — Data sem cotação

  - O que não está claro: o câmbio só tem dias úteis e só vai de 07-13 a 07-28.
    Faltam 07-01 a 07-10 e 07-29 a 07-31, que são dias úteis.
  - Caso: e-004 (sábado, 07-18, 30 EUR).
  - Interpretações:
    - (a) usar a cotação mais recente na data da despesa ou antes dela,
      procurada para aquela moeda: 07-17, 5,96 → 178,80;
    - (b) usar a próxima cotação: 07-20, 6,01 → 180,30;
    - (c) recusar com COTACAO_INDISPONIVEL;
    - (d) igual a (a), mas com uma janela máxima de N dias.
  - Recomendação: (a). Se não existir nenhuma cotação anterior, recusar com
    COTACAO_INDISPONIVEL. A justificativa cita a data e a taxa usadas.
  - Justificativa: é a prática da PTAX (último fechamento disponível) e não usa
    dado futuro. "Dia útil anterior" exigiria um calendário de feriados, o que
    vai contra a RN-012.
  - Ponto de atenção: sem janela, uma despesa de 07-31 usaria a cotação de 07-28
    sem aviso. Se isso incomodar, a saída é (d), mas o N precisa vir do RH.
  - Resultado: e-004 → 90,00, limitado, qualquer que seja a interpretação. Só a
    justificativa muda.

  AMB-027 — Arredondamento na conversão

  - O que não está claro: se o valor é arredondado antes de converter, depois de
    converter, ou nas duas vezes.
  - Caso: nenhum no envelope. Todos os valores e taxas têm duas casas, então os
    produtos são exatos (por exemplo, 14,50 × 5,88 = 85,26). Um caso hipotético
    mostra a diferença: 33,333 USD × 5,42.
    - Arredondando uma vez, depois da conversão: 180,66486 → 180,66.
    - Arredondando duas vezes (33,33 × 5,42): 180,6486 → 180,65.
  - Recomendação:
    - multiplicar o valor informado, sem arredondar, pela taxa, também sem
      arredondar;
    - arredondar uma única vez para centavos de BRL, com a metade se afastando
      do zero (RN-003);
    - esse resultado é o valor_considerado.
  - Justificativa: arredondar duas vezes acumula erro. Assim se mantém o
    princípio da RN-003: um único valor em centavos antes das regras.

  AMB-028 — Nota fiscal depois da conversão

  - O que não está claro: se o limiar de 100,00 vale para o valor na moeda
    original ou em BRL.
  - Caso: e-005 tem 40 USD, sem nota. Em BRL, 40 × 5,50 = 220,00. Na moeda
    original, 40 < 100. e-002 tem 22 EUR, que em BRL vira 130,46.
  - Interpretações:
    - (a) comparar o valor em BRL;
    - (b) comparar na moeda original.
  - Recomendação: (a). e-005 é recusado com NOTA_FISCAL_AUSENTE.
  - Justificativa: a política declara moeda_base: BRL, então o "100" está em
    reais. Comparar na moeda original faria o limiar variar com o câmbio.

  AMB-029 — Em que ponto da ordem entra a conversão

  - O que não está claro: se a conversão vem antes ou depois das etapas que não
    usam valor (período e categoria).
  - Caso: e-006. Um caso hipotético: coworking em GBP.
  - Interpretações:
    - (a) logo depois da normalização, antes da etapa de valor negativo. Nesse
      caso, uma despesa fora do período e sem cotação é recusada por
      COTACAO_INDISPONIVEL;
    - (b) depois da etapa de categoria. O motivo fica mais útil, mas a checagem
      de valor negativo teria que usar o valor original, o que reabre o caso
      −0,004 da RN-003.
  - Recomendação: (a). Ordem: dados → normalização → conversão e arredondamento
    → negativo → período → categoria → duplicatas → nota fiscal → limite.
  - Justificativa: todas as regras passam a usar um único valor em BRL e a ordem
    atual das etapas não muda. O custo é aceitável: o motivo de algumas recusas
    fica menos informativo.

  AMB-030 — Duplicatas com moeda estrangeira

  - O que não está claro: se 22 EUR e 130,46 BRL, na mesma data e no mesmo
    fornecedor, são duplicatas.
  - Caso: nenhum no envelope.
  - Interpretações:
    - (a) comparar o valor_considerado em BRL, com qualquer moeda;
    - (b) exigir a mesma moeda e o mesmo valor original arredondado.
  - Recomendação: (b). Os outros critérios da RN-006 continuam iguais.
  - Justificativa: duplicata é o mesmo comprovante lançado duas vezes, e um
    mesmo comprovante tem uma única moeda. Bater em BRL entre moedas diferentes
    seria coincidência. Na mesma moeda e na mesma data, (b) e (a) dão o mesmo
    resultado.

  AMB-031 — Arquivo de política ausente ou inválido

  - O que não está claro:
    - se o arquivo é obrigatório;
    - o que fazer se ele não for JSON, se faltar padrao ou se um limite for
      negativo, não numérico ou NaN;
    - o que fazer com uma periodicidade diferente de dia/diaria, ou com uma
      moeda_base diferente de BRL.
  - Caso: nenhum no envelope.
  - Interpretações:
    - (a) erro geral, sem saída;
    - (b) usar como reserva a tabela v3 embutida no código.
  - Recomendação: (a) em todos esses casos. O arquivo é obrigatório.
  - Justificativa: o problema atinge todas as despesas, como os erros gerais da
    AMB-017. Ter uma reserva embutida criaria duas fontes da verdade.
  - Efeito na CLI: o comando calcular ganha um parâmetro obrigatório e quebra a
    chamada atual. Isso vai para o plan.md.

  AMB-032 — Arquivo de câmbio ausente ou inválido

  - O que não está claro:
    - se o arquivo é obrigatório quando todas as despesas estão em BRL;
    - o que fazer com taxa ≤ 0 ou não numérica, com data inválida como chave, ou
      com moeda_base diferente da moeda_base da política.
  - Caso: o exemplo v3, que só tem BRL.
  - Interpretações:
    - (a) obrigatório sempre;
    - (b) opcional: sem o arquivo, despesas estrangeiras são recusadas com
      COTACAO_INDISPONIVEL.
  - Recomendação:
    - (b);
    - um arquivo presente mas malformado → erro geral;
    - moeda_base diferente entre os dois arquivos → erro geral;
    - BRL sempre usa taxa 1, sem consulta ao arquivo.
  - Justificativa: um documento só em BRL não deve depender do câmbio. Já um
    arquivo corrompido não deve ser tratado como "não há cotação".

  AMB-033 — O que a saída mostra da conversão

  - O que não está claro: a saída atual não tem como mostrar a moeda, a taxa e a
    data da cotação.
  - Caso: e-002 a e-006 e f-004.
  - Recomendação:
    - valor_informado = valor na moeda original;
    - novos campos moeda, taxa_cambio e data_cotacao, nulos quando não se
      aplicam;
    - valores em BRL nas justificativas;
    - a justificativa de limite cita o centro de custo ou a política padrão.
  - Justificativa: sem isso, não dá para conferir à mão o critério "verificável"
    do objetivo da spec.

  AMB-034 — Vigência da política

  - O que não está claro: o que fazer com despesas de antes de vigencia: 
    2026-07-01.
  - Caso: nenhum. O d-008 de abril já é recusado por FORA_DO_PERIODO.
  - Recomendação: tratar versao e vigencia como informativas e registrar o tema
    na §10.
  - Justificativa: só existe uma política, e aplicar uma política anterior seria
    escopo novo.

  AMB-035 — Acréscimo em viagem agora está no arquivo

  - O que não está claro: se ter acrescimo_em_viagem_percentual: 50 no arquivo
    obriga a aplicar a ampliação.
  - Casos: e-002 ("Lisboa"), e-006 e e-007 ("Londres", "3 noites").
  - Recomendação: continua sem aplicar. AMB-006, AMB-007 e AMB-008 continuam
    valendo.
  - Justificativa: continua não existindo um dado estruturado que indique
    viagem. Moeda estrangeira também não prova viagem, porque compra online pode
    ser em dólar.

  AMB-036 — periodicidade "dia" e "diaria"

  - O que não está claro: se os dois valores querem dizer coisas diferentes.
  - Caso: hospedagem usa diaria em todos os centros de custo.
  - Recomendação: os dois valem por data e categoria, como na RN-008, com cada
    hospedagem contando como uma diária. Qualquer outro valor → erro geral
    (AMB-031).
  - Justificativa: é exatamente a semântica atual da RN-008, com a AMB-008
    mantida.

  ---

  Resultado esperado de despesas-envelope.json (CC-COMERCIAL), aplicando as 
  recomendações

  ┌───────┬─────────────────────┬───────────┬───────────────────────────────┐
  │ Item  │      Conversão      │ Reembolso │        Status / motivo        │
  ├───────┼─────────────────────┼───────────┼───────────────────────────────┤
  │ e-001 │ BRL 340,00          │ 300,00    │ limitado (representação, 300) │
  ├───────┼─────────────────────┼───────────┼───────────────────────────────┤
  │ e-002 │ 22 EUR × 5,93 =     │ 90,00     │ limitado                      │
  │       │ 130,46              │           │                               │
  ├───────┼─────────────────────┼───────────┼───────────────────────────────┤
  │ e-003 │ 14,50 EUR × 5,88 =  │ 85,26     │ aprovado (≤ 100, não exige    │
  │       │ 85,26               │           │ nota)                         │
  ├───────┼─────────────────────┼───────────┼───────────────────────────────┤
  │       │ 30 EUR × 5,96       │           │                               │
  │ e-004 │ (cotação de 07-17)  │ 90,00     │ limitado                      │
  │       │ = 178,80            │           │                               │
  ├───────┼─────────────────────┼───────────┼───────────────────────────────┤
  │ e-005 │ 40 USD × 5,50 =     │ 0,00      │ recusado, NOTA_FISCAL_AUSENTE │
  │       │ 220,00              │           │                               │
  ├───────┼─────────────────────┼───────────┼───────────────────────────────┤
  │ e-006 │ GBP sem cotação     │ 0,00      │ recusado,                     │
  │       │                     │           │ COTACAO_INDISPONIVEL          │
  ├───────┼─────────────────────┼───────────┼───────────────────────────────┤
  │ e-007 │ BRL 1.200,00        │ 400,00    │ limitado (1 diária, AMB-008)  │
  ├───────┼─────────────────────┼───────────┼───────────────────────────────┤
  │ e-008 │ BRL 95,00           │ 90,00     │ limitado                      │
  ├───────┼─────────────────────┼───────────┼───────────────────────────────┤
  │ e-009 │ coworking           │ 0,00      │ recusado,                     │
  │       │                     │           │ CATEGORIA_NAO_REEMBOLSAVEL    │
  ├───────┼─────────────────────┼───────────┼───────────────────────────────┤
  │ e-010 │ sem moeda → BRL     │ 88,00     │ aprovado                      │
  │       │ 88,00               │           │                               │
  ├───────┼─────────────────────┼───────────┼───────────────────────────────┤
  │ Total │                     │ 1.143,26  │                               │
  └───────┴─────────────────────┴───────────┴───────────────────────────────┘

  Decisões que mais precisam da sua revisão

  1. AMB-021: centro de custo sem a categoria herda da padrão ou recusa? Esta é
     a decisão de maior risco de negócio.
  2. AMB-019: centro de custo desconhecido usa a padrão ou dá erro geral?
  3. AMB-022: limite 0 recusa a despesa por categoria? Isso muda o motivo de
     d-013 no exemplo atual.
  4. AMB-026: cotação sem limite de dias para trás, ou com uma janela definida
     pelo RH?
  5. AMB-029: em que ponto da ordem entra a conversão?
  6. §9: aceita reescrever o critério de aceite do exemplo atual para 351,43?

✻ Cogitated for 4m 3s · done 17:03

> Acho boas as decisões que você recomendou.                                    
                                                                                
  Só quero fixar estes pontos antes de mexer na spec:                           
                                                                                
   se o centro de custo não vier, usa a política padrão;                        
   se vier um centro desconhecido, também usa a padrão;                         
   se uma categoria não existir no centro, herda da padrão;                     
   limite 0 significa categoria não reembolsável;                               
   moeda ausente = BRL;                                                         
   moeda sem cotação disponível recusa só aquela despesa;                       
   em fim de semana/feriado, usa a última cotação anterior disponível;          
   converte primeiro e arredonda uma vez só em BRL;                             
   a regra da nota fiscal usa o valor já convertido;                            
   duplicata precisa considerar a mesma moeda e o mesmo valor original;         
   politica-v4.json é obrigatório;                                              
   cambio.json só é necessário quando houver despesa em moeda estrangeira;      
  viagem continua sem acréscimo porque não existe campo estruturado dizendo que 
  o colaborador está em viagem;                                                 
   não vamos fazer o item C de aprovação manual.                                
                                                                                
  Pode também atualizar o exemplo atual da seção 9 para a v4 e usar o total     
  351,43                                                                        
                                                                                
  Agora atualize apenas:                                                        
  - spec.md                                                                     
  - DECISIONS.md                                                                
                                                                                
  Não mexa em tasks.md ainda                                                    
  Não mexa em código.                                                           
  Não faça commit                                                               
                                                                                
  No fim, me diga resumidamente o que mudou para eu revisar.                    

  Ran 2 shell commands (ctrl+o to expand)

● Vou reescrever a spec.md (são muitas seções afetadas) e depois incluir a D-002
  no DECISIONS.md.

● Write(specs\001-motor-reembolso\spec.md)
  ⎿  Added 634 lines, removed 123 lines
      1  # Spec — Motor de Cálculo de Reembolso
      2  
      3 -**Versão:** 1.1 · **Status:** rascunho · **Última alteração:** 2
        -026-10-04                                                       
      3 +**Versão:** 2.0 · **Status:** rascunho · **Última alteração:** 2
        +026-10-04                                                       
      4  
      5  > **Regra de ouro deste arquivo:** ele descreve o QUÊ e o PORQUÊ
         . Nenhuma linha
      6  > aqui pode citar linguagem, biblioteca, classe, função ou estru
         tura de pasta.
     ...
      26  
      27  ## 3. Fora de escopo
      28  
      29 -- Não aplica a ampliação de limites para colaborador em viagem 
         -(ver AMB-006).                                                 
      29 +- Não aplica a ampliação de limites para colaborador em viagem 
         +(ver AMB-006, AMB-035).                                        
      30  - Não processa mais de um colaborador ou mais de um período por
           execução.
      31  - Não verifica a autenticidade da nota fiscal; considera apenas
           a informação
      32    "tem nota fiscal" declarada na entrada.
      33  - Não detecta duplicatas entre execuções diferentes nem guarda 
          histórico.
      34  - Não compensa estornos com despesas de outros períodos.
      35  - Não interpreta o texto da descrição para nenhum cálculo ou de
          cisão.
      36 -- Não converte moedas; todos os valores estão em reais.        
      36 +- Não aplica IOF, spread ou tarifa na conversão de moeda; usa s
         +ó a taxa do                                                    
      37 +  documento de câmbio (RN-018).                                
      38 +- Não escolhe política por vigência; aplica o documento de polí
         +tica informado,                                                
      39 +  qualquer que seja o período (AMB-034).                       
      40 +- Não trata aprovação manual de despesas (item C da política v4
         +, opcional).                                                   
      41  - Não aprova nem efetua pagamento; apenas calcula e justifica.
      38 -- Não reembolsa categorias além de alimentação, transporte urba
         -no e hospedagem.                                               
      42 +- Não reembolsa categorias que não constam da política aplicáve
         +l (RN-001).                                                    
      43  
      44  ## 4. Entrada e saída
      45  
      42 -**Entrada:** um documento no formato de `exemplos/despesas-exem
         -plo.json`.                                                     
      46 +**Entrada:** três documentos.                                  
      47  
      48 +- **Despesas:** obrigatório, no formato de `exemplos/despesas-e
         +xemplo.json` ou                                                
      49 +  `exemplos/envelope/despesas-envelope.json` (campos abaixo).  
      50 +- **Política:** obrigatório, no formato de `exemplos/envelope/p
         +olitica-v4.json`                                               
      51 +  (RN-015).                                                    
      52 +- **Câmbio:** no formato de `exemplos/envelope/cambio.json`; só
         + é necessário                                                  
      53 +  quando houver despesa em moeda estrangeira (RN-018).         
      54 +                                                               
      55 +Campos do documento de despesas:                               
      56 +                                                               
      57  | Campo | Tipo | Significado | Obrigatório |
      58  |---|---|---|---|
      59  | `colaborador.id` | texto | Identificador do colaborador | sim
           |
      60  | `colaborador.nome` | texto | Nome do colaborador (informativo
          ) | não |
      48 -| `colaborador.centro_custo` | texto | Centro de custo (informa
         -tivo) | não |                                                  
      61 +| `colaborador.centro_custo` | texto | Centro de custo; escolhe
         + a política aplicável (RN-016) | não |                         
      62  | `periodo.competencia` | texto `AAAA-MM` | Mês de competência 
          (informativo; ver AMB-009) | não |
      63  | `periodo.inicio` | data `AAAA-MM-DD` | Primeiro dia do períod
          o | sim |
      64  | `periodo.fim` | data `AAAA-MM-DD` | Último dia do período | s
          im |
     ...
      68  | `despesas[].categoria` | texto | Categoria da despesa | sim |
      69  | `despesas[].descricao` | texto | Descrição livre (informativa
          ; nunca usada em cálculo) | não |
      70  | `despesas[].fornecedor` | texto | Nome do fornecedor | sim |
      58 -| `despesas[].valor` | número | Valor em reais; pode ter mais d
         -e duas casas decimais ou ser negativo | sim |                  
      71 +| `despesas[].valor` | número | Valor na moeda da despesa; pode
         + ter mais de duas casas decimais ou ser negativo | sim |       
      72 +| `despesas[].moeda` | texto | Código da moeda da despesa; `BRL
         +` se ausente (RN-017) | não |                                  
      73  | `despesas[].tem_nota_fiscal` | verdadeiro/falso | Se há nota 
          fiscal | sim |
      74  
      75  A **posição** de uma despesa é a sua ordem na lista `despesas`,
           começando em 1.
     ...
       86  | `periodo` | objeto | Cópia do objeto `periodo` da entrada |
       87  | `itens` | lista | Um item para cada despesa da entrada, na m
           esma ordem |
       88  | `itens[].id` | texto ou nulo | `id` da despesa; nulo se ause
           nte, vazio ou com tipo inválido |
       75 -| `itens[].valor_informado` | número ou nulo | Valor numérico 
          -de `valor` na entrada, sem arredondamento; nulo se ausente ou 
          -não numérico. Só o valor importa, não a grafia: `72.5` e `72.5
          -0` são o mesmo valor |                                        
       76 -| `itens[].valor_considerado` | número ou nulo | Valor arredon
          -dado para centavos (RN-003); nulo sempre que o motivo for `DAD
          -OS_INVALIDOS` |                                               
       77 -| `itens[].valor_reembolsavel` | número | Valor a reembolsar, 
          -com duas casas decimais |                                     
       89 +| `itens[].valor_informado` | número ou nulo | Valor numérico 
          +de `valor` na entrada, na moeda da despesa, sem arredondamento
          +; nulo se ausente ou não numérico. Só o valor importa, não a g
          +rafia: `72.5` e `72.50` são o mesmo valor |                   
       90 +| `itens[].moeda` | texto ou nulo | Moeda da despesa após a no
          +rmalização (RN-017); nulo sempre que o motivo for `DADOS_INVAL
          +IDOS` |                                                       
       91 +| `itens[].taxa_cambio` | número ou nulo | Taxa usada na conve
          +rsão, como está no documento de câmbio; nulo quando a moeda é 
          +`BRL` ou não houve conversão |                                
       92 +| `itens[].data_cotacao` | data ou nulo | Data da taxa usada (
          +RN-018); nulo quando `taxa_cambio` é nulo |                   
       93 +| `itens[].valor_considerado` | número ou nulo | Valor em reai
          +s, convertido e arredondado para centavos (RN-003, RN-018); nu
          +lo sempre que o motivo for `DADOS_INVALIDOS` ou `COTACAO_INDIS
          +PONIVEL` |                                                    
       94 +| `itens[].valor_reembolsavel` | número | Valor a reembolsar, 
          +em reais, com duas casas decimais |                           
       95  | `itens[].status` | texto | `aprovado`, `limitado` ou `recusa
           do` (definições abaixo) |
       96  | `itens[].motivo` | texto ou nulo | Código do motivo (tabela 
           abaixo); nulo quando `aprovado` |
       97  | `itens[].justificativa` | texto | Explicação legível da deci
           são, citando a regra (RN-xxx) |
       81 -| `total_reembolsavel` | número | Soma de `valor_reembolsavel`
          - de todos os itens |                                          
       98 +| `total_reembolsavel` | número | Soma de `valor_reembolsavel`
          + de todos os itens, em reais |                                
       99  
      100  **Status:**
      101  
     ...
      109  
      110  | Código | Status | Regra |
      111  |---|---|---|
       95 -| `DADOS_INVALIDOS` | recusado | RN-013 |                     
      112 +| `DADOS_INVALIDOS` | recusado | RN-013, RN-017 |             
      113 +| `COTACAO_INDISPONIVEL` | recusado | RN-018 |                
      114  | `VALOR_NEGATIVO` | recusado | RN-005 |
      115  | `FORA_DO_PERIODO` | recusado | RN-004 |
       98 -| `CATEGORIA_NAO_REEMBOLSAVEL` | recusado | RN-001 |          
      116 +| `CATEGORIA_NAO_REEMBOLSAVEL` | recusado | RN-001, RN-016 |  
      117  | `DUPLICATA` | recusado | RN-006 |
      118  | `NOTA_FISCAL_AUSENTE` | recusado | RN-007 |
      119  | `LIMITE_DIARIO` | limitado | RN-008, RN-009, RN-010 |
      120  
      103 -A justificativa deve citar o `id` da despesa mantida, no caso 
          -de `DUPLICATA`, e o                                           
      104 -limite com o valor já consumido no dia, no caso de `LIMITE_DIA
          -RIO`.                                                         
      121 +A justificativa deve citar:                                   
      122  
      106 -**Exemplo** (entrada com período de 2026-07-01 a 2026-07-31): 
      123 +- no caso de `DUPLICATA`, o `id` da despesa mantida;          
      124 +- no caso de `LIMITE_DIARIO`, o limite, o valor já consumido n
          +o dia e a                                                     
      125 +  política de onde o limite veio (centro de custo ou política 
          +padrão, RN-016);                                              
      126 +- no caso de `CATEGORIA_NAO_REEMBOLSAVEL`, a política aplicada
          +;                                                             
      127 +- no caso de `COTACAO_INDISPONIVEL`, a moeda e a data da despe
          +sa.                                                           
      128  
      129 +**Exemplo 1** (`exemplos/despesas-exemplo.json`, centro de cus
          +to                                                            
      130 +`CC-ENG-PLATAFORMA`, período de 2026-07-01 a 2026-07-31):     
      131 +                                                              
      132  Entrada (trecho):
      133  
      134  ```
     ...
      141  
      142  ```
      143  "itens": [
      120 -  { "id": "d-001", "valor_informado": 72.50, "valor_considerad
          -o": 72.50, "valor_reembolsavel": 60.00,                       
      144 +  { "id": "d-001", "valor_informado": 72.50, "moeda": "BRL", "
          +taxa_cambio": null, "data_cotacao": null,                     
      145 +    "valor_considerado": 72.50, "valor_reembolsavel": 72.50,  
      146 +    "status": "aprovado", "motivo": null,                     
      147 +    "justificativa": "Despesa aprovada: passou por todas as re
          +gras e é reembolsada integralmente (RN-001, RN-004 a RN-008)."
          + },                                                           
      148 +  { "id": "d-002", "valor_informado": 38.00, "moeda": "BRL", "
          +taxa_cambio": null, "data_cotacao": null,                     
      149 +    "valor_considerado": 38.00, "valor_reembolsavel": 2.50,   
      150      "status": "limitado", "motivo": "LIMITE_DIARIO",
      122 -    "justificativa": "Limite diário de alimentação de R$ 60,00
          - aplicado; excedente de R$ 12,50 cortado (RN-008, RN-010)." },
      123 -  { "id": "d-002", "valor_informado": 38.00, "valor_considerad
          -o": 38.00, "valor_reembolsavel": 0.00,                        
      124 -    "status": "limitado", "motivo": "LIMITE_DIARIO",          
      125 -    "justificativa": "Limite diário de alimentação de R$ 60,00
          - já consumido por d-001 em 2026-07-03 (RN-008, RN-009)." },   
      126 -  { "id": "d-004", "valor_informado": 100.01, "valor_considera
          -do": 100.01, "valor_reembolsavel": 0.00,                      
      151 +    "justificativa": "Limite diário de alimentação de R$ 75,00
          + (centro de custo CC-ENG-PLATAFORMA), com R$ 72,50 já consumid
          +o por d-001 em 2026-07-03; excedente de R$ 35,50 cortado (RN-0
          +08, RN-009, RN-010)." },                                      
      152 +  { "id": "d-004", "valor_informado": 100.01, "moeda": "BRL", 
          +"taxa_cambio": null, "data_cotacao": null,                    
      153 +    "valor_considerado": 100.01, "valor_reembolsavel": 0.00,  
      154      "status": "recusado", "motivo": "NOTA_FISCAL_AUSENTE",
      155      "justificativa": "Valor acima de R$ 100,00 sem nota fiscal
            (RN-007)." }
      156  ],
      130 -"total_reembolsavel": 60.00                                   
      157 +"total_reembolsavel": 75.00                                   
      158  ```
      159  
      160 +**Exemplo 2** (`exemplos/envelope/despesas-envelope.json`, cen
          +tro de custo                                                  
      161 +`CC-COMERCIAL`, despesa em euro):                             
      162 +                                                              
      163 +Entrada (trecho):                                             
      164 +                                                              
      165 +```                                                           
      166 +{ "id": "e-002", "data": "2026-07-14", "categoria": "alimentac
          +ao", "fornecedor": "Taberna do Chiado", "valor": 22.00, "moeda
          +": "EUR", "tem_nota_fiscal": true }                           
      167 +```                                                           
      168 +                                                              
      169 +Saída (trecho):                                               
      170 +                                                              
      171 +```                                                           
      172 +{ "id": "e-002", "valor_informado": 22.00, "moeda": "EUR", "ta
          +xa_cambio": 5.93, "data_cotacao": "2026-07-14",               
      173 +  "valor_considerado": 130.46, "valor_reembolsavel": 90.00,   
      174 +  "status": "limitado", "motivo": "LIMITE_DIARIO",            
      175 +  "justificativa": "Limite diário de alimentação de R$ 90,00 (
          +centro de custo CC-COMERCIAL) aplicado; excedente de R$ 40,46 
          +cortado (RN-008, RN-010)." }                                  
      176 +```                                                           
      177 +                                                              
      178  ## 5. Regras de negócio
      179  
      180  ### RN-001 — Categorias reembolsáveis
      181  
      137 -**Regra:** Só são reembolsáveis as categorias `alimentacao`, `
          -transporte_urbano`                                            
      138 -e `hospedagem`, comparadas depois da normalização (RN-002). Qu
          -alquer outra                                                  
      139 -categoria é recusada com `CATEGORIA_NAO_REEMBOLSAVEL`.        
      140 -**Origem:** política do RH, item 9 (AMB-014)                  
      182 +**Regra:** Uma categoria é reembolsável quando consta da polít
          +ica aplicável                                                 
      183 +(RN-016) com limite maior que zero, comparada depois da normal
          +ização (RN-002).                                              
      184 +É recusada com `CATEGORIA_NAO_REEMBOLSAVEL` a despesa cuja cat
          +egoria:                                                       
      185 +                                                              
      186 +- não consta nem da tabela do centro de custo nem da política 
          +padrão; ou                                                    
      187 +- consta com limite 0,00. Limite zero significa "não reembolsá
          +vel naquele centro                                            
      188 +  de custo". O texto de `observacao` do documento de política 
          +não é usado.                                                  
      189 +                                                              
      190 +Categorias não são encaixadas por semelhança.                 
      191 +**Origem:** política do RH, item 9; política v4 (AMB-014, AMB-
          +021, AMB-022, AMB-023)                                        
      192  **Aceite:** d-005 (`coworking`, 89,00) → recusado, 0,00, `CATE
           GORIA_NAO_REEMBOLSAVEL`.
      193 +d-010 e d-013 (hospedagem, `CC-ENG-PLATAFORMA`, limite 0,00) →
          + recusados,                                                   
      194 +`CATEGORIA_NAO_REEMBOLSAVEL`. f-003 (`representacao`, política
          + padrão) →                                                    
      195 +recusado. e-001 (`representacao`, `CC-COMERCIAL`) → reembolsáv
          +el.                                                           
      196  
      197  ### RN-002 — Normalização de texto
      198  
      145 -**Regra:** Antes de qualquer comparação, categoria e fornecedo
          -r são normalizados:                                           
      146 -espaços no início e no fim são removidos, letras maiúsculas vi
          -ram minúsculas e                                              
      147 -acentos são removidos. A normalização não altera mais nada; es
          -paços internos e                                              
      148 -outros caracteres são mantidos.                               
      149 -**Origem:** decisão desta spec (AMB-013)                      
      199 +**Regra:** Antes de qualquer comparação, categoria, fornecedor
          + e centro de custo                                            
      200 +são normalizados: espaços no início e no fim são removidos, le
          +tras maiúsculas                                               
      201 +viram minúsculas e acentos são removidos. A normalização não a
          +ltera mais nada;                                              
      202 +espaços internos e outros caracteres são mantidos. As chaves d
          +e categoria e de                                              
      203 +centro de custo do documento de política passam pela mesma nor
          +malização.                                                    
      204 +**Origem:** decisão desta spec (AMB-013, AMB-020)             
      205  **Aceite:** categoria `ALIMENTACAO`, ` Alimentação ` e `alimen
           tacao` são tratadas
      206  como `alimentacao`. Fornecedores `Bistro Central` e `bistro ce
           ntral` são iguais.
      207 +Centro de custo ` cc-comercial ` é o mesmo que `CC-COMERCIAL`.
      208  
      209  ### RN-003 — Arredondamento
      210  
      155 -**Regra:** O valor de cada despesa é arredondado para centavos
          - antes de qualquer                                            
      156 -outra regra, com arredondamento comercial: a metade se afasta 
          -do zero (0,005                                                
      157 -vira 0,01). Todas as regras seguintes usam o valor arredondado
      158 -(`valor_considerado`). Na saída, `valor_considerado`, `valor_r
          -eembolsavel` e                                                
      159 -`total_reembolsavel` têm duas casas decimais; `valor_informado
          -` não é                                                       
      160 -arredondado e mantém as casas que tinha na entrada.           
      161 -**Origem:** decisão desta spec (AMB-012)                      
      211 +**Regra:** O valor de cada despesa é convertido para reais (RN
          +-018) e só então                                              
      212 +arredondado para centavos, **uma única vez**, com arredondamen
          +to comercial: a                                               
      213 +metade se afasta do zero (0,005 vira 0,01). O valor informado 
          +e a taxa não são                                              
      214 +arredondados antes da multiplicação. Em `BRL`, a conversão não
          + altera o valor.                                              
      215 +Todas as regras seguintes usam o valor resultante (`valor_cons
          +iderado`). Na                                                 
      216 +saída, `valor_considerado`, `valor_reembolsavel` e `total_reem
          +bolsavel` têm duas                                            
      217 +casas decimais; `valor_informado` e `taxa_cambio` não são arre
          +dondados.                                                     
      218 +**Origem:** decisão desta spec (AMB-012, AMB-027)             
      219  **Aceite:** d-011 (33,333) → `valor_considerado` 33,33. Valor 
           10,005 → 10,01.
      163 -Valor −0,004 → 0,00, tratado como valor zero (RN-005).        
      220 +Valor −0,004 → 0,00, tratado como valor zero (RN-005). 33,333 
          +USD em 2026-07-13                                             
      221 +(taxa 5,42) → 180,66486 → 180,66 (e não 180,65, que sairia de 
          +33,33 × 5,42).                                                
      222  
      223  ### RN-004 — Período de competência
      224  
     ...
      242  ### RN-006 — Duplicatas
      243  
      244  **Regra:** Duas ou mais despesas são duplicatas quando têm a m
           esma `data`, a
      187 -mesma categoria normalizada, o mesmo fornecedor normalizado e 
          -o mesmo                                                       
      188 -`valor_considerado`. Só despesas que passaram por RN-001, RN-0
          -04, RN-005 e RN-013                                           
      189 -participam dessa comparação. Em cada grupo de duplicatas, uma 
          -despesa é mantida:                                            
      245 +mesma categoria normalizada, o mesmo fornecedor normalizado, a
          + mesma moeda                                                  
      246 +(RN-017) e o mesmo valor informado arredondado para centavos n
          +a moeda original                                              
      247 +(com o arredondamento da RN-003). Em `BRL`, esse valor é o pró
          +prio                                                          
      248 +`valor_considerado`. Só despesas que passaram por RN-001, RN-0
          +04, RN-005,                                                   
      249 +RN-013 e RN-018 participam dessa comparação. Em cada grupo de 
          +duplicatas, uma                                               
      250 +despesa é mantida:                                            
      251  
      252  1. se houver despesas com nota fiscal no grupo, fica a de meno
           r posição entre elas;
      253  2. se nenhuma tiver nota fiscal, fica a de menor posição.
      254  
      255  As demais são recusadas com `DUPLICATA`, e a justificativa cit
           a o `id` da mantida.
      256  `id` e `descricao` não participam da comparação.
      196 -**Origem:** política do RH, item 8 (AMB-010)                  
      257 +**Origem:** política do RH, item 8 (AMB-010, AMB-030)         
      258  **Aceite:** d-006 e d-007 (2026-07-09, alimentação, Bistro Cen
           tral, 54,90, ambas
      259  com nota) → d-006 mantida; d-007 recusada, `DUPLICATA`, citand
           o d-006. Grupo em
      260  que só a segunda despesa tem nota → a segunda é mantida e a pr
           imeira é recusada.
      261 +Duas despesas de 22,00 EUR com a mesma data, categoria e forne
          +cedor → duplicatas.                                           
      262 +22,00 EUR e 130,46 BRL com a mesma data, categoria e fornecedo
          +r → não são                                                   
      263 +duplicatas.                                                   
      264  
      265  ### RN-007 — Nota fiscal
      266  
      203 -**Regra:** Despesa com `valor_considerado` estritamente maior 
          -que 100,00 e sem                                              
      204 -nota fiscal é recusada inteira com `NOTA_FISCAL_AUSENTE`. A ve
          -rificação usa o                                               
      205 -valor da própria despesa, e não a soma do dia nem o valor após
          - o limite.                                                    
      206 -Despesa de exatamente 100,00 não exige nota.                  
      207 -**Origem:** política do RH, item 5 (AMB-004, AMB-005)         
      267 +**Regra:** Despesa com `valor_considerado` (em reais, depois d
          +a conversão)                                                  
      268 +estritamente maior que o limiar `nota_fiscal_obrigatoria_acima
          +_de` do documento                                             
      269 +de política (100,00 na v4) e sem nota fiscal é recusada inteir
          +a com                                                         
      270 +`NOTA_FISCAL_AUSENTE`. A verificação usa o valor da própria de
          +spesa, e não a                                                
      271 +soma do dia nem o valor após o limite. Despesa de valor exatam
          +ente igual ao                                                 
      272 +limiar não exige nota.                                        
      273 +**Origem:** política do RH, item 5; política v4 (AMB-004, AMB-
          +005, AMB-028)                                                 
      274  **Aceite:** d-003 (100,00, sem nota) → não exige nota. d-004 (
           100,01, sem nota)
      209 -→ recusado, 0,00, `NOTA_FISCAL_AUSENTE`. d-013 (690,00, sem no
          -ta) → recusado.                                               
      275 +→ recusado, 0,00, `NOTA_FISCAL_AUSENTE`. e-005 (40,00 USD × 5,
          +50 = 220,00, sem                                              
      276 +nota) → recusado, `NOTA_FISCAL_AUSENTE`. e-003 (14,50 EUR × 5,
          +88 = 85,26, sem                                               
      277 +nota) → não exige nota.                                       
      278  
      279  ### RN-008 — Limites diários por categoria
      280  
      281  **Regra:** Para cada combinação de data e categoria, a soma re
           embolsada não
      214 -ultrapassa o limite:                                          
      282 +ultrapassa o limite da categoria na política aplicável (RN-016
          +). As                                                         
      283 +periodicidades `dia` e `diaria` do documento de política signi
          +ficam, as duas,                                               
      284 +limite por data.                                              
      285  
      216 -| Categoria | Limite por data |                               
      217 -|---|---|                                                     
      218 -| `alimentacao` | R$ 60,00 |                                  
      219 -| `transporte_urbano` | R$ 80,00 |                            
      220 -| `hospedagem` | R$ 250,00 |                                  
      221 -                                                              
      286  Cada despesa de hospedagem vale uma diária, qualquer que seja 
           o texto da
      223 -descrição. Como o limite é por data, várias hospedagens na mes
          -ma data dividem                                               
      224 -o mesmo limite de R$ 250,00. Só despesas que passaram por toda
          -s as regras                                                   
      287 +descrição. Como o limite é por data, várias despesas da mesma 
          +categoria na                                                  
      288 +mesma data dividem o mesmo limite. Só despesas que passaram po
          +r todas as regras                                             
      289  anteriores consomem o limite.
      226 -**Origem:** política do RH, itens 1, 2 e 3 (AMB-001, AMB-008) 
      227 -**Aceite:** d-010 (hospedagem, 480,00, descrição "2 diarias") 
          -→ 250,00, `limitado`.                                         
      228 -d-001 + d-002 (alimentação, 2026-07-03, 110,50 no total) → som
          -a reembolsada 60,00.                                          
      290  
      291 +Para conferência, a política v4 (`exemplos/envelope/politica-v
          +4.json`) resulta                                              
      292 +nos limites por data abaixo. Se o documento de política mudar,
          + valem os valores                                             
      293 +do documento.                                                 
      294 +                                                              
      295 +| Categoria | Padrão | `CC-ENG-PLATAFORMA` | `CC-COMERCIAL` | 
          +`CC-ADM` |                                                    
      296 +|---|---|---|---|---|                                         
      297 +| `alimentacao` | R$ 60,00 | R$ 75,00 | R$ 90,00 | R$ 45,00 | 
      298 +| `transporte_urbano` | R$ 80,00 | R$ 80,00 | R$ 150,00 | R$ 6
          +0,00 |                                                        
      299 +| `hospedagem` | R$ 250,00 | não reembolsável (0,00) | R$ 400,
          +00 | R$ 250,00 (herdado da padrão) |                          
      300 +| `representacao` | não consta | não consta | R$ 300,00 | não 
          +consta |                                                      
      301 +                                                              
      302 +"Não consta" e "não reembolsável" levam à recusa pela RN-001. 
      303 +**Origem:** política do RH, itens 1, 2 e 3; política v4 (AMB-0
          +01, AMB-008, AMB-023, AMB-036)                                
      304 +**Aceite:** e-007 (hospedagem, `CC-COMERCIAL`, 1.200,00, descr
          +ição "3 noites")                                              
      305 +→ 400,00, `limitado`. d-001 + d-002 (alimentação, `CC-ENG-PLAT
          +AFORMA`,                                                      
      306 +2026-07-03, 110,50 no total) → soma reembolsada 75,00. e-001 (
          +representação,                                                
      307 +`CC-COMERCIAL`, 340,00) → 300,00, `limitado`.                 
      308 +                                                              
      309  ### RN-009 — Distribuição do limite entre despesas da mesma da
           ta
      310  
      311  **Regra:** Quando várias despesas da mesma categoria e data di
           sputam o limite,
      312  ele é consumido na ordem da posição: cada despesa recebe o men
           or valor entre o
      313  seu `valor_considerado` e o saldo do limite que restou das ant
           eriores.
      314  **Origem:** decisão desta spec (AMB-002)
      236 -**Aceite:** d-001 (posição 1, 72,50) → 60,00; d-002 (posição 2
          -, 38,00) → 0,00,                                              
      315 +**Aceite:** d-001 (posição 1, 72,50) → 72,50; d-002 (posição 2
          +, 38,00) → 2,50,                                              
      316  `limitado`, justificativa citando d-001.
      317  
      318  ### RN-010 — Reembolso parcial
     ...
      320  **Regra:** Despesa que ultrapassa o saldo do limite é reembols
           ada até o saldo; o
      321  excedente é cortado. A despesa não é recusada por ultrapassar 
           o limite.
      322  **Origem:** política do RH, item 4 (AMB-003)
      244 -**Aceite:** d-014 (alimentação, 61,00) → 60,00, `limitado`, `L
          -IMITE_DIARIO`.                                                
      323 +**Aceite:** e-008 (alimentação, `CC-COMERCIAL`, 95,00) → 90,00
          +, `limitado`,                                                 
      324 +`LIMITE_DIARIO`.                                              
      325  
      326  ### RN-011 — Ampliação para colaborador em viagem
      327  
      248 -**Regra:** A ampliação de 50% dos limites prevista pela políti
          -ca **não é                                                    
      249 -aplicada**. A entrada não traz nenhuma informação estruturada 
          -que indique viagem.                                           
      250 -**Origem:** política do RH, item 6 (AMB-006, AMB-007)         
      328 +**Regra:** A ampliação dos limites prevista pela política     
      329 +(`acrescimo_em_viagem_percentual`, 50% na v4) **não é aplicada
          +**. A entrada não                                             
      330 +traz nenhuma informação estruturada que indique viagem; moeda 
          +estrangeira e                                                 
      331 +descrição não são tratadas como indício de viagem.            
      332 +**Origem:** política do RH, item 6; política v4 (AMB-006, AMB-
          +007, AMB-035)                                                 
      333  **Aceite:** d-003 ("Corrida aeroporto", 100,00) → limite de 80
           ,00 aplicado,
      252 -reembolso 80,00. Nenhuma despesa do exemplo recebe limite acim
          -a da tabela da RN-008.                                        
      334 +reembolso 80,00. e-002 ("Almoco - Lisboa", EUR) → limite de 90
          +,00 do                                                        
      335 +`CC-COMERCIAL`, sem acréscimo. Nenhuma despesa recebe limite a
          +cima do da                                                    
      336 +política aplicável.                                           
      337  
      338  ### RN-012 — Dias do calendário
      339  
      340  **Regra:** Todas as datas do calendário são tratadas da mesma 
           forma; não há
      257 -distinção entre dias úteis, fins de semana e feriados.        
      341 +distinção entre dias úteis, fins de semana e feriados. A falta
          + de cotação em                                                
      342 +fins de semana e feriados é tratada pela RN-018, sem calendári
          +o de feriados.                                                
      343  **Origem:** decisão desta spec (AMB-015)
      344  **Aceite:** d-012 (sábado, 2026-07-18, alimentação, 47,20) → a
           provado, 47,20.
      345  
     ...
      352  `AAAA-MM-DD` e existe no calendário (2026-02-30 não é válida).
      353  
      354  - **Erro geral:** o sistema encerra com mensagem de erro e não
            gera saída quando:
      270 -  - o documento de entrada não pode ser lido, o que inclui doc
          -umento que não                                                
      355 +  - o documento de despesas não pode ser lido, o que inclui do
          +cumento que não                                               
      356      segue o formato JSON, como `NaN` ou `Infinity` em qualquer
            campo;
      357    - `colaborador` ou `periodo` estão ausentes ou não são objet
           o;
      358    - `colaborador.id` está ausente, vazio ou não é texto;
      359 +  - `colaborador.centro_custo` está presente e não é texto (RN
          +-016);                                                        
      360    - `periodo.inicio` ou `periodo.fim` estão ausentes ou não sã
           o data válida;
      361    - `periodo.inicio` é posterior a `periodo.fim`;
      362    - `despesas` está ausente ou não é lista;
      277 -  - algum item de `despesas` não é objeto.                    
      363 +  - algum item de `despesas` não é objeto;                    
      364 +  - o documento de política está ausente ou é inválido (RN-015
          +);                                                            
      365 +  - o documento de câmbio foi informado e é inválido (RN-018).
      366  - **Erro em uma despesa:** apenas essa despesa é recusada com 
           `DADOS_INVALIDOS`,
      367    e as demais são processadas normalmente, quando:
      368    - falta um campo obrigatório da despesa, ou um campo obrigat
           ório de texto
     ...
      370    - `id`, `categoria` ou `fornecedor` não são texto;
      371    - `data` não é data válida;
      372    - `valor` não é numérico;
      285 -  - `tem_nota_fiscal` não é verdadeiro/falso.                 
      373 +  - `tem_nota_fiscal` não é verdadeiro/falso;                 
      374 +  - `moeda` está presente e é vazia ou não é texto (RN-017).  
      375  
      287 -  Na saída, a despesa recusada por `DADOS_INVALIDOS` tem `valo
          -r_considerado`                                                
      288 -  nulo, e também `id` nulo quando o problema está no `id`.    
      376 +  Na saída, a despesa recusada por `DADOS_INVALIDOS` tem `valo
          +r_considerado` e                                              
      377 +  `moeda` nulos, e também `id` nulo quando o problema está no 
          +`id`.                                                         
      378  - **Campos informativos e desconhecidos:** `colaborador.nome`,
      290 -  `colaborador.centro_custo`, `periodo.competencia` e `despesa
          -s[].descricao`,                                               
      291 -  além de qualquer campo que não conste da tabela de entrada, 
          -não são validados                                             
      292 -  e nunca participam de cálculo ou decisão. Tipo ou formato er
          -rado nesses campos                                            
      293 -  não gera erro.                                              
      379 +  `periodo.competencia` e `despesas[].descricao`, além de qual
          +quer campo que não                                            
      380 +  conste da tabela de entrada, não são validados e nunca parti
          +cipam de cálculo                                              
      381 +  ou decisão. Tipo ou formato errado nesses campos não gera er
          +ro.                                                           
      382  
      295 -**Origem:** decisão desta spec (AMB-017)                      
      383 +**Origem:** decisão desta spec (AMB-017, AMB-018, AMB-024, AMB
          +-031, AMB-032)                                                
      384  **Aceite:** despesa sem `tem_nota_fiscal` → recusado, `DADOS_I
           NVALIDOS`, e as
      385  outras despesas do documento aparecem na saída normalmente. Do
           cumento sem
      386  `periodo.fim` → erro, sem arquivo de saída. Despesa com `forne
           cedor` igual a
      387  `"   "` → recusado, `DADOS_INVALIDOS`. Despesa com `id` numéri
           co → recusado,
      388  `DADOS_INVALIDOS`, `itens[].id` nulo. `periodo.inicio` igual a
            `2026-02-30` →
      301 -erro, sem arquivo de saída. Despesa com `"moeda": "USD"` → cam
          -po ignorado.                                                  
      389 +erro, sem arquivo de saída. Despesa com `"projeto": "X"` → cam
          +po ignorado.                                                  
      390  
      391  ### RN-014 — Descrição é informativa
      392  
      393  **Regra:** O campo `descricao` nunca altera nenhum cálculo ou 
           decisão. Só campos
      306 -estruturados (data, categoria, fornecedor, valor, nota fiscal,
          - período e                                                    
      307 -posição) determinam o resultado.                              
      394 +estruturados (data, categoria, fornecedor, valor, moeda, nota 
          +fiscal, período,                                              
      395 +centro de custo e posição) e os documentos de política e de câ
          +mbio determinam o                                             
      396 +resultado.                                                    
      397  **Origem:** decisão desta spec (AMB-006, AMB-008, AMB-010)
      309 -**Aceite:** trocar a descrição de qualquer despesa do exemplo 
          -não altera nenhum                                             
      398 +**Aceite:** trocar a descrição de qualquer despesa dos exemplo
          +s não altera nenhum                                           
      399  `valor_reembolsavel`, `status` ou `motivo`.
      400  
      401 +### RN-015 — Documento de política                            
      402 +                                                              
      403 +**Regra:** Os valores da política vêm de um documento de polít
          +ica, obrigatório                                              
      404 +em toda execução, no formato de `exemplos/envelope/politica-v4
          +.json`:                                                       
      405 +                                                              
      406 +| Campo | Tipo | Significado | Obrigatório |                  
      407 +|---|---|---|---|                                             
      408 +| `moeda_base` | texto | Moeda dos limites e do limiar da nota
          + fiscal; deve ser `BRL` após a normalização da RN-017 | sim | 
      409 +| `padrao` | objeto | Tabela de categorias da política padrão 
          +| sim |                                                       
      410 +| `centros_custo` | objeto | Uma tabela de categorias por cent
          +ro de custo; pode ser vazio | sim |                           
      411 +| `nota_fiscal_obrigatoria_acima_de` | número ≥ 0 | Limiar da 
          +RN-007 | sim |                                                
      412 +| `<tabela>.<categoria>` | objeto | Entrada de uma categoria e
          +m uma tabela | — |                                            
      413 +| `<tabela>.<categoria>.limite` | número ≥ 0 | Limite por data
          + (RN-008); 0 significa não reembolsável (RN-001) | sim |      
      414 +| `<tabela>.<categoria>.periodicidade` | `dia` ou `diaria` | A
          +mbos significam limite por data (RN-008) | sim |              
      415 +                                                              
      416 +`versao`, `vigencia`, `acrescimo_em_viagem_percentual`, `obser
          +vacao` e campos                                               
      417 +não listados são informativos e não são validados.            
      418 +                                                              
      419 +O sistema encerra com erro geral, sem saída (RN-013), quando o
          + documento de                                                 
      420 +política:                                                     
      421 +                                                              
      422 +- está ausente ou não pode ser lido, o que inclui `NaN` ou `In
          +finity`;                                                      
      423 +- não tem algum campo obrigatório, ou tem campo obrigatório de
          + tipo errado;                                                 
      424 +- tem `moeda_base` diferente de `BRL`;                        
      425 +- tem limite negativo, ou limite ou limiar que não é número;  
      426 +- tem periodicidade diferente de `dia` e `diaria`;            
      427 +- tem, depois da normalização da RN-002, duas categorias iguai
          +s na mesma tabela                                             
      428 +  ou dois centros de custo iguais.                            
      429 +                                                              
      430 +**Origem:** política v4 (AMB-031, AMB-036)                    
      431 +**Aceite:** `politica-v4.json` → aceito. Execução sem document
          +o de política →                                               
      432 +erro, sem saída. Limite `-1` → erro. `"periodicidade": "mes"` 
          +→ erro. Documento                                             
      433 +sem `padrao` → erro. `"acrescimo_em_viagem_percentual": "x"` →
          + ignorado.                                                    
      434 +                                                              
      435 +### RN-016 — Política aplicável por centro de custo           
      436 +                                                              
      437 +**Regra:** A política aplicável a todas as despesas do documen
          +to é escolhida                                                
      438 +pelo `colaborador.centro_custo`, comparado após a normalização
          + da RN-002:                                                   
      439 +                                                              
      440 +1. centro de custo ausente ou vazio → política padrão;        
      441 +2. centro de custo cadastrado no documento de política → tabel
          +a desse centro;                                               
      442 +   para uma categoria que não consta da tabela do centro, vale
          + a entrada da                                                 
      443 +   política padrão (herança por categoria);                   
      444 +3. centro de custo informado e não cadastrado → política padrã
          +o;                                                            
      445 +4. centro de custo presente que não é texto → erro geral (RN-0
          +13).                                                          
      446 +                                                              
      447 +As justificativas de `LIMITE_DIARIO` e `CATEGORIA_NAO_REEMBOLS
          +AVEL` citam a                                                 
      448 +política usada: "centro de custo `<código>`", "política padrão
          +" ou, no caso 3,                                              
      449 +"política padrão; centro de custo `<código>` não cadastrado". 
      450 +**Origem:** política v4 (AMB-018, AMB-019, AMB-020, AMB-021)  
      451 +**Aceite:** `exemplos/despesas-exemplo.json` (`CC-ENG-PLATAFOR
          +MA`) → limite de                                              
      452 +alimentação de 75,00. `despesas-envelope-cc-desconhecido.json`
          + (`CC-SUPORTE-N2`)                                            
      453 +→ política padrão; f-002 (hospedagem, 310,00) → 250,00. Docume
          +nto sem                                                       
      454 +`centro_custo` → política padrão. `CC-ADM` com hospedagem de 3
          +00,00 → limite                                                
      455 +250,00 herdado da padrão; 250,00, `limitado`. `"centro_custo":
          + 42` → erro, sem                                              
      456 +saída.                                                        
      457 +                                                              
      458 +### RN-017 — Moeda da despesa                                 
      459 +                                                              
      460 +**Regra:** O campo `moeda` é opcional. Ausente, a moeda é `BRL
          +`. Presente, deve                                             
      461 +ser texto não vazio, e é normalizado removendo espaços no iníc
          +io e no fim e                                                 
      462 +convertendo letras para maiúsculas. Presente e vazio, ou prese
          +nte e de outro                                                
      463 +tipo, a despesa é recusada com `DADOS_INVALIDOS`. Qualquer cód
          +igo não vazio é                                               
      464 +aceito; um código sem cotação é tratado pela RN-018.          
      465 +**Origem:** política v4 (AMB-024)                             
      466 +**Aceite:** e-010 (sem `moeda`) → `BRL`; 88,00, aprovado. `" u
          +sd "` → `USD`.                                                
      467 +`""` → recusado, `DADOS_INVALIDOS`. `840` → recusado, `DADOS_I
          +NVALIDOS`.                                                    
      468 +                                                              
      469 +### RN-018 — Conversão cambial pela data da despesa           
      470 +                                                              
      471 +**Regra:**                                                    
      472 +                                                              
      473 +- Despesa em `BRL` não é convertida e não consulta o documento
          + de câmbio.                                                   
      474 +- Despesa em outra moeda é convertida para reais multiplicando
          + o valor                                                      
      475 +  informado pela taxa dessa moeda na `data` da despesa, segund
          +o o documento de                                              
      476 +  câmbio. Se não houver taxa dessa moeda nessa data (fim de se
          +mana, feriado ou                                              
      477 +  lacuna do documento), usa-se a taxa da data anterior mais pr
          +óxima que tenha                                               
      478 +  essa moeda. O produto é arredondado uma única vez (RN-003). 
      479 +- Se não houver taxa dessa moeda nem na data da despesa nem an
          +tes dela, ou se o                                             
      480 +  documento de câmbio não foi informado, apenas essa despesa é
          + recusada com                                                 
      481 +  `COTACAO_INDISPONIVEL`, e as demais são processadas normalme
          +nte.                                                          
      482 +                                                              
      483 +O documento de câmbio só é necessário quando houver despesa em
          + moeda                                                        
      484 +estrangeira; quando informado, ele é sempre validado. Formato 
          +de                                                            
      485 +`exemplos/envelope/cambio.json`:                              
      486 +                                                              
      487 +| Campo | Tipo | Significado | Obrigatório |                  
      488 +|---|---|---|---|                                             
      489 +| `moeda_base` | texto | Moeda para a qual as taxas convertem;
          + deve ser igual à `moeda_base` da política | sim |            
      490 +| `taxas` | objeto | Para cada data `AAAA-MM-DD`, um objeto de
          + código de moeda → taxa | sim |                               
      491 +| `taxas.<data>.<moeda>` | número > 0 | Quantos reais vale uma
          + unidade da moeda nessa data | — |                            
      492 +                                                              
      493 +Os códigos de moeda passam pela normalização da RN-017. `fonte
          +`, `observacao` e                                             
      494 +campos não listados são informativos.                         
      495 +                                                              
      496 +O sistema encerra com erro geral, sem saída (RN-013), quando o
          + documento de                                                 
      497 +câmbio informado:                                             
      498 +                                                              
      499 +- não pode ser lido, o que inclui `NaN` ou `Infinity`;        
      500 +- não tem `moeda_base` ou `taxas`, ou eles têm tipo errado;   
      501 +- tem `moeda_base` diferente da `moeda_base` da política;     
      502 +- tem chave de `taxas` que não é data válida;                 
      503 +- tem taxa que não é número ou que é menor ou igual a zero;   
      504 +- tem, na mesma data, dois códigos de moeda iguais depois da n
          +ormalização.                                                  
      505 +                                                              
      506 +**Origem:** política v4 (AMB-025, AMB-026, AMB-029, AMB-032)  
      507 +**Aceite:** e-002 (22,00 EUR, 2026-07-14, taxa 5,93) → 130,46.
          + e-004 (30,00 EUR,                                            
      508 +sábado 2026-07-18) → taxa de 2026-07-17 (5,96) → 178,80. e-006
          + (55,00 GBP) →                                                
      509 +recusado, `COTACAO_INDISPONIVEL`, `valor_considerado` nulo. De
          +spesa em USD em                                               
      510 +2026-07-10, antes da primeira data do documento → recusado,   
      511 +`COTACAO_INDISPONIVEL`. Despesa em USD sem documento de câmbio
          + → recusado,                                                  
      512 +`COTACAO_INDISPONIVEL`; despesas em BRL do mesmo documento pro
          +cessadas                                                      
      513 +normalmente. Documento de câmbio com taxa 0 → erro, sem saída.
      514 +                                                              
      515  ---
      516  
      517  ## 6. Ambiguidades identificadas e decisões
     ...
      522  **O que não está claro:** se o limite vale para a soma das des
           pesas do dia ou
      523  para cada despesa separadamente.
      524  **Decisão:** o limite vale para a soma das despesas da mesma c
           ategoria na mesma
      322 -data, para as três categorias.                                
      525 +data, para todas as categorias.                               
      526  **Justificativa:** o texto diz "por dia", e limitar por despes
           a permitiria
      527  contornar o limite dividindo a conta.
      528  **Regra afetada:** RN-008
     ...
      561  o valor após o limite; e se a falta da nota recusa a despesa i
           nteira ou paga até
      562  R$ 100,00.
      563  **Decisão:** compara o valor da própria despesa, já arredondad
           o; sem nota, a
      361 -despesa é recusada inteira.                                   
      564 +despesa é recusada inteira. Na v4, o valor comparado é o conve
          +rtido para reais                                              
      565 +(AMB-028).                                                    
      566  **Justificativa:** a nota comprova o gasto efetivamente feito,
            e "obrigatória"
      567  indica que sem ela a despesa não é aceita.
      568  **Regra afetada:** RN-007
     ...
      572  **Texto original do RH:** "Colaborador em viagem tem limites a
           mpliados em 50%."
      573  **O que não está claro:** a entrada não tem campo que indique 
           viagem. Seria
      574  preciso inferir pela hospedagem, pela descrição, ou não aplica
           r.
      371 -**Decisão:** a ampliação não é aplicada.                      
      575 +**Decisão:** a ampliação não é aplicada. Mantida na v4 (AMB-03
          +5).                                                           
      576  **Justificativa:** inferir viagem falha em casos evidentes (d-
           003, "Corrida
      577  aeroporto", sem hospedagem no dia) e cria brechas; sem dado, n
           ão há como verificar.
      578  **Regra afetada:** RN-011
     ...
      580  ### AMB-007 — Categorias alcançadas pela ampliação
      581  
      582  **Texto original do RH:** "Colaborador em viagem tem limites a
           mpliados em 50%."
      379 -**O que não está claro:** se a ampliação vale para as três cat
          -egorias ou só para                                            
      583 +**O que não está claro:** se a ampliação vale para todas as ca
          +tegorias ou só para                                           
      584  alimentação e transporte.
      585  **Decisão:** não se aplica enquanto valer a AMB-006; deve ser 
           decidida se um dado
      586  de viagem passar a existir.
     ...
      592  
      593  **Texto original do RH:** "Hospedagem tem limite de R$ 250 por
            diária."
      594  **O que não está claro:** a entrada não tem número de diárias;
            a informação só
      391 -aparece no texto livre (d-010, "2 diarias"; d-013, "3 noites")
          -.                                                             
      595 +aparece no texto livre (d-010, "2 diarias"; d-013, "3 noites";
          + e-007, "3 noites").                                          
      596  **Decisão:** cada despesa de hospedagem vale uma diária; a des
           crição não é usada.
      597 +Mantida na v4: a periodicidade `diaria` é tratada como limite 
          +por data (AMB-036).                                           
      598  **Justificativa:** texto livre não tem formato garantido e pod
           e ser manipulado;
      599  estadias de várias noites devem ser lançadas com uma despesa p
           or diária.
      600  **Regra afetada:** RN-008, RN-014
     ...
      618  ela: recusar todas, manter uma ou apenas sinalizar.
      619  **Decisão:** mesma data, categoria, fornecedor e valor, compar
           ados após
      620  normalização; mantém a que tem nota fiscal e, em empate, a de 
           menor posição; as
      416 -demais são recusadas.                                         
      621 +demais são recusadas. Na v4, também a mesma moeda, e o valor é
          + o original                                                   
      622 +(AMB-030).                                                    
      623  **Justificativa:** recusar todas puniria a despesa legítima, e
            preferir a com nota
      624  evita que uma duplicata anule um comprovante válido.
      625  **Regra afetada:** RN-006
     ...
      640  **Texto original do RH:** a política não menciona o caso.
      641  **O que não está claro:** como tratar valores com mais de duas
            casas decimais
      642  (d-011, 33,333) e quando arredondar.
      437 -**Decisão:** arredonda o valor de entrada para centavos, com a
          - metade se                                                    
      438 -afastando do zero, antes de qualquer regra.                   
      643 +**Decisão:** arredonda para centavos, com a metade se afastand
          +o do zero, antes                                              
      644 +de qualquer regra. Na v4, o arredondamento acontece depois da 
          +conversão para                                                
      645 +reais, uma única vez (AMB-027).                               
      646  **Justificativa:** dinheiro é pago em centavos, e arredondar a
           ntes evita efeitos
      647  de casas fracionárias nas comparações de fronteira.
      648  **Regra afetada:** RN-003
     ...
      663  **Texto original do RH:** "Categorias fora da política não são
            reembolsáveis."
      664  **O que não está claro:** se a lista de categorias é fechada n
           as três citadas ou
      665  se categorias parecidas (d-005, coworking) podem ser encaixada
           s.
      459 -**Decisão:** lista fechada: alimentação, transporte urbano e h
          -ospedagem.                                                    
      460 -**Justificativa:** a política só cita essas três; encaixar por
          - semelhança seria                                             
      461 -criar política.                                               
      666 +**Decisão (revista na v4):** a lista continua fechada, mas pas
          +sa a ser a das                                                
      667 +categorias com limite maior que zero na política aplicável (RN
          +-016), e não mais                                             
      668 +uma lista fixa de três. Encaixar por semelhança continua proib
          +ido.                                                          
      669 +**Justificativa:** a política v4 lista as categorias por centr
          +o de custo                                                    
      670 +(incluindo `representacao`); encaixar por semelhança seria cri
          +ar política.                                                  
      671  **Regra afetada:** RN-001
      672  
      673  ### AMB-015 — Fins de semana e feriados
     ...
      705  cálculo não têm motivo para recusar nada.
      706  **Regra afetada:** RN-013
      707  
      708 +### AMB-018 — Centro de custo ausente, vazio ou de tipo errado
      709 +                                                              
      710 +**Texto original da política v4:** `politica-v4.json` tem uma 
          +tabela `padrao` e                                             
      711 +tabelas em `centros_custo`, sem dizer quando a padrão vale.   
      712 +**O que não está claro:** que política usar quando o centro de
          + custo não vem, ou                                            
      713 +vem com tipo errado.                                          
      714 +**Decisão:** ausente ou vazio → política padrão; presente e nã
          +o texto → erro                                                
      715 +geral.                                                        
      716 +**Justificativa:** "não informado" é um caso legítimo, e é par
          +a isso que a                                                  
      717 +padrão existe; tipo errado é entrada malformada e afeta todas 
          +as despesas.                                                  
      718 +**Regra afetada:** RN-013, RN-016                             
      719 +                                                              
      720 +### AMB-019 — Centro de custo desconhecido                    
      721 +                                                              
      722 +**Texto original da política v4:** idem AMB-018.              
      723 +**O que não está claro:** se a padrão vale também para um cent
          +ro de custo que                                               
      724 +não está cadastrado (`despesas-envelope-cc-desconhecido.json`,
          + `CC-SUPORTE-N2`).                                            
      725 +**Decisão:** usa a política padrão, e a justificativa diz que 
          +o centro de custo                                             
      726 +não está cadastrado.                                          
      727 +**Justificativa:** "padrão" sugere fallback, e o próprio envel
          +ope traz o caso                                               
      728 +para ser processado. O risco de um erro de digitação cair na p
          +adrão sem aviso                                               
      729 +é reduzido pela justificativa explícita e pela normalização (A
          +MB-020).                                                      
      730 +**Regra afetada:** RN-016                                     
      731 +                                                              
      732 +### AMB-020 — Comparação do centro de custo                   
      733 +                                                              
      734 +**Texto original da política v4:** a política não menciona o c
          +aso.                                                          
      735 +**O que não está claro:** se ` cc-comercial ` é o mesmo centro
          + que `CC-COMERCIAL`.                                          
      736 +**Decisão:** compara após a normalização da RN-002, dos dois l
          +ados; o mesmo vale                                            
      737 +para as chaves de categoria do documento de política.         
      738 +**Justificativa:** mesmo raciocínio da AMB-013; e, com a AMB-0
          +19, um erro de                                                
      739 +grafia levaria à padrão sem aviso.                            
      740 +**Regra afetada:** RN-002, RN-016                             
      741 +                                                              
      742 +### AMB-021 — Centro de custo cadastrado sem a categoria      
      743 +                                                              
      744 +**Texto original da política v4:** a tabela de `CC-ADM` não te
          +m `hospedagem`.                                               
      745 +**O que não está claro:** se a tabela do centro substitui a pa
          +drão inteira (a                                               
      746 +categoria ausente não é reembolsável) ou só sobrescreve as cat
          +egorias que lista                                             
      747 +(a categoria ausente herda da padrão).                        
      748 +**Decisão:** herda da padrão, categoria por categoria. Categor
          +ia que não está                                               
      749 +nem no centro nem na padrão não é reembolsável.               
      750 +**Justificativa:** `CC-ENG-PLATAFORMA` precisou declarar hospe
          +dagem com limite 0                                            
      751 +e "nao reembolsavel"; se a ausência já significasse isso, a de
          +claração seria                                                
      752 +desnecessária.                                                
      753 +**Regra afetada:** RN-001, RN-016                             
      754 +                                                              
      755 +### AMB-022 — Limite zero                                     
      756 +                                                              
      757 +**Texto original da política v4:** `CC-ENG-PLATAFORMA` → `hosp
          +edagem`:                                                      
      758 +`"limite": 0.00`, `"observacao": "nao reembolsavel"`.         
      759 +**O que não está claro:** se a despesa é recusada ou "limitada
          + a zero", e se o                                              
      760 +texto de `observacao` tem efeito.                             
      761 +**Decisão:** limite 0,00 significa categoria não reembolsável 
          +naquele centro de                                             
      762 +custo, em qualquer categoria; a despesa é recusada com        
      763 +`CATEGORIA_NAO_REEMBOLSAVEL`. `observacao` é informativa.     
      764 +**Justificativa:** `limitado` sugere que algo foi pago; dizer 
          +que o centro de                                               
      765 +custo não cobre a categoria é mais claro. Como a etapa de cate
          +goria vem antes                                               
      766 +da de nota fiscal, d-013 passa a ser recusada por categoria.  
      767 +**Regra afetada:** RN-001                                     
      768 +                                                              
      769 +### AMB-023 — Categoria `representacao`                       
      770 +                                                              
      771 +**Texto original da política v4:** `CC-COMERCIAL` → `represent
          +acao`:                                                        
      772 +`"limite": 300.00`, `"periodicidade": "dia"`. Não consta da pa
          +drão.                                                         
      773 +**O que não está claro:** se divide limite com alimentação (e-
          +001 e f-003 são                                               
      774 +jantares), se exige nota fiscal e se o limite é por data.     
      775 +**Decisão:** categoria independente, com o mesmo tratamento da
          +s demais: limite                                              
      776 +próprio por data, mesma regra de nota fiscal e de duplicatas. 
          +Só é reembolsável                                             
      777 +onde a política aplicável a lista.                            
      778 +**Justificativa:** o documento dá a ela o mesmo formato das ou
          +tras categorias;                                              
      779 +qualquer tratamento especial seria inventado.                 
      780 +**Regra afetada:** RN-001, RN-008                             
      781 +                                                              
      782 +### AMB-024 — Moeda ausente ou inválida                       
      783 +                                                              
      784 +**Texto original da política v4:** `"moeda_base": "BRL"`; desp
          +esas com e sem                                                
      785 +o campo `moeda` (e-010 não tem).                              
      786 +**O que não está claro:** o que fazer sem `moeda`, com `"usd"`
          + minúsculo, com                                               
      787 +texto vazio ou com número.                                    
      788 +**Decisão:** ausente → `BRL`; texto é normalizado (espaços nas
          + pontas e                                                     
      789 +maiúsculas); vazio ou não texto → `DADOS_INVALIDOS`.          
      790 +**Justificativa:** mantém as entradas sem moeda (todo o exempl
          +o original)                                                   
      791 +válidas, e a política declara `BRL` como moeda base.          
      792 +**Regra afetada:** RN-013, RN-017                             
      793 +                                                              
      794 +### AMB-025 — Moeda sem cotação                               
      795 +                                                              
      796 +**Texto original da política v4:** `cambio.json` só tem USD e 
          +EUR.                                                          
      797 +**O que não está claro:** o que fazer com e-006 (GBP).        
      798 +**Decisão:** recusa só aquela despesa, com o motivo novo `COTA
          +CAO_INDISPONIVEL`;                                            
      799 +`valor_considerado` fica nulo.                                
      800 +**Justificativa:** o dado da despesa está certo, falta o dado 
          +de referência; uma                                            
      801 +despesa não deve impedir o cálculo das outras (AMB-017). Disti
          +nguir "moeda                                                  
      802 +inexistente" de "moeda sem cotação" exigiria uma lista de códi
          +gos de moeda, que                                             
      803 +seria escopo novo.                                            
      804 +**Regra afetada:** RN-018                                     
      805 +                                                              
      806 +### AMB-026 — Data sem cotação                                
      807 +                                                              
      808 +**Texto original da política v4:** `cambio.json`: "Cotacoes pu
          +blicadas apenas em                                            
      809 +dias uteis bancarios."                                        
      810 +**O que não está claro:** que taxa usar em e-004 (sábado, 2026
          +-07-18): a                                                    
      811 +anterior, a seguinte, nenhuma, ou a anterior com limite de dia
          +s.                                                            
      812 +**Decisão:** a taxa da data anterior mais próxima que tenha es
          +sa moeda, sem                                                 
      813 +limite de dias; sem nenhuma anterior, `COTACAO_INDISPONIVEL`. 
          +A data usada sai                                              
      814 +em `data_cotacao`.                                            
      815 +**Justificativa:** é a prática da PTAX (último fechamento disp
          +onível) e não usa                                             
      816 +dado futuro; "dia útil anterior" exigiria calendário de feriad
          +os, contra a                                                  
      817 +RN-012.                                                       
      818 +**Regra afetada:** RN-018                                     
      819 +                                                              
      820 +### AMB-027 — Arredondamento na conversão                     
      821 +                                                              
      822 +**Texto original da política v4:** a política não menciona o c
          +aso.                                                          
      823 +**O que não está claro:** se arredonda antes de converter, dep
          +ois, ou nas duas                                              
      824 +vezes (33,333 USD × 5,42 dá 180,66 com uma vez e 180,65 com du
          +as).                                                          
      825 +**Decisão:** multiplica o valor informado pela taxa, sem arred
          +ondar nenhum dos                                              
      826 +dois, e arredonda uma única vez em reais.                     
      827 +**Justificativa:** arredondar duas vezes acumula erro; mantém 
          +o princípio da                                                
      828 +RN-003 de um único valor em centavos antes das regras.        
      829 +**Regra afetada:** RN-003, RN-018                             
      830 +                                                              
      831 +### AMB-028 — Nota fiscal depois da conversão                 
      832 +                                                              
      833 +**Texto original da política v4:** `"nota_fiscal_obrigatoria_a
          +cima_de": 100.00`,                                            
      834 +com `"moeda_base": "BRL"`.                                    
      835 +**O que não está claro:** se o limiar vale na moeda original o
          +u em reais (e-005:                                            
      836 +40,00 USD, sem nota, vira 220,00).                            
      837 +**Decisão:** compara o valor já convertido para reais.        
      838 +**Justificativa:** o limiar está na moeda base; comparar na mo
          +eda original faria                                            
      839 +o limiar variar com o câmbio.                                 
      840 +**Regra afetada:** RN-007                                     
      841 +                                                              
      842 +### AMB-029 — Posição da conversão na ordem das regras        
      843 +                                                              
      844 +**Texto original da política v4:** a política não define ordem
          +.                                                             
      845 +**O que não está claro:** se a conversão vem logo depois da no
          +rmalização ou                                                 
      846 +depois das etapas que não usam valor (período, categoria).    
      847 +**Decisão:** logo depois da normalização e antes de valor nega
          +tivo (seção 8).                                               
      848 +**Justificativa:** todas as regras passam a usar um único valo
          +r em reais, e a                                               
      849 +ordem das etapas existentes não muda. Custo aceito: despesa es
          +trangeira sem                                                 
      850 +cotação e também fora do período ou de categoria não reembolsá
          +vel recebe                                                    
      851 +`COTACAO_INDISPONIVEL`.                                       
      852 +**Regra afetada:** RN-018, seção 8                            
      853 +                                                              
      854 +### AMB-030 — Duplicatas com moeda estrangeira                
      855 +                                                              
      856 +**Texto original da política v4:** a política não menciona o c
          +aso.                                                          
      857 +**O que não está claro:** se 22,00 EUR e 130,46 BRL, mesma dat
          +a e fornecedor,                                               
      858 +são duplicatas.                                               
      859 +**Decisão:** duplicata exige a mesma moeda e o mesmo valor ori
          +ginal (arredondado                                            
      860 +para centavos na moeda original), além dos critérios da AMB-01
          +0.                                                            
      861 +**Justificativa:** duplicata é o mesmo comprovante lançado dua
          +s vezes, e um                                                 
      862 +comprovante tem uma só moeda.                                 
      863 +**Regra afetada:** RN-006                                     
      864 +                                                              
      865 +### AMB-031 — Documento de política ausente ou inválido       
      866 +                                                              
      867 +**Texto original da política v4:** a política passa a ser um d
          +ocumento externo.                                             
      868 +**O que não está claro:** se o documento é obrigatório e o que
          + fazer com limite                                             
      869 +negativo, periodicidade desconhecida, falta de `padrao` etc.  
      870 +**Decisão:** obrigatório; qualquer problema estrutural é erro 
          +geral, sem saída                                              
      871 +(lista na RN-015). Não há política embutida como reserva.     
      872 +**Justificativa:** afeta todas as despesas igualmente (AMB-017
          +); uma reserva                                                
      873 +embutida criaria duas fontes da verdade.                      
      874 +**Regra afetada:** RN-013, RN-015                             
      875 +                                                              
      876 +### AMB-032 — Documento de câmbio ausente ou inválido         
      877 +                                                              
      878 +**Texto original da política v4:** câmbio em documento externo
          + (`cambio.json`).                                             
      879 +**O que não está claro:** se o documento é obrigatório quando 
          +todas as despesas                                             
      880 +estão em reais, e o que fazer com taxa inválida ou moeda base 
          +divergente.                                                   
      881 +**Decisão:** só é necessário quando houver despesa em moeda es
          +trangeira; sem                                                
      882 +ele, essas despesas são recusadas com `COTACAO_INDISPONIVEL`. 
          +Informado e                                                   
      883 +malformado, ou com `moeda_base` diferente da política, é erro 
          +geral.                                                        
      884 +**Justificativa:** um documento só em reais não deve depender 
          +do câmbio; um                                                 
      885 +arquivo corrompido não deve ser tratado como "não há cotação".
      886 +**Regra afetada:** RN-013, RN-018                             
      887 +                                                              
      888 +### AMB-033 — Rastreabilidade da conversão na saída           
      889 +                                                              
      890 +**Texto original da política v4:** a política não menciona o c
          +aso.                                                          
      891 +**O que não está claro:** a saída da v3 não mostra moeda, taxa
          + nem data da                                                  
      892 +cotação, e não diz de qual política veio o limite.            
      893 +**Decisão:** `valor_informado` fica na moeda original; novos c
          +ampos `moeda`,                                                
      894 +`taxa_cambio` e `data_cotacao`; justificativas de limite e de 
          +categoria citam o                                             
      895 +centro de custo ou a política padrão.                         
      896 +**Justificativa:** sem isso, o resultado não pode ser conferid
          +o à mão (seção 2).                                            
      897 +**Regra afetada:** seção 4, RN-016                            
      898 +                                                              
      899 +### AMB-034 — Vigência da política                            
      900 +                                                              
      901 +**Texto original da política v4:** `"vigencia": "2026-07-01"`.
      902 +**O que não está claro:** o que fazer com despesas anteriores 
          +à vigência.                                                   
      903 +**Decisão:** `versao` e `vigencia` são informativas; o documen
          +to informado vale                                             
      904 +para toda a execução.                                         
      905 +**Justificativa:** só existe um documento de política; escolhe
          +r entre versões                                               
      906 +seria escopo novo.                                            
      907 +**Regra afetada:** RN-015                                     
      908 +                                                              
      909 +### AMB-035 — Acréscimo em viagem parametrizado               
      910 +                                                              
      911 +**Texto original da política v4:** `"acrescimo_em_viagem_perce
          +ntual": 50`.                                                  
      912 +**O que não está claro:** se o percentual no documento obriga 
          +a aplicar a                                                   
      913 +ampliação (e-002 "Lisboa", e-006 e e-007 "Londres").          
      914 +**Decisão:** continua sem aplicar; o campo é informativo.     
      915 +**Justificativa:** continua não existindo dado estruturado de 
          +viagem; moeda                                                 
      916 +estrangeira não prova viagem (compra online em dólar, por exem
          +plo).                                                         
      917 +**Regra afetada:** RN-011                                     
      918 +                                                              
      919 +### AMB-036 — Periodicidade `dia` e `diaria`                  
      920 +                                                              
      921 +**Texto original da política v4:** alimentação, transporte e r
          +epresentação com                                              
      922 +`"periodicidade": "dia"`; hospedagem com `"diaria"`.          
      923 +**O que não está claro:** se os dois valores significam coisas
          + diferentes.                                                  
      924 +**Decisão:** os dois significam limite por data e categoria (R
          +N-008); cada                                                  
      925 +hospedagem vale uma diária (AMB-008). Outro valor → erro geral
          +.                                                             
      926 +**Justificativa:** é a semântica atual da RN-008.             
      927 +**Regra afetada:** RN-008, RN-015                             
      928 +                                                              
      929  ---
      930  
      931  ## 7. Casos de borda
      932  
      933  | Caso | Entrada | Comportamento esperado | Regra |
      934  |---|---|---|---|
      505 -| Duas despesas no mesmo dia somam acima do limite | d-001 (72
          -,50) + d-002 (38,00), alimentação, mesma data | 60,00 + 0,00 |
          - RN-008, RN-009 |                                             
      935 +| Duas despesas no mesmo dia somam acima do limite | d-001 (72
          +,50) + d-002 (38,00), alimentação, mesma data, `CC-ENG-PLATAFO
          +RMA` | 72,50 + 2,50 | RN-008, RN-009 |                        
      936  | Valor exatamente no limite da nota | d-003: 100,00, sem nota
            | não exige nota; 80,00 pelo limite | RN-007, RN-008 |
      937  | Valor um centavo acima do limite da nota | d-004: 100,01, se
           m nota | recusado, `NOTA_FISCAL_AUSENTE` | RN-007 |
      938  | Despesa recusada não consome limite | d-004 recusada na mesm
           a data de d-003 | d-003 recebe o limite inteiro de 80,00 | RN-
           008, seção 8 |
      509 -| Categoria fora da lista | d-005: coworking | recusado, `CATE
          -GORIA_NAO_REEMBOLSAVEL` | RN-001 |                            
      939 +| Categoria fora da política | d-005: coworking | recusado, `C
          +ATEGORIA_NAO_REEMBOLSAVEL` | RN-001 |                         
      940  | Duplicata idêntica, ambas com nota | d-006 e d-007 | d-006: 
           54,90; d-007: recusada, `DUPLICATA` | RN-006 |
      941  | Duplicata em que só a segunda tem nota | mesmas data, catego
           ria, fornecedor e valor; só a 2ª com nota | 2ª mantida; 1ª rec
           usada, `DUPLICATA` | RN-006 |
      942  | Duplicata com grafia diferente do fornecedor | `Bistro Centr
           al` e `BISTRO CENTRAL ` | tratadas como duplicata | RN-002, RN
           -006 |
     ...
      948  | Valor negativo que arredonda a zero | −0,004 | vira 0,00; ap
           rovado, 0,00 | RN-003, RN-005 |
      949  | Mais de duas casas decimais | d-011: 33,333 | considerado 33
           ,33; aprovado, 33,33 | RN-003 |
      950  | Arredondamento na metade | 10,005 | considerado 10,01 | RN-0
           03 |
      521 -| Hospedagem com várias diárias na descrição | d-010: 480,00, 
          -"2 diarias" | 1 diária; 250,00, `limitado` | RN-008, RN-014 | 
      522 -| Duas hospedagens na mesma data | 200,00 + 150,00, mesma data
          - | 200,00 + 50,00 | RN-008, RN-009 |                          
      523 -| Hospedagem sem nota acima de 100 | d-013: 690,00, sem nota |
          - recusado, `NOTA_FISCAL_AUSENTE` | RN-007 |                   
      524 -| Categoria em maiúsculas | d-014: `ALIMENTACAO`, 61,00 | trat
          -ada como alimentação; 60,00, `limitado` | RN-002, RN-010 |    
      951 +| Hospedagem com várias diárias na descrição | e-007: 1.200,00
          +, "3 noites", `CC-COMERCIAL` | 1 diária; 400,00, `limitado` | 
          +RN-008, RN-014 |                                              
      952 +| Duas hospedagens na mesma data | 200,00 + 150,00, mesma data
          +, política padrão | 200,00 + 50,00 | RN-008, RN-009 |         
      953 +| Hospedagem sem nota acima de 100 | 690,00, sem nota, polític
          +a padrão | recusado, `NOTA_FISCAL_AUSENTE` | RN-007 |         
      954 +| Categoria em maiúsculas | d-014: `ALIMENTACAO`, 61,00, `CC-E
          +NG-PLATAFORMA` | tratada como alimentação; 61,00, aprovado | R
          +N-002, RN-008 |                                               
      955  | Despesa em fim de semana | d-012: sábado | sem restrição; 47
           ,20 | RN-012 |
      956  | Indício de viagem na descrição | d-003: "Corrida aeroporto" 
           | limite normal de 80,00 | RN-011, RN-014 |
      957 +| Indício de viagem pela moeda | e-002: EUR, "Almoco - Lisboa"
          + | limite normal de 90,00 do `CC-COMERCIAL` | RN-011 |        
      958  | Campo obrigatório ausente em uma despesa | despesa sem `tem_
           nota_fiscal` | recusado, `DADOS_INVALIDOS`; demais processadas
            | RN-013 |
      959  | Campo obrigatório só com espaços | `fornecedor`: `"   "` | r
           ecusado, `DADOS_INVALIDOS`; `valor_considerado` nulo | RN-013 
           |
      960  | `id` com tipo errado | `id`: 17 | recusado, `DADOS_INVALIDOS
           `; `id` e `valor_considerado` nulos | RN-013 |
     ...
      962  | Data inexistente | `data`: `2026-02-30` | recusado, `DADOS_I
           NVALIDOS` | RN-013 |
      963  | Valor não numérico | `valor`: `"72.50"` | recusado, `DADOS_I
           NVALIDOS`; `valor_informado` e `valor_considerado` nulos | RN-
           013 |
      964  | Valor válido e outro campo inválido | `valor`: 50,00, sem `t
           em_nota_fiscal` | recusado, `DADOS_INVALIDOS`; `valor_informad
           o` 50,00, `valor_considerado` nulo | RN-013 |
      534 -| Campo desconhecido | despesa com `"moeda": "USD"` | campo ig
          -norado; despesa processada normalmente | RN-013 |             
      965 +| Campo desconhecido | despesa com `"projeto": "X"` | campo ig
          +norado; despesa processada normalmente | RN-013 |             
      966  | Campo informativo malformado | `descricao`: 123 ou `periodo.
           competencia`: `"julho"` | campo ignorado; sem erro | RN-013, R
           N-014 |
      967  | Período ausente | documento sem `periodo.fim` | erro, sem sa
           ída | RN-013 |
      968  | Data do período inválida | `periodo.inicio`: `2026-02-30` | 
           erro, sem saída | RN-013 |
     ...
       970  | Lista de despesas malformada | `despesas` não é lista, ou u
            m item não é objeto | erro, sem saída | RN-013 |
       971  | Documento com `NaN` ou `Infinity` | `valor`: `NaN` | erro, 
            sem saída | RN-013 |
       972  | Lista de despesas vazia | `despesas: []` | saída com `itens
            ` vazio e total 0,00 | RN-013 |
       973 +| Centro de custo ausente | documento sem `colaborador.centro
           +_custo` | política padrão | RN-016 |                         
       974 +| Centro de custo desconhecido | `CC-SUPORTE-N2` | política p
           +adrão; justificativa cita que não está cadastrado | RN-016 | 
       975 +| Centro de custo com grafia diferente | ` cc-comercial ` | t
           +ratado como `CC-COMERCIAL` | RN-002, RN-016 |                
       976 +| Centro de custo com tipo errado | `centro_custo`: 42 | erro
           +, sem saída | RN-013, RN-016 |                               
       977 +| Categoria ausente na tabela do centro | `CC-ADM`, hospedage
           +m de 300,00 | herda 250,00 da padrão; 250,00, `limitado` | RN
           +-016 |                                                       
       978 +| Categoria com limite zero | d-010: hospedagem, `CC-ENG-PLAT
           +AFORMA` | recusado, `CATEGORIA_NAO_REEMBOLSAVEL` | RN-001 |  
       979 +| Limite zero vem antes da nota fiscal | d-013: hospedagem, 6
           +90,00, sem nota, `CC-ENG-PLATAFORMA` | recusado, `CATEGORIA_N
           +AO_REEMBOLSAVEL` | RN-001, seção 8 |                         
       980 +| Representação em centro que não a tem | f-003: `representac
           +ao`, política padrão | recusado, `CATEGORIA_NAO_REEMBOLSAVEL`
           + | RN-001 |                                                  
       981 +| Representação acima do limite | e-001: 340,00, `CC-COMERCIA
           +L` | 300,00, `limitado` | RN-008, RN-010 |                   
       982 +| Moeda ausente | e-010: sem `moeda` | `BRL`; 88,00, aprovado
           + | RN-017 |                                                  
       983 +| Moeda em minúsculas | `moeda`: `" usd "` | tratada como `US
           +D` | RN-017 |                                                
       984 +| Moeda vazia ou de tipo errado | `moeda`: `""` ou 840 | recu
           +sado, `DADOS_INVALIDOS` | RN-013, RN-017 |                   
       985 +| Moeda estrangeira com cotação na data | e-002: 22,00 EUR em
           + 2026-07-14 | 130,46; 90,00, `limitado` | RN-018, RN-008 |   
       986 +| Moeda sem cotação | e-006: 55,00 GBP | recusado, `COTACAO_I
           +NDISPONIVEL`; `valor_considerado` nulo | RN-018 |            
       987 +| Data sem cotação (fim de semana) | e-004: 30,00 EUR em 2026
           +-07-18 | taxa de 2026-07-17 (5,96); 178,80; 90,00, `limitado`
           + | RN-018 |                                                  
       988 +| Data anterior à primeira cotação | USD em 2026-07-10 | recu
           +sado, `COTACAO_INDISPONIVEL` | RN-018 |                      
       989 +| Despesa em BRL em data sem cotação | BRL em sábado | sem co
           +nsulta ao câmbio; processada normalmente | RN-018 |          
       990 +| Arredondamento cambial | 33,333 USD em 2026-07-13 (5,42) | 
           +180,66 (uma única vez) | RN-003, RN-018 |                    
       991 +| Nota fiscal após conversão | e-005: 40,00 USD × 5,50 = 220,
           +00, sem nota | recusado, `NOTA_FISCAL_AUSENTE` | RN-007 |    
       992 +| Abaixo do limiar após conversão | e-003: 14,50 EUR × 5,88 =
           + 85,26, sem nota | não exige nota; 85,26, aprovado | RN-007 |
       993 +| Duplicata na mesma moeda estrangeira | duas despesas de 22,
           +00 EUR, mesmas data, categoria e fornecedor | tratadas como d
           +uplicata | RN-006 |                                          
       994 +| Mesmo valor em reais, moedas diferentes | 22,00 EUR e 130,4
           +6 BRL, mesmas data, categoria e fornecedor | não são duplicat
           +a | RN-006 |                                                 
       995 +| Estorno em moeda sem cotação | −10,00 GBP | recusado, `COTA
           +CAO_INDISPONIVEL` (conversão vem antes) | RN-018, seção 8 |  
       996 +| Estorno em moeda estrangeira | −10,00 USD em 2026-07-13 | −
           +54,20; recusado, `VALOR_NEGATIVO` | RN-005, RN-018 |         
       997 +| Documento de câmbio ausente, despesa estrangeira | despesa 
           +em USD, sem câmbio | recusado, `COTACAO_INDISPONIVEL`; demais
           + processadas | RN-018 |                                      
       998 +| Documento de câmbio ausente, tudo em reais | `exemplos/desp
           +esas-exemplo.json`, sem câmbio | processado normalmente | RN-
           +018 |                                                        
       999 +| Documento de política ausente | execução sem política | err
           +o, sem saída | RN-015 |                                      
      1000 +| Documento de política inválido | limite `-1`, sem `padrao` 
           +ou `"periodicidade": "mes"` | erro, sem saída | RN-015 |     
      1001 +| Documento de câmbio inválido | taxa 0 ou `"5,42"` | erro, s
           +em saída | RN-018 |                                          
      1002 +| Moedas base divergentes | câmbio com `moeda_base` diferente
           + da política | erro, sem saída | RN-018 |                    
      1003  
      1004  ## 8. Ordem de aplicação das regras
      1005  
      1006 +Antes das etapas por despesa, o sistema valida o documento de
           + despesas, o de                                              
      1007 +política e, se informado, o de câmbio (RN-013, RN-015, RN-018
           +), e escolhe a                                               
      1008 +política aplicável (RN-016). Qualquer erro geral encerra a ex
           +ecução sem saída.                                            
      1009 +                                                             
      1010  Cada despesa passa pelas etapas abaixo, nesta ordem. Uma desp
            esa recusada em uma
      1011  etapa recebe o motivo dessa etapa e não participa das etapas 
            seguintes, nem
      1012  consome limite.
      1013  
       549 -1. **Dados válidos** (RN-013) → `DADOS_INVALIDOS`            
       550 -2. **Normalização e arredondamento** (RN-002, RN-003)        
       551 -3. **Valor negativo** (RN-005) → `VALOR_NEGATIVO`            
       552 -4. **Período** (RN-004) → `FORA_DO_PERIODO`                  
       553 -5. **Categoria** (RN-001) → `CATEGORIA_NAO_REEMBOLSAVEL`     
       554 -6. **Duplicatas**, entre as despesas que passaram das etapas 
           -1 a 5 (RN-006) → `DUPLICATA`                                 
       555 -7. **Nota fiscal** (RN-007) → `NOTA_FISCAL_AUSENTE`          
       556 -8. **Limites por data e categoria**, distribuídos pela posiçã
           -o, entre as despesas                                         
       557 -   que passaram das etapas 1 a 7 (RN-008, RN-009, RN-010) → `
           -LIMITE_DIARIO`                                               
      1014 +1. **Dados válidos** (RN-013, RN-017) → `DADOS_INVALIDOS`    
      1015 +2. **Normalização** (RN-002, RN-017)                         
      1016 +3. **Conversão e arredondamento** (RN-018, RN-003) → `COTACAO
           +_INDISPONIVEL`                                               
      1017 +4. **Valor negativo** (RN-005) → `VALOR_NEGATIVO`            
      1018 +5. **Período** (RN-004) → `FORA_DO_PERIODO`                  
      1019 +6. **Categoria** na política aplicável (RN-001, RN-016) → `CA
           +TEGORIA_NAO_REEMBOLSAVEL`                                    
      1020 +7. **Duplicatas**, entre as despesas que passaram das etapas 
           +1 a 6 (RN-006) → `DUPLICATA`                                 
      1021 +8. **Nota fiscal** (RN-007) → `NOTA_FISCAL_AUSENTE`          
      1022 +9. **Limites por data e categoria**, distribuídos pela posiçã
           +o, entre as despesas                                         
      1023 +   que passaram das etapas 1 a 8 (RN-008, RN-009, RN-010) → `
           +LIMITE_DIARIO`                                               
      1024  
      1025  Se uma despesa falhar em mais de uma validação, o motivo regi
            strado é o da
      1026  primeira etapa em que falhou.
     ...
      1029  
      1030  O sistema está pronto quando:
      1031  
       566 -- [ ] Processando `exemplos/despesas-exemplo.json`, a saída t
           -em exatamente:                                               
      1032 +- [ ] Processando `exemplos/despesas-exemplo.json` (`CC-ENG-P
           +LATAFORMA`) com                                              
      1033 +  `exemplos/envelope/politica-v4.json` e sem documento de câm
           +bio, a saída tem                                             
      1034 +  exatamente:                                                
      1035  
      1036    | Item | `valor_reembolsavel` | `status` | `motivo` |
      1037    |---|---|---|---|
       570 -  | d-001 | 60,00 | limitado | `LIMITE_DIARIO` |             
       571 -  | d-002 | 0,00 | limitado | `LIMITE_DIARIO` |              
      1038 +  | d-001 | 72,50 | aprovado | nulo |                        
      1039 +  | d-002 | 2,50 | limitado | `LIMITE_DIARIO` |              
      1040    | d-003 | 80,00 | limitado | `LIMITE_DIARIO` |
      1041    | d-004 | 0,00 | recusado | `NOTA_FISCAL_AUSENTE` |
      1042    | d-005 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOLSAVEL` |
     ...
      1044    | d-007 | 0,00 | recusado | `DUPLICATA` |
      1045    | d-008 | 0,00 | recusado | `FORA_DO_PERIODO` |
      1046    | d-009 | 0,00 | recusado | `VALOR_NEGATIVO` |
       579 -  | d-010 | 250,00 | limitado | `LIMITE_DIARIO` |            
      1047 +  | d-010 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOLSAVEL` | 
      1048    | d-011 | 33,33 | aprovado | nulo |
      1049    | d-012 | 47,20 | aprovado | nulo |
       582 -  | d-013 | 0,00 | recusado | `NOTA_FISCAL_AUSENTE` |        
       583 -  | d-014 | 60,00 | limitado | `LIMITE_DIARIO` |             
       584 -  | **total_reembolsavel** | **585,43** | | |                
      1050 +  | d-013 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOLSAVEL` | 
      1051 +  | d-014 | 61,00 | aprovado | nulo |                        
      1052 +  | **total_reembolsavel** | **351,43** | | |                
      1053  
      1054 +- [ ] Processando `exemplos/envelope/despesas-envelope.json` 
           +(`CC-COMERCIAL`)                                             
      1055 +  com `exemplos/envelope/politica-v4.json` e `exemplos/envelo
           +pe/cambio.json`, a                                           
      1056 +  saída tem exatamente:                                      
      1057 +                                                             
      1058 +  | Item | `valor_considerado` | `valor_reembolsavel` | `stat
           +us` | `motivo` |                                             
      1059 +  |---|---|---|---|---|                                      
      1060 +  | e-001 | 340,00 | 300,00 | limitado | `LIMITE_DIARIO` |   
      1061 +  | e-002 | 130,46 | 90,00 | limitado | `LIMITE_DIARIO` |    
      1062 +  | e-003 | 85,26 | 85,26 | aprovado | nulo |                
      1063 +  | e-004 | 178,80 | 90,00 | limitado | `LIMITE_DIARIO` |    
      1064 +  | e-005 | 220,00 | 0,00 | recusado | `NOTA_FISCAL_AUSENTE` 
           +|                                                            
      1065 +  | e-006 | nulo | 0,00 | recusado | `COTACAO_INDISPONIVEL` |
      1066 +  | e-007 | 1.200,00 | 400,00 | limitado | `LIMITE_DIARIO` | 
      1067 +  | e-008 | 95,00 | 90,00 | limitado | `LIMITE_DIARIO` |     
      1068 +  | e-009 | 120,00 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOL
           +SAVEL` |                                                     
      1069 +  | e-010 | 88,00 | 88,00 | aprovado | nulo |                
      1070 +  | **total_reembolsavel** | | **1.143,26** | | |            
      1071 +                                                             
      1072 +- [ ] Processando `exemplos/envelope/despesas-envelope-cc-des
           +conhecido.json`                                              
      1073 +  (`CC-SUPORTE-N2`) com a mesma política e o mesmo câmbio, a 
           +saída usa a                                                  
      1074 +  política padrão e tem exatamente:                          
      1075 +                                                             
      1076 +  | Item | `valor_considerado` | `valor_reembolsavel` | `stat
           +us` | `motivo` |                                             
      1077 +  |---|---|---|---|---|                                      
      1078 +  | f-001 | 58,00 | 58,00 | aprovado | nulo |                
      1079 +  | f-002 | 310,00 | 250,00 | limitado | `LIMITE_DIARIO` |   
      1080 +  | f-003 | 190,00 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOL
           +SAVEL` |                                                     
      1081 +  | f-004 | 65,76 | 65,76 | aprovado | nulo |                
      1082 +  | **total_reembolsavel** | | **373,76** | | |              
      1083 +                                                             
      1084  - [ ] A saída tem um item para cada despesa da entrada, na me
            sma ordem.
      1085  - [ ] Todo item tem justificativa citando ao menos uma regra 
            (RN-xxx).
      1086  - [ ] Todos os casos da seção 7 produzem o comportamento desc
            rito.
     ...
      1090  
      1091  ## 10. O que fica em aberto
      1092  
       595 -- **Viagem (AMB-006, AMB-007):** a regra 6 da política fica s
           -em efeito até a                                              
       596 -  entrada trazer um dado de viagem. Colaboradores em viagem r
           -ecebem menos do que                                          
       597 -  o RH provavelmente pretendia.                              
       598 -- **Hospedagem com várias diárias (AMB-008):** d-010 recebe 2
           -50,00, embora a                                              
       599 -  descrição indique duas diárias de 240,00. Decisão provisóri
           -a: o colaborador                                             
       600 -  deve lançar uma despesa por diária.                        
      1093 +- **Viagem (AMB-006, AMB-007, AMB-035):** a regra de viagem f
           +ica sem efeito até                                           
      1094 +  a entrada trazer um dado de viagem, mesmo com o percentual 
           +agora no documento                                           
      1095 +  de política. Colaboradores em viagem recebem menos do que o
           + RH provavelmente                                            
      1096 +  pretendia.                                                 
      1097 +- **Hospedagem com várias diárias (AMB-008):** e-007 recebe 4
           +00,00, embora a                                              
      1098 +  descrição indique três noites. Decisão provisória: o colabo
           +rador deve lançar                                            
      1099 +  uma despesa por diária.                                    
      1100  - **Despesas lançadas com atraso (AMB-009):** despesas legíti
            mas de períodos
      1101    anteriores, como d-008, são recusadas sem possibilidade de 
            exceção.
      1102  - **Estorno de despesa já reembolsada (AMB-011):** se a despe
            sa original foi
     ...
      1104    fora de escopo.
      1105  - **`id` repetido na entrada:** não é validado. Decisão provi
            sória: as despesas
      1106    são processadas normalmente e distinguidas pela posição.
      1107 +- **Centro de custo desconhecido (AMB-019):** um erro de digi
           +tação que a                                                  
      1108 +  normalização não corrige leva à política padrão; a justific
           +ativa avisa, mas o                                           
      1109 +  cálculo não para.                                          
      1110 +- **Herança da padrão (AMB-021):** a leitura de que `CC-ADM` 
           +herda hospedagem da                                          
      1111 +  padrão se apoia no limite 0 explícito do `CC-ENG-PLATAFORMA
           +`; deve ser                                                  
      1112 +  confirmada com o RH.                                       
      1113 +- **Lacunas no câmbio (AMB-026):** sem limite de dias para tr
           +ás, uma despesa de                                           
      1114 +  2026-07-31 usaria a taxa de 2026-07-28, embora 29 a 31 seja
           +m dias úteis sem                                             
      1115 +  cotação no documento. A data usada aparece em `data_cotacao
           +`.                                                           
      1116 +- **Vigência (AMB-034):** a política v4 é aplicada mesmo a pe
           +ríodos anteriores a                                          
      1117 +  2026-07-01.                                                
      1118 +- **Aprovação manual (item C da política v4):** opcional; não
           + implementado.                                               

● Agora a entrada D-002 no DECISIONS.md.

● Update(specs\001-motor-reembolso\DECISIONS.md)
  ⎿  Added 89 lines
       10  
       11  ---
       12  
       13 +## D-002 — Política v4: política externa por centro de custo, 
          +representação e câmbio · `2026-10-04`                         
       14 +                                                              
       15 +**Gatilho:** envelope lacrado do Dia 2 (Política de Reembolso 
          +v4), com                                                      
       16 +`politica-v4.json`, `cambio.json` e dois documentos de despesa
          +s de exemplo                                                  
       17 +(`despesas-envelope.json`, `despesas-envelope-cc-desconhecido.
          +json`). Antes de                                              
       18 +mexer na spec, o Claude fez uma análise de impacto e listou 19
          + ambiguidades                                                 
       19 +novas (AMB-018 a AMB-036). As decisões foram revisadas e confi
          +rmadas por mim                                                
       20 +antes da edição.                                              
       21 +                                                              
       22 +**O que mudou na spec (1.1 → 2.0):**                          
       23 +- **Entrada:** passam a ser três documentos. Despesas; polític
          +a, obrigatória                                                
       24 +  (RN-015); câmbio, só necessário com moeda estrangeira (RN-01
          +8).                                                           
       25 +  `colaborador.centro_custo` deixa de ser informativo e escolh
          +e a política                                                  
       26 +  (RN-016). Novo campo opcional `despesas[].moeda` (RN-017).  
       27 +- **Saída:**                                                  
       28 +  - `valor_informado` fica na moeda original;                 
       29 +  - novos campos `moeda`, `taxa_cambio` e `data_cotacao`;     
       30 +  - `valor_considerado` é em reais e fica nulo também em `COTA
          +CAO_INDISPONIVEL`;                                            
       31 +  - novo motivo `COTACAO_INDISPONIVEL`;                       
       32 +  - as justificativas de limite e de categoria citam o centro 
          +de custo ou a                                                 
       33 +    política padrão;                                          
       34 +  - exemplo da seção 4 refeito para `CC-ENG-PLATAFORMA` e novo
          + exemplo em EUR.                                              
       35 +- **Regras alteradas:**                                       
       36 +  - RN-001: categorias da política aplicável; limite 0 = não r
          +eembolsável;                                                  
       37 +  - RN-002: normalização vale também para o centro de custo e 
          +para as chaves do                                             
       38 +    documento de política;                                    
       39 +  - RN-003: converte primeiro e arredonda uma vez só em reais;
       40 +  - RN-006: duplicata exige mesma moeda e mesmo valor original
          +;                                                             
       41 +  - RN-007: limiar vem do documento e é comparado com o valor 
          +convertido;                                                   
       42 +  - RN-008: limites vêm da política aplicável; `dia` e `diaria
          +` = limite por data;                                          
       43 +  - RN-011: percentual de viagem está no documento, mas contin
          +ua sem ser aplicado;                                          
       44 +  - RN-013: novos erros gerais (centro de custo com tipo errad
          +o, documento de                                               
       45 +    política ou de câmbio inválido) e `moeda` inválida → `DADO
          +S_INVALIDOS`;                                                 
       46 +  - RN-014: moeda e centro de custo entram na lista de campos 
          +estruturados.                                                 
       47 +- **Regras novas:** RN-015 (documento de política), RN-016 (po
          +lítica aplicável                                              
       48 +  por centro de custo: ausente ou desconhecido → padrão; categ
          +oria ausente no                                               
       49 +  centro → herda da padrão), RN-017 (moeda), RN-018 (conversão
          + pela data da                                                 
       50 +  despesa, com a última cotação anterior disponível; sem cotaç
          +ão → recusa só                                                
       51 +  aquela despesa).                                            
       52 +- **Seção 6:** AMB-018 a AMB-036 novas; AMB-005, 006, 008, 010
          +, 012 e 014                                                   
       53 +  revistas.                                                   
       54 +- **Seção 7:** casos que dependiam da tabela fixa foram reescr
          +itos para o                                                   
       55 +  centro de custo do exemplo; o caso "`moeda: USD` ignorado" v
          +irou `projeto`;                                               
       56 +  32 casos novos de centro de custo, moeda, câmbio e documento
          +s.                                                            
       57 +- **Seção 8:** nova etapa 3, conversão e arredondamento, antes
          + de valor                                                     
       58 +  negativo. As etapas seguintes foram renumeradas (4 a 9) sem 
          +mudar de ordem.                                               
       59 +- **Seção 9:** o exemplo original passa a ser avaliado com a v
          +4 (é                                                          
       60 +  `CC-ENG-PLATAFORMA`): total de **585,43 → 351,43**. Novos cr
          +itérios para os                                               
       61 +  dois documentos do envelope (1.143,26 e 373,76).            
       62 +- **Seção 3:** sai "não converte moedas" e a lista fixa de cat
          +egorias; entram                                               
       63 +  vigência e aprovação manual (item C) como fora de escopo.   
       64 +                                                              
       65 +**Por quê:**                                                  
       66 +- A v4 tira os valores da política do código e os põe em docum
          +ento externo,                                                 
       67 +  com limites por centro de custo e uma política padrão.      
       68 +- A herança por categoria se apoia no limite 0 explícito do   
       69 +  `CC-ENG-PLATAFORMA`, que seria desnecessário se a ausência j
          +á recusasse.                                                  
       70 +- Converter e arredondar uma vez evita erro de arredondamento 
          +duplo, e todas as                                             
       71 +  regras passam a usar um único valor em reais.               
       72 +- O limiar da nota fiscal está na moeda base; compará-lo na mo
          +eda original o                                                
       73 +  faria variar com o câmbio.                                  
       74 +- Falta de cotação é falta de dado de referência, não da despe
          +sa; não deve                                                  
       75 +  impedir o cálculo das outras.                               
       76 +- Viagem continua sem acréscimo: não existe campo estruturado 
          +que a indique.                                                
       77 +- Item C (aprovação manual) é opcional e ficou fora.          
       78 +                                                              
       79 +**O que isso invalidou:**                                     
       80 +- Critério de aceite da seção 9: 7 dos 14 itens mudam (d-001, 
          +d-002, d-010,                                                 
       81 +  d-013, d-014 e o total). d-013 muda de motivo (`NOTA_FISCAL_
          +AUSENTE` →                                                    
       82 +  `CATEGORIA_NAO_REEMBOLSAVEL`) porque a etapa de categoria ve
          +m antes da de                                                 
       83 +  nota fiscal.                                                
       84 +- Justificativas exatas da seção 4 (passam a citar R$ 75,00 e 
          +o centro de custo).                                           
       85 +- Código: a política fixa em `politica.py`, a etapa de categor
          +ia, a de nota                                                 
       86 +  fiscal, a de limite, as justificativas, a leitura da entrada
          + (centro de                                                   
       87 +  custo, moeda), a CLI (novos documentos) e a serialização da 
          +saída (campos                                                 
       88 +  novos).                                                     
       89 +- Testes: aceite da seção 9, justificativas exatas, casos de b
          +orda da seção 7                                               
       90 +  (o de `moeda: USD` agora contradiz a spec), testes de RN-001
          +, RN-007, RN-008,                                             
       91 +  RN-009, RN-010 e RN-013 que assumem a tabela fixa, e a verif
          +icação de                                                     
       92 +  rastreabilidade (RN-015 a RN-018 ainda não têm arquivo de te
          +ste).                                                         
       93 +                                                              
       94 +**Tasks afetadas:** T-007, T-012, T-014, T-015, T-016, T-018, 
          +T-019, T-020,                                                 
       95 +T-021, T-022, T-024. As tasks novas ainda não foram criadas; e
          +ntram na Fase 7                                               
       96 +de `tasks.md` a partir de T-026.                              
       97 +                                                              
       98 +**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`), antes de qu
          +alquer código.                                                
       99 +                                                              
      100 +---                                                           
      101 +                                                              
      102  ## D-001 — Validação de entrada, campos inesperados e valores 
           nulos na saída · `2026-10-04`
      103  
      104  **Gatilho:** ao desenhar a validação de entrada para o `plan.m
           d`, o Claude

● Bash(cd "C:/Learning/AI/AnthropicAcademy/Desafio/sdd-desafio" && sed -i
      's/Critério de aceite da seção 9: 7 dos 14 itens mudam (d-001, d-002,
      d-010,/Critério de acei…)
  ⎿  56:  31 casos novos de centro de custo, moeda, câmbio e documentos.
     80:- Critério de aceite da seção 9: 5 dos 14 itens mudam (d-001, d-002
     , d-010,
     … +3 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\DECISIONS.md (+155 -155)
        1 -# Log de Decisões e Mudanças de Spec                          
        2 -                                                              
        3 -> Uma entrada **toda vez** que a spec mudar. Este arquivo é a 
          -prova de que a spec                                           
        4 -> foi tratada como artefato vivo e não como cerimônia de abert
          -ura.                                                          
        5 ->                                                             
        6 -> Spec que não muda em dois dias é spec que ninguém consultou.
          - Mudança não é                                                
        7 -> demérito — mudança não registrada é.                        
        8 -                                                              
        9 -Ordem cronológica inversa: a mais recente primeiro.           
       10 -                                                              
       11 ----                                                           
       12 -                                                              
       13 -## D-002 — Política v4: política externa por centro de custo, 
          -representação e câmbio · `2026-10-04`                         
       14 -                                                              
       15 -**Gatilho:** envelope lacrado do Dia 2 (Política de Reembolso 
          -v4), com                                                      
       16 -`politica-v4.json`, `cambio.json` e dois documentos de despesa
          -s de exemplo                                                  
       17 -(`despesas-envelope.json`, `despesas-envelope-cc-desconhecido.
          -json`). Antes de                                              
       18 -mexer na spec, o Claude fez uma análise de impacto e listou 19
          - ambiguidades                                                 
       19 -novas (AMB-018 a AMB-036). As decisões foram revisadas e confi
          -rmadas por mim                                                
       20 -antes da edição.                                              
       21 -                                                              
       22 -**O que mudou na spec (1.1 → 2.0):**                          
       23 -- **Entrada:** passam a ser três documentos. Despesas; polític
          -a, obrigatória                                                
       24 -  (RN-015); câmbio, só necessário com moeda estrangeira (RN-01
          -8).                                                           
       25 -  `colaborador.centro_custo` deixa de ser informativo e escolh
          -e a política                                                  
       26 -  (RN-016). Novo campo opcional `despesas[].moeda` (RN-017).  
       27 -- **Saída:**                                                  
       28 -  - `valor_informado` fica na moeda original;                 
       29 -  - novos campos `moeda`, `taxa_cambio` e `data_cotacao`;     
       30 -  - `valor_considerado` é em reais e fica nulo também em `COTA
          -CAO_INDISPONIVEL`;                                            
       31 -  - novo motivo `COTACAO_INDISPONIVEL`;                       
       32 -  - as justificativas de limite e de categoria citam o centro 
          -de custo ou a                                                 
       33 -    política padrão;                                          
       34 -  - exemplo da seção 4 refeito para `CC-ENG-PLATAFORMA` e novo
          - exemplo em EUR.                                              
       35 -- **Regras alteradas:**                                       
       36 -  - RN-001: categorias da política aplicável; limite 0 = não r
          -eembolsável;                                                  
       37 -  - RN-002: normalização vale também para o centro de custo e 
          -para as chaves do                                             
       38 -    documento de política;                                    
       39 -  - RN-003: converte primeiro e arredonda uma vez só em reais;
       40 -  - RN-006: duplicata exige mesma moeda e mesmo valor original
          -;                                                             
     … 270 more lines (ctrl+o to expand)

● Atualizei só spec.md e DECISIONS.md. Não mexi em tasks.md nem em código, e não
  fiz commit. Também não rodei os testes: vários deles agora contradizem a
  spec, como esperado.

  spec.md (1.1 → 2.0)

  Entrada e saída (seção 4)
  - A entrada passa a ter três documentos: despesas, política (obrigatória) e
    câmbio (só com moeda estrangeira).
  - centro_custo passa a escolher a política e entra o campo opcional moeda.
  - Na saída, valor_informado fica na moeda original e valor_considerado fica em
    reais.
  - Campos novos na saída: moeda, taxa_cambio e data_cotacao.
  - Motivo novo: COTACAO_INDISPONIVEL.
  - As justificativas de limite e de categoria citam o centro de custo ou a
    política padrão.
  - O exemplo da seção 4 foi refeito para CC-ENG-PLATAFORMA (R$ 75,00) e ganhou
    um segundo exemplo em EUR (e-002).

  Regras alteradas: RN-001 (categorias da política; limite 0 = não
  reembolsável), RN-002, RN-003 (converte e arredonda uma vez), RN-006 (mesma
  moeda e mesmo valor original), RN-007 (valor convertido), RN-008 (tabela da
  v4, só para conferência), RN-011, RN-013 e RN-014.

  Regras novas: RN-015 (documento de política), RN-016 (política por centro de
  custo, com herança da padrão), RN-017 (moeda) e RN-018 (câmbio pela data,
  usando a última cotação anterior).

  Seção 6: ambiguidades novas AMB-018 a AMB-036, com os números da análise;
  AMB-005, 006, 008, 010, 012 e 014 foram revistas.

  Seção 7: os casos que dependiam da tabela antiga foram ajustados e entraram 31
  casos novos.

  Seção 8: entra a etapa 3, de conversão, antes de valor negativo. A ordem das
  demais etapas não muda.

  Seção 9:
  - Exemplo original: total de 351,43. d-013 agora é recusado por
    CATEGORIA_NAO_REEMBOLSAVEL, porque a etapa de categoria vem antes da de nota
    fiscal.
  - Acrescentei critérios de aceite para despesas-envelope.json (1.143,26) e
    para o caso de centro de custo desconhecido (373,76). Você não pediu isso
    explicitamente; se preferir, eu retiro.

  Seções 3 e 10: atualizadas, com o item C fora de escopo e os pontos que
  continuam em aberto (vigência, lacunas no câmbio, herança a confirmar com o
  RH).

  DECISIONS.md

  Nova entrada D-002, no mesmo formato da D-001:
  - Gatilho: o envelope do Dia 2.
  - O que mudou: as alterações da spec, por seção.
  - Por quê: a justificativa de cada decisão.
  - O que isso invalidou: o aceite da seção 9, as justificativas exatas, o
    código e os testes atingidos.
  - Tasks afetadas: T-007, T-012, T-014 a T-016, T-018 a T-022 e T-024. As tasks
    novas começam em T-026.

  Pontos para você confirmar

  1. Câmbio ausente com despesa estrangeira: interpretei "só é necessário quando
     houver moeda estrangeira" como "sem o arquivo, só essas despesas são
     recusadas com COTACAO_INDISPONIVEL". A outra leitura possível é erro geral.
  2. Detalhes da análise que você não citou (centro de custo com tipo errado →
     erro geral; moeda vazia → DADOS_INVALIDOS; política exigindo moeda_base
     BRL; vigência informativa): segui o que eu tinha recomendado.

✻ Baked for 6m 32s · done 17:19

> Confirmo os dois pontos                                                       
                                                                                
  Pode manter também os critérios de aceite dos dois arquivos do envelope na    
  seção 9.                                                                      
                                                                                
    Não faça mais nenhuma alteração agora                                       
                                                                                
   Não mexa em tasks.md                                                         
                                                                                
    Não mexa em código.                                                         
                                                                                
   Não faça commit.                                                             

● Combinado, as decisões ficam como estão. Não fiz mais nenhuma alteração, nem
  em tasks.md, nem no código, e não fiz commit.

  Os dois pontos confirmados já estão na spec assim:
  - Câmbio ausente com despesa estrangeira: só aquela despesa é recusada, com
    COTACAO_INDISPONIVEL (RN-018, AMB-032).
  - Detalhes que eu tinha recomendado:
    - centro de custo com tipo errado gera erro geral;
    - moeda vazia ou de outro tipo dá DADOS_INVALIDOS;
    - a política precisa ter moeda_base BRL;
    - a vigência é só informativa.
  - Seção 9: os critérios de aceite dos dois arquivos do envelope foram mantidos
    (1.143,26 e 373,76).

  Ficam como alterações não commitadas no repositório: spec.md, DECISIONS.md e a
  pasta exemplos/envelope/, que ainda não está versionada. Quando quiser
  seguir, o próximo passo é criar as tasks a partir da T-026.

✻ Churned for 5s · done 17:22