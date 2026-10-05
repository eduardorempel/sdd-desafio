 ▐▛███▛█   Claude Code v2.1.289
▝▜██████▀  Opus 5.5 · API Usage Billing
 ▝▝   ▝▝   C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\reembolso


> Leia:                                                                         
   CLAUDE.md                                                                    
  - specs/001-motor-reembolso/spec.md                                           
     specs/001-motor-reembolso/plan.md                                          
  - specs/001-motor-reembolso/tasks.md                                          
    specs/001-motor-reembolso/DECISIONS.md                                      
                                                                                
  Agora crie as novas tasks do Envelope do Dia 2 em:                            
                                                                                
  specs/001-motor-reembolso/tasks.md                                            
                                                                                
  Continue a numeração a partir da T-026.                                       
                                                                                
  As tasks devem cobrir somente as mudanças da spec 2.0 e da D-002, incluindo:  
   leitura e validação de politica-v4.json                                      
   seleção da política por centro de custo e fallback para a padrão             
   herança de categorias da política padrão;                                    
   limite zero como categoria não reembolsável                                  
   campo moeda;                                                                 
  leitura e validação opcional de cambio.json                                   
   conversão pela data da despesa                                               
   uso da última cotação anterior disponível                                    
   COTACAO_INDISPONIVEL                                                         
   nota fiscal usando valor convertido                                          
   duplicatas considerando mesma moeda e mesmo valor original                   
   novos campos de saída                                                        
   atualização dos testes afetados da v3                                        
   testes dos dois arquivos do envelope                                         
   atualização de rastreabilidade.                                              
                                                                                
  Cada task deve ter:                                                           
  - requisitos/ambiguidades atendidos;                                          
  - critério de aceite;                                                         
  - teste associado;                                                            
  - campo Commit vazio.                                                         
                                                                                
  Não implemente código.                                                        
  Não faça commit.                                                              
                                                                                
  No final, mostre a lista das novas tasks e diga se tasks.md está pronta para  
  revisão.                                                                      

  Read 4 files, ran 3 shell commands (ctrl+o to expand)

● Li spec 2.0, plan, D-002 e tasks; agora confiro como os testes de aceite da v3
  rodam o exemplo para ordenar as tasks sem deixar a suíte vermelha entre
  commits.

  Ran 1 shell command (ctrl+o to expand)

