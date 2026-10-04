 ▐▛███▛█   Claude Code v2.1.289
▝▜██████▀  Opus 5.5 · API Usage Billing
 ▝▝   ▝▝   C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio


> Leia:                                                                         
  CLAUDE.md                                                                     
  specs/001-motor-reembolso/spec.md                                             
  specs/001-motor-reembolso/plan.md                                             
  DESAFIO.md                                                                    
  RUBRICA.md                                                                    
                                                                                
  Agora quero definir o plano técnico.                                          
                                                                                
  Primeiro analise e proponha:                                                  
  stack                                                                         
  estrutura geral da solução                                                    
  modelo de dados                                                               
  como representar as regras                                                    
  estratégia de testes                                                          
  principais riscos técnicos                                                    
                                                                                
  Não altere nenhum arquivo ainda.                                              
                                                                                
  E não invente regra de negócio nova: tudo que for negócio tem que vir da      
  spec.                                                                         

  Ran 4 shell commands (ctrl+o to expand)

● Li os cinco arquivos. A spec já define quase tudo de negócio que o plano
  precisa. Abaixo vai a proposta técnica. Não alterei nenhum arquivo.

  ---

  1. Stack

  Escolha: Linguagem
  Proposta: Python 3.12+
  Por quê: Tem decimal e json na biblioteca padrão, nenhuma dependência de
  runtime, e é rápido de escrever em 2 dias
  Alternativa descartada: Node/TS: não tem decimal nativo, JSON.parse já
  transforma 33.333 em float e precisaria de biblioteca para isso. Go: mais
  cerimônia para um CLI deste tamanho
  ────────────────────────────────────────
  Escolha: Testes
  Proposta: pytest
  Por quê: parametrize cobre bem a tabela da seção 7, e os IDs dos casos
  aparecem
  no relatório
  Alternativa descartada: unittest: verboso e sem parametrização tão boa
  ────────────────────────────────────────
  Escolha: Parsing/validação
  Proposta: stdlib (json) + validação manual
  Por quê: A RN-013 recusa a despesa ruim e segue com as outras. Uma biblioteca
  de schema (pydantic, jsonschema) tende a falhar o documento inteiro, e
  adaptar dá mais trabalho que escrever umas 40 linhas
  Alternativa descartada: pydantic
  ────────────────────────────────────────
  Escolha: Dinheiro
  Proposta: Decimal, com json.loads(parse_float=Decimal)
  Por quê: Se o número virar float no parse, 10.005 vira 10.00499… e arredonda
  para 10,00, quebrando a RN-003. Isso é decidido no parse, não depois
  Alternativa descartada: float; inteiro em centavos (precisaria arredondar já
  no
  parse, e a RN-003 quer o valor original guardado em valor_informado)
  ────────────────────────────────────────
  Escolha: CLI
  Proposta: argparse
  Por quê: Biblioteca padrão; só existe um subcomando
  Alternativa descartada: click/typer
  ────────────────────────────────────────
  Escolha: Lint/format
  Proposta: ruff
  Por quê: Uma ferramenta só
  Alternativa descartada: flake8 + black

  Comando: python -m reembolso calcular --input X --output Y.

  2. Estrutura geral

  JSON ──► entrada ──► motor (pipeline da seção 8) ──► saída ──► JSON
   (I/O)   parse +      núcleo puro, sem I/O           serializa
           validação                                    + total

  src/reembolso/
    __main__.py / cli.py   # argparse, lê/escreve arquivo, código de saída
    entrada.py             # JSON → Documento; erro geral vs. DADOS_INVALIDOS 
  (RN-013)
    modelo.py              # dataclasses e enums
    politica.py            # tabela de limites, categorias e limiar da NF 
  (dados)
    normalizacao.py        # RN-002, RN-003
    etapas.py              # uma função por etapa da seção 8
    motor.py               # a lista ordenada de etapas e a execução dela
    saida.py               # Resultado → dict JSON, 2 casas, total
  tests/

  Fronteira: motor, etapas, normalizacao e politica não fazem I/O e não conhecem
  JSON. A CLI é a única parte que toca disco.

  3. Modelo de dados

  - Documento: colaborador (dict, copiado como veio), período (inicio: date,
    fim: date, além do dict original para copiar na saída), despesas: 
    list[DespesaBruta].
  - Despesa, que só existe depois da validação: posicao (começa em 1), id, data:
    date, categoria e fornecedor já normalizados, tem_nota_fiscal: bool,
    valor_informado (o Decimal original) e valor_considerado (o Decimal
    arredondado).
  - Resultado: id, valor_informado, valor_considerado, valor_reembolsavel: 
    Decimal, status: Status, motivo: Motivo | None, justificativa: str.
  - Status e Motivo como enums, com os códigos exatamente iguais aos da tabela
    de motivos da spec.

  4. Como representar as regras

  - A política fica em dados, num só lugar (politica.py): LIMITES_POR_DATA = 
    {"alimentacao": Decimal("60.00"), ...}, CATEGORIAS_REEMBOLSAVEIS e
    LIMIAR_NOTA_FISCAL = Decimal("100.00"). Prefiro um módulo Python a um
    arquivo de configuração externo, porque config externa exigiria validar a
    própria config (YAGNI). Essa é a decisão que mais pesa no envelope do dia 2,
    então vale registrar como DT.
  - A seção 8 vira código quase literal. O motor.py tem uma lista ordenada de
    etapas, e cada uma cita a sua RN:
    - etapas por item (valor negativo, período, categoria, nota fiscal), cada
      uma devolvendo "passa" ou "recusa com motivo X";
    - etapas de grupo (duplicatas, limites), que recebem as despesas ainda vivas
      e decidem sobre o conjunto.
  - A ordem das etapas é a ordem da lista. Se o envelope mudar a ordem ou
    trouxer uma regra nova, a mudança é inserir ou mover uma linha.
  - Cada etapa monta a própria justificativa citando a RN. Os textos ficam em
    templates fixos, para a saída ser determinística.

  5. Estratégia de testes

  - Unitários por RN: um arquivo por regra, tests/test_rn004_periodo.py, com
    testes como test_rn004_ultimo_dia_do_periodo_e_aceito. O nome do teste leva
    à regra.
  - Seção 7 da spec: um único teste parametrizado, com uma linha por linha da
    tabela e ids= iguais ao nome do caso. A correção consegue ligar tabela e
    teste em 1:1.
  - Aceite da seção 9: um teste ponta a ponta que roda
    exemplos/despesas-exemplo.json e confere as 14 linhas e o total de 585,43.
    Conferi a soma e ela fecha.
  - CLI: via subprocess. Arquivo gerado, erro geral sem arquivo de saída, código
    de saída diferente de zero.
  - Invariantes da seção 9: determinismo (duas execuções iguais) e independência
    da descrição (RN-014, que troca as descrições e compara o resultado).
  - Rastreabilidade: a matriz de cobertura do tasks.md aponta para o nome de
    cada teste. Também dá para ter um teste simples que lê a spec.md, extrai os
    RN-0NN e confirma que cada um tem um arquivo de teste.

  6. Principais riscos técnicos

  ┌─────────────────────────────┬───────────────────────────────────────────┐
  │            Risco            │                 Mitigação                 │
  ├─────────────────────────────┼───────────────────────────────────────────┤
  │ Float no parse estraga a    │ parse_float=Decimal mais um teste         │
  │ RN-003 (10,005 e 33,333)    │ específico para 10,005 → 10,01            │
  ├─────────────────────────────┼───────────────────────────────────────────┤
  │ Modo de arredondamento: o   │ quantize(Decimal("0.01"), ROUND_HALF_UP), │
  │ round() do Python arredonda │  que no Decimal já afasta a metade do     │
  │  metade para par            │ zero, como a spec pede                    │
  ├─────────────────────────────┼───────────────────────────────────────────┤
  │ −0,004 vira -0.00           │ Normalizar o zero negativo para 0.00 e    │
  │                             │ testar o caso da seção 7                  │
  ├─────────────────────────────┼───────────────────────────────────────────┤
  │ Saída com "duas casas":     │                                           │
  │ json.dumps não serializa    │ Serializador próprio que escreve o        │
  │ Decimal, e float perde      │ literal 60.00                             │
  │ 60.00 → 60.0                │                                           │
  ├─────────────────────────────┼───────────────────────────────────────────┤
  │ NaN/Infinity: o json do     │ parse_constant rejeitando, o que gera     │
  │ Python aceita por padrão    │ DADOS_INVALIDOS                           │
  ├─────────────────────────────┼───────────────────────────────────────────┤
  │ bool é subclasse de int:    │                                           │
  │ "valor": true passaria como │ Checar o tipo de forma explícita          │
  │  número                     │                                           │
  ├─────────────────────────────┼───────────────────────────────────────────┤
  │                             │ unicodedata.normalize("NFD") e remoção    │
  │ Remoção de acento (RN-002)  │ dos caracteres combinantes; testar        │
  │                             │ Alimentação e ç                           │
  ├─────────────────────────────┼───────────────────────────────────────────┤
  │ Mudança do dia 2 exigir     │ Política em dados e pipeline como lista   │
  │ reestruturar                │ explícita (seção 4 acima)                 │
  └─────────────────────────────┴───────────────────────────────────────────┘

  7. Lacunas que a spec ainda deixa para o código decidir

  Encontrei estes casos ao desenhar a validação. Não decidi nenhum. Pela regra
  do CLAUDE.md, cada um precisa de uma decisão na spec, ou o código vai decidir
  em silêncio:

  1. String vazia em campo obrigatório ("categoria": "", "fornecedor": "  "):
     conta como "faltar campo" (RN-013)?
  2. periodo.inicio/fim com data inválida ("2026-02-30"): a RN-013 só fala em
     faltar o campo ou inicio > fim. É erro geral?
  3. despesas que existe mas não é lista, ou um item que não é objeto: erro
     geral ou DADOS_INVALIDOS?
  4. Tipo de id/categoria/fornecedor: um número no lugar de texto é inválido?
  5. Formato da data: 2026-7-3 é aceito ou só AAAA-MM-DD estrito?
  6. "Vazio" na saída (valor_informado/valor_considerado): é null ou o campo
     some? Isso é schema de saída, então pertence à spec.
  7. valor_informado "exatamente como veio": 72.5 e 72.50 são o mesmo número em
     JSON. A saída precisa preservar o literal?
  8. Erro geral: código de saída e destino da mensagem (stderr). Isso é técnico,
     posso decidir no plano, mas confirme.

  Os itens 1 a 7 afetam o que o sistema aceita ou emite, então são de spec. O
  item 8 eu resolvo no plan.md.

  ---

  Próximos passos: confirme se a stack é Python mesmo e decida os itens 1 a 7
  (ou me diga para deixar algum fora de escopo). Depois disso eu preencho o
  plan.md e faço um commit docs(plan):. Para os itens 1 a 7, atualizo antes a
  spec.md e registro a mudança no DECISIONS.md com docs(spec):.