● Agora escrevo a Fase 7 em tasks.md.

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 278 lines, removed 4 lines
      268  
      269  ---
      270  
      271 -## Fase 7 — Envelope (criar no Dia 2)                         
      271 +## Fase 7 — Envelope (Dia 2)                                  
      272  
      273 -<Novas tasks a partir da mudança de requisito. Numeração conti
          -nua de onde parou                                             
      274 -(T-026) — não reinicie e não renumere as antigas: a numeração 
          -é o eixo da                                                   
      275 -rastreabilidade.>                                             
      273 +**Baseado em:** spec 2.0 (D-002) · plan 1.0, **a atualizar par
          +a a spec 2.0 antes                                            
      274 +da T-026** (`docs(plan):`). Nomes de módulo, função e argument
          +o de CLI citados                                              
      275 +abaixo seguem a arquitetura do plan 1.0 e são provisórios até 
          +essa revisão.                                                 
      276  
      277 +Sequência pensada para a suíte ficar verde em todo commit:    
      278 +                                                              
      279 +- T-026 a T-030 criam os documentos novos e o campo `moeda`, s
          +em mudar o                                                    
      280 +  resultado de nenhuma despesa.                               
      281 +- T-031 a T-037 levam as regras para a política externa e o câ
          +mbio. Até a                                                   
      282 +  T-038, o fluxo real (CLI e testes de exemplo) usa a **políti
          +ca padrão** da                                                
      283 +  v4, que tem os mesmos valores da v3, e por isso os testes de
          + aceite da v3                                                 
      284 +  continuam passando. As regras novas são testadas passando a 
          +política                                                      
      285 +  aplicável explicitamente ao motor.                          
      286 +- T-038 liga a seleção por centro de custo e o câmbio no fluxo
          + real e atualiza,                                             
      287 +  no mesmo commit, os testes da v3 cujo resultado muda.       
      288 +- T-039 a T-041 fecham a §7, a §9 e a rastreabilidade.        
      289 +                                                              
      290 +Com a T-031, as constantes de `politica.py` deixam de existir 
          +(fim da regra                                                 
      291 +"constantes sem task própria" do topo deste arquivo).         
      292 +                                                              
      293 +### 7.1 — Modelo e documentos de entrada                      
      294 +                                                              
      295 +- [ ] **T-026** — `modelo.py`: motivo `COTACAO_INDISPONIVEL`; 
          +`Despesa` ganha                                               
      296 +  `moeda`, `taxa_cambio` e `data_cotacao`; `Resultado` ganha `
          +moeda`,                                                       
      297 +  `taxa_cambio` e `data_cotacao`. Valores padrão (`BRL`, nulo,
          + nulo) mantêm as                                              
      298 +  despesas da v3 como estão.                                  
      299 +  - **Atende:** spec §4 (tabela de motivos, campos de saída), 
          +RN-018, AMB-025, AMB-033                                      
      300 +  - **Aceite:** os oito motivos têm exatamente os códigos da s
          +pec;                                                          
      301 +    `COTACAO_INDISPONIVEL` existe; a suíte da v3 continua pass
          +ando sem alteração.                                           
      302 +  - **Teste:** `tests/test_modelo.py::test_motivos_iguais_aos_
          +codigos_da_spec`                                              
      303 +    (atualizado para oito motivos)                            
      304 +  - **Commit:**                                               
      305 +                                                              
      306 +- [ ] **T-027** — Leitura e validação do documento de política
          + (`politica.py`                                               
      307 +  passa a ler `politica-v4.json` e devolver um objeto `Politic
          +a`). Chaves de                                                
      308 +  categoria e de centro de custo normalizadas pela RN-002; `mo
          +eda_base`                                                     
      309 +  normalizada pela RN-017. Erro → `EntradaInvalida`. Ainda não
          + é usado pelo motor.                                          
      310 +  - **Atende:** RN-015, RN-002 (chaves do documento), RN-013 (
          +erro geral),                                                  
      311 +    AMB-031, AMB-034, AMB-036                                 
      312 +  - **Aceite:** `politica-v4.json` → aceito, com `padrao` e tr
          +ês centros.                                                   
      313 +    Erro geral para: JSON ilegível, `NaN`, `Infinity`; sem `pa
          +drao`, sem                                                    
      314 +    `centros_custo`, sem `moeda_base` ou sem `nota_fiscal_obri
          +gatoria_acima_de`;                                            
      315 +    `padrao` que não é objeto; entrada de categoria que não é 
          +objeto; limite                                                
      316 +    `-1`, `"60"` ou `true`; limiar negativo ou não numérico; `
          +moeda_base` `USD`;                                            
      317 +    `"periodicidade": "mes"` ou ausente; `Alimentação` e `alim
          +entacao` na mesma                                             
      318 +    tabela; `CC-ADM` e ` cc-adm ` em `centros_custo`. Sem erro
          +: `moeda_base`                                                
      319 +    `" brl "`; `centros_custo: {}`; limite `0`; `"acrescimo_em
          +_viagem_percentual": "x"`,                                    
      320 +    `versao`, `vigencia` e `observacao` com qualquer valor.   
      321 +  - **Teste:** `tests/test_rn015_politica.py`                 
      322 +  - **Commit:**                                               
      323 +                                                              
      324 +- [ ] **T-028** — Política aplicável: função que recebe a `Pol
          +itica` e o                                                    
      325 +  `colaborador.centro_custo` e devolve a tabela efetiva (centr
          +o sobre a padrão,                                             
      326 +  herança por categoria) e a origem a citar nas justificativas
          +. Na validação do                                             
      327 +  documento de despesas, `centro_custo` presente e não texto v
          +ira erro geral.                                               
      328 +  Ainda não é usada pelo motor.                               
      329 +  - **Atende:** RN-016, RN-002 (centro de custo), RN-013 (erro
          + geral do centro de                                           
      330 +    custo), AMB-018, AMB-019, AMB-020, AMB-021                
      331 +  - **Aceite:** sem `centro_custo` ou `"  "` → padrão, origem 
          +"política padrão";                                            
      332 +    `CC-COMERCIAL` e ` cc-comercial ` → tabela do `CC-COMERCIA
          +L`, origem                                                    
      333 +    "centro de custo `CC-COMERCIAL`"; `CC-SUPORTE-N2` → padrão
          +, origem "política                                            
      334 +    padrão; centro de custo `CC-SUPORTE-N2` não cadastrado"; `
          +CC-ADM` →                                                     
      335 +    `hospedagem` 250,00 herdada da padrão e `alimentacao` 45,0
          +0 do centro;                                                  
      336 +    `CC-ENG-PLATAFORMA` → `hospedagem` 0,00 (não herda, porque
          + consta);                                                     
      337 +    `CC-COMERCIAL` → `representacao` 300,00; padrão → sem `rep
          +resentacao`;                                                  
      338 +    `"centro_custo": 42` → `EntradaInvalida`.                 
      339 +  - **Teste:** `tests/test_rn016_politica_aplicavel.py`,      
      340 +    `tests/test_rn013_dados_invalidos.py::test_rn013_erro_gera
          +l_*` (caso                                                    
      341 +    `centro_custo` numérico)                                  
      342 +  - **Commit:**                                               
      343 +                                                              
      344 +- [ ] **T-029** — Leitura e validação do documento de câmbio (
          +`cambio.py` →                                                 
      345 +  objeto `Cambio`), opcional. Quando informado, é sempre valid
          +ado. Códigos de                                               
      346 +  moeda normalizados pela RN-017. Erro → `EntradaInvalida`. Ai
          +nda não é usado                                               
      347 +  pelo motor.                                                 
      348 +  - **Atende:** RN-018 (documento de câmbio), RN-013 (erro ger
          +al), AMB-032                                                  
      349 +  - **Aceite:** `cambio.json` → aceito, com 12 datas. Erro ger
          +al para: JSON                                                 
      350 +    ilegível, `NaN`, `Infinity`; sem `moeda_base` ou sem `taxa
          +s`; `taxas` que não                                           
      351 +    é objeto; `moeda_base` diferente da da política; chave `20
          +26-7-13` ou                                                   
      352 +    `2026-02-30`; taxa `0`, `-5.42`, `"5,42"` ou `true`; `USD`
          + e ` usd ` na mesma                                           
      353 +    data. Sem erro: `fonte` e `observacao` com qualquer valor;
          + `" usd "` lido como                                          
      354 +    `USD`.                                                    
      355 +  - **Teste:** `tests/test_rn018_cambio.py::test_rn018_documen
          +to_*`                                                         
      356 +  - **Commit:**                                               
      357 +                                                              
      358 +- [ ] **T-030** — Campo `moeda` da despesa: ausente → `BRL`; t
          +exto normalizado                                              
      359 +  (pontas e maiúsculas); vazio ou não texto → `DADOS_INVALIDOS
          +` com `moeda` nulo.                                           
      360 +  Qualquer código não vazio é aceito. Revisa a T-007, onde `mo
          +eda` era ignorada.                                            
      361 +  - **Atende:** RN-017, RN-013 (erro em uma despesa), AMB-024 
      362 +  - **Aceite:** e-010 (sem `moeda`) → `BRL`; `" usd "` → `USD`
          +; `"XYZ"` → aceito;                                           
      363 +    `""`, `"   "` e `840` → `DADOS_INVALIDOS` e as demais desp
          +esas seguem.                                                  
      364 +    O teste da T-007 que tratava `"moeda": "USD"` como campo i
          +gnorado passa a                                               
      365 +    usar `"projeto": "X"`.                                    
      366 +  - **Teste:** `tests/test_rn017_moeda.py`,                   
      367 +    `tests/test_rn013_dados_invalidos.py::test_rn013_despesa_c
          +ampo_desconhecido_e_ignorado`                                 
      368 +  - **Commit:**                                               
      369 +                                                              
      370 +### 7.2 — Regras com política externa e câmbio                
      371 +                                                              
      372 +- [ ] **T-031** — Política externa no motor e na CLI: `calcula
          +r` recebe a                                                   
      373 +  política aplicável (T-028); as etapas de nota fiscal e de li
          +mites passam a ler                                            
      374 +  o limiar e os limites dela; `periodicidade` `dia` e `diaria`
          + têm o mesmo                                                  
      375 +  efeito. As constantes de `politica.py` saem. A CLI ganha `--
          +politica`                                                     
      376 +  (obrigatório); documento de política ausente ou inválido é e
          +rro geral, sem                                                
      377 +  saída. Até a T-038, CLI e testes de exemplo usam a política 
          +padrão.                                                       
      378 +  - **Atende:** RN-015, RN-007 (limiar do documento), RN-008 (
          +limites do                                                    
      379 +    documento), RN-013 (erro geral), AMB-031, AMB-036, DT-004 
          +(revisão), DT-006                                             
      380 +  - **Aceite:** com a padrão da v4, toda a suíte da v3 passa (
          +só as chamadas                                                
      381 +    mudam para informar a política). Política com `alimentacao
          +` 70,00 → duas                                                
      382 +    despesas de 50,00 na mesma data → 50,00 + 20,00. Limiar 15
          +0,00 → 120,00 sem                                             
      383 +    nota passa. CLI sem `--politica` → erro, arquivo de saída 
          +não criado;                                                   
      384 +    `--politica` com limite `-1` → código 1, arquivo de saída 
          +existente intacto.                                            
      385 +  - **Teste:** `tests/test_rn007_nota_fiscal.py::test_rn007_li
          +miar_vem_do_documento`,                                       
      386 +    `tests/test_rn008_limites.py::test_rn008_limite_vem_do_doc
          +umento`,                                                      
      387 +    `::test_rn008_dia_e_diaria_sao_limite_por_data`,          
      388 +    `tests/test_cli.py::test_rn015_sem_politica_e_erro_geral`,
      389 +    `::test_rn015_politica_invalida_nao_sobrescreve_saida`    
      390 +  - **Commit:**                                               
      391 +                                                              
      392 +- [ ] **T-032** — Etapa de categoria pela política aplicável: 
          +reembolsável só se                                            
      393 +  consta da tabela efetiva com limite maior que zero; limite 0
          +,00 →                                                         
      394 +  `CATEGORIA_NAO_REEMBOLSAVEL`; `observacao` ignorada. A justi
          +ficativa cita a                                               
      395 +  política aplicada (origem da T-028). Revisa a T-012.        
      396 +  - **Atende:** RN-001, RN-016, spec §4 (justificativa de cate
          +goria), AMB-014,                                              
      397 +    AMB-021, AMB-022, AMB-023                                 
      398 +  - **Aceite:** d-005 (`coworking`) → recusado, `CATEGORIA_NAO
          +_REEMBOLSAVEL`.                                               
      399 +    `CC-ENG-PLATAFORMA`: d-010 (hospedagem) → recusado, `CATEG
          +ORIA_NAO_REEMBOLSAVEL`;                                       
      400 +    d-013 (hospedagem, 690,00, sem nota) → `CATEGORIA_NAO_REEM
          +BOLSAVEL`, e não                                              
      401 +    `NOTA_FISCAL_AUSENTE`. Padrão: f-003 (`representacao`) → r
          +ecusado.                                                      
      402 +    `CC-COMERCIAL`: e-001 (`representacao`) → passa. `CC-ADM`:
          + hospedagem →                                                 
      403 +    passa (herança). Limite 0 em qualquer categoria de qualque
          +r tabela → recusado.                                          
      404 +    A justificativa cita a RN-001 e a origem da política.     
      405 +  - **Teste:** `tests/test_rn001_categoria.py`                
      406 +  - **Commit:**                                               
      407 +                                                              
      408 +- [ ] **T-033** — Etapa de limites pela tabela efetiva, inclui
          +ndo                                                           
      409 +  `representacao` como categoria independente, e justificativa
          + de                                                           
      410 +  `LIMITE_DIARIO` citando a origem do limite. O acréscimo em v
          +iagem do documento                                            
      411 +  não é aplicado. Revisa a T-015 e a T-016.                   
      412 +  - **Atende:** RN-008, RN-009, RN-010, RN-011, RN-016, spec §
          +4 (justificativa                                              
      413 +    de limite), AMB-008, AMB-021, AMB-023, AMB-035, AMB-036   
      414 +  - **Aceite:** `CC-COMERCIAL`: e-007 (hospedagem, 1.200,00, "
          +3 noites") →                                                  
      415 +    400,00, `limitado`; e-001 (`representacao`, 340,00) → 300,
          +00, `limitado`;                                               
      416 +    e-008 (alimentação, 95,00) → 90,00, `limitado`; alimentaçã
          +o e representação                                             
      417 +    na mesma data não dividem limite. `CC-ADM`: hospedagem 300
          +,00 → 250,00,                                                 
      418 +    `limitado`. `CC-ENG-PLATAFORMA`: d-001 + d-002 → 72,50 + 2
          +,50. Padrão:                                                  
      419 +    f-002 (310,00) → 250,00. `acrescimo_em_viagem_percentual` 
          +50 → nenhum limite                                            
      420 +    acima da tabela. A justificativa cita o limite, o valor co
          +nsumido, os `id`                                              
      421 +    que consumiram e a origem.                                
      422 +  - **Teste:** `tests/test_rn008_limites.py`, `tests/test_rn00
          +9_distribuicao.py`,                                           
      423 +    `tests/test_rn010_parcial.py`, `tests/test_rn011_viagem.py
          +`                                                             
      424 +  - **Commit:**                                               
      425 +                                                              
      426 +- [ ] **T-034** — Etapa de conversão e arredondamento (etapa 3
          + da §8, antes de                                              
      427 +  valor negativo): `BRL` não consulta o câmbio; outra moeda us
          +a a taxa da data                                              
      428 +  da despesa ou a da data anterior mais próxima com essa moeda
          +; o produto é                                                 
      429 +  arredondado uma vez. Sem taxa, ou sem documento de câmbio → 
      430 +  `COTACAO_INDISPONIVEL`, com `valor_considerado` nulo e justi
          +ficativa citando                                              
      431 +  moeda e data. `calcular` recebe o `Cambio` opcional. A linha
          + da §7 "campo                                                 
      432 +  desconhecido" (que usava `moeda: USD`) passa a usar `projeto
          +`.                                                            
      433 +  - **Atende:** RN-018, RN-003, RN-012, spec §8 (etapa 3), spe
          +c §4                                                          
      434 +    (justificativa de cotação), AMB-025, AMB-026, AMB-027, AMB
          +-029                                                          
      435 +  - **Aceite:** e-002 (22,00 EUR, 2026-07-14) → taxa 5,93, `da
          +ta_cotacao`                                                   
      436 +    2026-07-14, 130,46. e-004 (30,00 EUR, sábado 2026-07-18) →
          + taxa 5,96 de                                                 
      437 +    2026-07-17, 178,80. f-004 (12,00 USD, 2026-07-21) → 65,76.
          + 33,333 USD em                                                
      438 +    2026-07-13 → 180,66. e-006 (55,00 GBP) → recusado, `COTACA
          +O_INDISPONIVEL`,                                              
      439 +    `valor_considerado` nulo, justificativa citando `GBP` e a 
          +data. USD em                                                  
      440 +    2026-07-10 → `COTACAO_INDISPONIVEL`. USD sem câmbio → `COT
          +ACAO_INDISPONIVEL`                                            
      441 +    e as despesas em BRL seguem. BRL em sábado → sem taxa, pro
          +cessada.                                                      
      442 +    −10,00 GBP → `COTACAO_INDISPONIVEL`; −10,00 USD em 2026-07
          +-13 → −54,20,                                                 
      443 +    `VALOR_NEGATIVO`. USD sem cotação e fora do período → `COT
          +ACAO_INDISPONIVEL`.                                           
      444 +  - **Teste:** `tests/test_rn018_cambio.py::test_rn018_convers
          +ao_*`,                                                        
      445 +    `tests/test_rn003_arredondamento.py::test_rn003_arredonda_
          +uma_vez_depois_da_conversao`,                                 
      446 +    `tests/test_secao7_casos_de_borda.py` (linha "Campo descon
          +hecido")                                                      
      447 +  - **Commit:**                                               
      448 +                                                              
      449 +- [ ] **T-035** — Nota fiscal comparada com o valor convertido
          + para reais                                                   
      450 +  (`test(T-035)`; a T-034 já entrega `valor_considerado` em re
          +ais).                                                         
      451 +  - **Atende:** RN-007, AMB-028                               
      452 +  - **Aceite:** e-005 (40,00 USD × 5,50 = 220,00, sem nota) → 
          +recusado,                                                     
      453 +    `NOTA_FISCAL_AUSENTE`. e-003 (14,50 EUR × 5,88 = 85,26, se
          +m nota) → passa.                                              
      454 +    20,00 USD (abaixo de 100 na moeda original, acima em reais
          +), sem nota →                                                 
      455 +    recusado.                                                 
      456 +  - **Teste:** `tests/test_rn007_nota_fiscal.py::test_rn007_co
          +mpara_valor_convertido_*`                                     
      457 +  - **Commit:**                                               
      458 +                                                              
      459 +- [ ] **T-036** — Duplicatas exigem a mesma moeda e o mesmo va
          +lor informado                                                 
      460 +  arredondado para centavos na moeda original (em `BRL`, o pró
          +prio                                                          
      461 +  `valor_considerado`). Despesas recusadas por `COTACAO_INDISP
          +ONIVEL` não entram                                            
      462 +  no grupo. Revisa a T-013.                                   
      463 +  - **Atende:** RN-006, AMB-010, AMB-030                      
      464 +  - **Aceite:** duas despesas de 22,00 EUR, mesmas data, categ
          +oria e fornecedor                                             
      465 +    → a segunda é `DUPLICATA`, citando a primeira. 22,00 EUR e
          + 130,46 BRL → não                                             
      466 +    são duplicatas. 22,00 EUR e 22,00 USD → não são duplicatas
          +. 22,004 EUR e                                                
      467 +    22,00 EUR → duplicatas. Duas GBP iguais → ambas `COTACAO_I
          +NDISPONIVEL`,                                                 
      468 +    nenhuma `DUPLICATA`.                                      
      469 +  - **Teste:** `tests/test_rn006_duplicatas.py`               
      470 +  - **Commit:**                                               
      471 +                                                              
      472 +- [ ] **T-037** — Saída com os campos novos, na ordem da §4: `
          +moeda`,                                                       
      473 +  `taxa_cambio` (como está no documento, sem quantizar) e `dat
          +a_cotacao`                                                    
      474 +  (`AAAA-MM-DD`); `valor_considerado` nulo também em `COTACAO_
          +INDISPONIVEL`;                                                
      475 +  `moeda` nula em `DADOS_INVALIDOS`. Revisa a T-018.          
      476 +  - **Atende:** spec §4 (saída), RN-003, RN-017, RN-018, AMB-0
          +33, DT-005                                                    
      477 +  - **Aceite:** item em BRL → `"moeda": "BRL"`, `taxa_cambio` 
          +e `data_cotacao`                                              
      478 +    `null`. e-002 → `"taxa_cambio": 5.93`, `"data_cotacao": "2
          +026-07-14"`,                                                  
      479 +    `"valor_considerado": 130.46`, `"valor_informado": 22.00`.
          + e-006 →                                                      
      480 +    `"moeda": "GBP"`, `valor_considerado`, `taxa_cambio` e `da
          +ta_cotacao` `null`.                                           
      481 +    `DADOS_INVALIDOS` → `moeda` `null`. Campos do item na orde
          +m da tabela da §4.                                            
      482 +  - **Teste:** `tests/test_saida_serializacao.py::test_dt005_c
          +ampos_do_item_na_ordem_da_spec`,                              
      483 +    `::test_dt005_moeda_e_cotacao_em_brl`, `::test_dt005_taxa_
          +cambio_sem_quantizar`,                                        
      484 +    `::test_dt005_nulos_em_cotacao_indisponivel`, `::test_dt00
          +5_nulos_em_dados_invalidos`                                   
      485 +  - **Commit:**                                               
      486 +                                                              
      487 +### 7.3 — Integração, aceite e rastreabilidade                
      488 +                                                              
      489 +- [ ] **T-038** — Fluxo real completo: a CLI ganha `--cambio` 
          +(opcional) e passa                                            
      490 +  a escolher a política pelo `colaborador.centro_custo` (T-028
          +). No mesmo                                                   
      491 +  commit, atualiza os testes da v3 cujo resultado muda com o  
      492 +  `CC-ENG-PLATAFORMA`: tabela da §9 (total 585,43 → 351,43), j
          +ustificativas                                                 
      493 +  exatas da §4 (Exemplo 1) e as linhas da §7 reescritas pela s
          +pec 2.0. Atualiza                                             
      494 +  o comando de execução no README e no `CLAUDE.md`. Revisa as 
          +T-019, T-020,                                                 
      495 +  T-021, T-022 e T-025.                                       
      496 +  - **Atende:** RN-016, RN-018 (câmbio opcional), RN-013 (erro
          + geral dos                                                    
      497 +    documentos), spec §4 (Exemplo 1), spec §8 (validação antes
          + das etapas),                                                 
      498 +    spec §9 (exemplo original), DT-006                        
      499 +  - **Aceite:** `exemplos/despesas-exemplo.json` + `politica-v
          +4.json`, sem                                                  
      500 +    câmbio → as 14 linhas da §9 e total 351,43; d-001, d-002 e
          + d-004 com                                                    
      501 +    exatamente as justificativas do Exemplo 1 da §4. Sem `cent
          +ro_custo` →                                                   
      502 +    padrão. `"centro_custo": 42`, câmbio com taxa 0 ou câmbio 
          +com `moeda_base`                                              
      503 +    diferente → código 1, arquivo de saída existente intacto. 
          +Linhas da §7                                                  
      504 +    reescritas ("Duas despesas no mesmo dia...", "Hospedagem c
          +om várias                                                     
      505 +    diárias", "Duas hospedagens na mesma data", "Hospedagem se
          +m nota acima de                                               
      506 +    100", "Categoria em maiúsculas", "Campo desconhecido") bat
          +em com a spec 2.0.                                            
      507 +  - **Teste:** `tests/test_secao9_aceite_exemplo.py`,         
      508 +    `tests/test_secao7_casos_de_borda.py` (linhas reescritas),
      509 +    `tests/test_cli.py::test_cli_exemplo_gera_arquivo`,       
      510 +    `::test_rn016_centro_custo_invalido_e_erro_geral`,        
      511 +    `::test_rn018_cambio_invalido_nao_sobrescreve_saida`,     
      512 +    `::test_rn018_moedas_base_divergentes_e_erro_geral`       
      513 +  - **Commit:**                                               
      514 +                                                              
      515 +- [ ] **T-039** — Casos novos da §7 da spec 2.0 na tabela para
          +metrizada, com o                                              
      516 +  nome do caso como `id` (`test(T-039)`).                     
      517 +  - **Atende:** spec §7 (casos de RN-001, RN-006, RN-007, RN-0
          +13, RN-015 a                                                  
      518 +    RN-018 e seção 8 incluídos na spec 2.0)                   
      519 +  - **Aceite:** os 68 casos da §7 passam e aparecem no relatór
          +io do pytest com o                                            
      520 +    nome da spec; o teste de contagem passa de 37 para 68.    
      521 +  - **Teste:** `tests/test_secao7_casos_de_borda.py::test_seca
          +o7_caso_de_borda`,                                            
      522 +    `::test_secao7_tem_68_casos`                              
      523 +  - **Commit:**                                               
      524 +                                                              
      525 +- [ ] **T-040** — Aceite dos dois documentos do envelope pela 
          +CLI, com                                                      
      526 +  `politica-v4.json` e `cambio.json` (`test(T-040)`).         
      527 +  - **Atende:** spec §9 (envelope), spec §4 (Exemplo 2), RN-01
          +4, RN-016, AMB-019                                            
      528 +  - **Aceite:** `despesas-envelope.json` → as 10 linhas da §9 
      529 +    (`valor_considerado`, `valor_reembolsavel`, `status`, `mot
          +ivo`) e total                                                 
      530 +    1.143,26; e-002 com exatamente a justificativa do Exemplo 
          +2 da §4.                                                      
      531 +    `despesas-envelope-cc-desconhecido.json` → as 4 linhas e t
          +otal 373,76; as                                               
      532 +    justificativas de f-002 e f-003 citam "política padrão; ce
          +ntro de custo                                                 
      533 +    `CC-SUPORTE-N2` não cadastrado". Nos dois: um item por des
          +pesa, na ordem;                                               
      534 +    todo item cita `RN-\d{3}`; duas execuções idênticas byte a
          + byte; trocar as                                              
      535 +    descrições não altera `valor_reembolsavel`, `status` nem `
          +motivo`.                                                      
      536 +  - **Teste:** `tests/test_secao9_aceite_envelope.py`         
      537 +  - **Commit:**                                               
      538 +                                                              
      539 +- [ ] **T-041** — Rastreabilidade: o teste exige `test_rnNNN_*
          +.py` de RN-001 a                                              
      540 +  RN-018; a tabela de Cobertura deste arquivo ganha RN-015 a R
          +N-018, AMB-018 a                                              
      541 +  AMB-036 e as tasks da Fase 7 nas linhas revistas. Fica por ú
          +ltimo porque só                                               
      542 +  passa quando RN-015 a RN-018 têm teste.                     
      543 +  - **Atende:** plan §6, D-002 (rastreabilidade)              
      544 +  - **Aceite:** a `spec.md` 2.0 tem RN-001 a RN-018 e todas tê
          +m arquivo de                                                  
      545 +    teste; remover `test_rn018_cambio.py` faz o teste falhar; 
          +toda RN e toda AMB                                            
      546 +    da spec aparecem na Cobertura com task e teste.           
      547 +  - **Teste:** `tests/test_rastreabilidade.py::test_rastreabil
          +idade_spec_tem_rn001_a_rn018`,                                
      548 +    `::test_rastreabilidade_toda_rn_tem_arquivo_de_teste`     
      549 +  - **Commit:**                                               
      550 +                                                              
      551  ---
      552  
      553  ## Cobertura

  Ran 1 shell command (ctrl+o to expand)

● Escrevi a Fase 7 em specs/001-motor-reembolso/tasks.md, com 16 tasks (T-026 a
  T-041). Não implementei código nem fiz commit. Cada task tem Atende, Aceite,
  Teste e o campo Commit vazio.

  Novas tasks

  7.1 — Modelo e documentos de entrada

  ┌───────┬─────────────────────────────────────────────┬───────────────────┐
  │ Task  │                  Conteúdo                   │ Principais itens  │
  │       │                                             │     atendidos     │
  ├───────┼─────────────────────────────────────────────┼───────────────────┤
  │ T-026 │ Motivo COTACAO_INDISPONIVEL e campos novos  │ §4, RN-018        │
  │       │ no modelo                                   │                   │
  ├───────┼─────────────────────────────────────────────┼───────────────────┤
  │ T-027 │ Leitura e validação de politica-v4.json     │ RN-015,           │
  │       │                                             │ AMB-031/034/036   │
  ├───────┼─────────────────────────────────────────────┼───────────────────┤
  │       │ Escolha da política pelo centro de custo,   │                   │
  │ T-028 │ volta para a padrão e herança de categorias │ RN-016,           │
  │       │  da padrão; centro_custo que não é texto    │ AMB-018–021       │
  │       │ vira erro geral                             │                   │
  ├───────┼─────────────────────────────────────────────┼───────────────────┤
  │ T-029 │ Leitura e validação opcional de cambio.json │ RN-018, AMB-032   │
  ├───────┼─────────────────────────────────────────────┼───────────────────┤
  │ T-030 │ Campo moeda (padrão BRL, normalização,      │ RN-017, AMB-024   │
  │       │ DADOS_INVALIDOS)                            │                   │
  └───────┴─────────────────────────────────────────────┴───────────────────┘

  7.2 — Regras com política externa e câmbio

  ┌───────┬───────────────────────────────────────────┬─────────────────────┐
  │ Task  │                 Conteúdo                  │  Principais itens   │
  │       │                                           │      atendidos      │
  ├───────┼───────────────────────────────────────────┼─────────────────────┤
  │       │ Motor e CLI passam a usar a política do   │ RN-015, RN-007,     │
  │ T-031 │ documento (--politica); saem as           │ RN-008              │
  │       │ constantes fixas                          │                     │
  ├───────┼───────────────────────────────────────────┼─────────────────────┤
  │ T-032 │ Categoria pela política aplicável e       │ RN-001, AMB-022/023 │
  │       │ limite zero como não reembolsável         │                     │
  ├───────┼───────────────────────────────────────────┼─────────────────────┤
  │       │ Limites pela tabela da política aplicável │                     │
  │ T-033 │  e justificativa citando a política de    │ RN-008–011, AMB-035 │
  │       │ origem                                    │                     │
  ├───────┼───────────────────────────────────────────┼─────────────────────┤
  │       │ Conversão pela data da despesa, uso da    │ RN-018, RN-003,     │
  │ T-034 │ última cotação anterior e                 │ AMB-025–027/029     │
  │       │ COTACAO_INDISPONIVEL                      │                     │
  ├───────┼───────────────────────────────────────────┼─────────────────────┤
  │ T-035 │ Nota fiscal comparada com o valor         │ RN-007, AMB-028     │
  │       │ convertido (só teste)                     │                     │
  ├───────┼───────────────────────────────────────────┼─────────────────────┤
  │ T-036 │ Duplicatas exigem mesma moeda e mesmo     │ RN-006, AMB-030     │
  │       │ valor original                            │                     │
  ├───────┼───────────────────────────────────────────┼─────────────────────┤
  │ T-037 │ Campos novos na saída (moeda,             │ §4, AMB-033         │
  │       │ taxa_cambio, data_cotacao)                │                     │
  └───────┴───────────────────────────────────────────┴─────────────────────┘

  7.3 — Integração, aceite e rastreabilidade

  ┌───────┬──────────────────────────────────────────────────────────────────┐
  │ Task  │                             Conteúdo                             │
  ├───────┼──────────────────────────────────────────────────────────────────┤
  │       │ CLI com --cambio e escolha da política pelo centro de custo;     │
  │ T-038 │ atualiza os testes da v3 afetados (§9 passa a 351,43, Exemplo 1  │
  │       │ da §4, linhas reescritas da §7) e o comando no README e no       │
  │       │ CLAUDE.md                                                        │
  ├───────┼──────────────────────────────────────────────────────────────────┤
  │ T-039 │ Casos novos da §7: a contagem vai de 37 para 68 (conferi na      │
  │       │ spec)                                                            │
  ├───────┼──────────────────────────────────────────────────────────────────┤
  │ T-040 │ Aceite dos dois arquivos do envelope (1.143,26 e 373,76),        │
  │       │ Exemplo 2, determinismo e descrição sem efeito no resultado      │
  ├───────┼──────────────────────────────────────────────────────────────────┤
  │ T-041 │ Rastreabilidade: teste cobrindo RN-001 a RN-018 e tabela de      │
  │       │ Cobertura atualizada                                             │
  └───────┴──────────────────────────────────────────────────────────────────┘

  A ordem foi pensada para os testes passarem a cada commit. Até a T-038, a CLI
  e os testes de exemplo usam a política padrão da v4, que tem os mesmos valores
  da v3. Os testes da v3 cujo resultado muda são atualizados no mesmo commit
  que liga a escolha por centro de custo.

  Pronta para revisão?

  Sim, tasks.md está pronta para revisão. Para implementar, ainda faltam duas 
  coisas:

  1. O plan.md está desatualizado. Ele ainda diz "plan 1.0, baseado na spec 1.1"
     e não trata a política em arquivo externo, o câmbio, os novos argumentos
     de CLI nem a nova etapa de conversão. Coloquei esse aviso no início da
     Fase 7. Os nomes de módulo, função e argumento (--politica, --cambio,
     cambio.py) são provisórios até a revisão do plan (docs(plan):). Também é o
     plan que deve definir o código de saída quando falta a política: 1 (erro
     geral) ou 2 (argumento inválido).
  2. Três pontos que a spec não define. Não decidi nenhum deles. As tasks evitam
     fixar o comportamento, mas T-028, T-032, T-033 e T-040 dependem deles:
     - Herança e justificativa: para CC-ADM com hospedagem (limite herdado da
       padrão), a justificativa cita "centro de custo CC-ADM" ou "política
       padrão"? A §4 fala da "política de onde o limite veio", e a RN-016 fala
       da "política usada".
     - Grafia do centro de custo na justificativa: com cc-comercial, ela mostra
       o código como veio na entrada ou a chave do documento de política?
     - periodicidade: "Dia" ou " dia " são aceitos depois de normalizar, ou só
       os valores exatos dia e diaria?

  Se você decidir esses três pontos, eles entram na spec e em DECISIONS.md antes
  da implementação.

✻ Brewed for 4m 16s · done 17:36

> Decido os três pontos assim:                                                  
                                                                                
  1. Quando um centro de custo herdar uma categoria da política padrão, a       
  justificativa deve deixar claros os dois fatos: o centro de custo processado  
  e que o limite veio da política padrão. Exemplo: "CC-ADM usando limite        
  herdado da política padrão".                                                  
  2. Quando o centro de custo informado corresponder a uma chave da política    
  após normalização, use nas justificativas a grafia canônica da chave do       
  arquivo de política. Exemplo: "cc-comercial" aparece como "CC-COMERCIAL".     
  3. O campo periodicidade deve ser normalizado antes da validação. Portanto    
  "Dia" e " dia " são aceitos como "dia", e o mesmo vale para "diaria". Depois  
  da normalização, qualquer outro valor é erro geral.                           
                                                                                
  Agora atualize SOMENTE:                                                       
  - spec.md                                                                     
  - DECISIONS.md                                                                
                                                                                
  Registre essas três decisões como complemento da v4/D-002.                    
                                                                                
  Não altere plan.md ainda.                                                     
  Não altere tasks.md.                                                          
  Não altere código.                                                            
  Não faça commit.                                                              
                                                                                
  No fim, diga resumidamente o que mudou.                                       

  Ran 1 shell command (ctrl+o to expand)

● Edito a spec: versão, §4, RN-002, RN-015, RN-016, novas AMB e casos da §7.

● Bash(cd "C:/Learning/AI/AnthropicAcademy/Desafio/sdd-desafio/specs/001-motor-r
      eembolso" && python - <<'EOF'
      from pathlib import Path…)
  ⎿  warning: in the working copy of 'specs/001-motor-reembolso/tasks.md',
     LF will be replaced by CRLF the next time Git touches it
      specs/001-motor-reembolso/spec.md  |  81 +++++++++--
     … +3 lines (ctrl+o to expand)
  ⎿  1 file changed (binary, mode only or too large to show)

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\DECISIONS.md)
  ⎿  Added 43 lines
      10  
      11  ---
      12  
      13 +## D-003 — Complemento da D-002: justificativa de herança, graf
         +ia do centro de custo e periodicidade · `2026-10-04`           
      14 +                                                               
      15 +**Gatilho:** ao escrever as tasks da Fase 7 (T-026 a T-041), o 
         +Claude apontou                                                 
      16 +três pontos que a spec 2.0 não decidia e dos quais dependem T-0
         +27, T-028, T-032,                                              
      17 +T-033 e T-040. As decisões abaixo são minhas e completam a v4/D
         +-002.                                                          
      18 +                                                               
      19 +**O que mudou na spec (2.0 → 2.1):**                           
      20 +- **RN-016:** a justificativa de categoria herdada da padrão ci
         +ta os dois fatos:                                              
      21 +  "centro de custo CC-ADM usando limite herdado da política pad
         +rão" (AMB-037).                                                
      22 +  Com o centro cadastrado, o código citado é a grafia da chave 
         +no documento de                                                
      23 +  política: `" cc-comercial "` aparece como `CC-COMERCIAL` (AMB
         +-038). A lista                                                 
      24 +  de textos de origem ficou explícita para cada caso.          
      25 +- **RN-002 e RN-015:** `periodicidade` passa pela normalização 
         +antes da                                                       
      26 +  validação; `"Dia"` e `" dia "` são `dia`, e o mesmo vale para
         + `diaria`.                                                     
      27 +  Depois da normalização, outro valor ou tipo diferente de text
         +o é erro geral                                                 
      28 +  (AMB-039).                                                   
      29 +- **Seção 4:** a justificativa de `LIMITE_DIARIO` inclui o caso
         + de limite                                                     
      30 +  herdado da padrão.                                           
      31 +- **Seção 6:** novas AMB-037, AMB-038 e AMB-039.               
      32 +- **Seção 7:** 3 casos novos (justificativa de herança, grafia 
         +do centro de                                                   
      33 +  custo, grafia da periodicidade); o caso "Categoria ausente na
         + tabela do                                                     
      34 +  centro" passa a conferir a justificativa. Total de 68 → 71 ca
         +sos.                                                           
      35 +                                                               
      36 +**Por quê:**                                                   
      37 +- Citar só o centro esconde que o limite veio da padrão; citar 
         +só a padrão                                                    
      38 +  sugere que o centro não foi reconhecido.                     
      39 +- A grafia do documento de política é a canônica, e a mesma ent
         +rada com grafias                                               
      40 +  diferentes deve gerar a mesma justificativa.                 
      41 +- Diferença de grafia não muda significado (mesmo raciocínio da
         + AMB-013 e da                                                  
      42 +  AMB-020).                                                    
      43 +                                                               
      44 +**O que isso invalidou:** nada implementado ainda. Os totais da
         + seção 9 não                                                   
      45 +mudam.                                                         
      46 +                                                               
      47 +**Tasks afetadas:** T-027 (periodicidade normalizada), T-028 (o
         +rigem com                                                      
      48 +herança e grafia canônica), T-032, T-033 e T-040 (texto das jus
         +tificativas),                                                  
      49 +T-039 (68 → 71 casos) e o cabeçalho da Fase 7 (spec 2.0 → 2.1).
         + `tasks.md`                                                    
      50 +ainda não foi ajustado.                                        
      51 +                                                               
      52 +**Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`), antes de qua
         +lquer código.                                                  
      53 +                                                               
      54 +---                                                            
      55 +                                                               
      56  ## D-002 — Política v4: política externa por centro de custo, r
          epresentação e câmbio · `2026-10-04`
      57  
      58  **Gatilho:** envelope lacrado do Dia 2 (Política de Reembolso v
          4), com

  Ran 1 shell command (ctrl+o to expand)

● Recontei: são 2 casos novos na §7 (o de herança foi ajustado, não
  acrescentado), então o total é 70. Corrijo o D-003.

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\DECISIONS.md)
  ⎿  Added 3 lines, removed 3 lines
      29  - **Seção 4:** a justificativa de `LIMITE_DIARIO` inclui o caso
           de limite
      30    herdado da padrão.
      31  - **Seção 6:** novas AMB-037, AMB-038 e AMB-039.
      32 -- **Seção 7:** 3 casos novos (justificativa de herança, grafia 
         -do centro de                                                   
      33 -  custo, grafia da periodicidade); o caso "Categoria ausente na
         - tabela do                                                     
      34 -  centro" passa a conferir a justificativa. Total de 68 → 71 ca
         -sos.                                                           
      32 +- **Seção 7:** 2 casos novos (grafia do centro de custo na just
         +ificativa,                                                     
      33 +  grafia da periodicidade); o caso "Categoria ausente na tabela
         + do centro"                                                    
      34 +  passa a conferir a justificativa de herança. Total de 68 → 70
         + casos.                                                        
      35  
      36  **Por quê:**
      37  - Citar só o centro esconde que o limite veio da padrão; citar 
          só a padrão

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\DECISIONS.md)
  ⎿  Added 1 line, removed 1 line
      46  
      47  **Tasks afetadas:** T-027 (periodicidade normalizada), T-028 (o
          rigem com
      48  herança e grafia canônica), T-032, T-033 e T-040 (texto das jus
          tificativas),
      49 -T-039 (68 → 71 casos) e o cabeçalho da Fase 7 (spec 2.0 → 2.1).
         - `tasks.md`                                                    
      49 +T-039 (68 → 70 casos) e o cabeçalho da Fase 7 (spec 2.0 → 2.1).
         + `tasks.md`                                                    
      50  ainda não foi ajustado.
      51  
      52  **Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`), antes de qua
          lquer código.

● Registrei as três decisões em spec.md e DECISIONS.md. A spec passou de 2.0
  para 2.1. Não mexi em plan.md, tasks.md nem no código, e não fiz commit.

  spec.md:
  - RN-016: cada caso agora tem o texto de origem que a justificativa cita:
    - centro de custo que tem a categoria → "centro de custo <código>";
    - categoria herdada → "centro de custo <código> usando limite herdado da
      política padrão";
    - centro sem cadastro → texto da 2.0 mantido;
    - sem centro de custo → "política padrão".

    Para centro cadastrado, o <código> é a grafia da chave no arquivo de
    política. Os novos critérios de aceite cobrem CC-ADM com hospedagem, CC-ADM
    com alimentação e " cc-comercial " → CC-COMERCIAL.
  - RN-002 e RN-015: periodicidade é normalizada antes da validação. "Dia", " 
    dia " e "DIARIA" são aceitos. Depois da normalização, qualquer outro valor é
    erro geral; um valor que não é texto também é.
  - §4: a justificativa de LIMITE_DIARIO agora prevê o caso de limite herdado.
  - §6: novas AMB-037 (justificativa de herança), AMB-038 (grafia do centro de
    custo) e AMB-039 (periodicidade).
  - §7: 2 casos novos (grafia do centro de custo e grafia da periodicidade). O
    caso de categoria herdada passa a conferir também a justificativa. A tabela
    vai de 68 para 70 casos.

  DECISIONS.md: nova entrada D-003, registrada como complemento da D-002 (spec
  2.0 → 2.1). Ela traz o gatilho, o que mudou, o porquê e as tasks afetadas. Os
  totais da §9 não mudam.

  tasks.md ficou desatualizada em alguns pontos:
  - o cabeçalho da Fase 7 ainda diz spec 2.0;
  - a T-039 ainda conta 68 casos;
  - os critérios de aceite de T-027, T-028, T-032, T-033 e T-040 ainda não citam
    essas decisões.

  Faço esses ajustes quando você liberar tasks.md.

  Ficou um ponto em aberto: para centro de custo sem cadastro, a spec não diz se
  o código aparece exatamente como veio ou já sem os espaços das pontas. Não há
  chave no arquivo de política para servir de grafia canônica.

✻ Crunched for 1m 22s · done 18:45

> Fecho o ponto restante assim:                                                 
                                                                                
  Para centro de custo sem cadastro, use na justificativa o valor normalizado   
  da entrada:                                                                   
   remove espaços das pontas;                                                   
   usa essa grafia normalizada na saída/justificativa.                          
                                                                                
  Exemplo:                                                                      
  " CC-SUPORTE-N2 " → "CC-SUPORTE-N2".                                          
                                                                                
  Agora atualize tasks.md com as decisões da D-003:                             
   cabeçalho da Fase 7 para spec 2.1;                                           
   T-027;                                                                       
   T-028;                                                                       
   T-032;                                                                       
   T-033;                                                                       
   T-039 de 68 para 70 casos;                                                   
   T-040.                                                                       
                                                                                
  Não implemente código.                                                        
  Não faça commit.                                                              
                                                                                
  No fim, mostre resumidamente o que mudou em tasks.md                          

● Antes de mexer: a regra nova (grafia de centro de custo sem cadastro) não está
  na spec nem na D-003. Pelo CLAUDE.md, ela precisa entrar primeiro na spec e
  no DECISIONS.md. Por isso, agora atualizo tasks.md só com o que já está na
  D-003 e explico o ponto no final.

  Ran 2 shell commands (ctrl+o to expand)

● O script falhou antes de escrever nada, então faço as mesmas alterações com o
  Edit.

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 2 lines, removed 2 lines
      270  
      271  ## Fase 7 — Envelope (Dia 2)
      272  
      273 -**Baseado em:** spec 2.0 (D-002) · plan 1.0, **a atualizar par
          -a a spec 2.0 antes                                            
      274 -da T-026** (`docs(plan):`). Nomes de módulo, função e argument
          -o de CLI citados                                              
      273 +**Baseado em:** spec 2.1 (D-002, D-003) · plan 1.0, **a atuali
          +zar para a spec                                               
      274 +2.1 antes da T-026** (`docs(plan):`). Nomes de módulo, função 
          +e argumento de CLI citados                                    
      275  abaixo seguem a arquitetura do plan 1.0 e são provisórios até 
           essa revisão.
      276  
      277  Sequência pensada para a suíte ficar verde em todo commit:

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 6 lines, removed 4 lines
      305  
      306  - [ ] **T-027** — Leitura e validação do documento de política
            (`politica.py`
      307    passa a ler `politica-v4.json` e devolver um objeto `Politic
           a`). Chaves de
      308 -  categoria e de centro de custo normalizadas pela RN-002; `mo
          -eda_base`                                                     
      309 -  normalizada pela RN-017. Erro → `EntradaInvalida`. Ainda não
          - é usado pelo motor.                                          
      310 -  - **Atende:** RN-015, RN-002 (chaves do documento), RN-013 (
          -erro geral),                                                  
      311 -    AMB-031, AMB-034, AMB-036                                 
      308 +  categoria e de centro de custo e o valor de `periodicidade` 
          +normalizados pela                                             
      309 +  RN-002; `moeda_base` normalizada pela RN-017. A grafia origi
          +nal de cada chave                                             
      310 +  de centro de custo é guardada para as justificativas (AMB-03
          +8). Erro →                                                    
      311 +  `EntradaInvalida`. Ainda não é usado pelo motor.            
      312 +  - **Atende:** RN-015, RN-002 (chaves e periodicidade do docu
          +mento), RN-013                                                
      313 +    (erro geral), AMB-031, AMB-034, AMB-036, AMB-038, AMB-039 
      314    - **Aceite:** `politica-v4.json` → aceito, com `padrao` e tr
           ês centros.
      315      Erro geral para: JSON ilegível, `NaN`, `Infinity`; sem `pa
           drao`, sem
      316      `centros_custo`, sem `moeda_base` ou sem `nota_fiscal_obri
           gatoria_acima_de`;

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 6 lines, removed 3 lines
      316      `centros_custo`, sem `moeda_base` ou sem `nota_fiscal_obri
           gatoria_acima_de`;
      317      `padrao` que não é objeto; entrada de categoria que não é 
           objeto; limite
      318      `-1`, `"60"` ou `true`; limiar negativo ou não numérico; `
           moeda_base` `USD`;
      319 -    `"periodicidade": "mes"` ou ausente; `Alimentação` e `alim
          -entacao` na mesma                                             
      320 -    tabela; `CC-ADM` e ` cc-adm ` em `centros_custo`. Sem erro
          -: `moeda_base`                                                
      321 -    `" brl "`; `centros_custo: {}`; limite `0`; `"acrescimo_em
          -_viagem_percentual": "x"`,                                    
      319 +    `"periodicidade": "mes"`, `1` ou ausente; `Alimentação` e 
          +`alimentacao` na                                              
      320 +    mesma tabela; `CC-ADM` e ` cc-adm ` em `centros_custo`. Se
          +m erro:                                                       
      321 +    `moeda_base` `" brl "`; `centros_custo: {}`; limite `0`;  
      322 +    `"periodicidade": "Dia"` e `" dia "` → `dia`; `"DIARIA"` →
          + `diaria`; a chave                                            
      323 +    `CC-COMERCIAL` mantém essa grafia para as justificativas; 
      324 +    `"acrescimo_em_viagem_percentual": "x"`,                  
      325      `versao`, `vigencia` e `observacao` com qualquer valor.
      326    - **Teste:** `tests/test_rn015_politica.py`
      327    - **Commit:**

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 4 lines, removed 2 lines
      330    `colaborador.centro_custo` e devolve a tabela efetiva (centr
           o sobre a padrão,
      331    herança por categoria) e a origem a citar nas justificativas
           . Na validação do
      332    documento de despesas, `centro_custo` presente e não texto v
           ira erro geral.
      333 -  Ainda não é usada pelo motor.                               
      333 +  A origem é por categoria (centro, padrão, herdada da padrão 
          +ou centro sem                                                 
      334 +  cadastro); com o centro cadastrado, o código sai na grafia d
          +a chave do                                                    
      335 +  documento de política. Ainda não é usada pelo motor.        
      336    - **Atende:** RN-016, RN-002 (centro de custo), RN-013 (erro
            geral do centro de
      335 -    custo), AMB-018, AMB-019, AMB-020, AMB-021                
      337 +    custo), AMB-018, AMB-019, AMB-020, AMB-021, AMB-037, AMB-0
          +38                                                            
      338    - **Aceite:** sem `centro_custo` ou `"  "` → padrão, origem 
           "política padrão";
      339      `CC-COMERCIAL` e ` cc-comercial ` → tabela do `CC-COMERCIA
           L`, origem
      340      "centro de custo `CC-COMERCIAL`"; `CC-SUPORTE-N2` → padrão
           , origem "política

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)  ⎿  Added 7 lines, removed 4 lines
      336    - **Atende:** RN-016, RN-002 (centro de custo), RN-013 (erro
            geral do centro de
      337      custo), AMB-018, AMB-019, AMB-020, AMB-021, AMB-037, AMB-0
           38
      338    - **Aceite:** sem `centro_custo` ou `"  "` → padrão, origem 
           "política padrão";
      339 -    `CC-COMERCIAL` e ` cc-comercial ` → tabela do `CC-COMERCIA
          -L`, origem                                                    
      340 -    "centro de custo `CC-COMERCIAL`"; `CC-SUPORTE-N2` → padrão
          -, origem "política                                            
      341 -    padrão; centro de custo `CC-SUPORTE-N2` não cadastrado"; `
          -CC-ADM` →                                                     
      342 -    `hospedagem` 250,00 herdada da padrão e `alimentacao` 45,0
          -0 do centro;                                                  
      339 +    `CC-COMERCIAL`, ` cc-comercial ` e `Cc-Comercial` → tabela
          + do                                                           
      340 +    `CC-COMERCIAL`, origem "centro de custo CC-COMERCIAL" (gra
          +fia do documento                                              
      341 +    de política); `CC-SUPORTE-N2` → padrão, origem "política p
          +adrão; centro de                                              
      342 +    custo CC-SUPORTE-N2 não cadastrado"; `CC-ADM` → `hospedage
          +m` 250,00 herdada                                             
      343 +    da padrão, origem "centro de custo CC-ADM usando limite he
          +rdado da política                                             
      344 +    padrão", e `alimentacao` 45,00, origem "centro de custo CC
          +-ADM"; `CC-ADM` →                                             
      345 +    `representacao`, ausente do centro e da padrão, origem "ce
          +ntro de custo CC-ADM";                                        
      346      `CC-ENG-PLATAFORMA` → `hospedagem` 0,00 (não herda, porque
            consta);
      347      `CC-COMERCIAL` → `representacao` 300,00; padrão → sem `rep
           resentacao`;
      348      `"centro_custo": 42` → `EntradaInvalida`.

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 2 lines, removed 2 lines
      402  - [ ] **T-032** — Etapa de categoria pela política aplicável: 
           reembolsável só se
      403    consta da tabela efetiva com limite maior que zero; limite 0
           ,00 →
      404    `CATEGORIA_NAO_REEMBOLSAVEL`; `observacao` ignorada. A justi
           ficativa cita a
      405 -  política aplicada (origem da T-028). Revisa a T-012.        
      405 +  origem da categoria (T-028). Revisa a T-012.                
      406    - **Atende:** RN-001, RN-016, spec §4 (justificativa de cate
           goria), AMB-014,
      407 -    AMB-021, AMB-022, AMB-023                                 
      407 +    AMB-021, AMB-022, AMB-023, AMB-037, AMB-038               
      408    - **Aceite:** d-005 (`coworking`) → recusado, `CATEGORIA_NAO
           _REEMBOLSAVEL`.
      409      `CC-ENG-PLATAFORMA`: d-010 (hospedagem) → recusado, `CATEG
           ORIA_NAO_REEMBOLSAVEL`;
      410      d-013 (hospedagem, 690,00, sem nota) → `CATEGORIA_NAO_REEM
           BOLSAVEL`, e não

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 6 lines, removed 1 line
      411      `NOTA_FISCAL_AUSENTE`. Padrão: f-003 (`representacao`) → r
           ecusado.
      412      `CC-COMERCIAL`: e-001 (`representacao`) → passa. `CC-ADM`:
            hospedagem →
      413      passa (herança). Limite 0 em qualquer categoria de qualque
           r tabela → recusado.
      414 -    A justificativa cita a RN-001 e a origem da política.     
      414 +    A justificativa cita a RN-001 e a origem: d-010 → "centro 
          +de custo                                                      
      415 +    CC-ENG-PLATAFORMA"; ` cc-eng-plataforma ` → "centro de cus
          +to                                                            
      416 +    CC-ENG-PLATAFORMA"; f-003 → "política padrão; centro de cu
          +sto CC-SUPORTE-N2                                             
      417 +    não cadastrado"; `CC-ADM` com `representacao` → "centro de
          + custo CC-ADM";                                               
      418 +    política com `hospedagem` 0 na padrão e `CC-ADM` → "centro
          + de custo CC-ADM                                              
      419 +    usando limite herdado da política padrão".                
      420    - **Teste:** `tests/test_rn001_categoria.py`
      421    - **Commit:**
      422  

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 1 line, removed 1 line
      425    `LIMITE_DIARIO` citando a origem do limite. O acréscimo em v
           iagem do documento
      426    não é aplicado. Revisa a T-015 e a T-016.
      427    - **Atende:** RN-008, RN-009, RN-010, RN-011, RN-016, spec §
           4 (justificativa
      428 -    de limite), AMB-008, AMB-021, AMB-023, AMB-035, AMB-036   
      428 +    de limite), AMB-008, AMB-021, AMB-023, AMB-035, AMB-036, A
          +MB-037, AMB-038                                               
      429    - **Aceite:** `CC-COMERCIAL`: e-007 (hospedagem, 1.200,00, "
           3 noites") →
      430      400,00, `limitado`; e-001 (`representacao`, 340,00) → 300,
           00, `limitado`;
      431      e-008 (alimentação, 95,00) → 90,00, `limitado`; alimentaçã
           o e representação

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 5 lines, removed 1 line
      433      `limitado`. `CC-ENG-PLATAFORMA`: d-001 + d-002 → 72,50 + 2
           ,50. Padrão:
      434      f-002 (310,00) → 250,00. `acrescimo_em_viagem_percentual` 
           50 → nenhum limite
      435      acima da tabela. A justificativa cita o limite, o valor co
           nsumido, os `id`
      436 -    que consumiram e a origem.                                
      436 +    que consumiram e a origem: `CC-ADM` com hospedagem 300,00 
          +→ "centro de custo                                            
      437 +    CC-ADM usando limite herdado da política padrão"; `CC-ADM`
          + com alimentação                                              
      438 +    acima de 45,00 → "centro de custo CC-ADM"; ` cc-comercial 
          +` com alimentação                                             
      439 +    de 95,00 → 90,00, `limitado`, citando "centro de custo CC-
          +COMERCIAL"; f-002                                             
      440 +    → "política padrão; centro de custo CC-SUPORTE-N2 não cada
          +strado".                                                      
      441    - **Teste:** `tests/test_rn008_limites.py`, `tests/test_rn00
           9_distribuicao.py`,
      442      `tests/test_rn010_parcial.py`, `tests/test_rn011_viagem.py
           `
      443    - **Commit:**

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 7 lines, removed 5 lines
      531      `::test_rn018_moedas_base_divergentes_e_erro_geral`
      532    - **Commit:**
      533  
      534 -- [ ] **T-039** — Casos novos da §7 da spec 2.0 na tabela para
          -metrizada, com o                                              
      534 +- [ ] **T-039** — Casos novos da §7 da spec 2.1 na tabela para
          +metrizada, com o                                              
      535    nome do caso como `id` (`test(T-039)`).
      536    - **Atende:** spec §7 (casos de RN-001, RN-006, RN-007, RN-0
           13, RN-015 a
      537 -    RN-018 e seção 8 incluídos na spec 2.0)                   
      538 -  - **Aceite:** os 68 casos da §7 passam e aparecem no relatór
          -io do pytest com o                                            
      539 -    nome da spec; o teste de contagem passa de 37 para 68.    
      537 +    RN-018 e seção 8 incluídos nas specs 2.0 e 2.1), AMB-037, 
          +AMB-038, AMB-039                                              
      538 +  - **Aceite:** os 70 casos da §7 passam e aparecem no relatór
          +io do pytest com o                                            
      539 +    nome da spec; o teste de contagem passa de 37 para 70. Inc
          +lui "Grafia do                                                
      540 +    centro de custo na justificativa", "Periodicidade com graf
          +ia diferente" e a                                             
      541 +    justificativa de herança em "Categoria ausente na tabela d
          +o centro".                                                    
      542    - **Teste:** `tests/test_secao7_casos_de_borda.py::test_seca
           o7_caso_de_borda`,
      541 -    `::test_secao7_tem_68_casos`                              
      543 +    `::test_secao7_tem_70_casos`                              
      544    - **Commit:**
      545  
      546  - [ ] **T-040** — Aceite dos dois documentos do envelope pela 
           CLI, com

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 2 lines, removed 1 line
      545  
      546  - [ ] **T-040** — Aceite dos dois documentos do envelope pela 
           CLI, com
      547    `politica-v4.json` e `cambio.json` (`test(T-040)`).
      548 -  - **Atende:** spec §9 (envelope), spec §4 (Exemplo 2), RN-01
          -4, RN-016, AMB-019                                            
      548 +  - **Atende:** spec §9 (envelope), spec §4 (Exemplo 2), RN-01
          +4, RN-016,                                                    
      549 +    AMB-019, AMB-038                                          
      550    - **Aceite:** `despesas-envelope.json` → as 10 linhas da §9
      551      (`valor_considerado`, `valor_reembolsavel`, `status`, `mot
           ivo`) e total
      552      1.143,26; e-002 com exatamente a justificativa do Exemplo 
           2 da §4.

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 4 lines, removed 1 line
      549      AMB-019, AMB-038
      550    - **Aceite:** `despesas-envelope.json` → as 10 linhas da §9
      551      (`valor_considerado`, `valor_reembolsavel`, `status`, `mot
           ivo`) e total
      552 -    1.143,26; e-002 com exatamente a justificativa do Exemplo 
          -2 da §4.                                                      
      552 +    1.143,26; e-002 com exatamente a justificativa do Exemplo 
          +2 da §4; as                                                   
      553 +    justificativas de `LIMITE_DIARIO` e `CATEGORIA_NAO_REEMBOL
          +SAVEL` citam                                                  
      554 +    "centro de custo CC-COMERCIAL", sem herança (todas as cate
          +gorias reembolsadas                                           
      555 +    do documento constam do centro).                          
      556      `despesas-envelope-cc-desconhecido.json` → as 4 linhas e t
           otal 373,76; as
      557      justificativas de f-002 e f-003 citam "política padrão; ce
           ntro de custo
      558      `CC-SUPORTE-N2` não cadastrado". Nos dois: um item por des
           pesa, na ordem;

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 1 line, removed 1 line
      555      do documento constam do centro).
      556      `despesas-envelope-cc-desconhecido.json` → as 4 linhas e t
           otal 373,76; as
      557      justificativas de f-002 e f-003 citam "política padrão; ce
           ntro de custo
      558 -    `CC-SUPORTE-N2` não cadastrado". Nos dois: um item por des
          -pesa, na ordem;                                               
      558 +    CC-SUPORTE-N2 não cadastrado". Nos dois: um item por despe
          +sa, na ordem;                                                 
      559      todo item cita `RN-\d{3}`; duas execuções idênticas byte a
            byte; trocar as
      560      descrições não altera `valor_reembolsavel`, `status` nem `
           motivo`.
      561    - **Teste:** `tests/test_secao9_aceite_envelope.py`

● Atualizei tasks.md com as decisões da D-003. Não mexi em código nem fiz
  commit.

  O que mudou em tasks.md:
  - Cabeçalho da Fase 7: agora diz spec 2.1 (D-002, D-003) e plan a atualizar
    para a 2.1.
  - T-027: periodicidade é normalizada antes da validação. "Dia" e " dia " viram
    dia, "DIARIA" vira diaria, e 1 é erro. A grafia original das chaves de
    centro de custo fica guardada para as justificativas. Entram AMB-038 e
    AMB-039.
  - T-028: a origem é calculada por categoria. Os critérios de aceite agora têm
    os textos exatos dos casos CC-ADM, " cc-comercial " e Cc-Comercial (os dois
    últimos aparecem como CC-COMERCIAL). Entram AMB-037 e AMB-038.
  - T-032: a justificativa de categoria passa a ter texto exato por caso: d-010,
    " cc-eng-plataforma ", f-003, representação no CC-ADM e limite zero herdado
    da padrão.
  - T-033: a justificativa de limite passa a ter texto exato para hospedagem e
    alimentação no CC-ADM, alimentação de 95,00 em " cc-comercial " e f-002.
  - T-039: de 68 para 70 casos, com o teste test_secao7_tem_70_casos. Lista os
    dois casos novos e a justificativa de herança.
  - T-040: o envelope CC-COMERCIAL cita "centro de custo CC-COMERCIAL", sem
    herança. Os códigos de f-002 e f-003 deixam de aparecer entre crases.

  A regra nova para centro de custo sem cadastro ainda não entrou em tasks.md.
  Pelo CLAUDE.md, ela precisa ir antes para a spec e para o DECISIONS.md. Há
  também um conflito de termo a resolver nesse registro:
  - Na spec, "normalizado" é a normalização da RN-002: tira os espaços das
    pontas, passa para minúsculas e tira acentos. Por ela, " CC-SUPORTE-N2 "
    viraria cc-suporte-n2.
  - O seu exemplo mantém as maiúsculas (CC-SUPORTE-N2). Então a regra que você
    quer é só tirar os espaços das pontas, sem a normalização completa da
    RN-002.

  Se confirmar, registro assim na RN-016 (com uma AMB-040, um caso na §7 e um
  complemento à D-003). Depois atualizo T-028, T-032, T-033 e a contagem da
  T-039, que vai para 71.

✻ Brewed for 1m 36s · done 18:49

> atualizar spec.md;                                                            
  atualizar DECISIONS.md;                                                       
  registrar essa decisão nova;                                                  
  provavelmente criar AMB-040;                                                  
  ajustar a contagem da seção 7;                                                
  sem código;                                                                   
  sem commit.                                                                   
  Confirmo, só remove espaços das pontas; registre na spec e DECISIONS          

  Searched for 1 pattern (ctrl+o to expand)

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\spec.md)
  ⎿  Added 5 lines, removed 2 lines
      460  - caso 3: "política padrão; centro de custo `<código>` não cad
           astrado".
      461  
      462  No caso 2, `<código>` é a chave do centro de custo **como está
            escrita no
      463 -documento de política**, e não como veio no documento de despe
          -sas.                                                          
      464 -**Origem:** política v4 (AMB-018, AMB-019, AMB-020, AMB-021, A
          -MB-037, AMB-038)                                              
      463 +documento de política**, e não como veio no documento de despe
          +sas. No caso 3,                                               
      464 +como não há chave, `<código>` é o valor do documento de despes
          +as apenas sem os                                              
      465 +espaços do início e do fim; maiúsculas, minúsculas e acentos s
          +ão mantidos                                                   
      466 +(não é a normalização da RN-002).                             
      467 +**Origem:** política v4 (AMB-018, AMB-019, AMB-020, AMB-021, A
          +MB-037, AMB-038, AMB-040)                                     
      468  **Aceite:** `exemplos/despesas-exemplo.json` (`CC-ENG-PLATAFOR
           MA`) → limite de
      469  alimentação de 75,00. `despesas-envelope-cc-desconhecido.json`
            (`CC-SUPORTE-N2`)
      470  → política padrão; f-002 (hospedagem, 310,00) → 250,00. Docume
           nto sem

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\spec.md)
  ⎿  Added 15 lines
      978  grafia não muda o significado, e as chaves do documento já são
            normalizadas.
      979  **Regra afetada:** RN-002, RN-015
      980  
      981 +### AMB-040 — Grafia do centro de custo não cadastrado na just
          +ificativa                                                     
      982 +                                                              
      983 +**Texto original da política v4:** a política não menciona o c
          +aso.                                                          
      984 +**O que não está claro:** com centro de custo não cadastrado n
          +ão há chave no                                                
      985 +documento de política para dar a grafia canônica (AMB-038). Fi
          +ca a dúvida entre                                             
      986 +citar o valor exatamente como veio, sem os espaços das pontas 
          +ou normalizado                                                
      987 +pela RN-002.                                                  
      988 +**Decisão:** remove só os espaços do início e do fim e mantém 
          +o resto como veio:                                            
      989 +`" CC-SUPORTE-N2 "` → `CC-SUPORTE-N2`. Maiúsculas, minúsculas 
          +e acentos não são                                             
      990 +alterados.                                                    
      991 +**Justificativa:** espaços nas pontas são ruído sem significad
          +o; manter o resto                                             
      992 +como veio deixa reconhecível o código digitado e ajuda a achar
          + o erro de                                                    
      993 +digitação que levou à política padrão (AMB-019).              
      994 +**Regra afetada:** RN-016                                     
      995 +                                                              
      996  ---
      997  
      998  ## 7. Casos de borda

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\spec.md)
  ⎿  Added 1 line
      1039  | Lista de despesas vazia | `despesas: []` | saída com `itens
            ` vazio e total 0,00 | RN-013 |
      1040  | Centro de custo ausente | documento sem `colaborador.centro
            _custo` | política padrão | RN-016 |
      1041  | Centro de custo desconhecido | `CC-SUPORTE-N2` | política p
            adrão; justificativa cita que não está cadastrado | RN-016 |
      1042 +| Centro de custo desconhecido com espaços nas pontas | `" CC
           +-Suporte-N2 "` | política padrão; justificativa cita "centro 
           +de custo CC-Suporte-N2 não cadastrado" | RN-016 |            
      1043  | Centro de custo com grafia diferente | ` cc-comercial ` | t
            ratado como `CC-COMERCIAL` | RN-002, RN-016 |
      1044  | Centro de custo com tipo errado | `centro_custo`: 42 | erro
            , sem saída | RN-013, RN-016 |
      1045  | Categoria ausente na tabela do centro | `CC-ADM`, hospedage
            m de 300,00 | herda 250,00 da padrão; 250,00, `limitado`; jus
            tificativa cita "centro de custo CC-ADM usando limite herdado
             da política padrão" | RN-016 |