✻ Cogitated for 1m 12s · done 1:27

> Pode seguir com Python.                                                       
                                                                                
  Sobre os pontos que você encontrou:                                           
                                                                                
  1. campo obrigatório vazio ou só com espaços = DADOS_INVALIDOS                
  2. data inválida em inicio/fim = erro geral da entrada                        
  3. despesas que não for lista = erro geral; item que não for objeto = erro    
  geral                                                                         
  4. id, categoria e fornecedor precisam ser texto; tipo errado =               
  DADOS_INVALIDOS                                                               
  5. data só aceita AAAA-MM-DD                                                  
  6. na saída, valor ausente ou inválido fica como null                         
  7. valor_informado representa o valor numérico, não precisa preservar se veio 
  como 72.5 ou 72.50                                                            
                                                                                
  O item 8 pode ser decisão técnica do plano.                                   
                                                                                
  Antes de alterar qualquer arquivo, me diz se essas decisões criam algum       
  conflito com a spec atual.                                                    

● Os sete pontos fecham o que eu tinha levantado. Mas dois deles se chocam com o
  texto atual da spec, e quatro deixam perguntas novas. Não alterei nenhum
  arquivo.

  Conflitos com o texto atual

  A. Ponto 7 contra a RN-003 e a definição de valor_informado
  - A seção 4 diz que valor_informado é o "valor exatamente como veio na
    entrada". Com a sua decisão, essa frase passa a ser falsa e precisa ser
    reescrita como "valor numérico informado na entrada".
  - A RN-003 diz que "todos os valores de saída têm duas casas decimais". Para
    d-011, valor_informado é 33.333. Esse conflito já existia antes, e o ponto 7
    só o deixa mais visível. A RN-003 precisa abrir uma exceção explícita para
    valor_informado, ou então dizer que "duas casas" vale só para
    valor_considerado, valor_reembolsavel e total_reembolsavel.
  - Efeito colateral: o exemplo da seção 4 mostra "valor_informado": 72.50. Pela
    decisão, a saída pode sair 72.5. Numericamente é o mesmo valor, mas convém
    anotar no exemplo para ninguém tratar a diferença como bug.

  B. Ponto 3, item que não é objeto, contra o espírito da RN-013
  A RN-013 separa "erro geral" de "erro em uma despesa", e o segundo caso existe
  para que uma despesa ruim não derrube as outras. Um item que não é objeto
  ("despesas": [ {...}, 42 ]) é, à primeira leitura, um erro em uma despesa. A
  sua decisão é defensável: esse item não tem id nem campos para gerar uma linha
  de saída. Mas é uma escolha que contraria a leitura natural da regra, então
  precisa estar escrita de forma explícita na lista de erros gerais, com a
  justificativa.

  Lacunas que as decisões abrem

  C. Ponto 4: id inválido e itens[].id na saída. A saída define itens[].id como
  texto, igual ao id da despesa. Se o id estiver ausente, vazio ou for número, a
  despesa vira DADOS_INVALIDOS, mas o que aparece em itens[].id? Opções: null,
  o valor bruto (número, por exemplo) ou null só quando ausente. O ponto 6 cobre
  só os campos de valor.

  D. Ponto 6: valor_considerado de uma despesa recusada por outro campo. Um
  exemplo: valor é 50.00 e válido, mas falta tem_nota_fiscal. A seção 4 diz que
  valor_considerado fica vazio só se o valor for inválido, o que daria 50.00. A
  seção 8 diz que a etapa 1 (dados válidos) recusa antes da etapa 2
  (arredondamento), o que daria null. As duas seções levam a respostas
  diferentes. Precisa escolher uma.

  E. Pontos 1 e 2 no nível do documento. As decisões cobrem campos da despesa e
  as datas do período. Ficam de fora:
  - colaborador.id vazio, só com espaços ou não-texto: entra como erro geral,
    por analogia com a regra de "faltar"?
  - colaborador ou periodo que não sejam objeto: erro geral?

  F. Campos opcionais com tipo errado. descricao numérica, ou
  periodo.competencia fora do formato AAAA-MM. A RN-014 diz que a descrição
  nunca afeta decisão, o que sugere ignorar. Mas isso precisa estar escrito,
  senão o código decide sozinho.

  Sem conflito, apenas extensões da RN-013

  - Ponto 1: amplia "faltar campo" para incluir vazio ou só espaços. Compatível
    com a RN-002, porque o trim já faria um fornecedor "  " virar vazio.
  - Ponto 2: acrescenta um caso à lista de erros gerais.
  - Ponto 4: detalha "dado inválido".
  - Ponto 5: só torna explícito o formato que a tabela da seção 4 já sugere.
    Vale para as datas de despesa (DADOS_INVALIDOS) e para as do período (erro
    geral).
  - Item 8: fica no plano, como combinado.

  O que eu proporia fazer

  Depois que você responder C, D, E e F:

  1. docs(spec):
     - reescrever a RN-013 com as listas completas de erro geral e de erro em
       uma despesa;
     - ajustar a definição de valor_informado, valor_considerado e itens[].id na
       seção 4;
     - restringir o "duas casas" da RN-003;
     - acrescentar os casos novos à seção 7;
     - registrar tudo como D-001 no DECISIONS.md.
  2. docs(plan): preencher o plan.md com a proposta anterior mais o item 8:
     mensagem em stderr, código de saída 1 e nenhum arquivo de saída criado.

✻ Brewed for 35s · done 1:31

> Fechou:                                                                       
                                                                                
  C. se o id estiver ausente, vazio ou com tipo inválido, itens[].id fica null. 
                                                                                
  D. se a despesa cair em DADOS_INVALIDOS por qualquer campo, valor_considerado 
  fica null.                                                                    
                                                                                
  E. colaborador.id vazio, só com espaços ou com tipo errado = erro geral.      
  colaborador ou periodo que não sejam objeto = erro geral.                     
                                                                                
  F. campos opcionais informativos com tipo ou formato errado não invalidam a   
  entrada.                                                                      
  descricao e periodo.competencia não participam do cálculo.                    
                                                                                
  Com essas decisões, confere mais uma vez se ficou tudo coerente.              
                                                                                
  Ainda não altera arquivo.                                                     

● Conferi as decisões contra a spec inteira (seções 4, 7, 8 e 9, RN-003, RN-013
  e RN-014). O conjunto fecha. Não alterei nenhum arquivo.

  Como as decisões ficam na spec

  RN-013: erro geral (encerra com mensagem, não gera saída):
  - o documento não pode ser lido;
  - colaborador ou periodo não são objeto;
  - colaborador.id ausente, vazio, só com espaços ou que não é texto;
  - periodo.inicio ou periodo.fim ausentes, fora do formato AAAA-MM-DD ou com
    data inexistente;
  - periodo.inicio posterior a periodo.fim;
  - despesas ausente ou que não é lista;
  - algum item de despesas que não é objeto.

  RN-013: erro em uma despesa (DADOS_INVALIDOS, as demais seguem):
  - campo obrigatório ausente, vazio ou só com espaços;
  - id, categoria ou fornecedor que não são texto;
  - data fora de AAAA-MM-DD ou inexistente;
  - valor não numérico;
  - tem_nota_fiscal que não é verdadeiro/falso.

  Campos informativos (colaborador.nome, colaborador.centro_custo,
  periodo.competencia, descricao): tipo ou formato errado não invalida nada, e
  esses campos não entram em cálculo. Isso confirma o que a RN-014 e a AMB-009
  já dizem.

  Seção 4, saída:
  - itens[].id: null se o id estiver ausente, vazio ou com tipo inválido.
  - valor_informado: o valor numérico da entrada, sem preservar a grafia; null
    se ausente ou inválido.
  - valor_considerado: null sempre que o status for DADOS_INVALIDOS. Isso bate
    com a seção 8, em que o arredondamento é a etapa 2 e a validação é a
    etapa 1.

  RN-003: a frase "todos os valores de saída têm duas casas" passa a valer para
  valor_considerado, valor_reembolsavel e total_reembolsavel. valor_informado
  fica de fora.

  Verificações cruzadas que passam

  - Seção 9, "um item para cada despesa, na mesma ordem": continua verdadeira.
    Como item que não é objeto vira erro geral, toda saída gerada tem itens 1:1
    com a entrada.
  - Status recusado com valor_reembolsavel 0,00: vale também para
    DADOS_INVALIDOS com id e valores null, e o total continua somando certo.
  - Duplicatas (RN-006): só participam despesas que passaram da etapa 1, então
    nunca se compara id ou valor null. A despesa mantida sempre tem id válido
    para a justificativa citar.
  - Lista vazia: continua válida (itens vazios, total 0,00). A exigência é ser
    lista, não ter itens.
  - Assimetria entre colaborador.id (erro geral) e despesas[].id 
    (DADOS_INVALIDOS): é intencional e coerente com a separação entre documento
    e despesa.
  - Exemplo da seção 4 e critério da seção 9: nada muda. Nenhuma despesa do
    exemplo é afetada pelas decisões novas, e o total segue em 585,43.

  Dois pontos ainda sem decisão

  1. NaN e Infinity em valor. Não são JSON válido pela norma, mas o leitor de
     JSON do Python aceita por padrão. A escolha técnica decide o resultado de
     negócio: se o documento é "ilegível", vira erro geral; se o valor é "não
     numérico", vira DADOS_INVALIDOS só naquela despesa. Precisa estar na spec.
     Minha sugestão é erro geral, porque o documento não é JSON válido, mas a
     decisão é sua.
  2. Campos desconhecidos (por exemplo "moeda": "USD" numa despesa, ou uma chave
     extra na raiz). A spec não diz se são ignorados ou se invalidam. Pelo
     espírito do ponto F, o natural seria ignorar, mas hoje isso não está
     escrito.

  O que fica para o plan.md (técnico, sem regra de negócio)

  - Item 8: em erro geral, mensagem em stderr, código de saída 1, e o arquivo de
    saída não é criado nem sobrescrito.
  - colaborador e periodo são copiados para a saída como vieram. O serializador
    precisa aceitar números Decimal dentro desses objetos copiados.

  Quando você decidir os pontos 1 e 2, sigo com o commit docs(spec): mais D-001
  no DECISIONS.md, e depois docs(plan):.

✻ Baked for 33s · done 1:33