● Acrescento um exemplo nos critérios de aceite da RN-016 e atualizo a D-003.

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\spec.md)
  ⎿  Added 2 lines
      473  "centro de custo CC-ADM usando limite herdado da política padr
           ão". `CC-ADM` com
      474  alimentação acima do limite → justificativa citando "centro de
            custo CC-ADM".
      475  `" cc-comercial "` → justificativas citando "centro de custo C
           C-COMERCIAL".
      476 +`" CC-SUPORTE-N2 "` → política padrão; justificativas citando 
          +"política padrão;                                             
      477 +centro de custo CC-SUPORTE-N2 não cadastrado".                
      478  `"centro_custo": 42` → erro, sem saída.
      479  
      480  ### RN-017 — Moeda da despesa

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\DECISIONS.md)
  ⎿  Error editing file

  Read 1 file (ctrl+o to expand)

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\DECISIONS.md)
  ⎿  Added 3 lines, removed 1 line
      14  
      15  **Gatilho:** ao escrever as tasks da Fase 7 (T-026 a T-041), o 
          Claude apontou
      16  três pontos que a spec 2.0 não decidia e dos quais dependem T-0
          27, T-028, T-032,
      17 -T-033 e T-040. As decisões abaixo são minhas e completam a v4/D
         --002.                                                          
      17 +T-033 e T-040. Ao ajustar as tasks, apontou um quarto ponto: a 
         +grafia do                                                      
      18 +centro de custo não cadastrado na justificativa. As decisões ab
         +aixo são minhas e                                              
      19 +completam a v4/D-002.                                          
      20  
      21  **O que mudou na spec (2.0 → 2.1):**
      22  - **RN-016:** a justificativa de categoria herdada da padrão ci
          ta os dois fatos:

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\DECISIONS.md)
  ⎿  Added 5 lines, removed 2 lines
      22  - **RN-016:** a justificativa de categoria herdada da padrão ci
          ta os dois fatos:
      23    "centro de custo CC-ADM usando limite herdado da política pad
          rão" (AMB-037).
      24    Com o centro cadastrado, o código citado é a grafia da chave 
          no documento de
      25 -  política: `" cc-comercial "` aparece como `CC-COMERCIAL` (AMB
         --038). A lista                                                 
      26 -  de textos de origem ficou explícita para cada caso.          
      25 +  política: `" cc-comercial "` aparece como `CC-COMERCIAL` (AMB
         +-038). Com o                                                   
      26 +  centro não cadastrado, sem chave no documento, o código citad
         +o é o valor da                                                 
      27 +  entrada só sem os espaços das pontas, mantendo maiúsculas, mi
         +núsculas e                                                     
      28 +  acentos: `" CC-SUPORTE-N2 "` → `CC-SUPORTE-N2`. Não é a norma
         +lização da RN-002                                              
      29 +  (AMB-040). A lista de textos de origem ficou explícita para c
         +ada caso.                                                      
      30  - **RN-002 e RN-015:** `periodicidade` passa pela normalização 
          antes da
      31    validação; `"Dia"` e `" dia "` são `dia`, e o mesmo vale para
           `diaria`.
      32    Depois da normalização, outro valor ou tipo diferente de text
          o é erro geral

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\DECISIONS.md)
  ⎿  Added 5 lines, removed 4 lines
      33    (AMB-039).
      34  - **Seção 4:** a justificativa de `LIMITE_DIARIO` inclui o caso
           de limite
      35    herdado da padrão.
      36 -- **Seção 6:** novas AMB-037, AMB-038 e AMB-039.               
      37 -- **Seção 7:** 2 casos novos (grafia do centro de custo na just
         -ificativa,                                                     
      38 -  grafia da periodicidade); o caso "Categoria ausente na tabela
         - do centro"                                                    
      39 -  passa a conferir a justificativa de herança. Total de 68 → 70
         - casos.                                                        
      36 +- **Seção 6:** novas AMB-037, AMB-038, AMB-039 e AMB-040.      
      37 +- **Seção 7:** 3 casos novos (grafia do centro de custo na just
         +ificativa,                                                     
      38 +  grafia da periodicidade, centro de custo desconhecido com esp
         +aços nas                                                       
      39 +  pontas); o caso "Categoria ausente na tabela do centro" passa
         + a conferir a                                                  
      40 +  justificativa de herança. Total de 68 → 71 casos.            
      41  
      42  **Por quê:**
      43  - Citar só o centro esconde que o limite veio da padrão; citar 
          só a padrão

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\DECISIONS.md)  ⎿  Added 5 lines, removed 2 lines
      46    diferentes deve gerar a mesma justificativa.
      47  - Diferença de grafia não muda significado (mesmo raciocínio da
           AMB-013 e da
      48    AMB-020).
      49 +- Sem chave canônica, manter o código como foi digitado (só sem
         + espaços nas                                                   
      50 +  pontas) ajuda a achar o erro de digitação que levou à polític
         +a padrão.                                                      
      51  
      52  **O que isso invalidou:** nada implementado ainda. Os totais da
           seção 9 não
      53  mudam.
      54  
      55  **Tasks afetadas:** T-027 (periodicidade normalizada), T-028 (o
          rigem com
      56  herança e grafia canônica), T-032, T-033 e T-040 (texto das jus
          tificativas),
      55 -T-039 (68 → 70 casos) e o cabeçalho da Fase 7 (spec 2.0 → 2.1).
         - `tasks.md`                                                    
      56 -ainda não foi ajustado.                                        
      57 +T-039 e o cabeçalho da Fase 7 (spec 2.0 → 2.1). `tasks.md` já r
         +eflete os três                                                 
      58 +primeiros pontos. Falta a AMB-040 em T-028, T-032 e T-033, e a 
         +T-039 passa de                                                 
      59 +70 para 71 casos.                                              
      60  
      61  **Custo:** 2 arquivos (`spec.md`, `DECISIONS.md`), antes de qua
          lquer código.
      62  

  Ran 2 shell commands (ctrl+o to expand)

● Registrei a decisão na spec e na D-003. Não mexi em tasks.md nem no código, e
  não fiz commit.

  spec.md:
  - RN-016: para centro de custo sem cadastro, a justificativa cita o valor da
    entrada só sem os espaços das pontas. Maiúsculas, minúsculas e acentos ficam
    como vieram, e a regra deixa claro que isso não é a normalização da RN-002.
    Novo critério de aceite: " CC-SUPORTE-N2 " → "política padrão; centro de
    custo CC-SUPORTE-N2 não cadastrado".
  - §6: nova AMB-040 (grafia do centro de custo sem cadastro na justificativa).
  - §7: novo caso "Centro de custo desconhecido com espaços nas pontas": " 
    CC-Suporte-N2 " sai como CC-Suporte-N2, o que confirma que as maiúsculas e
    minúsculas ficam como vieram. A tabela passa de 70 para 71 casos; recontei
    no arquivo.

  DECISIONS.md: registrei como complemento da D-003, sem criar uma entrada nova.
  Como nada disso foi commitado, a spec continua na 2.1 e o cabeçalho da Fase 7
  em tasks.md continua certo. Na D-003, atualizei o gatilho (quarto ponto), a
  RN-016, a §6 (AMB-040), a §7 (68 → 71), o porquê e as tasks afetadas.

  tasks.md ainda não traz essa decisão. Faltam a AMB-040 e os critérios de
  aceite com espaços nas pontas em T-028, T-032 e T-033, e a T-039 precisa
  passar de 70 para 71 casos. Atualizo quando você pedir.

✻ Baked for 1m 3s · done 18:54