> Conferi as decisões contra a spec inteira (seções 4, 7, 8 e 9, RN-003, RN-013 
  e RN-014). O conjunto fecha. Não alterei nenhum arquivo.                      
                                                                                
  Como as decisões ficam na spec                                                
                                                                                
  RN-013: erro geral (encerra com mensagem, não gera saída):                    
  - o documento não pode ser lido;                                              
  - colaborador ou periodo não são objeto;                                      
  - colaborador.id ausente, vazio, só com espaços ou que não é texto;           
  - periodo.inicio ou periodo.fim ausentes, fora do formato AAAA-MM-DD ou com   
  data inexistente;                                                             
  - periodo.inicio posterior a periodo.fim;                                     
  - despesas ausente ou que não é lista;                                        
  - algum item de despesas que não é objeto.                                    
                                                                                
  RN-013: erro em uma despesa (DADOS_INVALIDOS, as demais seguem):              
  - campo obrigatório ausente, vazio ou só com espaços;                         
  - id, categoria ou fornecedor que não são texto;                              
  - data fora de AAAA-MM-DD ou inexistente;                                     
  - valor não numérico;                                                         
  - tem_nota_fiscal que não é verdadeiro/falso.                                 
                                                                                
  Campos informativos (colaborador.nome, colaborador.centro_custo,              
  periodo.competencia, descricao): tipo ou formato errado não invalida nada, e  
  esses campos não entram em cálculo. Isso confirma o que a RN-014 e a AMB-009  
  já dizem.                                                                     
                                                                                
  Seção 4, saída:                                                               
  - itens[].id: null se o id estiver ausente, vazio ou com tipo inválido.       
  - valor_informado: o valor numérico da entrada, sem preservar a grafia; null  
  se ausente ou inválido.                                                       
  - valor_considerado: null sempre que o status for DADOS_INVALIDOS. Isso bate  
  com a seção 8, em que o arredondamento é a etapa 2 e a validação é a etapa 1. 
                                                                                
  RN-003: a frase "todos os valores de saída têm duas casas" passa a valer para 
  valor_considerado, valor_reembolsavel e total_reembolsavel. valor_informado   
  fica de fora.                                                                 
                                                                                
  Verificações cruzadas que passam                                              
                                                                                
  - Seção 9, "um item para cada despesa, na mesma ordem": continua verdadeira.  
  Como item que não é objeto vira erro geral, toda saída gerada tem itens 1:1   
  com a entrada.                                                                
  - Status recusado com valor_reembolsavel 0,00: vale também para               
  DADOS_INVALIDOS com id e valores null, e o total continua somando certo.      
  - Duplicatas (RN-006): só participam despesas que passaram da etapa 1, então  
  nunca se compara id ou valor null. A despesa mantida sempre tem id válido     
  para a justificativa citar.                                                   
  - Lista vazia: continua válida (itens vazios, total 0,00). A exigência é ser  
  lista, não ter itens.                                                         
  - Assimetria entre colaborador.id (erro geral) e despesas[].id                
  (DADOS_INVALIDOS): é intencional e coerente com a separação entre documento e 
  despesa.                                                                      
  - Exemplo da seção 4 e critério da seção 9: nada muda. Nenhuma despesa do     
  exemplo é afetada pelas decisões novas, e o total segue em 585,43.            
                                                                                
  Dois pontos ainda sem decisão                                                 
                                                                                
  1. NaN e Infinity em valor. Não são JSON válido pela norma, mas o leitor de   
  JSON do Python aceita por padrão. A escolha técnica decide o resultado de     
  negócio: se o documento é "ilegível", vira erro geral; se o valor é "não      
  numérico", vira DADOS_INVALIDOS só naquela despesa. Precisa estar na spec.    
  Minha sugestão é erro geral, porque o documento não é JSON válido, mas a      
  decisão é sua.                                                                
  2. Campos desconhecidos (por exemplo "moeda": "USD" numa despesa, ou uma      
  chave extra na raiz). A spec não diz se são ignorados ou se invalidam. Pelo   
  espírito do ponto F, o natural seria ignorar, mas hoje isso não está escrito. 
                                                                                
  O que fica para o plan.md (técnico, sem regra de negócio)                     
                                                                                
  - Item 8: em erro geral, mensagem em stderr, código de saída 1, e o arquivo   
  de saída não é criado nem sobrescrito.                                        
  - colaborador e periodo são copiados para a saída como vieram. O serializador 
  precisa aceitar números Decimal dentro desses objetos copiados.               
                                                                                
  Quando você decidir os pontos 1 e 2, sigo com o commit docs(spec): mais D-001 
  no DECISIONS.md, e depois docs(plan):.                                        

● A mensagem que chegou é o texto da minha resposta anterior, sem nada novo.
  Parece que foi colado por engano. Não alterei nenhum arquivo.

  Para seguir, preciso das suas decisões nos dois pontos que ficaram abertos:

  1. NaN/Infinity em valor: é erro geral, porque o documento não é JSON válido
     (minha sugestão)? Ou é DADOS_INVALIDOS só naquela despesa?
  2. Campos desconhecidos (por exemplo "moeda": "USD" numa despesa, ou uma chave
     extra na raiz): são ignorados ou invalidam?

  Com as duas respostas, faço primeiro o docs(spec): com D-001 no DECISIONS.md,
  e depois o docs(plan):.

✻ Cooked for 5s · done 1:35

> 1. NaN e Infinity = erro geral, porque considero isso JSON inválido.          
  2. Campos desconhecidos devem ser ignorados e não participam do cálculo.      
                                                                                
  Com isso, atualiza a spec.md e registra essa mudança no DECISIONS.md como     
  D-001.                                                                        
                                                                                
  Não mexe ainda no plan.md.                                                    

  Read 2 files (ctrl+o to expand)