> agora                                                                         
  Atualize SOMENTE o tasks.md para refletir a AMB-040 e a decisão registrada na 
  D-003                                                                         
                                                                                
  Ajuste:                                                                       
   T-028, T-032, - T-033,T-039 passando de 70 para 71 casos.                    
                                                                                
  Inclua nos critérios de aceite o comportamento:                               
  " CC-Suporte-N2 " -> justificativa com "CC-Suporte-N2", removendo apenas      
  espaços das pontas e preservando maiúsculas/minúsculas.                       
                                                                                
  Não altere spec.md                                                            
  Não altere DECISIONS.md                                                       
  Não altere plan.md                                                            
  Não mexa em código                                                            
  Não faça commit                                                               
                                                                                
  No fim, diga de forma reduzida o que mudou                                    

  Searched for 1 pattern, read 1 file (ctrl+o to expand)

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 4 lines, removed 3 lines
      331    herança por categoria) e a origem a citar nas justificativas
           . Na validação do
      332    documento de despesas, `centro_custo` presente e não texto v
           ira erro geral.
      333    A origem é por categoria (centro, padrão, herdada da padrão 
           ou centro sem
      334 -  cadastro); com o centro cadastrado, o código sai na grafia d
          -a chave do                                                    
      335 -  documento de política. Ainda não é usada pelo motor.        
      334 +  cadastro). Com o centro cadastrado, o código sai na grafia d
          +a chave do                                                    
      335 +  documento de política. Sem cadastro, sai o valor da entrada 
          +só sem os espaços                                             
      336 +  das pontas, sem a normalização da RN-002. Ainda não é usada 
          +pelo motor.                                                   
      337    - **Atende:** RN-016, RN-002 (centro de custo), RN-013 (erro
            geral do centro de
      337 -    custo), AMB-018, AMB-019, AMB-020, AMB-021, AMB-037, AMB-0
          -38                                                            
      338 +    custo), AMB-018, AMB-019, AMB-020, AMB-021, AMB-037, AMB-0
          +38, AMB-040                                                   
      339    - **Aceite:** sem `centro_custo` ou `"  "` → padrão, origem 
           "política padrão";
      340      `CC-COMERCIAL`, ` cc-comercial ` e `Cc-Comercial` → tabela
            do
      341      `CC-COMERCIAL`, origem "centro de custo CC-COMERCIAL" (gra
           fia do documento

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 4 lines, removed 1 line
      340      `CC-COMERCIAL`, ` cc-comercial ` e `Cc-Comercial` → tabela
            do
      341      `CC-COMERCIAL`, origem "centro de custo CC-COMERCIAL" (gra
           fia do documento
      342      de política); `CC-SUPORTE-N2` → padrão, origem "política p
           adrão; centro de
      343 -    custo CC-SUPORTE-N2 não cadastrado"; `CC-ADM` → `hospedage
          -m` 250,00 herdada                                             
      343 +    custo CC-SUPORTE-N2 não cadastrado"; `" CC-Suporte-N2 "` →
          + padrão, origem                                               
      344 +    "política padrão; centro de custo CC-Suporte-N2 não cadast
          +rado" (só as pontas                                           
      345 +    removidas, maiúsculas e minúsculas preservadas, e não `cc-
          +suporte-n2`);                                                 
      346 +    `CC-ADM` → `hospedagem` 250,00 herdada                    
      347      da padrão, origem "centro de custo CC-ADM usando limite he
           rdado da política
      348      padrão", e `alimentacao` 45,00, origem "centro de custo CC
           -ADM"; `CC-ADM` →
      349      `representacao`, ausente do centro e da padrão, origem "ce
           ntro de custo CC-ADM";

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 1 line, removed 1 line
      408    `CATEGORIA_NAO_REEMBOLSAVEL`; `observacao` ignorada. A justi
           ficativa cita a
      409    origem da categoria (T-028). Revisa a T-012.
      410    - **Atende:** RN-001, RN-016, spec §4 (justificativa de cate
           goria), AMB-014,
      411 -    AMB-021, AMB-022, AMB-023, AMB-037, AMB-038               
      411 +    AMB-021, AMB-022, AMB-023, AMB-037, AMB-038, AMB-040      
      412    - **Aceite:** d-005 (`coworking`) → recusado, `CATEGORIA_NAO
           _REEMBOLSAVEL`.
      413      `CC-ENG-PLATAFORMA`: d-010 (hospedagem) → recusado, `CATEG
           ORIA_NAO_REEMBOLSAVEL`;
      414      d-013 (hospedagem, 690,00, sem nota) → `CATEGORIA_NAO_REEM
           BOLSAVEL`, e não

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 3 lines, removed 1 line
      418      A justificativa cita a RN-001 e a origem: d-010 → "centro 
           de custo
      419      CC-ENG-PLATAFORMA"; ` cc-eng-plataforma ` → "centro de cus
           to
      420      CC-ENG-PLATAFORMA"; f-003 → "política padrão; centro de cu
           sto CC-SUPORTE-N2
      421 -    não cadastrado"; `CC-ADM` com `representacao` → "centro de
          - custo CC-ADM";                                               
      421 +    não cadastrado"; `" CC-Suporte-N2 "` com `representacao` →
          + "política padrão;                                            
      422 +    centro de custo CC-Suporte-N2 não cadastrado"; `CC-ADM` co
          +m `representacao`                                             
      423 +    → "centro de custo CC-ADM";                               
      424      política com `hospedagem` 0 na padrão e `CC-ADM` → "centro
            de custo CC-ADM
      425      usando limite herdado da política padrão".
      426    - **Teste:** `tests/test_rn001_categoria.py`

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 2 lines, removed 1 line
      431    `LIMITE_DIARIO` citando a origem do limite. O acréscimo em v
           iagem do documento
      432    não é aplicado. Revisa a T-015 e a T-016.
      433    - **Atende:** RN-008, RN-009, RN-010, RN-011, RN-016, spec §
           4 (justificativa
      434 -    de limite), AMB-008, AMB-021, AMB-023, AMB-035, AMB-036, A
          -MB-037, AMB-038                                               
      434 +    de limite), AMB-008, AMB-021, AMB-023, AMB-035, AMB-036, A
          +MB-037, AMB-038,                                              
      435 +    AMB-040                                                   
      436    - **Aceite:** `CC-COMERCIAL`: e-007 (hospedagem, 1.200,00, "
           3 noites") →
      437      400,00, `limitado`; e-001 (`representacao`, 340,00) → 300,
           00, `limitado`;
      438      e-008 (alimentação, 95,00) → 90,00, `limitado`; alimentaçã
           o e representação

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 3 lines, removed 1 line
      444      CC-ADM usando limite herdado da política padrão"; `CC-ADM`
            com alimentação
      445      acima de 45,00 → "centro de custo CC-ADM"; ` cc-comercial 
           ` com alimentação
      446      de 95,00 → 90,00, `limitado`, citando "centro de custo CC-
           COMERCIAL"; f-002
      447 -    → "política padrão; centro de custo CC-SUPORTE-N2 não cada
          -strado".                                                      
      447 +    → "política padrão; centro de custo CC-SUPORTE-N2 não cada
          +strado";                                                      
      448 +    `" CC-Suporte-N2 "` com hospedagem de 310,00 → 250,00, `li
          +mitado`, citando                                              
      449 +    "política padrão; centro de custo CC-Suporte-N2 não cadast
          +rado".                                                        
      450    - **Teste:** `tests/test_rn008_limites.py`, `tests/test_rn00
           9_distribuicao.py`,
      451      `tests/test_rn010_parcial.py`, `tests/test_rn011_viagem.py
           `
      452    - **Commit:**

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 9 lines, removed 6 lines
      543  - [ ] **T-039** — Casos novos da §7 da spec 2.1 na tabela para
           metrizada, com o
      544    nome do caso como `id` (`test(T-039)`).
      545    - **Atende:** spec §7 (casos de RN-001, RN-006, RN-007, RN-0
           13, RN-015 a
      546 -    RN-018 e seção 8 incluídos nas specs 2.0 e 2.1), AMB-037, 
          -AMB-038, AMB-039                                              
      547 -  - **Aceite:** os 70 casos da §7 passam e aparecem no relatór
          -io do pytest com o                                            
      548 -    nome da spec; o teste de contagem passa de 37 para 70. Inc
          -lui "Grafia do                                                
      549 -    centro de custo na justificativa", "Periodicidade com graf
          -ia diferente" e a                                             
      550 -    justificativa de herança em "Categoria ausente na tabela d
          -o centro".                                                    
      546 +    RN-018 e seção 8 incluídos nas specs 2.0 e 2.1), AMB-037, 
          +AMB-038, AMB-039,                                             
      547 +    AMB-040                                                   
      548 +  - **Aceite:** os 71 casos da §7 passam e aparecem no relatór
          +io do pytest com o                                            
      549 +    nome da spec; o teste de contagem passa de 37 para 71. Inc
          +lui "Grafia do                                                
      550 +    centro de custo na justificativa", "Periodicidade com graf
          +ia diferente",                                                
      551 +    "Centro de custo desconhecido com espaços nas pontas" (`" 
          +CC-Suporte-N2 "`                                              
      552 +    → justificativa com "CC-Suporte-N2") e a justificativa de 
          +herança em                                                    
      553 +    "Categoria ausente na tabela do centro".                  
      554    - **Teste:** `tests/test_secao7_casos_de_borda.py::test_seca
           o7_caso_de_borda`,
      552 -    `::test_secao7_tem_70_casos`                              
      555 +    `::test_secao7_tem_71_casos`                              
      556    - **Commit:**
      557  
      558  - [ ] **T-040** — Aceite dos dois documentos do envelope pela 
           CLI, com

● Atualizei só tasks.md. Não mexi em spec, DECISIONS.md, plan nem código, e não
  fiz commit.

  - T-028: a descrição agora diz que, para centro de custo sem cadastro, a
    justificativa usa o valor da entrada só sem os espaços das pontas, sem a
    normalização da RN-002. O critério de aceite inclui " CC-Suporte-N2 " →
    "política padrão; centro de custo CC-Suporte-N2 não cadastrado", preservando
    maiúsculas e minúsculas (e não cc-suporte-n2). Entra a AMB-040.
  - T-032: novo critério de aceite: " CC-Suporte-N2 " com representacao →
    justificativa de categoria citando "CC-Suporte-N2 não cadastrado". Entra a
    AMB-040.
  - T-033: novo critério de aceite: " CC-Suporte-N2 " com hospedagem de 310,00 →
    250,00, limitado, citando "CC-Suporte-N2 não cadastrado". Entra a AMB-040.
  - T-039: de 70 para 71 casos, com o teste test_secao7_tem_71_casos. Inclui o
    caso "Centro de custo desconhecido com espaços nas pontas". Entra a AMB-040.

✻ Worked for 32s · done 22:30

> agora atualiza o plan.md pra ficar de acordo com a spec 2.1 e essas mudancas  
  da v4                                                                         
                                                                                
  coloca la a parte da politica externa centro de custo heranca da padrao moeda 
  cambio conversao antes das regras mudanca da nota fiscal duplicatas novos     
  campos na saida e como a cli vai receber politica e cambio                    
                                                                                
  politica obrigatoria faltando pode ser erro geral                             
  erro de argumento da cli codigo 2                                             
  cambio so precisa se tiver moeda estrangeira                                  
  se nao tiver cambio a despesa estrangeira fica COTACAO_INDISPONIVEL           
                                                                                
  nao mexe em spec decisions tasks nem codigo                                   
  nao commita                                                                   
                                                                                
  no final me fala se alguma task t-026 pra frente precisa mudar por causa do   
  plan                                                                          

  Ran 1 shell command (ctrl+o to expand)

● Li o código atual (motor, CLI, assinaturas) para o plano encaixar nele. Agora
  reescrevo o plan.md.

● Write(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-reem
       bolso\plan.md)
  ⎿  Added 309 lines, removed 100 lines
       1  # Plano Técnico — Motor de Cálculo de Reembolso
       2  
       3 -**Versão:** 1.0 · **Baseado na spec:** 1.1 (inclui D-001)      
       3 +**Versão:** 2.0 · **Baseado na spec:** 2.1 (inclui D-001, D-002
         + e D-003)                                                      
       4  
       5  > Aqui mora o COMO. Este arquivo pode e deve falar de linguagem
          , biblioteca e
       6  > arquitetura. O que ele **não** pode é introduzir regra de neg
          ócio nova — se
       7  > apareceu uma, ela pertence à `spec.md`.
       8  
       9 +**O que mudou da 1.0 para a 2.0:** a política sai do código e v
         +ira documento                                                  
      10 +externo (RN-015), escolhido por centro de custo (RN-016); entra
         +m moeda (RN-017)                                               
      11 +e câmbio (RN-018), com a conversão antes das regras; a CLI rece
         +be os                                                          
      12 +documentos de política e de câmbio; a saída ganha `moeda`, `tax
         +a_cambio` e                                                    
      13 +`data_cotacao`. Revistas: DT-004, DT-005, DT-006. Novas: DT-009
         + a DT-014.                                                     
      14 +                                                               
      15  ---
      16  
      17  ## 1. Stack
     ...
      20  |---|---|---|---|
      21  | Linguagem | Python 3.12+ | `decimal` e `json` na biblioteca p
          adrão; nenhuma dependência de runtime; rápido de escrever em 2 
          dias | Node/TS: sem decimal nativo, e `JSON.parse` converte `33
          .333` em float antes de qualquer código nosso rodar. Go: cerimô
          nia demais para um CLI deste tamanho |
      22  | Testes | pytest | `parametrize` com `ids` legíveis cobre a ta
          bela da seção 7 da spec linha a linha | `unittest`: verboso e c
          om parametrização pobre |
      17 -| Parsing/validação | `json` da stdlib + validação manual | A R
         -N-013 recusa uma despesa e segue com as outras; validação escri
         -ta à mão expressa isso direto | pydantic/jsonschema: falham o d
         -ocumento inteiro por padrão; adaptar ao "erro por despesa" cust
         -a mais do que escrever ~50 linhas |                            
      18 -| Aritmética monetária | `decimal.Decimal`, lido direto do JSON
         - com `parse_float=Decimal` | Float no parse transforma `10.005`
         - em `10.00499…`, que arredonda para 10,00 e quebra a RN-003. O 
         -tipo certo precisa existir desde a leitura | float (erro de rep
         -resentação); inteiro em centavos (exigiria arredondar já no par
         -se, e `valor_informado` precisa do valor sem arredondamento) | 
      23 +| Parsing/validação | `json` da stdlib + validação manual, para
         + os três documentos | A RN-013 recusa uma despesa e segue com a
         +s outras; validação escrita à mão expressa isso direto. Polític
         +a e câmbio reaproveitam os mesmos utilitários (DT-012) | pydant
         +ic/jsonschema: falham o documento inteiro por padrão; adaptar a
         +o "erro por despesa" custa mais do que escrever ~50 linhas |   
      24 +| Aritmética monetária | `decimal.Decimal`, lido direto do JSON
         + com `parse_float=Decimal`, inclusive limites, limiar e taxas d
         +e câmbio | Float no parse transforma `10.005` em `10.00499…`, q
         +ue arredonda para 10,00 e quebra a RN-003; o mesmo vale para `3
         +3.333 × 5.42` (AMB-027) | float (erro de representação); inteir
         +o em centavos (exigiria arredondar já no parse, e `valor_inform
         +ado` e `taxa_cambio` precisam sair sem arredondamento) |       
      25  | CLI | `argparse` | Biblioteca padrão; há um único subcomando 
          | click/typer: dependência sem ganho |
      26  | Lint/format | ruff | Uma ferramenta para lint e formatação | 
          flake8 + black |
      27  
      28  **Comandos:**
      29  
      24 -- Rodar: `python -m reembolso calcular --input despesas.json --
         -output resultado.json`                                         
      30 +- Rodar: `python -m reembolso calcular --input despesas.json --
         +politica politica.json [--cambio cambio.json] --output resultad
         +o.json`                                                        
      31  - Testes: `python -m pytest`
      32  - Lint/format: `ruff check .` · `ruff format .`
      33  
      34  ## 2. Arquitetura
      35  
      36  ```
      31 -arquivo JSON                                                   
      32 -   │                                                           
      33 -   ▼                                                           
      34 -cli ──► entrada ──────────► motor ─────────────────────► saida 
         -──► arquivo JSON                                               
      35 -(I/O)   parse + validação   etapas 3–8 da seção 8        serial
         -ização                                                         
      36 -        (etapas 1–2)        (núcleo puro)                + tota
         -l                                                              
      37 +despesas.json ─┐                                               
      38 +politica.json ─┼─► cli ──► entrada / politica / cambio ──► moto
         +r ───────────► saida ──► resultado.json                        
      39 +cambio.json  ──┘   (I/O)   parse + validação dos 3 docs     eta
         +pas 3–9          serialização                                  
      40 +  (opcional)               (etapas 1–2), política           da 
         +seção 8          + total                                       
      41 +                           aplicável (RN-016)               (nú
         +cleo puro)                                                     
      42  ```
      43  
      44  | Módulo | Responsabilidade | Regras |
      45  |---|---|---|
      46  | `cli.py` / `__main__.py` | Argumentos, leitura e escrita de a
          rquivo, mensagem de erro, código de saída | — |
      42 -| `entrada.py` | JSON → `Documento`. Detecta erro geral (exceçã
         -o `EntradaInvalida`) e erro por despesa (`DADOS_INVALIDOS`). Co
         -nstrói `Despesa` já normalizada e arredondada | RN-013, AMB-017
         - |                                                             
      43 -| `normalizacao.py` | Normalização de texto e arredondamento | 
         -RN-002, RN-003 |                                               
      44 -| `politica.py` | Dados da política: categorias, limites, limia
         -r da nota fiscal | RN-001, RN-007, RN-008 |                    
      45 -| `etapas.py` | Uma função por etapa da seção 8 da spec | RN-00
         -1, RN-004 a RN-010 |                                           
      47 +| `entrada.py` | JSON de despesas → `Documento`. Erro geral (`E
         +ntradaInvalida`) e erro por despesa (`DADOS_INVALIDOS`). Valida
         + `centro_custo` e `moeda`. Também guarda os utilitários de pars
         +e estrito usados por `politica.py` e `cambio.py` (DT-012) | RN-
         +013, RN-017, AMB-017, AMB-018, AMB-024 |                       
      48 +| `politica.py` | JSON de política → `Politica` (validação da R
         +N-015) e escolha da `PoliticaAplicavel` pelo centro de custo, c
         +om herança por categoria | RN-015, RN-016, RN-002 (chaves e per
         +iodicidade) |                                                  
      49 +| `cambio.py` | JSON de câmbio → `Cambio` (validação da RN-018)
         + e busca da taxa pela data da despesa ou a anterior mais próxim
         +a | RN-018 |                                                   
      50 +| `normalizacao.py` | Normalização de texto, de moeda e arredon
         +damento | RN-002, RN-003, RN-017 |                             
      51 +| `etapas.py` | Uma função por etapa da seção 8 da spec, de 3 a
         + 9 | RN-001, RN-003 a RN-010, RN-018 |                         
      52  | `motor.py` | Lista ordenada de etapas e execução | Seção 8 |
      47 -| `justificativas.py` | Templates de texto das justificativas e
         - formatação `R$ 0,00` | Seção 4 (justificativa) |              
      53 +| `justificativas.py` | Templates de texto das justificativas, 
         +formatação `R$ 0,00` e texto da origem da política | Seção 4 (j
         +ustificativa), RN-016 |                                        
      54  | `saida.py` | `Resultado` → estrutura JSON, `null`, duas casas
          , total | Seção 4 (saída), RN-003 |
      55  | `modelo.py` | Dataclasses e enums | — |
      56  
      57  **Fronteiras:**
      58  
      59  - Só `cli.py` toca disco, stdout e stderr.
      54 -- `entrada.py` recebe texto e devolve objetos; não abre arquivo
         -.                                                              
      55 -- `motor.py`, `etapas.py`, `normalizacao.py` e `politica.py` nã
         -o conhecem JSON                                                
      56 -  nem arquivo. Recebem e devolvem objetos do `modelo.py`.      
      60 +- `entrada.py`, `politica.py` e `cambio.py` recebem texto e dev
         +olvem objetos;                                                 
      61 +  não abrem arquivo.                                           
      62 +- `motor.py`, `etapas.py`, `normalizacao.py`, `justificativas.p
         +y` e a parte de                                                
      63 +  seleção de `politica.py` não conhecem JSON nem arquivo. Receb
         +em e devolvem                                                  
      64 +  objetos do `modelo.py`, de `politica.py` e de `cambio.py`.   
      65  
      58 -Essa divisão permite testar toda regra de negócio sem I/O, e um
         -a mudança de                                                   
      59 -política tende a tocar só `politica.py` e `etapas.py`.         
      66 +Essa divisão permite testar toda regra de negócio sem I/O. Uma 
         +mudança de                                                     
      67 +valor da política agora é só uma mudança no documento de políti
         +ca, sem código.                                                
      68  
      69  ## 3. Modelo de dados
      70  
     ...
      76    periodo: dict              # cópia como veio, para a saída
      77    inicio: date
      78    fim: date
      79 +  centro_custo: str | None   # como veio (já validado como text
         +o); None se ausente                                            
      80    despesas: list[Despesa | Invalida]   # na ordem da entrada
      81  
      73 -Despesa                      # passou pela etapa 1 (RN-013)    
      82 +Despesa                      # passou pela etapa 1 (RN-013, RN-
         +017)                                                           
      83    posicao: int               # 1, 2, 3...
      84    id: str
      85    data: date
      86    categoria: str             # normalizada (RN-002)
      87    fornecedor: str            # normalizado (RN-002)
      88    tem_nota_fiscal: bool
      80 -  valor_informado: Decimal   # sem arredondamento              
      81 -  valor_considerado: Decimal # arredondado (RN-003)            
      89 +  moeda: str                 # normalizada (RN-017); "BRL" se a
         +usente                                                         
      90 +  valor_informado: Decimal   # na moeda da despesa, sem arredon
         +damento                                                        
      91 +  valor_considerado: Decimal | None  # em reais (RN-003, RN-018
         +); None até a etapa 3                                          
      92 +                                     # nas despesas em moeda es
         +trangeira (DT-010)                                             
      93 +  taxa_cambio: Decimal | None        # como está no documento d
         +e câmbio; None em BRL                                          
      94 +  data_cotacao: date | None          # data da taxa usada; None
         + em BRL                                                        
      95  
      96  Invalida                     # recusada na etapa 1
      97    posicao: int
     ...
      102  Resultado
      103    id: str | None
      104    valor_informado: Decimal | None
       92 -  valor_considerado: Decimal | None # None quando DADOS_INVALI
          -DOS                                                           
      105 +  moeda: str | None                 # None quando DADOS_INVALI
          +DOS                                                           
      106 +  taxa_cambio: Decimal | None                                 
      107 +  data_cotacao: date | None                                   
      108 +  valor_considerado: Decimal | None # None quando DADOS_INVALI
          +DOS ou COTACAO_INDISPONIVEL                                   
      109    valor_reembolsavel: Decimal
      110    status: Status
      111    motivo: Motivo | None             # None quando APROVADO
      112    justificativa: str
      113  ```
      114  
      115 +Política e câmbio (em `politica.py` e `cambio.py`):           
      116 +                                                              
      117 +```                                                           
      118 +Politica                                                      
      119 +  moeda_base: str                          # "BRL"            
      120 +  limiar_nota_fiscal: Decimal                                 
      121 +  padrao: dict[str, Decimal]               # categoria normali
          +zada → limite                                                 
      122 +  centros: dict[str, Centro]               # chave normalizada
          + → Centro                                                     
      123 +                                                              
      124 +Centro                                                        
      125 +  codigo: str                              # grafia da chave n
          +o documento (AMB-038)                                         
      126 +  limites: dict[str, Decimal]              # categoria normali
          +zada → limite                                                 
      127 +                                                              
      128 +Origem                                     # de onde veio a en
          +trada de uma categoria (RN-016)                               
      129 +  tipo: TipoOrigem                         # PADRAO, CENTRO, H
          +ERDADA, NAO_CADASTRADO                                        
      130 +  codigo: str | None                       # código a citar (A
          +MB-038, AMB-040)                                              
      131 +                                                              
      132 +PoliticaAplicavel                                             
      133 +  limiar_nota_fiscal: Decimal                                 
      134 +  regra(categoria) -> (limite: Decimal | None, origem: Origem)
      135 +                                           # limite None = cat
          +egoria não consta                                             
      136 +                                                              
      137 +Cambio                                                        
      138 +  moeda_base: str                                             
      139 +  taxas: dict[str, list[tuple[date, Decimal]]]   # moeda → (da
          +ta, taxa), ordenado por data                                  
      140 +  cotacao(moeda, data) -> tuple[Decimal, date] | None         
      141 +```                                                           
      142 +                                                              
      143  - `Status`: `APROVADO`, `LIMITADO`, `RECUSADO`, com valores ig
           uais aos textos
      144    da spec (`"aprovado"`...).
      101 -- `Motivo`: os sete códigos da tabela de motivos da spec, com 
          -valor igual ao                                                
      102 -  código (`"DUPLICATA"`...).                                  
      145 +- `Motivo`: os oito códigos da tabela de motivos da spec, com 
          +valor igual ao                                                
      146 +  código (`"COTACAO_INDISPONIVEL"`...).                       
      147 +- A periodicidade não é guardada: depois de validada (`dia` ou
          + `diaria`), as                                                
      148 +  duas têm o mesmo efeito (AMB-036).                          
      149  - A saída mantém um `Resultado` por posição. A lista final é m
           ontada por ordem
      150    de posição, o que garante "um item por despesa, na mesma ord
           em".
      151  
      152  ## 4. Como a política é representada
      153  
      108 -Os valores da política ficam **em um único módulo, `politica.p
          -y`, como dados**:                                             
      154 +Os valores da política **não estão mais no código**: vêm do do
          +cumento de                                                    
      155 +política informado na execução (RN-015). `politica.py` só lê, 
          +valida e escolhe:                                             
      156  
      157  ```python
      111 -CATEGORIAS_REEMBOLSAVEIS = frozenset({"alimentacao", "transpor
          -te_urbano", "hospedagem"})                                    
      112 -LIMITE_POR_DATA = {                                           
      113 -    "alimentacao": Decimal("60.00"),                          
      114 -    "transporte_urbano": Decimal("80.00"),                    
      115 -    "hospedagem": Decimal("250.00"),                          
      116 -}                                                             
      117 -LIMIAR_NOTA_FISCAL = Decimal("100.00")   # exige nota se valor
          - > limiar (RN-007)                                            
      158 +politica = ler_politica(texto)                          # RN-0
          +15 → Politica                                                 
      159 +aplicavel = politica_aplicavel(politica, centro_custo)  # RN-0
          +16 → PoliticaAplicavel                                        
      160  ```
      161  
      120 -Cada constante tem um comentário com a RN de origem.          
      162 +Seleção (RN-016), com o centro de custo comparado após `normal
          +izar_texto`:                                                  
      163  
      122 -A **ordem das regras** também é dado, em `motor.py`:          
      164 +| `centro_custo` | Categoria no centro | Categoria só na padrã
          +o | Categoria em nenhum |                                     
      165 +|---|---|---|---|                                             
      166 +| ausente ou vazio | — | limite da padrão, `PADRAO` | `None`, 
          +`PADRAO` |                                                    
      167 +| cadastrado | limite do centro, `CENTRO` | limite da padrão, 
          +`HERDADA` | `None`, `CENTRO` |                                
      168 +| não cadastrado | — | limite da padrão, `NAO_CADASTRADO` | `N
          +one`, `NAO_CADASTRADO` |                                      
      169  
      170 +O texto da origem fica em `justificativas.py` (DT-011).       
      171 +                                                              
      172 +A **ordem das regras** continua sendo dado, em `motor.py`:    
      173 +                                                              
      174  ```python
      175  ETAPAS = [
      176 +    Conversao(conversao),         # RN-018, RN-003 → COTACAO_I
          +NDISPONIVEL                                                   
      177      PorItem(valor_negativo),      # RN-005 → VALOR_NEGATIVO
      178      PorItem(periodo),             # RN-004 → FORA_DO_PERIODO
      128 -    PorItem(categoria),           # RN-001 → CATEGORIA_NAO_REE
          -MBOLSAVEL                                                     
      179 +    PorItem(categoria),           # RN-001, RN-016 → CATEGORIA
          +_NAO_REEMBOLSAVEL                                             
      180      EmGrupo(duplicatas),          # RN-006 → DUPLICATA
      181      PorItem(nota_fiscal),         # RN-007 → NOTA_FISCAL_AUSEN
           TE
      182      EmGrupo(limites_por_data),    # RN-008, RN-009, RN-010 → L
           IMITE_DIARIO
      183  ]
      184  ```
      185  
      186 +- **Etapa de conversão:** recebe uma `Despesa` e devolve a mes
          +ma despesa com                                                
      187 +  `valor_considerado`, `taxa_cambio` e `data_cotacao` preenchi
          +dos, ou uma                                                   
      188 +  recusa. A despesa devolvida substitui a da lista viva.      
      189  - **Etapa por item:** recebe uma `Despesa` e devolve `None` (p
           assa) ou uma recusa
      190    com motivo e justificativa.
      191  - **Etapa em grupo:** recebe todas as despesas ainda vivas, em
            ordem de posição,
      192    e decide sobre o conjunto. A de duplicatas devolve recusas. 
           A de limites
      193    devolve o valor reembolsável de cada despesa.
      140 -- As etapas 1 e 2 (validação, normalização e arredondamento) a
          -contecem em                                                   
      141 -  `entrada.py`, porque precisam do JSON bruto. As despesas `In
          -valida` não entram                                            
      142 -  no motor.                                                   
      194 +- Todas as etapas recebem um `Contexto` com o documento, a pol
          +ítica aplicável e                                             
      195 +  o câmbio (DT-009).                                          
      196 +- As etapas 1 e 2 (validação e normalização) acontecem em `ent
          +rada.py`, porque                                              
      197 +  precisam do JSON bruto. As despesas `Invalida` não entram no
          + motor.                                                       
      198  - Uma despesa recusada sai da lista viva e não chega às etapas
            seguintes. É isso
      199    que impede uma despesa recusada de consumir limite (seção 8 
           da spec).
      145 -- Ao final, uma despesa que chegou à etapa 8 é `APROVADO` se  
      200 +- Ao final, uma despesa que chegou à etapa 9 é `APROVADO` se  
      201    `valor_reembolsavel == valor_considerado`, senão `LIMITADO`,
            exatamente como a
      202    seção 4 da spec define.
      203  
     ...
      210  **Decisão:** `json.loads(texto, parse_float=Decimal)`. Inteiro
           s (`parse_int`)
      211  também são convertidos para `Decimal` na validação. O arredond
           amento usa
      212  `quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)`, que no `D
           ecimal` afasta a
      158 -metade do zero, inclusive para negativos.                     
      213 +metade do zero, inclusive para negativos. Vale para os três do
          +cumentos.                                                     
      214  **Alternativa descartada:** float com `round()`. O Python arre
           donda metade para
      215  par, e o float já chega com erro de representação.
      216  **Consequência:** nenhuma comparação de fronteira (100,00 vs 1
           00,01) depende de
     ...
      223  `EntradaInvalida(mensagem)`. Em seguida valida cada despesa e 
           produz `Despesa` ou
      224  `Invalida`. Pontos de cuidado, todos derivados da RN-013:
      225  - `bool` é subclasse de `int` em Python, então `"valor": true`
            precisa ser
      171 -  rejeitado com teste explícito de tipo;                      
      226 +  rejeitado com teste explícito de tipo; o mesmo vale para lim
          +ite, limiar e                                                 
      227 +  taxa nos outros documentos;                                 
      228  - datas validadas com regex `^\d{4}-\d{2}-\d{2}$` e depois `da
           te.fromisoformat`.
      173 -  O regex é necessário porque `fromisoformat` aceita formatos 
          -além de `AAAA-MM-DD`;                                         
      229 +  O regex é necessário porque `fromisoformat` aceita formatos 
          +além de `AAAA-MM-DD`.                                         
      230 +  Vale também para as chaves de `taxas` do câmbio;            
      231  - texto "vazio" = `str.strip() == ""`;
      232 +- `centro_custo` presente e não texto → `EntradaInvalida`; `mo
          +eda` presente e                                               
      233 +  vazia ou não texto → `DADOS_INVALIDOS` (RN-017);            
      234  - campos informativos e desconhecidos não são lidos pela valid
           ação.
      235  **Alternativa descartada:** pydantic, que falha o documento in
           teiro por padrão.
      236  **Consequência:** cada caso da RN-013 vira um `if` com teste p
           róprio. Mais código
     ...
      241  **Contexto:** a RN-013 (D-001) trata `NaN`/`Infinity` como JSO
           N inválido, mas o
      242  `json` do Python aceita esses literais por padrão.
      243  **Decisão:** `parse_constant` levanta `EntradaInvalida`, o que
            vira erro geral.
      244 +O mesmo parser estrito é usado na política e no câmbio (DT-012
          +).                                                            
      245  **Alternativa descartada:** aceitar e rejeitar depois como val
           or não numérico.
      246  Isso contradiria a spec.
      247  **Consequência:** o parser fica estrito como a norma JSON.
      248  
      189 -### DT-004 — Política em módulo Python, pipeline como lista   
      249 +### DT-004 — Política em documento externo, pipeline como list
          +a (revista na 2.0)                                            
      250  
      191 -**Contexto:** a mudança de requisito do dia 2 é desconhecida. 
          -É provável que ela                                            
      192 -mexa em limites, categorias, ordem das regras ou crie uma regr
          -a nova.                                                       
      193 -**Decisão:** valores da política em `politica.py` e ordem das 
          -etapas em                                                     
      194 -`ETAPAS` (seção 4 deste plano).                               
      195 -**Alternativa descartada:** arquivo de configuração externo (J
          -SON/YAML). Ele                                                
      196 -exigiria validar a própria configuração e documentar um format
          -o a mais, sem                                                 
      197 -ganho enquanto quem muda a política é quem muda o código.     
      198 -**Consequência:** trocar um valor é uma linha. Uma regra nova 
          -é uma função mais                                             
      199 -uma linha em `ETAPAS`. Se a política precisar variar por execu
          -ção (por exemplo,                                             
      200 -um dado de viagem na entrada), `politica.py` vira um objeto pa
          -ssado ao motor, e                                             
      201 -isso é uma refatoração local.                                 
      251 +**Contexto:** na 1.0, os valores da política ficavam em `polit
          +ica.py` como                                                  
      252 +constantes. A v4 (RN-015) passa a política para um documento e
          +xterno, com                                                   
      253 +tabelas por centro de custo. A 1.0 já previa a saída: "`politi
          +ca.py` vira um                                                
      254 +objeto passado ao motor".                                     
      255 +**Decisão:** `politica.py` deixa de ter constantes e passa a l
          +er e validar o                                                
      256 +documento (`ler_politica`) e a escolher a `PoliticaAplicavel` 
      257 +(`politica_aplicavel`). A política aplicável é escolhida uma v
          +ez por execução,                                              
      258 +antes do motor, e chega às etapas pelo `Contexto` (DT-009). Nã
          +o existe política                                             
      259 +embutida de reserva (AMB-031). A ordem das etapas continua em 
          +`ETAPAS`.                                                     
      260 +**Alternativa descartada:** manter as constantes como padrão q
          +uando não houver                                              
      261 +documento. A spec proíbe (AMB-031) e criaria duas fontes da ve
          +rdade.                                                        
      262 +**Consequência:** mudar um valor da política é editar o JSON; 
          +regra nova                                                    
      263 +continua sendo uma função mais uma linha em `ETAPAS`. Os teste
          +s de regra montam                                             
      264 +a `PoliticaAplicavel` a partir de `exemplos/envelope/politica-
          +v4.json` ou de                                                
      265 +dicionários pequenos.                                         
      266  
      203 -### DT-005 — Serialização da saída                            
      267 +### DT-005 — Serialização da saída (revista na 2.0)           
      268  
      269  **Contexto:** a saída exige duas casas em `valor_considerado`,
      270  `valor_reembolsavel` e `total_reembolsavel` (RN-003), `null` n
           os campos sem
      271  valor (D-001), e `colaborador`/`periodo` copiados como vieram,
            que podem conter
      208 -`Decimal` do parse.                                           
      209 -**Decisão:** `saida.py` monta a estrutura com `None` onde a sp
          -ec pede nulo. Um                                              
      210 -encoder próprio escreve todo `Decimal` como literal numérico J
          -SON:                                                          
      272 +`Decimal` do parse. A 2.0 acrescenta `moeda`, `taxa_cambio` e 
          +`data_cotacao`.                                               
      273 +**Decisão:** `saida.py` monta a estrutura com `None` onde a sp
          +ec pede nulo, com                                             
      274 +os campos do item na ordem da tabela da seção 4 da spec: `id`,
      275 +`valor_informado`, `moeda`, `taxa_cambio`, `data_cotacao`, `va
          +lor_considerado`,                                             
      276 +`valor_reembolsavel`, `status`, `motivo`, `justificativa`. Um 
          +encoder próprio                                               
      277 +escreve todo `Decimal` como literal numérico JSON:            
      278  - os três campos monetários saem quantizados em duas casas (`6
           0.00`);
      212 -- `valor_informado` sai com `str(Decimal)`, sem quantizar (`33
          -.333`);                                                       
      279 +- `valor_informado` e `taxa_cambio` saem com `str(Decimal)`, s
          +em quantizar                                                  
      280 +  (`33.333`, `5.93`);                                         
      281 +- `data_cotacao` sai como texto `AAAA-MM-DD`;                 
      282  - zero negativo (`-0.00`, resultado de arredondar `-0.004`) é 
           normalizado para
      283    `0.00` antes de qualquer etapa, para que a RN-005 o veja com
           o zero.
      284  JSON escrito em UTF-8, com `ensure_ascii=False` e `indent=2`.
     ...
      287  spec.
      288  **Consequência:** um ponto único de formatação, testado isolad
           amente.
      289  
      221 -### DT-006 — Erro geral na CLI                                
      290 +### DT-006 — Erro geral e argumentos na CLI (revista na 2.0)  
      291  
      292  **Contexto:** a RN-013 diz que, em erro geral, o sistema "ence
           rra com mensagem
      224 -de erro e não gera saída". A forma de encerrar é técnica.     
      293 +de erro e não gera saída". A forma de encerrar é técnica. A 2.
          +0 acrescenta os                                               
      294 +documentos de política (obrigatório) e de câmbio (opcional).  
      295  **Decisão:**
      226 -- a mensagem vai para **stderr**;                             
      227 -- o código de saída é **1**;                                  
      228 -- o arquivo de saída **não é criado nem sobrescrito**. A CLI s
          -ó abre o arquivo                                              
      229 -  de saída depois que leitura, validação e cálculo terminaram 
          -sem erro. Se um                                               
      230 -  arquivo com esse nome já existir, ele fica intacto.         
      231 -Sucesso retorna 0. Argumentos inválidos de linha de comando re
          -tornam 2 (padrão                                              
      232 -do `argparse`).                                               
      233 -**Alternativa descartada:** gravar um JSON de erro no arquivo 
          -de saída. Contradiz                                           
      234 -"não gera saída".                                             
      296 +- argumentos: `calcular --input <despesas> --politica <polític
          +a> [--cambio                                                  
      297 +  <câmbio>] --output <resultado>`;                            
      298 +- `--input` e `--output` são obrigatórios no `argparse`. Falta
          +ndo um deles, ou                                              
      299 +  com argumento desconhecido, o código é **2** (padrão do `arg
          +parse`);                                                      
      300 +- `--politica` **não** é marcado como obrigatório no `argparse
          +`. A falta do                                                 
      301 +  documento de política é um erro geral da RN-013/RN-015, trat
          +ado pela CLI                                                  
      302 +  como os demais: código **1**;                               
      303 +- `--cambio` é opcional. Sem ele, o motor recebe `cambio=None`
          +, e as despesas                                               
      304 +  em moeda estrangeira são recusadas com `COTACAO_INDISPONIVEL
          +` (RN-018); as                                                
      305 +  despesas em BRL não precisam dele;                          
      306 +- erro geral em qualquer documento (arquivo inexistente ou ile
          +gível, JSON                                                   
      307 +  inválido, estrutura inválida): mensagem em **stderr**, códig
          +o **1**, e o                                                  
      308 +  arquivo de saída **não é criado nem sobrescrito**. A CLI só 
          +abre o arquivo de                                             
      309 +  saída depois que leitura, validação e cálculo terminaram sem
          + erro;                                                        
      310 +- ordem de leitura: despesas, política, câmbio. O câmbio preci
          +sa da política já                                             
      311 +  lida para comparar `moeda_base`.                            
      312 +Sucesso retorna 0.                                            
      313 +**Alternativa descartada:** `--politica` obrigatório no `argpa
          +rse`, que daria                                               
      314 +código 2 para um caso que a spec classifica como erro geral; o
          +u gravar um JSON                                              
      315 +de erro no arquivo de saída, que contradiz "não gera saída".  
      316  **Consequência:** quem chama a CLI distingue sucesso de erro s
           ó pelo código de
      236 -saída.                                                        
      317 +saída; 2 sempre significa linha de comando mal formada.       
      318  
      319  ### DT-007 — Normalização de texto
      320  
      321  **Contexto:** a RN-002 manda remover espaços das pontas, maiús
           culas e acentos.
      322  **Decisão:** `strip()`, depois `casefold()`/`lower()`, depois
      323  `unicodedata.normalize("NFD", s)` removendo caracteres de cate
           goria `Mn`
      243 -(marcas combinantes). Nada mais é alterado: espaços internos f
          -icam.                                                         
      324 +(marcas combinantes). Nada mais é alterado: espaços internos f
          +icam. Aplicada a                                              
      325 +categoria, fornecedor, centro de custo e, no documento de polí
          +tica, às chaves                                               
      326 +de categoria e de centro e à `periodicidade` (AMB-020, AMB-039
          +).                                                            
      327 +Moeda tem normalização própria, `normalizar_moeda`: `strip()` 
          +e `upper()`                                                   
      328 +(RN-017), usada na despesa, nas chaves do câmbio e em `moeda_b
          +ase`.                                                         
      329  **Alternativa descartada:** biblioteca `unidecode`, que transl
           itera além de
      330  acentos e mudaria texto que a spec manda preservar.
      246 -**Consequência:** `Alimentação` → `alimentacao`, `ç` → `c`.   
      331 +**Consequência:** `Alimentação` → `alimentacao`, `ç` → `c`, `"
          + usd "` → `USD`.                                              
      332  
      333  ### DT-008 — Justificativas por template
      334  
      335  **Contexto:** a seção 9 da spec exige saída determinística e j
           ustificativas que
      251 -citem a RN, o `id` da despesa mantida (duplicata) e o limite j
          -á consumido.                                                  
      336 +citem a RN, o `id` da despesa mantida (duplicata), o limite já
          + consumido e,                                                 
      337 +desde a 2.0, a origem da política e a moeda/data sem cotação. 
      338  **Decisão:** uma função por motivo em `justificativas.py`, com
            o mesmo texto dos
      253 -exemplos da seção 4 da spec. Valores formatados como `R$ 60,00
          -`.                                                            
      339 +exemplos da seção 4 da spec. Valores formatados como `R$ 60,00
          +`. Novas:                                                     
      340 +`cotacao_indisponivel(moeda, data)` e `origem(Origem)` (DT-011
          +).                                                            
      341  **Alternativa descartada:** montar o texto dentro de cada etap
           a, que espalharia
      342  a formatação.
      343  **Consequência:** os testes de regra verificam `status`, `moti
           vo` e valores, e
      257 -checam na justificativa só a presença da RN e dos `id` citados
          -. Isso evita testes                                           
      258 -frágeis a mudanças de redação.                                
      344 +checam na justificativa só a presença da RN, dos `id` citados 
          +e do texto de                                                 
      345 +origem. Isso evita testes frágeis a mudanças de redação.      
      346  
      347 +### DT-009 — `Contexto` das etapas                            
      348 +                                                              
      349 +**Contexto:** na 1.0, as etapas recebiam a despesa e o `Docume
          +nto`. Agora                                                   
      350 +categoria, nota fiscal e limites precisam da política aplicáve
          +l, e a conversão                                              
      351 +precisa do câmbio.                                            
      352 +**Decisão:** `calcular(documento, politica, cambio=None, etapa
          +s=None)` monta um                                             
      353 +`Contexto(documento, politica: PoliticaAplicavel, cambio: Camb
          +io | None)` e o                                               
      354 +passa a todas as etapas no lugar do `Documento`.              
      355 +**Alternativa descartada:** variáveis globais ou parâmetros di
          +ferentes por                                                  
      356 +etapa, que quebrariam a assinatura uniforme de `PorItem`/`EmGr
          +upo`.                                                         
      357 +**Consequência:** a troca de assinatura é mecânica e atinge to
          +das as etapas e os                                            
      358 +testes que chamam etapas diretamente; o `Contexto` absorve dad
          +os futuros sem                                                
      359 +mudar assinaturas de novo.                                    
      360 +                                                              
      361 +### DT-010 — Conversão de moeda                               
      362 +                                                              
      363 +**Contexto:** a RN-018 converte pela data da despesa, com a úl
          +tima taxa anterior                                            
      364 +disponível, e a RN-003 manda arredondar uma única vez, em reai
          +s. A conversão é a                                            
      365 +etapa 3 da seção 8, antes de valor negativo.                  
      366 +**Decisão:**                                                  
      367 +- **BRL:** `entrada.py` já preenche `valor_considerado = arred
          +ondar(valor_informado)`,                                      
      368 +  como na 1.0; a etapa de conversão deixa a despesa passar sem
          + consultar o                                                  
      369 +  câmbio. Em BRL a conversão é a identidade (RN-003), então o 
          +resultado é o                                                 
      370 +  mesmo de convertê-la na etapa 3.                            
      371 +- **Outra moeda:** `entrada.py` deixa `valor_considerado = Non
          +e`; a etapa de                                                
      372 +  conversão chama `cambio.cotacao(moeda, data)`. A busca usa a
          + lista                                                        
      373 +  `(data, taxa)` da moeda, ordenada, e `bisect_right` para ach
          +ar a maior data                                               
      374 +  ≤ data da despesa. Achou: `valor_considerado = arredondar(va
          +lor_informado ×                                               
      375 +  taxa)`, com `taxa_cambio` e `data_cotacao` preenchidos. Não 
          +achou, ou                                                     
      376 +  `cambio is None`: recusa `COTACAO_INDISPONIVEL`.            
      377 +- Os dois fatores são `Decimal` sem arredondamento; o produto 
          +usa o contexto                                                
      378 +  decimal padrão (28 dígitos), suficiente para os valores do d
          +omínio.                                                       
      379 +**Alternativa descartada:** converter em `entrada.py`, que obr
          +igaria a entrada a                                            
      380 +conhecer o câmbio e tiraria `COTACAO_INDISPONIVEL` da ordem da
          + seção 8.                                                     
      381 +Converter todas as moedas na etapa 3, inclusive BRL, mudaria a
          + construção da                                                
      382 +`Despesa` e os testes da 1.0 sem ganho de comportamento.      
      383 +**Consequência:** todas as etapas de 4 em diante veem `valor_c
          +onsiderado` em                                                
      384 +reais e nunca `None`. Despesa estrangeira sem cotação e também
          + fora do período                                              
      385 +recebe `COTACAO_INDISPONIVEL` (custo aceito na AMB-029).      
      386 +                                                              
      387 +### DT-011 — Origem da política como dado                     
      388 +                                                              
      389 +**Contexto:** as justificativas de `LIMITE_DIARIO` e          
      390 +`CATEGORIA_NAO_REEMBOLSAVEL` citam a origem (RN-016, AMB-037, 
          +AMB-038, AMB-040).                                            
      391 +**Decisão:** `politica_aplicavel` devolve, por categoria, uma 
          +`Origem(tipo,                                                 
      392 +codigo)`. `justificativas.origem` transforma em texto:        
      393 +- `PADRAO` → "política padrão";                               
      394 +- `CENTRO` → "centro de custo `<codigo>`";                    
      395 +- `HERDADA` → "centro de custo `<codigo>` usando limite herdad
          +o da política padrão";                                        
      396 +- `NAO_CADASTRADO` → "política padrão; centro de custo `<codig
          +o>` não cadastrado".                                          
      397 +Para centro cadastrado, `codigo` é `Centro.codigo`, a grafia d
          +a chave no                                                    
      398 +documento de política. Para não cadastrado, é o valor da entra
          +da só com                                                     
      399 +`strip()`, **sem** `normalizar_texto`.                        
      400 +**Alternativa descartada:** a seleção devolver o texto pronto,
          + que misturaria                                               
      401 +formatação com a regra de seleção.                            
      402 +**Consequência:** a seleção é testada pelo `tipo` e pelo `codi
          +go`; o texto é                                                
      403 +testado uma vez em `justificativas.py`.                       
      404 +                                                              
      405 +### DT-012 — Validação dos documentos de política e de câmbio 
      406 +                                                              
      407 +**Contexto:** RN-015 e RN-018 listam os erros gerais de cada d
          +ocumento.                                                     
      408 +**Decisão:** `politica.py` e `cambio.py` usam os utilitários d
          +e `entrada.py`                                                
      409 +(`ler_json` estrito, `data_valida`, `texto_preenchido`, número
          + que não é `bool`)                                            
      410 +e levantam a mesma `EntradaInvalida`, com mensagem que cita o 
          +documento e o                                                 
      411 +campo. Pontos de cuidado:                                     
      412 +- chaves normalizadas que colidem (`Alimentação`/`alimentacao`
          +, `CC-ADM`/` cc-adm `,                                        
      413 +  `USD`/` usd `) são detectadas comparando o tamanho do dicion
          +ário antes e depois                                           
      414 +  da normalização, por tabela/data;                           
      415 +- `moeda_base` da política: `normalizar_moeda` e igual a `BRL`
          +; do câmbio:                                                  
      416 +  igual à da política após a mesma normalização;              
      417 +- campos informativos (`versao`, `vigencia`, `acrescimo_em_via
          +gem_percentual`,                                              
      418 +  `observacao`, `fonte`) não são lidos.                       
      419 +**Alternativa descartada:** um módulo de validação genérico po
          +r esquema, que                                                
      420 +seria maior que as duas validações juntas.                    
      421 +**Consequência:** a CLI trata os três documentos com o mesmo `
          +except                                                        
      422 +EntradaInvalida`.                                             
      423 +                                                              
      424 +### DT-013 — Chave de duplicatas                              
      425 +                                                              
      426 +**Contexto:** a RN-006 passou a exigir a mesma moeda e o mesmo
          + valor original                                               
      427 +arredondado na moeda original (AMB-030).                      
      428 +**Decisão:** a chave do grupo é `(data, categoria, fornecedor,
          + moeda,                                                       
      429 +arredondar(valor_informado))`. Em BRL, `arredondar(valor_infor
          +mado)` é o                                                    
      430 +próprio `valor_considerado`, então a regra da 1.0 é um caso pa
          +rticular.                                                     
      431 +**Alternativa descartada:** comparar `valor_considerado`, que 
          +juntaria 22,00 EUR                                            
      432 +e 130,46 BRL.                                                 
      433 +**Consequência:** uma só fórmula para todas as moedas.        
      434 +                                                              
      435 +### DT-014 — Nota fiscal e limites lidos da política aplicável
      436 +                                                              
      437 +**Contexto:** RN-007 e RN-008 passam a usar o limiar e os limi
          +tes do documento;                                             
      438 +RN-001 passa a recusar limite 0 (AMB-022).                    
      439 +**Decisão:**                                                  
      440 +- `categoria`: `limite is None or limite == 0` → `CATEGORIA_NA
          +O_REEMBOLSAVEL`,                                              
      441 +  com a origem na justificativa;                              
      442 +- `nota_fiscal`: `valor_considerado > politica.limiar_nota_fis
          +cal` e sem nota →                                             
      443 +  recusa. Como `valor_considerado` já está em reais, a AMB-028
          + sai de graça;                                                
      444 +- `limites_por_data`: agrupa por `(data, categoria)` e usa `po
          +litica.regra(categoria)`;                                     
      445 +  `representacao` não tem tratamento especial (AMB-023). O acr
          +éscimo em viagem                                              
      446 +  não é lido (AMB-035).                                       
      447 +**Alternativa descartada:** —                                 
      448 +**Consequência:** as três etapas mudam só na origem do dado; a
          + lógica da 1.0                                                
      449 +fica igual.                                                   
      450 +                                                              
      451  ## 6. Estratégia de testes
      452  
      453  Estrutura:
      454  
      455  ```
      456  tests/
      266 -  test_rn001_categoria.py ... test_rn014_descricao.py   # um a
          -rquivo por RN                                                 
      457 +  fabrica.py                                            # desp
          +esa(), documento(), politica_aplicavel()                      
      458 +  test_rn001_categoria.py ... test_rn018_cambio.py      # um a
          +rquivo por RN                                                 
      459    test_secao7_casos_de_borda.py                         # tabe
           la da seção 7
      268 -  test_secao9_aceite_exemplo.py                         # exem
          -plo completo                                                  
      460 +  test_secao9_aceite_exemplo.py                         # exem
          +plo original (CC-ENG-PLATAFORMA)                              
      461 +  test_secao9_aceite_envelope.py                        # dois
          + documentos do envelope                                       
      462    test_cli.py                                           # pont
           a a ponta via subprocess
      463    test_saida_serializacao.py                            # DT-0
           05
      464    test_rastreabilidade.py                               # toda
            RN tem teste
      465  ```
      466  
      467  - **Nível:**
      275 -  - **unitário** (~70%): regras e normalização, sem I/O, com d
          -espesas montadas                                              
      276 -    por um helper `despesa(**campos)`;                        
      277 -  - **integração** (~20%): `entrada` → `motor` → `saida` a par
          -tir de dicts;                                                 
      468 +  - **unitário** (~70%): regras, normalização, seleção da polí
          +tica, busca de                                                
      469 +    cotação, sem I/O, com despesas montadas por `despesa(**cam
          +pos)` e política                                              
      470 +    por `politica_aplicavel(centro_custo=..., documento=...)`;
      471 +  - **integração** (~20%): `entrada` → `politica`/`cambio` → `
          +motor` → `saida`                                              
      472 +    a partir de texto;                                        
      473    - **ponta a ponta** (~10%): CLI via `subprocess`, conferindo
            arquivo gerado,
      474      stderr e código de saída.
      475 +- **Política nos testes:** `fabrica.politica_aplicavel()` lê  
      476 +  `exemplos/envelope/politica-v4.json` e devolve, por padrão, 
          +a política padrão,                                            
      477 +  que tem os mesmos valores da v3. Testes de regra que depende
          +m de centro de                                                
      478 +  custo pedem o centro explicitamente. Testes de validação usa
          +m dicionários                                                 
      479 +  pequenos.                                                   
      480  - **Cada `RN-NNN` da spec tem teste?** Há um arquivo `test_rnN
           NN_*.py` por regra,
      281 -  e o "Aceite" de cada RN vira pelo menos um teste nele. O    
      481 +  de RN-001 a RN-018, e o "Aceite" de cada RN vira pelo menos 
          +um teste nele. O                                              
      482    `test_rastreabilidade.py` lê a `spec.md`, extrai os IDs `RN-
           \d{3}` e falha se
      483    algum não tiver arquivo de teste correspondente.
      484  - **Casos de borda da seção 7 da spec:** um teste parametrizad
           o com uma linha
      285 -  por caso da tabela. O `id` do parâmetro é o nome do caso na 
          -spec, então o                                                 
      286 -  relatório do pytest lista os casos com os mesmos nomes da sp
          -ec.                                                           
      287 -- **Aceite da seção 9 da spec:** roda `exemplos/despesas-exemp
          -lo.json` e                                                    
      288 -  compara as 14 linhas (`valor_reembolsavel`, `status`, `motiv
          -o`) e o total                                                 
      289 -  585,43.                                                     
      485 +  por caso da tabela (71 na spec 2.1). O `id` do parâmetro é o
          + nome do caso na                                              
      486 +  spec.                                                       
      487 +- **Aceite da seção 9 da spec:**                              
      488 +  - `exemplos/despesas-exemplo.json` com a política v4 e sem c
          +âmbio: 14 linhas                                              
      489 +    e total 351,43;                                           
      490 +  - `despesas-envelope.json` com política e câmbio: 10 linhas 
          +e total 1.143,26;                                             
      491 +  - `despesas-envelope-cc-desconhecido.json`: 4 linhas e total
          + 373,76.                                                      
      492  - **Invariantes da seção 9 da spec:**
      493    - determinismo: duas execuções produzem saídas idênticas byt
           e a byte;
      494    - RN-014: trocar todas as descrições não altera `valor_reemb
           olsavel`,
      495      `status` nem `motivo`;
      496    - "todo item tem justificativa citando RN-xxx", verificado p
           or regex.
      295 -- **DT-006:** em erro geral, o teste cria antes um arquivo de 
          -saída com conteúdo                                            
      296 -  conhecido e confirma que ele continua igual depois da execuç
          -ão.                                                           
      497 +- **DT-006:** em erro geral (inclusive política ausente ou inv
          +álida e câmbio                                                
      498 +  inválido), o teste cria antes um arquivo de saída com conteú
          +do conhecido e                                                
      499 +  confirma que ele continua igual depois da execução e que o c
          +ódigo é 1.                                                    
      500 +  Argumento desconhecido ou `--input` ausente → código 2.     
      501  - **Nomenclatura:** `test_rnNNN_<comportamento>`, por exemplo
      298 -  `test_rn007_valor_exatamente_100_nao_exige_nota`. Testes de 
          -decisão técnica                                               
      299 -  usam `test_dtNNN_<comportamento>`.                          
      502 +  `test_rn018_sabado_usa_taxa_de_sexta`. Testes de decisão téc
          +nica usam                                                     
      503 +  `test_dtNNN_<comportamento>`.                               
      504  
      505  ## 7. Riscos
      506  
      507  | Risco | Probabilidade | O que faço se acontecer |
      508  |---|---|---|
      305 -| Float vazar em algum ponto (parse, soma, literal no código) 
          -e errar uma fronteira | Média | DT-001; constantes sempre como
          - `Decimal("…")`; teste para 10,005 → 10,01 e para 100,00 vs 10
          -0,01 |                                                        
      509 +| Float vazar em algum ponto (parse, soma, literal no código, 
          +taxa) e errar uma fronteira | Média | DT-001 nos três document
          +os; teste para 10,005 → 10,01, 100,00 vs 100,01 e 33,333 USD ×
          + 5,42 → 180,66 |                                              
      510 +| Arredondar duas vezes na conversão | Média | DT-010: um únic
          +o `arredondar` sobre o produto; teste 180,66 vs 180,65 |      
      511 +| Busca de cotação pegar a data seguinte em vez da anterior | 
          +Média | `bisect_right` − 1 (DT-010); testes de sábado (e-004),
          + de data antes da primeira cotação e de data exata |          
      512  | Usar `round()` ou `ROUND_HALF_EVEN` por engano | Média | Uma
            única função de arredondamento em `normalizacao.py`, com test
           e de metade positiva e negativa |
      513  | `-0.00` aparecer na saída ou não ser tratado como zero | Méd
           ia | Normalização em `normalizacao.py` (DT-005) e caso da seçã
           o 7 (−0,004) |
      308 -| Serializador perder as duas casas (`60.0`) ou falhar com `De
          -cimal` em `colaborador`/`periodo` | Alta se não testado | `tes
          -t_saida_serializacao.py` cobre os dois casos |                
      309 -| `bool` aceito como número em `valor` | Média | Teste explíci
          -to em RN-013 |                                                
      310 -| `date.fromisoformat` aceitar formatos além de `AAAA-MM-DD` |
          - Alta (Python 3.11+ aceita mais formatos) | Regex antes do par
          -se (DT-002) |                                                 
      514 +| Serializador perder as duas casas, quantizar `taxa_cambio` o
          +u falhar com `Decimal` em `colaborador`/`periodo` | Alta se nã
          +o testado | `test_saida_serializacao.py` cobre os casos |     
      515 +| `bool` aceito como número em `valor`, limite, limiar ou taxa
          + | Média | Teste explícito em RN-013, RN-015 e RN-018 |       
      516 +| `date.fromisoformat` aceitar formatos além de `AAAA-MM-DD` (
          +também nas chaves do câmbio) | Alta (Python 3.11+ aceita mais 
          +formatos) | Regex antes do parse (DT-002) |                   
      517 +| Centro não cadastrado sair normalizado (`cc-suporte-n2`) na 
          +justificativa | Média | DT-011: só `strip()`; caso da seção 7 
          +com `" CC-Suporte-N2 "` |                                     
      518 +| `--politica` marcado como obrigatório no `argparse` e devolv
          +er 2 em vez de 1 | Média | DT-006; teste de CLI sem `--politic
          +a` esperando 1 e saída intacta |                              
      519 +| Troca de assinatura das etapas (DT-009) quebrar muitos teste
          +s de uma vez | Alta | Fazer a troca num único commit, junto co
          +m a `fabrica.politica_aplicavel()` |                          
      520 +| Testes de aceite da v3 mudarem de resultado quando o centro 
          +de custo passar a valer | Certa | Atualizar a tabela da seção 
          +9 (585,43 → 351,43) e as justificativas da seção 4 no mesmo co
          +mmit em que a seleção por centro de custo entra no fluxo real 
          +|                                                             
      521  | Acentos não removidos em todos os casos (letras compostas, `
           ç`) | Baixa | DT-007, com testes para `Alimentação`, `ç` e mai
           úsculas acentuadas |
      312 -| Mudança do dia 2 exigir reestruturação | Média | DT-004. Se 
          -a mudança não couber em `politica.py` ou `ETAPAS`, registrar o
          - motivo no `DECISIONS.md` e na seção 5 deste plano |          
      313 -| Justificativa divergir dos exemplos da spec e o teste não pe
          -gar | Baixa | Testes da seção 9 checam RN citada e `id`; os ex
          -emplos da seção 4 viram um teste de texto exato |             
      522 +| Justificativa divergir dos exemplos da spec e o teste não pe
          +gar | Baixa | Testes da seção 9 checam RN citada, `id` e orige
          +m; os exemplos da seção 4 viram um teste de texto exato |     
      523  | Comportamento implementado sem regra na spec | Média | Toda 
           dúvida de negócio que aparecer na implementação volta para a s
           pec antes do código (regra do `CLAUDE.md`) |

● Atualizei o plan.md para a versão 2.0, baseada na spec 2.1. Não mexi em spec,
  DECISIONS.md, tasks.md nem código, e não fiz commit.

  O que o plan cobre agora

  - Política externa: politica.py deixa de ter constantes. Passa a ler e validar
    o documento e a escolher a política aplicável a partir do centro de custo.
    Não existe política embutida de reserva (DT-004 revista, DT-012, DT-014).
  - Centro de custo e herança: a seção 4 tem uma tabela da escolha (padrão,
    centro, herdada, não cadastrado). A justificativa vem de um dado de origem
    (tipo e código) que justificativas.py transforma em texto (DT-011):
    - centro cadastrado: código na grafia da chave da política;
    - centro sem cadastro: valor da entrada só sem os espaços das pontas.
  - Moeda: normalização própria (tira os espaços das pontas e passa para
    maiúsculas) e validação em entrada.py (DT-002, DT-007).
  - Câmbio e conversão antes das regras:
    - novo cambio.py, que acha a taxa da data da despesa ou a última anterior;
    - nova etapa de conversão no início do motor, antes de valor negativo;
    - BRL continua arredondado em entrada.py, porque em reais a conversão não
      muda o valor;
    - moeda estrangeira é convertida na etapa, com arredondamento uma vez só.
      Sem cotação, a despesa fica COTACAO_INDISPONIVEL (DT-010).
  - Política e câmbio nas etapas: todas as etapas passam a receber um objeto com
    o documento, a política aplicável e o câmbio (DT-009).
  - Nota fiscal: compara o valor já convertido com o limiar da política
    (DT-014).
  - Duplicatas: a chave passa a incluir a moeda e o valor original arredondado
    (DT-013).
  - Saída: campos novos na ordem da §4; taxa_cambio sai sem arredondar e
    data_cotacao sai como texto (DT-005 revista).
  - CLI (DT-006 revista): calcular --input --politica [--cambio] --output.
    - Sem política ou com política inválida: erro geral, código 1, saída
      intacta. Para isso, --politica não é marcado como obrigatório no argparse.
    - Outros erros de argumento: código 2.
    - Sem câmbio: as despesas estrangeiras ficam COTACAO_INDISPONIVEL e as em
      BRL seguem normalmente.
  - Também atualizei a estratégia de testes (RN-001 a RN-018, 71 casos da §7,
    três aceites da §9) e a tabela de riscos.

  Li "política faltando pode ser erro geral" junto com "argumento código 2"
  assim: a falta de --politica dá código 1, como a RN-013 classifica, e o código
  2 fica para linha de comando mal formada. Se você queria código 2 também para
  a falta de --politica, me avise.

  Tasks de T-026 em diante que precisam mudar por causa do plan

  - Cabeçalho da Fase 7: ainda diz "plan 1.0, a atualizar" e que os nomes são
    provisórios. Agora seria plan 2.0, e os nomes estão definidos.
  - T-031: diz --politica "(obrigatório)" e, no aceite, "sem --politica → erro".
    Precisa deixar explícito que é código 1, não um argumento obrigatório do
    argparse. Também deve citar a troca de assinatura das etapas (DT-009) e o
    helper de política nos testes.
  - T-028: a seleção devolve um dado de origem (tipo e código), e o texto sai de
    justificativas.py (DT-011). O aceite continua válido, mas o teste do texto
    fica em justificativas.py.
  - T-034: deixar claro que só a moeda estrangeira é convertida na etapa, e que
    BRL continua arredondado em entrada.py (DT-010). Também deve citar a nova
    etapa de conversão no motor.
  - T-038: vale acrescentar ao aceite "argumento desconhecido ou --input ausente
    → código 2".

  As demais (T-026, T-027, T-029, T-030, T-032, T-033, T-035 a T-037, T-039 a
  T-041) estão de acordo com o plan.

✻ Brewed for 3m 3s · done 22:38

> beleza mantem falta de --politica como codigo 1 mesmo                         
                                                                                
  agora ajusta só o tasks.md com o que vc falou por causa do plan 2.0           
                                                                                
  corrige o cabecalho da fase 7                                                 
  t-028                                                                         
  t-031                                                                         
  t-034                                                                         
  t-038                                                                         
                                                                                
  nao mexe em spec decisions plan nem codigo                                    
  nao commita                                                                   
                                                                                
  no final so me fala o que mudou                                               

  Searched for 1 pattern, read 1 file (ctrl+o to expand)

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 3 lines, removed 3 lines
      270  
      271  ## Fase 7 — Envelope (Dia 2)
      272  
      273 -**Baseado em:** spec 2.1 (D-002, D-003) · plan 1.0, **a atuali
          -zar para a spec                                               
      274 -2.1 antes da T-026** (`docs(plan):`). Nomes de módulo, função 
          -e argumento de CLI citados                                    
      275 -abaixo seguem a arquitetura do plan 1.0 e são provisórios até 
          -essa revisão.                                                 
      273 +**Baseado em:** spec 2.1 (D-002, D-003) · plan 2.0. Nomes de m
          +ódulo, função,                                                
      274 +tipo e argumento de CLI citados abaixo seguem o plan 2.0 (seçõ
          +es 2 a 4 e DT-004                                             
      275 +a DT-014).                                                    
      276  
      277  Sequência pensada para a suíte ficar verde em todo commit:
      278  

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 12 lines, removed 9 lines
      326    - **Teste:** `tests/test_rn015_politica.py`
      327    - **Commit:**
      328  
      329 -- [ ] **T-028** — Política aplicável: função que recebe a `Pol
          -itica` e o                                                    
      330 -  `colaborador.centro_custo` e devolve a tabela efetiva (centr
          -o sobre a padrão,                                             
      331 -  herança por categoria) e a origem a citar nas justificativas
          -. Na validação do                                             
      332 -  documento de despesas, `centro_custo` presente e não texto v
          -ira erro geral.                                               
      333 -  A origem é por categoria (centro, padrão, herdada da padrão 
          -ou centro sem                                                 
      334 -  cadastro). Com o centro cadastrado, o código sai na grafia d
          -a chave do                                                    
      335 -  documento de política. Sem cadastro, sai o valor da entrada 
          -só sem os espaços                                             
      336 -  das pontas, sem a normalização da RN-002. Ainda não é usada 
          -pelo motor.                                                   
      329 +- [ ] **T-028** — Política aplicável: `politica_aplicavel(poli
          +tica, centro_custo)`                                          
      330 +  devolve uma `PoliticaAplicavel` cujo `regra(categoria)` dá o
          + limite (ou `None`                                            
      331 +  se a categoria não consta) e a `Origem(tipo, codigo)` daquel
          +a categoria. O                                                
      332 +  `tipo` é `PADRAO`, `CENTRO`, `HERDADA` ou `NAO_CADASTRADO`. 
          +Com o centro                                                  
      333 +  cadastrado, `codigo` é `Centro.codigo` (grafia da chave do d
          +ocumento de                                                   
      334 +  política). Sem cadastro, é o valor da entrada só com `strip(
          +)`, sem a                                                     
      335 +  normalização da RN-002. O texto da origem sai de `justificat
          +ivas.origem`                                                  
      336 +  (DT-011). `Documento` ganha `centro_custo`, e na validação d
          +o documento de                                                
      337 +  despesas `centro_custo` presente e não texto vira erro geral
          +. Ainda não é                                                 
      338 +  usada pelo motor.                                           
      339    - **Atende:** RN-016, RN-002 (centro de custo), RN-013 (erro
            geral do centro de
      338 -    custo), AMB-018, AMB-019, AMB-020, AMB-021, AMB-037, AMB-0
          -38, AMB-040                                                   
      340 +    custo), AMB-018, AMB-019, AMB-020, AMB-021, AMB-037, AMB-0
          +38, AMB-040,                                                  
      341 +    plan DT-011                                               
      342    - **Aceite:** sem `centro_custo` ou `"  "` → padrão, origem 
           "política padrão";
      343      `CC-COMERCIAL`, ` cc-comercial ` e `Cc-Comercial` → tabela
            do
      344      `CC-COMERCIAL`, origem "centro de custo CC-COMERCIAL" (gra
           fia do documento

  Read 1 file (ctrl+o to expand)

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 3 lines, removed 1 line
      339    - **Atende:** RN-016, RN-002 (centro de custo), RN-013 (erro
            geral do centro de
      340      custo), AMB-018, AMB-019, AMB-020, AMB-021, AMB-037, AMB-0
           38, AMB-040,
      341      plan DT-011
      342 -  - **Aceite:** sem `centro_custo` ou `"  "` → padrão, origem 
          -"política padrão";                                            
      342 +  - **Aceite:** a seleção é conferida pelo `tipo`, pelo `codig
          +o` e pelo limite;                                             
      343 +    o texto de cada origem é conferido em `justificativas.orig
          +em`.                                                          
      344 +    Sem `centro_custo` ou `"  "` → padrão, origem "política pa
          +drão";                                                        
      345      `CC-COMERCIAL`, ` cc-comercial ` e `Cc-Comercial` → tabela
            do
      346      `CC-COMERCIAL`, origem "centro de custo CC-COMERCIAL" (gra
           fia do documento
      347      de política); `CC-SUPORTE-N2` → padrão, origem "política p
           adrão; centro de

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 2 lines, removed 1 line
      355      `CC-ENG-PLATAFORMA` → `hospedagem` 0,00 (não herda, porque
            consta);
      356      `CC-COMERCIAL` → `representacao` 300,00; padrão → sem `rep
           resentacao`;
      357      `"centro_custo": 42` → `EntradaInvalida`.
      358 -  - **Teste:** `tests/test_rn016_politica_aplicavel.py`,      
      358 +  - **Teste:** `tests/test_rn016_politica_aplicavel.py` (seleç
          +ão e                                                          
      359 +    `justificativas.origem`),                                 
      360      `tests/test_rn013_dados_invalidos.py::test_rn013_erro_gera
           l_*` (caso
      361      `centro_custo` numérico)
      362    - **Commit:**
● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 23 lines, removed 12 lines
      389  
      390  ### 7.2 — Regras com política externa e câmbio
      391  
      392 -- [ ] **T-031** — Política externa no motor e na CLI: `calcula
          -r` recebe a                                                   
      393 -  política aplicável (T-028); as etapas de nota fiscal e de li
          -mites passam a ler                                            
      394 -  o limiar e os limites dela; `periodicidade` `dia` e `diaria`
          - têm o mesmo                                                  
      395 -  efeito. As constantes de `politica.py` saem. A CLI ganha `--
          -politica`                                                     
      396 -  (obrigatório); documento de política ausente ou inválido é e
          -rro geral, sem                                                
      397 -  saída. Até a T-038, CLI e testes de exemplo usam a política 
          -padrão.                                                       
      392 +- [ ] **T-031** — Política externa no motor e na CLI:         
      393 +  `calcular(documento, politica, cambio=None, etapas=None)` mo
          +nta um                                                        
      394 +  `Contexto(documento, politica, cambio)` e o passa a todas as
          + etapas no lugar                                              
      395 +  do `Documento` (troca mecânica de assinatura de todas as eta
          +pas, num único                                                
      396 +  commit). As etapas de nota fiscal e de limites passam a ler 
          +o limiar e os                                                 
      397 +  limites da `PoliticaAplicavel`; `periodicidade` `dia` e `dia
          +ria` têm o mesmo                                              
      398 +  efeito. As constantes de `politica.py` saem. `tests/fabrica.
          +py` ganha                                                     
      399 +  `politica_aplicavel()`, que lê `politica-v4.json` e devolve 
          +a padrão por                                                  
      400 +  padrão. A CLI ganha `--politica`, **não** marcado como obrig
          +atório no                                                     
      401 +  `argparse`: a falta dele é erro geral (código 1), assim como
          + documento de                                                 
      402 +  política inexistente, ilegível ou inválido. Até a T-038, CLI
          + e testes de                                                  
      403 +  exemplo usam a política padrão.                             
      404    - **Atende:** RN-015, RN-007 (limiar do documento), RN-008 (
           limites do
      399 -    documento), RN-013 (erro geral), AMB-031, AMB-036, DT-004 
          -(revisão), DT-006                                             
      405 +    documento), RN-013 (erro geral), AMB-031, AMB-036, plan DT
          +-004, DT-006,                                                 
      406 +    DT-009, DT-014                                            
      407    - **Aceite:** com a padrão da v4, toda a suíte da v3 passa (
           só as chamadas
      401 -    mudam para informar a política). Política com `alimentacao
          -` 70,00 → duas                                                
      402 -    despesas de 50,00 na mesma data → 50,00 + 20,00. Limiar 15
          -0,00 → 120,00 sem                                             
      403 -    nota passa. CLI sem `--politica` → erro, arquivo de saída 
          -não criado;                                                   
      404 -    `--politica` com limite `-1` → código 1, arquivo de saída 
          -existente intacto.                                            
      408 +    mudam para informar a política e as etapas recebem `Contex
          +to`). Política com                                            
      409 +    `alimentacao` 70,00 → duas despesas de 50,00 na mesma data
          + → 50,00 + 20,00.                                             
      410 +    Limiar 150,00 → 120,00 sem nota passa. CLI sem `--politica
          +` → código 1,                                                 
      411 +    mensagem em stderr, arquivo de saída não criado e arquivo 
          +existente intacto                                             
      412 +    (não é código 2). `--politica` apontando para arquivo inex
          +istente ou com                                                
      413 +    limite `-1` → código 1, arquivo de saída existente intacto
          +.                                                             
      414    - **Teste:** `tests/test_rn007_nota_fiscal.py::test_rn007_li
           miar_vem_do_documento`,
      415      `tests/test_rn008_limites.py::test_rn008_limite_vem_do_doc
           umento`,
      416      `::test_rn008_dia_e_diaria_sao_limite_por_data`,
      408 -    `tests/test_cli.py::test_rn015_sem_politica_e_erro_geral`,
      417 +    `tests/test_motor.py::test_dt009_etapas_recebem_contexto`,
      418 +    `tests/test_cli.py::test_rn015_sem_politica_retorna_1_e_na
          +o_cria_saida`,                                                
      419 +    `::test_rn015_politica_inexistente_e_erro_geral`,         
      420      `::test_rn015_politica_invalida_nao_sobrescreve_saida`
      421    - **Commit:**
      422  

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 16 lines, removed 8 lines
      468      `tests/test_rn010_parcial.py`, `tests/test_rn011_viagem.py
           `
      469    - **Commit:**
      470  
      471 -- [ ] **T-034** — Etapa de conversão e arredondamento (etapa 3
          - da §8, antes de                                              
      472 -  valor negativo): `BRL` não consulta o câmbio; outra moeda us
          -a a taxa da data                                              
      473 -  da despesa ou a da data anterior mais próxima com essa moeda
          -; o produto é                                                 
      474 -  arredondado uma vez. Sem taxa, ou sem documento de câmbio → 
      475 -  `COTACAO_INDISPONIVEL`, com `valor_considerado` nulo e justi
          -ficativa citando                                              
      476 -  moeda e data. `calcular` recebe o `Cambio` opcional. A linha
          - da §7 "campo                                                 
      477 -  desconhecido" (que usava `moeda: USD`) passa a usar `projeto
          -`.                                                            
      471 +- [ ] **T-034** — Etapa de conversão (etapa 3 da §8, antes de 
          +valor negativo):                                              
      472 +  novo tipo de etapa `Conversao` em `motor.py`, primeiro item 
          +de `ETAPAS`, que                                              
      473 +  devolve a `Despesa` com `valor_considerado`, `taxa_cambio` e
          + `data_cotacao`                                               
      474 +  preenchidos (ela substitui a da lista viva) ou uma recusa.  
      475 +  - **BRL:** `entrada.py` continua preenchendo `valor_consider
          +ado =                                                         
      476 +    arredondar(valor_informado)`, como na v3; a etapa deixa pa
          +ssar sem consultar                                            
      477 +    o câmbio.                                                 
      478 +  - **Outra moeda:** `entrada.py` deixa `valor_considerado = N
          +one`; a etapa                                                 
      479 +    chama `Cambio.cotacao(moeda, data)`, que busca a maior dat
          +a ≤ data da                                                   
      480 +    despesa (`bisect_right`), e arredonda o produto uma única 
          +vez.                                                          
      481 +  - Sem taxa, ou `cambio=None` → `COTACAO_INDISPONIVEL`, com `
          +valor_considerado`                                            
      482 +    nulo e justificativa `justificativas.cotacao_indisponivel(
          +moeda, data)`.                                                
      483 +                                                              
      484 +  A linha da §7 "campo desconhecido" (que usava `moeda: USD`) 
          +passa a usar                                                  
      485 +  `projeto`.                                                  
      486    - **Atende:** RN-018, RN-003, RN-012, spec §8 (etapa 3), spe
           c §4
      479 -    (justificativa de cotação), AMB-025, AMB-026, AMB-027, AMB
          --029                                                          
      487 +    (justificativa de cotação), AMB-025, AMB-026, AMB-027, AMB
          +-029, plan DT-010                                             
      488    - **Aceite:** e-002 (22,00 EUR, 2026-07-14) → taxa 5,93, `da
           ta_cotacao`
      489      2026-07-14, 130,46. e-004 (30,00 EUR, sábado 2026-07-18) →
            taxa 5,96 de
      490      2026-07-17, 178,80. f-004 (12,00 USD, 2026-07-21) → 65,76.
            33,333 USD em

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 5 lines
      494      e as despesas em BRL seguem. BRL em sábado → sem taxa, pro
           cessada.
      495      −10,00 GBP → `COTACAO_INDISPONIVEL`; −10,00 USD em 2026-07
           -13 → −54,20,
      496      `VALOR_NEGATIVO`. USD sem cotação e fora do período → `COT
           ACAO_INDISPONIVEL`.
      497 +    Despesa BRL construída pela entrada chega à etapa 4 com o 
          +mesmo                                                         
      498 +    `valor_considerado` da v3; nenhuma despesa chega à etapa 4
          + com                                                          
      499 +    `valor_considerado` nulo.                                 
      500    - **Teste:** `tests/test_rn018_cambio.py::test_rn018_convers
           ao_*`,
      501 +    `::test_rn018_cotacao_usa_data_anterior_mais_proxima`,    
      502 +    `tests/test_motor.py::test_dt010_conversao_e_a_primeira_et
          +apa`,                                                         
      503      `tests/test_rn003_arredondamento.py::test_rn003_arredonda_
           uma_vez_depois_da_conversao`,
      504      `tests/test_secao7_casos_de_borda.py` (linha "Campo descon
           hecido")
      505    - **Commit:**

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 3 lines, removed 1 line
      545  ### 7.3 — Integração, aceite e rastreabilidade
      546  
      547  - [ ] **T-038** — Fluxo real completo: a CLI ganha `--cambio` 
           (opcional) e passa
      548 -  a escolher a política pelo `colaborador.centro_custo` (T-028
          -). No mesmo                                                   
      548 +  a escolher a política pelo `colaborador.centro_custo` (T-028
          +). Ordem de                                                   
      549 +  leitura: despesas, política, câmbio (o câmbio compara `moeda
          +_base` com a                                                  
      550 +  política). Sem `--cambio`, o motor recebe `cambio=None`. No 
          +mesmo                                                         
      551    commit, atualiza os testes da v3 cujo resultado muda com o
      552    `CC-ENG-PLATAFORMA`: tabela da §9 (total 585,43 → 351,43), j
           ustificativas
      553    exatas da §4 (Exemplo 1) e as linhas da §7 reescritas pela s
           pec 2.0. Atualiza

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 6 lines, removed 3 lines
      555    T-021, T-022 e T-025.
      556    - **Atende:** RN-016, RN-018 (câmbio opcional), RN-013 (erro
            geral dos
      557      documentos), spec §4 (Exemplo 1), spec §8 (validação antes
            das etapas),
      558 -    spec §9 (exemplo original), DT-006                        
      558 +    spec §9 (exemplo original), plan DT-006                   
      559    - **Aceite:** `exemplos/despesas-exemplo.json` + `politica-v
           4.json`, sem
      560      câmbio → as 14 linhas da §9 e total 351,43; d-001, d-002 e
            d-004 com
      561      exatamente as justificativas do Exemplo 1 da §4. Sem `cent
           ro_custo` →
      562 -    padrão. `"centro_custo": 42`, câmbio com taxa 0 ou câmbio 
          -com `moeda_base`                                              
      563 -    diferente → código 1, arquivo de saída existente intacto. 
          -Linhas da §7                                                  
      562 +    padrão. `"centro_custo": 42`, `--cambio` para arquivo inex
          +istente, câmbio                                               
      563 +    com taxa 0 ou câmbio com `moeda_base` diferente → código 1
          +, arquivo de                                                  
      564 +    saída existente intacto. Despesa em USD sem `--cambio` →  
      565 +    `COTACAO_INDISPONIVEL` e código 0. Argumento desconhecido 
          +ou `--input`                                                  
      566 +    ausente → código 2. Linhas da §7                          
      567      reescritas ("Duas despesas no mesmo dia...", "Hospedagem c
           om várias
      568      diárias", "Duas hospedagens na mesma data", "Hospedagem se
           m nota acima de
      569      100", "Categoria em maiúsculas", "Campo desconhecido") bat
           em com a spec 2.0.

● Update(C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio\specs\001-motor-ree
        mbolso\tasks.md)
  ⎿  Added 4 lines, removed 1 line
      572      `tests/test_cli.py::test_cli_exemplo_gera_arquivo`,
      573      `::test_rn016_centro_custo_invalido_e_erro_geral`,
      574      `::test_rn018_cambio_invalido_nao_sobrescreve_saida`,
      575 -    `::test_rn018_moedas_base_divergentes_e_erro_geral`       
      575 +    `::test_rn018_moedas_base_divergentes_e_erro_geral`,      
      576 +    `::test_rn018_sem_cambio_despesa_estrangeira_cotacao_indis
          +ponivel`,                                                     
      577 +    `::test_dt006_argumentos_invalidos_retornam_2` (com `--inp
          +ut` ausente e                                                 
      578 +    argumento desconhecido)                                   
      579    - **Commit:**
      580  
      581  - [ ] **T-039** — Casos novos da §7 da spec 2.1 na tabela para
           metrizada, com o

● Atualizei só tasks.md, nos cinco pontos que você pediu. Não mexi em spec,
  DECISIONS.md, plan nem código, e não fiz commit.

  - Cabeçalho da Fase 7: agora diz "spec 2.1 · plan 2.0". Saiu o aviso de "plan
    a atualizar / nomes provisórios", e os nomes citados passam a remeter às
    seções 2 a 4 e às DT-004 a DT-014 do plan.
  - T-028:
    - descreve politica_aplicavel(politica, centro_custo), que dá o limite e a
      origem (tipo e código) de cada categoria;
    - o texto da origem sai de justificativas.origem (DT-011);
    - Documento ganha centro_custo;
    - o aceite passa a conferir a escolha pelo tipo, pelo código e pelo limite,
      e o texto em justificativas.origem.
  - T-031:
    - calcular(documento, politica, cambio=None) passa um objeto com documento,
      política e câmbio a todas as etapas, com a troca de assinatura num único
      commit (DT-009);
    - fabrica.politica_aplicavel() entra para os testes;
    - --politica não é marcado como obrigatório no argparse, então a falta dele
      dá código 1, com stderr e saída intacta, e não 2;
    - aceite e testes novos para --politica ausente, inexistente ou inválido, e
      para as etapas receberem o novo objeto.
  - T-034:
    - nova etapa de conversão, a primeira de ETAPAS;
    - BRL continua com valor_considerado calculado em entrada.py; moeda
      estrangeira chega sem ele e é convertida na etapa, buscando a última data
      anterior;
    - a justificativa vem de cotacao_indisponivel (DT-010);
    - o aceite garante que nenhuma despesa chega à etapa 4 com valor_considerado
      nulo e que BRL fica igual à v3. Entram dois testes novos.
  - T-038:
    - ordem de leitura: despesas, política, câmbio; sem --cambio, o câmbio vai
      vazio ao motor;
    - aceite novo: --cambio para arquivo inexistente → código 1; USD sem câmbio
      → COTACAO_INDISPONIVEL e código 0; argumento desconhecido ou --input
      ausente → código 2;
    - dois testes de CLI novos, e test_dt006_argumentos_invalidos_retornam_2
      passa a cobrir também --input ausente e argumento desconhecido.

✻ Worked for 1m 10s · done 22:50