● Vou fazer as edições na spec.

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 1 line, removed 1 line
      1  # Spec — Motor de Cálculo de Reembolso
      2  
      3 -**Versão:** 1.0 · **Status:** rascunho · **Última alteração:** 2
        -026-10-04                                                       
      3 +**Versão:** 1.1 · **Status:** rascunho · **Última alteração:** 2
        +026-10-04                                                       
      4  
      5  > **Regra de ouro deste arquivo:** ele descreve o QUÊ e o PORQUÊ
         . Nenhuma linha
      6  > aqui pode citar linguagem, biblioteca, classe, função ou estru
         tura de pasta.

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 3 lines
      61  A **posição** de uma despesa é a sua ordem na lista `despesas`,
           começando em 1.
      62  Ela é usada como critério de desempate (RN-006 e RN-009).
      63  
      64 +Campos marcados como informativos e campos que não constam dest
         +a tabela não são                                               
      65 +validados e nunca participam de cálculo ou decisão (RN-013).   
      66 +                                                               
      67  **Saída:** um documento com a seguinte estrutura.
      68  
      69  | Campo | Tipo | Significado |

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 3 lines, removed 3 lines
      71  | `colaborador` | objeto | Cópia do objeto `colaborador` da ent
          rada |
      72  | `periodo` | objeto | Cópia do objeto `periodo` da entrada |
      73  | `itens` | lista | Um item para cada despesa da entrada, na me
          sma ordem |
      74 -| `itens[].id` | texto | `id` da despesa |                     
      75 -| `itens[].valor_informado` | número | `valor` exatamente como 
         -veio na entrada; vazio se ausente ou inválido |                
      76 -| `itens[].valor_considerado` | número | Valor arredondado para
         - centavos (RN-003); vazio se inválido |                        
      74 +| `itens[].id` | texto ou nulo | `id` da despesa; nulo se ausen
         +te, vazio ou com tipo inválido |                               
      75 +| `itens[].valor_informado` | número ou nulo | Valor numérico d
         +e `valor` na entrada, sem arredondamento; nulo se ausente ou nã
         +o numérico. Só o valor importa, não a grafia: `72.5` e `72.50` 
         +são o mesmo valor |                                            
      76 +| `itens[].valor_considerado` | número ou nulo | Valor arredond
         +ado para centavos (RN-003); nulo sempre que o motivo for `DADOS
         +_INVALIDOS` |                                                  
      77  | `itens[].valor_reembolsavel` | número | Valor a reembolsar, c
          om duas casas decimais |
      78  | `itens[].status` | texto | `aprovado`, `limitado` ou `recusad
          o` (definições abaixo) |
      79  | `itens[].motivo` | texto ou vazio | Código do motivo (tabela 
          abaixo); vazio quando `aprovado` |

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 3 lines, removed 1 line
      155  **Regra:** O valor de cada despesa é arredondado para centavos
            antes de qualquer
      156  outra regra, com arredondamento comercial: a metade se afasta 
           do zero (0,005
      157  vira 0,01). Todas as regras seguintes usam o valor arredondado
      158 -(`valor_considerado`). Todos os valores de saída têm duas casa
          -s decimais.                                                   
      158 +(`valor_considerado`). Na saída, `valor_considerado`, `valor_r
          +eembolsavel` e                                                
      159 +`total_reembolsavel` têm duas casas decimais; `valor_informado
          +` não é                                                       
      160 +arredondado e mantém as casas que tinha na entrada.           
      161  **Origem:** decisão desta spec (AMB-012)
      162  **Aceite:** d-011 (33,333) → `valor_considerado` 33,33. Valor 
           10,005 → 10,01.
      163  Valor −0,004 → 0,00, tratado como valor zero (RN-005).

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 34 lines, removed 10 lines
      262  
      263  **Regra:**
      264  
      265 -- **Erro geral:** se o documento de entrada não puder ser lido
          -, ou se faltar                                                
      266 -  `colaborador.id`, `periodo.inicio`, `periodo.fim` ou `despes
          -as`, ou se                                                    
      267 -  `periodo.inicio` for posterior a `periodo.fim`, o sistema en
          -cerra com mensagem                                            
      268 -  de erro e não gera saída.                                   
      269 -- **Erro em uma despesa:** se faltar um campo obrigatório da d
          -espesa, se a data                                             
      270 -  não for uma data válida, se o valor não for numérico ou se `
          -tem_nota_fiscal`                                              
      271 -  não for verdadeiro/falso, apenas essa despesa é recusada com
          - `DADOS_INVALIDOS`.                                           
      272 -  As demais são processadas normalmente.                      
      265 +Um campo de texto é considerado **vazio** quando não tem nenhu
          +m caractere ou só                                             
      266 +tem espaços. Uma data é **válida** quando está exatamente no f
          +ormato                                                        
      267 +`AAAA-MM-DD` e existe no calendário (2026-02-30 não é válida).
      268  
      274 -**Origem:** decisão desta spec                                
      269 +- **Erro geral:** o sistema encerra com mensagem de erro e não
          + gera saída quando:                                           
      270 +  - o documento de entrada não pode ser lido, o que inclui doc
          +umento que não                                                
      271 +    segue o formato JSON, como `NaN` ou `Infinity` em qualquer
          + campo;                                                       
      272 +  - `colaborador` ou `periodo` estão ausentes ou não são objet
          +o;                                                            
      273 +  - `colaborador.id` está ausente, vazio ou não é texto;      
      274 +  - `periodo.inicio` ou `periodo.fim` estão ausentes ou não sã
          +o data válida;                                                
      275 +  - `periodo.inicio` é posterior a `periodo.fim`;             
      276 +  - `despesas` está ausente ou não é lista;                   
      277 +  - algum item de `despesas` não é objeto.                    
      278 +- **Erro em uma despesa:** apenas essa despesa é recusada com 
          +`DADOS_INVALIDOS`,                                            
      279 +  e as demais são processadas normalmente, quando:            
      280 +  - falta um campo obrigatório da despesa, ou um campo obrigat
          +ório de texto                                                 
      281 +    está vazio;                                               
      282 +  - `id`, `categoria` ou `fornecedor` não são texto;          
      283 +  - `data` não é data válida;                                 
      284 +  - `valor` não é numérico;                                   
      285 +  - `tem_nota_fiscal` não é verdadeiro/falso.                 
      286 +                                                              
      287 +  Na saída, a despesa recusada por `DADOS_INVALIDOS` tem `valo
          +r_considerado`                                                
      288 +  nulo, e também `id` nulo quando o problema está no `id`.    
      289 +- **Campos informativos e desconhecidos:** `colaborador.nome`,
      290 +  `colaborador.centro_custo`, `periodo.competencia` e `despesa
          +s[].descricao`,                                               
      291 +  além de qualquer campo que não conste da tabela de entrada, 
          +não são validados                                             
      292 +  e nunca participam de cálculo ou decisão. Tipo ou formato er
          +rado nesses campos                                            
      293 +  não gera erro.                                              
      294 +                                                              
      295 +**Origem:** decisão desta spec (AMB-017)                      
      296  **Aceite:** despesa sem `tem_nota_fiscal` → recusado, `DADOS_I
           NVALIDOS`, e as
      297  outras despesas do documento aparecem na saída normalmente. Do
           cumento sem
      277 -`periodo.fim` → erro, sem arquivo de saída.                   
      298 +`periodo.fim` → erro, sem arquivo de saída. Despesa com `forne
          +cedor` igual a                                                
      299 +`"   "` → recusado, `DADOS_INVALIDOS`. Despesa com `id` numéri
          +co → recusado,                                                
      300 +`DADOS_INVALIDOS`, `itens[].id` nulo. `periodo.inicio` igual a
          + `2026-02-30` →                                               
      301 +erro, sem arquivo de saída. Despesa com `"moeda": "USD"` → cam
          +po ignorado.                                                  
      302  
      303  ### RN-014 — Descrição é informativa
      304  

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 16 lines
      480  válida.
      481  **Regra afetada:** todas
      482  
      483 +### AMB-017 — Entrada malformada e campos inesperados         
      484 +                                                              
      485 +**Texto original do RH:** a política não menciona o caso.     
      486 +**O que não está claro:** o que fazer com campo vazio ou de ti
          +po errado, data                                               
      487 +fora do formato, valor que não é número, item da lista que não
          + é despesa, campo                                             
      488 +informativo malformado e campo que a entrada não prevê; e quai
          +s desses casos                                                
      489 +invalidam o documento inteiro ou só uma despesa.              
      490 +**Decisão:** problemas na identificação do colaborador, no per
          +íodo, na lista de                                             
      491 +despesas ou no formato do documento invalidam o documento inte
          +iro; problemas em                                             
      492 +campos obrigatórios de uma despesa recusam só essa despesa; ca
          +mpos informativos                                             
      493 +e desconhecidos são ignorados. Detalhes na RN-013.            
      494 +**Justificativa:** sem colaborador, período ou lista não há o 
          +que calcular; uma                                             
      495 +despesa ruim não deve impedir o cálculo das outras; e campos q
          +ue não entram em                                              
      496 +cálculo não têm motivo para recusar nada.                     
      497 +**Regra afetada:** RN-013                                     
      498 +                                                              
      499  ---
      500  
      501  ## 7. Casos de borda

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 12 lines
      525  | Despesa em fim de semana | d-012: sábado | sem restrição; 47
           ,20 | RN-012 |
      526  | Indício de viagem na descrição | d-003: "Corrida aeroporto" 
           | limite normal de 80,00 | RN-011, RN-014 |
      527  | Campo obrigatório ausente em uma despesa | despesa sem `tem_
           nota_fiscal` | recusado, `DADOS_INVALIDOS`; demais processadas
            | RN-013 |
      528 +| Campo obrigatório só com espaços | `fornecedor`: `"   "` | r
          +ecusado, `DADOS_INVALIDOS`; `valor_considerado` nulo | RN-013 
          +|                                                             
      529 +| `id` com tipo errado | `id`: 17 | recusado, `DADOS_INVALIDOS
          +`; `id` e `valor_considerado` nulos | RN-013 |                
      530 +| Data fora do formato | `data`: `2026-7-3` | recusado, `DADOS
          +_INVALIDOS` | RN-013 |                                        
      531 +| Data inexistente | `data`: `2026-02-30` | recusado, `DADOS_I
          +NVALIDOS` | RN-013 |                                          
      532 +| Valor não numérico | `valor`: `"72.50"` | recusado, `DADOS_I
          +NVALIDOS`; `valor_informado` e `valor_considerado` nulos | RN-
          +013 |                                                         
      533 +| Valor válido e outro campo inválido | `valor`: 50,00, sem `t
          +em_nota_fiscal` | recusado, `DADOS_INVALIDOS`; `valor_informad
          +o` 50,00, `valor_considerado` nulo | RN-013 |                 
      534 +| Campo desconhecido | despesa com `"moeda": "USD"` | campo ig
          +norado; despesa processada normalmente | RN-013 |             
      535 +| Campo informativo malformado | `descricao`: 123 ou `periodo.
          +competencia`: `"julho"` | campo ignorado; sem erro | RN-013, R
          +N-014 |                                                       
      536  | Período ausente | documento sem `periodo.fim` | erro, sem sa
           ída | RN-013 |
      537 +| Data do período inválida | `periodo.inicio`: `2026-02-30` | 
          +erro, sem saída | RN-013 |                                    
      538 +| Colaborador sem identificação | `colaborador.id`: `"  "` ou 
          +417 | erro, sem saída | RN-013 |                              
      539 +| Lista de despesas malformada | `despesas` não é lista, ou um
          + item não é objeto | erro, sem saída | RN-013 |               
      540 +| Documento com `NaN` ou `Infinity` | `valor`: `NaN` | erro, s
          +em saída | RN-013 |                                           
      541  | Lista de despesas vazia | `despesas: []` | saída com `itens`
            vazio e total 0,00 | RN-013 |
      542  
      543  ## 8. Ordem de aplicação das regras

● Agora o D-001 no DECISIONS.md:

● Update(specs\001-motor-reembolso\DECISIONS.md)
  ⎿  Added 42 lines, removed 23 lines
      10  
      11  ---
      12  
      13 -## D-002 — <título curto> · `<data>`                           
      13 +## D-001 — Validação de entrada, campos inesperados e valores n
         +ulos na saída · `2026-10-04`                                   
      14  
      15 -**Gatilho:** <o que provocou: envelope lacrado / erro descobert
         -o na implementação /                                           
      16 -ambiguidade que só apareceu ao testar / o Claude apontou uma co
         -ntradição>                                                     
      15 +**Gatilho:** ao desenhar a validação de entrada para o `plan.md
         +`, o Claude                                                    
      16 +listou casos que a spec 1.0 não decidia (campo vazio, tipo erra
         +do, data em                                                    
      17 +formato diferente, item da lista que não é objeto, `NaN`, campo
         +s desconhecidos).                                              
      18 +Também apontou duas contradições: `valor_informado` "exatamente
         + como veio"                                                    
      19 +conflitava com "todos os valores de saída têm duas casas" (RN-0
         +03) no caso de                                                 
      20 +d-011 (33,333), e `valor_considerado` de uma despesa com `DADOS
         +_INVALIDOS`                                                    
      21 +recebia respostas diferentes da seção 4 e da seção 8. Sem decis
         +ão, o código                                                   
      22 +resolveria esses casos em silêncio.                            
      23  
      18 -**O que mudou na spec:** <de → para, citando o ID da regra>    
      24 +**O que mudou na spec (1.0 → 1.1):**                           
      25 +- **RN-013:** antes era uma frase por tipo de erro. Agora há li
         +stas explícitas:                                               
      26 +  - **erro geral:** documento ilegível, incluindo `NaN`/`Infini
         +ty`; `colaborador`                                             
      27 +    ou `periodo` que não são objeto; `colaborador.id` ausente, 
         +vazio ou que não é                                             
      28 +    texto; datas do período fora de `AAAA-MM-DD` ou inexistente
         +s; `despesas` que                                              
      29 +    não é lista; item de `despesas` que não é objeto;          
      30 +  - **`DADOS_INVALIDOS`:** campo obrigatório vazio ou só com es
         +paços; `id`,                                                   
      31 +    `categoria` ou `fornecedor` que não são texto; data fora de
         + `AAAA-MM-DD` ou                                               
      32 +    inexistente;                                               
      33 +  - **ignorados:** campos informativos com tipo ou formato erra
         +do, e campos                                                   
      34 +    desconhecidos.                                             
      35 +- **Seção 4, saída:**                                          
      36 +  - `itens[].id` fica nulo se o `id` for inválido;             
      37 +  - `valor_informado` passa de "exatamente como veio" para "val
         +or numérico, sem                                               
      38 +    preservar grafia", nulo se ausente ou não numérico;        
      39 +  - `valor_considerado` fica nulo sempre que o motivo for `DADO
         +S_INVALIDOS`                                                   
      40 +    (antes, "vazio se inválido").                              
      41 +- **Seção 4, entrada:** nota de que campos informativos e desco
         +nhecidos não são                                               
      42 +  validados.                                                   
      43 +- **RN-003:** "todos os valores de saída têm duas casas" passa 
         +a valer só para                                                
      44 +  `valor_considerado`, `valor_reembolsavel` e `total_reembolsav
         +el`.                                                           
      45 +- **Seção 6:** nova AMB-017 (entrada malformada e campos inespe
         +rados).                                                        
      46 +- **Seção 7:** 13 casos de borda novos de RN-013.              
      47  
      48  **Por quê:**
      49 +- Uma despesa ruim não deve impedir o cálculo das outras.      
      50 +- Sem colaborador, período ou lista legível não há o que calcul
         +ar.                                                            
      51 +- Item que não é objeto não tem nem `id` para gerar uma linha d
         +e saída.                                                       
      52 +- `NaN`/`Infinity` não são JSON válido.                        
      53 +- Campos que não entram em cálculo não têm motivo para recusar 
         +nada.                                                          
      54  
      22 -**O que isso invalidou:** <requisitos, decisões técnicas, teste
         -s que caíram>                                                  
      55 +**O que isso invalidou:** nada implementado ainda. O critério d
         +e aceite da                                                    
      56 +seção 9 e o total de 585,43 não mudam: nenhuma despesa do exemp
         +lo é afetada.                                                  
      57  
      24 -**Tasks afetadas:** <as que precisaram ser refeitas + as novas 
         -criadas>                                                       
      58 +**Tasks afetadas:** nenhuma; `tasks.md` ainda não foi escrito. 
         +As tasks de                                                    
      59 +validação de entrada e de saída devem cobrir os casos novos da 
         +seção 7.                                                       
      60  
      26 -**Custo:** <quantos arquivos tocados, quanto tempo>            
      27 -                                                               
      28 ----                                                            
      29 -                                                               
      30 -## D-001 — <título curto> · `<data>`                           
      31 -                                                               
      32 -**Gatilho:**                                                   
      33 -                                                               
      34 -**O que mudou na spec:**                                       
      35 -                                                               
      36 -**Por quê:**                                                   
      37 -                                                               
      38 -**O que isso invalidou:**                                      
      39 -                                                               
      40 -**Tasks afetadas:**                                            
      41 -                                                               
      42 -**Custo:**                                                     
      61 +**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`), antes de qua
         +lquer código.                                                  

● Update(specs\001-motor-reembolso\DECISIONS.md)
  ⎿  Added 1 line, removed 1 line
      43  - **RN-003:** "todos os valores de saída têm duas casas" passa 
          a valer só para
      44    `valor_considerado`, `valor_reembolsavel` e `total_reembolsav
          el`.
      45  - **Seção 6:** nova AMB-017 (entrada malformada e campos inespe
          rados).
      46 -- **Seção 7:** 13 casos de borda novos de RN-013.              
      46 +- **Seção 7:** 12 casos de borda novos de RN-013.              
      47  
      48  **Por quê:**
      49  - Uma despesa ruim não deve impedir o cálculo das outras.

  Ran 1 shell command (ctrl+o to expand)

● Atualizei a spec.md (versão 1.0 → 1.1) e registrei a mudança como D-001 no
  DECISIONS.md. Não mexi no plan.md e ainda não fiz commit.

  O que mudou na spec.md:
  - Seção 4, entrada: nota dizendo que campos informativos e desconhecidos não
    são validados nem usados em cálculo.
  - Seção 4, saída: itens[].id passa a ser nulo quando o id é inválido.
    valor_informado passa a ser o valor numérico, sem preservar a grafia, e nulo
    se ausente ou não numérico. valor_considerado fica nulo sempre que o motivo
    for DADOS_INVALIDOS.
  - RN-003: "duas casas decimais" vale só para valor_considerado,
    valor_reembolsavel e total_reembolsavel. Isso resolve o conflito com o caso
    do 33,333.
  - RN-013: reescrita com três blocos: erro geral (agora incluindo
    NaN/Infinity), erro em uma despesa e campos informativos ou desconhecidos
    (ignorados). Também ficou definido o que é campo "vazio" e data "válida", e
    há casos de aceite novos.
  - Nova AMB-017 (entrada malformada e campos inesperados), que passa a ser a
    origem da RN-013. Antes ela só dizia "decisão desta spec", sem ambiguidade
    associada.
  - Seção 7: 12 casos de borda novos, um para cada decisão.

  DECISIONS.md: substituí os dois blocos de modelo por uma entrada D-001
  preenchida, com gatilho, o que mudou, por quê, o que invalidou e custo. Não
  sobrou o placeholder de D-002; a próxima entrada é escrita quando houver nova
  mudança.

  Uma coisa que suas decisões não cobriram: itens[].motivo continua descrito
  como "texto ou vazio … vazio quando aprovado". O item 6 fixou null só para os
  campos de valor. Para ficar coerente, o natural seria motivo também ser null
  quando aprovado, mas não mudei isso sem você decidir.

  Quer que eu faça o commit agora como docs(spec): resolve validacao de entrada 
  e nulos na saida (D-001)? Ou prefere decidir o motivo antes e incluir no mesmo
  commit?

✻ Brewed for 1m 19s · done 1:41
> Prefiro fechar isso antes do commit.                                          
                                                                                
  Define itens[].motivo como null quando o status for aprovado.                 
                                                                                
  Atualiza a spec e a D-001 se precisar, sem mexer no plan.md.                  
                                                                                
  Depois me mostra o que mudou e não faça commit ainda.                         

● Update(specs\001-motor-reembolso\spec.md)
  ⎿  Added 1 line, removed 1 line
      76  | `itens[].valor_considerado` | número ou nulo | Valor arredond
          ado para centavos (RN-003); nulo sempre que o motivo for `DADOS
          _INVALIDOS` |
      77  | `itens[].valor_reembolsavel` | número | Valor a reembolsar, c
          om duas casas decimais |
      78  | `itens[].status` | texto | `aprovado`, `limitado` ou `recusad
          o` (definições abaixo) |
      79 -| `itens[].motivo` | texto ou vazio | Código do motivo (tabela 
         -abaixo); vazio quando `aprovado` |                             
      79 +| `itens[].motivo` | texto ou nulo | Código do motivo (tabela a
         +baixo); nulo quando `aprovado` |                               
      80  | `itens[].justificativa` | texto | Explicação legível da decis
          ão, citando a regra (RN-xxx) |
      81  | `total_reembolsavel` | número | Soma de `valor_reembolsavel` 
          de todos os itens |
      82  

  Searched for 1 pattern (ctrl+o to expand)

● Na tabela da seção 9, o motivo dos itens aprovados aparece como "—". Vou
  trocar por "nulo" para o critério ficar verificável sem interpretação.

● Bash(cd "C:/Learning/AI/AnthropicAcademy/Desafio/sdd-desafio" && sed -i 's/^\(
       | d-0\(06\|11\|12\) | [0-9,]* | aprovado | \)— |$/\1nulo |/'
      specs/001-motor-reembols…)
  ⎿    | d-006 | 54,90 | aprovado | nulo |
       | d-007 | 0,00 | recusado | `DUPLICATA` |
       | d-008 | 0,00 | recusado | `FORA_DO_PERIODO` |
     … +4 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\spec.md (+3 -3)
      572    | d-003 | 80,00 | limitado | `LIMITE_DIARIO` |
      573    | d-004 | 0,00 | recusado | `NOTA_FISCAL_AUSENTE` |
      574    | d-005 | 0,00 | recusado | `CATEGORIA_NAO_REEMBOLSAVEL` |
      575 -  | d-006 | 54,90 | aprovado | — |                            
      575 +  | d-006 | 54,90 | aprovado | nulo |                         
      576    | d-007 | 0,00 | recusado | `DUPLICATA` |
      577    | d-008 | 0,00 | recusado | `FORA_DO_PERIODO` |
      578    | d-009 | 0,00 | recusado | `VALOR_NEGATIVO` |
      579    | d-010 | 250,00 | limitado | `LIMITE_DIARIO` |
      580 -  | d-011 | 33,33 | aprovado | — |                            
      581 -  | d-012 | 47,20 | aprovado | — |                            
      580 +  | d-011 | 33,33 | aprovado | nulo |                         
      581 +  | d-012 | 47,20 | aprovado | nulo |                         
      582    | d-013 | 0,00 | recusado | `NOTA_FISCAL_AUSENTE` |
      583    | d-014 | 60,00 | limitado | `LIMITE_DIARIO` |
      584    | **total_reembolsavel** | **585,43** | | |

● Agora a D-001:

● Update(specs\001-motor-reembolso\DECISIONS.md)
  ⎿  Added 4 lines, removed 1 line
      37    - `valor_informado` passa de "exatamente como veio" para "val
          or numérico, sem
      38      preservar grafia", nulo se ausente ou não numérico;
      39    - `valor_considerado` fica nulo sempre que o motivo for `DADO
          S_INVALIDOS`
      40 -    (antes, "vazio se inválido").                              
      40 +    (antes, "vazio se inválido");                              
      41 +  - `motivo` passa de "texto ou vazio" para "texto ou nulo", nu
         +lo quando o                                                    
      42 +    status for `aprovado`. Na tabela da seção 9, o "—" dos iten
         +s aprovados                                                    
      43 +    virou "nulo".                                              
      44  - **Seção 4, entrada:** nota de que campos informativos e desco
          nhecidos não são
      45    validados.
      46  - **RN-003:** "todos os valores de saída têm duas casas" passa 
          a valer só para

● Update(specs\001-motor-reembolso\DECISIONS.md)
  ⎿  Added 2 lines
      54  - Item que não é objeto não tem nem `id` para gerar uma linha d
          e saída.
      55  - `NaN`/`Infinity` não são JSON válido.
      56  - Campos que não entram em cálculo não têm motivo para recusar 
          nada.
      57 +- Todo campo de saída sem valor usa a mesma representação (nulo
         +), em vez de                                                   
      58 +  "vazio", que podia ser lido como texto vazio ou campo omitido
         +.                                                              
      59  
      60  **O que isso invalidou:** nada implementado ainda. O critério d
          e aceite da
      61  seção 9 e o total de 585,43 não mudam: nenhuma despesa do exemp
          lo é afetada.

  Ran 1 shell command (ctrl+o to expand)

● itens[].motivo agora é nulo quando o status é aprovado. Atualizei a spec.md e
  a D-001. Não mexi no plan.md e não fiz commit.

  spec.md:
  - Seção 4, tabela de saída: itens[].motivo passou de "texto ou vazio … vazio
    quando aprovado" para "texto ou nulo … nulo quando aprovado".
  - Seção 9, critério de aceite: d-006, d-011 e d-012 tinham "—" na coluna
    motivo, o que dava margem a interpretação. Agora mostram "nulo".
  - O exemplo de saída da seção 4 não muda, porque não tem nenhum item aprovado.

  DECISIONS.md, entrada D-001:
  - Em "O que mudou", entrou um item sobre motivo ("texto ou vazio" → "texto ou
    nulo"), citando também a troca do "—" na seção 9.
  - Em "Por quê", entrou a justificativa: todo campo de saída sem valor usa a
    mesma representação, nulo. "Vazio" podia ser lido como texto vazio ou como
    campo omitido.

  Conferi o arquivo inteiro: não sobrou nenhum "vazio" referente a campo de
  saída. Os que restam são da definição de campo de texto vazio na RN-013 e da
  lista de despesas vazia.

  Estado atual: 2 arquivos modificados, nada commitado (spec.md com +97/−? e
  DECISIONS.md com +74/−?; no total, 126 inserções e 45 remoções). Quando
  quiser, sugiro um commit único: docs(spec): resolve validacao de entrada e 
  nulos na saida (D-001).

✻ Crunched for 25s · done 1:43

> Agora pode preencher o plan.md com a proposta técnica que você apresentou     
  antes, considerando a spec 1.1 e a decisão D-001.                             
                                                                                
  Inclua:                                                                       
  stack                                                                         
  arquitetura                                                                   
  modelo de dados                                                               
  representação das regras                                                      
  estratégia de testes                                                          
  riscos técnicos                                                               
  decisão do erro geral: stderr, exit code 1 e não criar nem sobrescrever o     
  arquivo de saída                                                              
                                                                                
  Não altere a spec nem o DECISIONS.md.                                         
                                                                                
  Quando terminar, me mostra um resumo do que escreveu e não faça commit ainda  

  Read 1 file (ctrl+o to expand)

● Write(specs\001-motor-reembolso\plan.md)
  ⎿  Added 275 lines, removed 30 lines
      1  # Plano Técnico — Motor de Cálculo de Reembolso
      2  
      3 -**Versão:** 1.0 · **Baseado na spec:** 1.0                      
      3 +**Versão:** 1.0 · **Baseado na spec:** 1.1 (inclui D-001)       
      4  
      5  > Aqui mora o COMO. Este arquivo pode e deve falar de linguagem,
          biblioteca e
      6  > arquitetura. O que ele **não** pode é introduzir regra de negó
         cio nova — se
     ...
       12  
       13  | Escolha | O quê | Por quê | O que descartei e por quê |
       14  |---|---|---|---|
       15 -| Linguagem | | | |                                           
       16 -| Testes | | | |                                              
       17 -| Parsing/validação | | | |                                   
       18 -| Aritmética monetária | | | |                                
       15 +| Linguagem | Python 3.12+ | `decimal` e `json` na biblioteca 
          +padrão; nenhuma dependência de runtime; rápido de escrever em 
          +2 dias | Node/TS: sem decimal nativo, e `JSON.parse` converte 
          +`33.333` em float antes de qualquer código nosso rodar. Go: ce
          +rimônia demais para um CLI deste tamanho |                    
       16 +| Testes | pytest | `parametrize` com `ids` legíveis cobre a t
          +abela da seção 7 da spec linha a linha | `unittest`: verboso e
          + com parametrização pobre |                                   
       17 +| Parsing/validação | `json` da stdlib + validação manual | A 
          +RN-013 recusa uma despesa e segue com as outras; validação esc
          +rita à mão expressa isso direto | pydantic/jsonschema: falham 
          +o documento inteiro por padrão; adaptar ao "erro por despesa" 
          +custa mais do que escrever ~50 linhas |                       
       18 +| Aritmética monetária | `decimal.Decimal`, lido direto do JSO
          +N com `parse_float=Decimal` | Float no parse transforma `10.00
          +5` em `10.00499…`, que arredonda para 10,00 e quebra a RN-003.
          + O tipo certo precisa existir desde a leitura | float (erro de
          + representação); inteiro em centavos (exigiria arredondar já n
          +o parse, e `valor_informado` precisa do valor sem arredondamen
          +to) |                                                         
       19 +| CLI | `argparse` | Biblioteca padrão; há um único subcomando
          + | click/typer: dependência sem ganho |                       
       20 +| Lint/format | ruff | Uma ferramenta para lint e formatação |
          + flake8 + black |                                             
       21  
       20 -<A linha de aritmética monetária não é decoração. Ponto flutua
          -nte em dinheiro é                                             
       21 -a fonte de bug mais previsível deste projeto.>                
       22 +**Comandos:**                                                 
       23  
       24 +- Rodar: `python -m reembolso calcular --input despesas.json -
          +-output resultado.json`                                       
       25 +- Testes: `python -m pytest`                                  
       26 +- Lint/format: `ruff check .` · `ruff format .`               
       27 +                                                              
       28  ## 2. Arquitetura
       29  
       25 -<Diagrama em blocos ou lista. Quais são as peças, o que cada u
          -ma faz, como                                                  
       26 -conversam. Uma tela, não uma tese.>                           
       27 -                                                              
       30  ```
       29 -entrada JSON → <...> → <...> → saída JSON                     
       31 +arquivo JSON                                                  
       32 +   │                                                          
       33 +   ▼                                                          
       34 +cli ──► entrada ──────────► motor ─────────────────────► saida
          + ──► arquivo JSON                                             
       35 +(I/O)   parse + validação   etapas 3–8 da seção 8        seria
          +lização                                                       
       36 +        (etapas 1–2)        (núcleo puro)                + tot
          +al                                                            
       37  ```
       38  
       32 -**Fronteiras:** <o que é núcleo de regra de negócio puro e o q
          -ue é I/O. Onde                                                
       33 -essa linha está desenhada determina o quanto o sistema vai res
          -istir a mudança                                               
       34 -de requisito.>                                                
       39 +| Módulo | Responsabilidade | Regras |                        
       40 +|---|---|---|                                                 
       41 +| `cli.py` / `__main__.py` | Argumentos, leitura e escrita de 
          +arquivo, mensagem de erro, código de saída | — |              
       42 +| `entrada.py` | JSON → `Documento`. Detecta erro geral (exceç
          +ão `EntradaInvalida`) e erro por despesa (`DADOS_INVALIDOS`). 
          +Constrói `Despesa` já normalizada e arredondada | RN-013, AMB-
          +017 |                                                         
       43 +| `normalizacao.py` | Normalização de texto e arredondamento |
          + RN-002, RN-003 |                                             
       44 +| `politica.py` | Dados da política: categorias, limites, limi
          +ar da nota fiscal | RN-001, RN-007, RN-008 |                  
       45 +| `etapas.py` | Uma função por etapa da seção 8 da spec | RN-0
          +01, RN-004 a RN-010 |                                         
       46 +| `motor.py` | Lista ordenada de etapas e execução | Seção 8 |
       47 +| `justificativas.py` | Templates de texto das justificativas 
          +e formatação `R$ 0,00` | Seção 4 (justificativa) |            
       48 +| `saida.py` | `Resultado` → estrutura JSON, `null`, duas casa
          +s, total | Seção 4 (saída), RN-003 |                          
       49 +| `modelo.py` | Dataclasses e enums | — |                     
       50  
       51 +**Fronteiras:**                                               
       52 +                                                              
       53 +- Só `cli.py` toca disco, stdout e stderr.                    
       54 +- `entrada.py` recebe texto e devolve objetos; não abre arquiv
          +o.                                                            
       55 +- `motor.py`, `etapas.py`, `normalizacao.py` e `politica.py` n
          +ão conhecem JSON                                              
       56 +  nem arquivo. Recebem e devolvem objetos do `modelo.py`.     
       57 +                                                              
       58 +Essa divisão permite testar toda regra de negócio sem I/O, e u
          +ma mudança de                                                 
       59 +política tende a tocar só `politica.py` e `etapas.py`.        
       60 +                                                              
       61  ## 3. Modelo de dados
       62  
       38 -<Estruturas internas. Como uma despesa é representada, como um
          - resultado de                                                 
       39 -avaliação é representado, o que carrega a justificativa.>     
       63 +Todas as estruturas são `@dataclass(frozen=True)`.            
       64  
       65 +```                                                           
       66 +Documento                                                     
       67 +  colaborador: dict          # cópia como veio, para a saída  
       68 +  periodo: dict              # cópia como veio, para a saída  
       69 +  inicio: date                                                
       70 +  fim: date                                                   
       71 +  despesas: list[Despesa | Invalida]   # na ordem da entrada  
       72 +                                                              
       73 +Despesa                      # passou pela etapa 1 (RN-013)   
       74 +  posicao: int               # 1, 2, 3...                     
       75 +  id: str                                                     
       76 +  data: date                                                  
       77 +  categoria: str             # normalizada (RN-002)           
       78 +  fornecedor: str            # normalizado (RN-002)           
       79 +  tem_nota_fiscal: bool                                       
       80 +  valor_informado: Decimal   # sem arredondamento             
       81 +  valor_considerado: Decimal # arredondado (RN-003)           
       82 +                                                              
       83 +Invalida                     # recusada na etapa 1            
       84 +  posicao: int                                                
       85 +  id: str | None             # None se o id for inválido      
       86 +  valor_informado: Decimal | None   # None se ausente ou não n
          +umérico                                                       
       87 +  detalhe: str               # qual campo falhou, para a justi
          +ficativa                                                      
       88 +                                                              
       89 +Resultado                                                     
       90 +  id: str | None                                              
       91 +  valor_informado: Decimal | None                             
       92 +  valor_considerado: Decimal | None # None quando DADOS_INVALI
          +DOS                                                           
       93 +  valor_reembolsavel: Decimal                                 
       94 +  status: Status                                              
       95 +  motivo: Motivo | None             # None quando APROVADO    
       96 +  justificativa: str                                          
       97 +```                                                           
       98 +                                                              
       99 +- `Status`: `APROVADO`, `LIMITADO`, `RECUSADO`, com valores ig
          +uais aos textos                                               
      100 +  da spec (`"aprovado"`...).                                  
      101 +- `Motivo`: os sete códigos da tabela de motivos da spec, com 
          +valor igual ao                                                
      102 +  código (`"DUPLICATA"`...).                                  
      103 +- A saída mantém um `Resultado` por posição. A lista final é m
          +ontada por ordem                                              
      104 +  de posição, o que garante "um item por despesa, na mesma ord
          +em".                                                          
      105 +                                                              
      106  ## 4. Como a política é representada
      107  
       43 -<Os limites vivem onde? Constantes no código, arquivo de confi
          -guração, tabela?                                              
       44 -Esta decisão é a que mais barato ou mais caro vai custar se a 
          -política mudar.>                                              
      108 +Os valores da política ficam **em um único módulo, `politica.p
          +y`, como dados**:                                             
      109  
      110 +```python                                                     
      111 +CATEGORIAS_REEMBOLSAVEIS = frozenset({"alimentacao", "transpor
          +te_urbano", "hospedagem"})                                    
      112 +LIMITE_POR_DATA = {                                           
      113 +    "alimentacao": Decimal("60.00"),                          
      114 +    "transporte_urbano": Decimal("80.00"),                    
      115 +    "hospedagem": Decimal("250.00"),                          
      116 +}                                                             
      117 +LIMIAR_NOTA_FISCAL = Decimal("100.00")   # exige nota se valor
          + > limiar (RN-007)                                            
      118 +```                                                           
      119 +                                                              
      120 +Cada constante tem um comentário com a RN de origem.          
      121 +                                                              
      122 +A **ordem das regras** também é dado, em `motor.py`:          
      123 +                                                              
      124 +```python                                                     
      125 +ETAPAS = [                                                    
      126 +    PorItem(valor_negativo),      # RN-005 → VALOR_NEGATIVO   
      127 +    PorItem(periodo),             # RN-004 → FORA_DO_PERIODO  
      128 +    PorItem(categoria),           # RN-001 → CATEGORIA_NAO_REE
          +MBOLSAVEL                                                     
      129 +    EmGrupo(duplicatas),          # RN-006 → DUPLICATA        
      130 +    PorItem(nota_fiscal),         # RN-007 → NOTA_FISCAL_AUSEN
          +TE                                                            
      131 +    EmGrupo(limites_por_data),    # RN-008, RN-009, RN-010 → L
          +IMITE_DIARIO                                                  
      132 +]                                                             
      133 +```                                                           
      134 +                                                              
      135 +- **Etapa por item:** recebe uma `Despesa` e devolve `None` (p
          +assa) ou uma recusa                                           
      136 +  com motivo e justificativa.                                 
      137 +- **Etapa em grupo:** recebe todas as despesas ainda vivas, em
          + ordem de posição,                                            
      138 +  e decide sobre o conjunto. A de duplicatas devolve recusas. 
          +A de limites                                                  
      139 +  devolve o valor reembolsável de cada despesa.               
      140 +- As etapas 1 e 2 (validação, normalização e arredondamento) a
          +contecem em                                                   
      141 +  `entrada.py`, porque precisam do JSON bruto. As despesas `In
          +valida` não entram                                            
      142 +  no motor.                                                   
      143 +- Uma despesa recusada sai da lista viva e não chega às etapas
          + seguintes. É isso                                            
      144 +  que impede uma despesa recusada de consumir limite (seção 8 
          +da spec).                                                     
      145 +- Ao final, uma despesa que chegou à etapa 8 é `APROVADO` se  
      146 +  `valor_reembolsavel == valor_considerado`, senão `LIMITADO`,
          + exatamente como a                                            
      147 +  seção 4 da spec define.                                     
      148 +                                                              
      149  ## 5. Decisões técnicas
      150  
       48 -### DT-001 — <decisão>                                        
      151 +### DT-001 — `Decimal` desde o parse do JSON                  
      152  
       50 -**Contexto:** <o que forçou a escolha>                        
       51 -**Decisão:** <o que foi decidido>                             
       52 -**Alternativa descartada:** <e por quê>                       
       53 -**Consequência:** <o que isso torna fácil e o que torna difíci
          -l>                                                            
      153 +**Contexto:** a RN-003 exige arredondamento comercial (10,005 
          +→ 10,01), e d-011                                             
      154 +tem três casas.                                               
      155 +**Decisão:** `json.loads(texto, parse_float=Decimal)`. Inteiro
          +s (`parse_int`)                                               
      156 +também são convertidos para `Decimal` na validação. O arredond
          +amento usa                                                    
      157 +`quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`, que no `D
          +ecimal` afasta a                                              
      158 +metade do zero, inclusive para negativos.                     
      159 +**Alternativa descartada:** float com `round()`. O Python arre
          +donda metade para                                             
      160 +par, e o float já chega com erro de representação.            
      161 +**Consequência:** nenhuma comparação de fronteira (100,00 vs 1
          +00,01) depende de                                             
      162 +float. O serializador precisa saber escrever `Decimal` (DT-005
          +).                                                            
      163  
       55 -### DT-002 — ...                                              
      164 +### DT-002 — Validação manual em dois níveis                  
      165  
      166 +**Contexto:** a RN-013 separa erro geral de erro em uma despes
          +a.                                                            
      167 +**Decisão:** `entrada.py` valida o documento e, se algo falhar
          +, levanta                                                     
      168 +`EntradaInvalida(mensagem)`. Em seguida valida cada despesa e 
          +produz `Despesa` ou                                           
      169 +`Invalida`. Pontos de cuidado, todos derivados da RN-013:     
      170 +- `bool` é subclasse de `int` em Python, então `"valor": true`
          + precisa ser                                                  
      171 +  rejeitado com teste explícito de tipo;                      
      172 +- datas validadas com regex `^\d{4}-\d{2}-\d{2}$` e depois `da
          +te.fromisoformat`.                                            
      173 +  O regex é necessário porque `fromisoformat` aceita formatos 
          +além de `AAAA-MM-DD`;                                         
      174 +- texto "vazio" = `str.strip() == ""`;                        
      175 +- campos informativos e desconhecidos não são lidos pela valid
          +ação.                                                         
      176 +**Alternativa descartada:** pydantic, que falha o documento in
          +teiro por padrão.                                             
      177 +**Consequência:** cada caso da RN-013 vira um `if` com teste p
          +róprio. Mais código                                           
      178 +explícito, mas cada linha aponta para um item da spec.        
      179 +                                                              
      180 +### DT-003 — `NaN` e `Infinity` como documento ilegível       
      181 +                                                              
      182 +**Contexto:** a RN-013 (D-001) trata `NaN`/`Infinity` como JSO
          +N inválido, mas o                                             
      183 +`json` do Python aceita esses literais por padrão.            
      184 +**Decisão:** `parse_constant` levanta `EntradaInvalida`, o que
          + vira erro geral.                                             
      185 +**Alternativa descartada:** aceitar e rejeitar depois como val
          +or não numérico.                                              
      186 +Isso contradiria a spec.                                      
      187 +**Consequência:** o parser fica estrito como a norma JSON.    
      188 +                                                              
      189 +### DT-004 — Política em módulo Python, pipeline como lista   
      190 +                                                              
      191 +**Contexto:** a mudança de requisito do dia 2 é desconhecida. 
          +É provável que ela                                            
      192 +mexa em limites, categorias, ordem das regras ou crie uma regr
          +a nova.                                                       
      193 +**Decisão:** valores da política em `politica.py` e ordem das 
          +etapas em                                                     
      194 +`ETAPAS` (seção 4 deste plano).                               
      195 +**Alternativa descartada:** arquivo de configuração externo (J
          +SON/YAML). Ele                                                
      196 +exigiria validar a própria configuração e documentar um format
          +o a mais, sem                                                 
      197 +ganho enquanto quem muda a política é quem muda o código.     
      198 +**Consequência:** trocar um valor é uma linha. Uma regra nova 
          +é uma função mais                                             
      199 +uma linha em `ETAPAS`. Se a política precisar variar por execu
          +ção (por exemplo,                                             
      200 +um dado de viagem na entrada), `politica.py` vira um objeto pa
          +ssado ao motor, e                                             
      201 +isso é uma refatoração local.                                 
      202 +                                                              
      203 +### DT-005 — Serialização da saída                            
      204 +                                                              
      205 +**Contexto:** a saída exige duas casas em `valor_considerado`,
      206 +`valor_reembolsavel` e `total_reembolsavel` (RN-003), `null` n
          +os campos sem                                                 
      207 +valor (D-001), e `colaborador`/`periodo` copiados como vieram,
          + que podem conter                                             
      208 +`Decimal` do parse.                                           
      209 +**Decisão:** `saida.py` monta a estrutura com `None` onde a sp
          +ec pede nulo. Um                                              
      210 +encoder próprio escreve todo `Decimal` como literal numérico J
          +SON:                                                          
      211 +- os três campos monetários saem quantizados em duas casas (`6
          +0.00`);                                                       
      212 +- `valor_informado` sai com `str(Decimal)`, sem quantizar (`33
          +.333`);                                                       
      213 +- zero negativo (`-0.00`, resultado de arredondar `-0.004`) é 
          +normalizado para                                              
      214 +  `0.00` antes de qualquer etapa, para que a RN-005 o veja com
          +o zero.                                                       
      215 +JSON escrito em UTF-8, com `ensure_ascii=False` e `indent=2`. 
      216 +**Alternativa descartada:** converter para float na saída, que
          + perde as duas                                                
      217 +casas (`60.0`); ou emitir string (`"60.00"`), que contradiz o 
          +tipo "número" da                                              
      218 +spec.                                                         
      219 +**Consequência:** um ponto único de formatação, testado isolad
          +amente.                                                       
      220 +                                                              
      221 +### DT-006 — Erro geral na CLI                                
      222 +                                                              
      223 +**Contexto:** a RN-013 diz que, em erro geral, o sistema "ence
          +rra com mensagem                                              
      224 +de erro e não gera saída". A forma de encerrar é técnica.     
      225 +**Decisão:**                                                  
      226 +- a mensagem vai para **stderr**;                             
      227 +- o código de saída é **1**;                                  
      228 +- o arquivo de saída **não é criado nem sobrescrito**. A CLI s
          +ó abre o arquivo                                              
      229 +  de saída depois que leitura, validação e cálculo terminaram 
          +sem erro. Se um                                               
      230 +  arquivo com esse nome já existir, ele fica intacto.         
      231 +Sucesso retorna 0. Argumentos inválidos de linha de comando re
          +tornam 2 (padrão                                              
      232 +do `argparse`).                                               
      233 +**Alternativa descartada:** gravar um JSON de erro no arquivo 
          +de saída. Contradiz                                           
      234 +"não gera saída".                                             
      235 +**Consequência:** quem chama a CLI distingue sucesso de erro s
          +ó pelo código de                                              
      236 +saída.                                                        
      237 +                                                              
      238 +### DT-007 — Normalização de texto                            
      239 +                                                              
      240 +**Contexto:** a RN-002 manda remover espaços das pontas, maiús
          +culas e acentos.                                              
      241 +**Decisão:** `strip()`, depois `casefold()`/`lower()`, depois 
      242 +`unicodedata.normalize("NFD", s)` removendo caracteres de cate
          +goria `Mn`                                                    
      243 +(marcas combinantes). Nada mais é alterado: espaços internos f
          +icam.                                                         
      244 +**Alternativa descartada:** biblioteca `unidecode`, que transl
          +itera além de                                                 
      245 +acentos e mudaria texto que a spec manda preservar.           
      246 +**Consequência:** `Alimentação` → `alimentacao`, `ç` → `c`.   
      247 +                                                              
      248 +### DT-008 — Justificativas por template                      
      249 +                                                              
      250 +**Contexto:** a seção 9 da spec exige saída determinística e j
          +ustificativas que                                             
      251 +citem a RN, o `id` da despesa mantida (duplicata) e o limite j
          +á consumido.                                                  
      252 +**Decisão:** uma função por motivo em `justificativas.py`, com
          + o mesmo texto dos                                            
      253 +exemplos da seção 4 da spec. Valores formatados como `R$ 60,00
          +`.                                                            
      254 +**Alternativa descartada:** montar o texto dentro de cada etap
          +a, que espalharia                                             
      255 +a formatação.                                                 
      256 +**Consequência:** os testes de regra verificam `status`, `moti
          +vo` e valores, e                                              
      257 +checam na justificativa só a presença da RN e dos `id` citados
          +. Isso evita testes                                           
      258 +frágeis a mudanças de redação.                                
      259 +                                                              
      260  ## 6. Estratégia de testes
      261  
       59 -- **Nível:** <unitário, integração, ponta a ponta — e a propor
          -ção entre eles>                                               
       60 -- **Cada `RN-NNN` da spec tem teste?** <como você garante isso
          ->                                                             
       61 -- **Casos de borda da seção 7 da spec:** <cobertos como>      
       62 -- **Nomenclatura:** <como o nome do teste remete ao requisito 
          -— isso é o que                                                
       63 -  fecha a rastreabilidade na correção>                        
      262 +Estrutura:                                                    
      263  
      264 +```                                                           
      265 +tests/                                                        
      266 +  test_rn001_categoria.py ... test_rn014_descricao.py   # um a
          +rquivo por RN                                                 
      267 +  test_secao7_casos_de_borda.py                         # tabe
          +la da seção 7                                                 
      268 +  test_secao9_aceite_exemplo.py                         # exem
          +plo completo                                                  
      269 +  test_cli.py                                           # pont
          +a a ponta via subprocess                                      
      270 +  test_saida_serializacao.py                            # DT-0
          +05                                                            
      271 +  test_rastreabilidade.py                               # toda
          + RN tem teste                                                 
      272 +```                                                           
      273 +                                                              
      274 +- **Nível:**                                                  
      275 +  - **unitário** (~70%): regras e normalização, sem I/O, com d
          +espesas montadas                                              
      276 +    por um helper `despesa(**campos)`;                        
      277 +  - **integração** (~20%): `entrada` → `motor` → `saida` a par
          +tir de dicts;                                                 
      278 +  - **ponta a ponta** (~10%): CLI via `subprocess`, conferindo
          + arquivo gerado,                                              
      279 +    stderr e código de saída.                                 
      280 +- **Cada `RN-NNN` da spec tem teste?** Há um arquivo `test_rnN
          +NN_*.py` por regra,                                           
      281 +  e o "Aceite" de cada RN vira pelo menos um teste nele. O    
      282 +  `test_rastreabilidade.py` lê a `spec.md`, extrai os IDs `RN-
          +\d{3}` e falha se                                             
      283 +  algum não tiver arquivo de teste correspondente.            
      284 +- **Casos de borda da seção 7 da spec:** um teste parametrizad
          +o com uma linha                                               
      285 +  por caso da tabela. O `id` do parâmetro é o nome do caso na 
          +spec, então o                                                 
      286 +  relatório do pytest lista os casos com os mesmos nomes da sp
          +ec.                                                           
      287 +- **Aceite da seção 9 da spec:** roda `exemplos/despesas-exemp
          +lo.json` e                                                    
      288 +  compara as 14 linhas (`valor_reembolsavel`, `status`, `motiv
          +o`) e o total                                                 
      289 +  585,43.                                                     
      290 +- **Invariantes da seção 9 da spec:**                         
      291 +  - determinismo: duas execuções produzem saídas idênticas byt
          +e a byte;                                                     
      292 +  - RN-014: trocar todas as descrições não altera `valor_reemb
          +olsavel`,                                                     
      293 +    `status` nem `motivo`;                                    
      294 +  - "todo item tem justificativa citando RN-xxx", verificado p
          +or regex.                                                     
      295 +- **DT-006:** em erro geral, o teste cria antes um arquivo de 
          +saída com conteúdo                                            
      296 +  conhecido e confirma que ele continua igual depois da execuç
          +ão.                                                           
      297 +- **Nomenclatura:** `test_rnNNN_<comportamento>`, por exemplo 
      298 +  `test_rn007_valor_exatamente_100_nao_exige_nota`. Testes de 
          +decisão técnica                                               
      299 +  usam `test_dtNNN_<comportamento>`.                          
      300 +                                                              
      301  ## 7. Riscos
      302  
      303  | Risco | Probabilidade | O que faço se acontecer |
      304  |---|---|---|
       69 -| | | |                                                       
      305 +| Float vazar em algum ponto (parse, soma, literal no código) 
          +e errar uma fronteira | Média | DT-001; constantes sempre como
          + `Decimal("…")`; teste para 10,005 → 10,01 e para 100,00 vs 10
          +0,01 |                                                        
      306 +| Usar `round()` ou `ROUND_HALF_EVEN` por engano | Média | Uma
          + única função de arredondamento em `normalizacao.py`, com test
          +e de metade positiva e negativa |                             
      307 +| `-0.00` aparecer na saída ou não ser tratado como zero | Méd
          +ia | Normalização em `normalizacao.py` (DT-005) e caso da seçã
          +o 7 (−0,004) |                                                
      308 +| Serializador perder as duas casas (`60.0`) ou falhar com `De
          +cimal` em `colaborador`/`periodo` | Alta se não testado | `tes
          +t_saida_serializacao.py` cobre os dois casos |                
      309 +| `bool` aceito como número em `valor` | Média | Teste explíci
          +to em RN-013 |                                                
      310 +| `date.fromisoformat` aceitar formatos além de `AAAA-MM-DD` |
          + Alta (Python 3.11+ aceita mais formatos) | Regex antes do par
          +se (DT-002) |                                                 
      311 +| Acentos não removidos em todos os casos (letras compostas, `
          +ç`) | Baixa | DT-007, com testes para `Alimentação`, `ç` e mai
          +úsculas acentuadas |                                          
      312 +| Mudança do dia 2 exigir reestruturação | Média | DT-004. Se 
          +a mudança não couber em `politica.py` ou `ETAPAS`, registrar o
          + motivo no `DECISIONS.md` e na seção 5 deste plano |          
      313 +| Justificativa divergir dos exemplos da spec e o teste não pe
          +gar | Baixa | Testes da seção 9 checam RN citada e `id`; os ex
          +emplos da seção 4 viram um teste de texto exato |             
      314 +| Comportamento implementado sem regra na spec | Média | Toda 
          +dúvida de negócio que aparecer na implementação volta para a s
          +pec antes do código (regra do `CLAUDE.md`) |                  

● Preenchi o specs/001-motor-reembolso/plan.md com base na spec 1.1 e na D-001.
  Não alterei a spec.md nem o DECISIONS.md, e não fiz commit. Os testes não
  rodaram porque ainda não existe código.

  O que o plano contém, por seção:

  1. Stack: Python 3.12+, pytest, json da biblioteca padrão com validação
     manual, Decimal lido direto do JSON, argparse e ruff. Cada linha tem a
     alternativa descartada e o motivo. Também traz os comandos de rodar, testar
     e lint, que depois podem ir para o CLAUDE.md.
  2. Arquitetura: o caminho cli → entrada → motor → saida, com uma tabela de
     módulos dizendo quais regras cada um atende. Só a CLI faz I/O; motor,
     etapas, normalização e política não sabem nada de JSON.
  3. Modelo de dados: Documento, Despesa (validada e normalizada), Invalida
     (recusada na etapa 1, com id e valor_informado que podem ser nulos),
     Resultado e os enums Status e Motivo com os mesmos textos da spec.
  4. Representação das regras:
     - os valores da política ficam como dados em politica.py;
     - a ordem da seção 8 vira uma lista ETAPAS, com etapas por item e etapas em
       grupo;
     - validação e arredondamento (etapas 1 e 2) ficam em entrada.py;
     - a distinção entre aprovado e limitado segue exatamente a definição da
       seção 4.
  5. Decisões técnicas, DT-001 a DT-008:
     - DT-001: Decimal e ROUND_HALF_UP;
     - DT-002: validação em dois níveis, com cuidado para bool, regex de data e
       texto vazio;
     - DT-003: NaN/Infinity viram erro geral via parse_constant;
     - DT-004: política em módulo Python e regras numa lista ordenada;
     - DT-005: serialização com duas casas, null, valor_informado sem quantizar
       e zero negativo virando 0,00;
     - DT-006, o erro geral: mensagem em stderr, código de saída 1, e o arquivo
       de saída só é aberto depois de tudo dar certo, então não é criado nem
       sobrescrito. Sucesso retorna 0; argumento de linha de comando inválido
       retorna 2, o padrão do argparse;
     - DT-007: normalização com NFD e remoção dos acentos;
     - DT-008: justificativas montadas a partir de templates fixos.
  6. Estratégia de testes:
     - um arquivo test_rnNNN_*.py por regra;
     - um teste parametrizado com a tabela da seção 7, em que o nome de cada
       caso é o mesmo da spec;
     - o exemplo completo da seção 9 com o total de 585,43;
     - testes da CLI via subprocess, incluindo o caso de um arquivo de saída que
       já existia e deve continuar intacto;
     - invariantes de determinismo e da RN-014;
     - um test_rastreabilidade.py que lê a spec e falha se alguma RN não tiver
       teste.
  7. Riscos: 10 riscos com probabilidade e mitigação. Os principais: float
     vazando para algum cálculo, round() arredondando metade para par, -0.00 na
     saída, serialização de Decimal, bool aceito como número e fromisoformat
     aceitando formatos fora de AAAA-MM-DD.

  Dois pontos para você revisar:
  - Código 2 para argumento de linha de comando inválido. Isso não estava na sua
    decisão do item 8. É o padrão do argparse e não é regra de negócio, mas se
    preferir tudo como 1, eu ajusto.
  - Justificativas. Os testes de regra conferem só a RN e os id citados, não o
    texto inteiro. A exceção são os exemplos da seção 4 da spec, testados com
    texto exato. Assim, mudar a redação não quebra a suíte inteira.

  Sugestão de commit quando quiser: um docs(spec): com a spec e o D-001, e
  depois um docs(plan): separado com o plano.

✻ Brewed for 1m 39s · done 1:47