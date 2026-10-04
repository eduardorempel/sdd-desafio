 ▐▛███▛█   Claude Code v2.1.289
▝▜██████▀  Opus 5.5 · API Usage Billing
 ▝▝   ▝▝   C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio


> Preciso acelerar a implementação sem perder a rastreabilidade exigida pelo    
  desafio.                                                                      
                                                                                
  Leia:                                                                         
  - CLAUDE.md                                                                   
  - specs/001-motor-reembolso/spec.md                                           
  - specs/001-motor-reembolso/plan.md                                           
  - specs/001-motor-reembolso/tasks.md                                          
  - specs/001-motor-reembolso/DECISIONS.md                                      
                                                                                
  A T-001 já está concluída.                                                    
                                                                                
  A partir da T-002, trabalhe sequencialmente nas tasks pendentes.              
                                                                                
  Para CADA task:                                                               
                                                                                
  1. implemente somente o que a task pede;                                      
  2. crie/ajuste os testes previstos;                                           
  3. rode os testes relacionados e o lint;                                      
  4. se passar, marque a task como [x] em tasks.md;                             
  5. faça um commit separado referenciando a task, por exemplo:                 
     feat(T-002): ...                                                           
     test(T-017): ...                                                           
  6. não misture duas tasks no mesmo commit;                                    
  7. só depois passe para a task seguinte.                                      
                                                                                
  Não altere regras de negócio da spec por conta própria.                       
  Se encontrar uma decisão de negócio que não esteja definida na spec, PARE     
  antes de implementar essa parte e me avise.                                   
                                                                                
  Pode executar várias tasks nesta mesma sessão.                                
  Não faça /export entre as tasks.                                              
                                                                                
  Comece na T-002 e avance o máximo possível.                                   

  Read 1 file, ran 3 shell commands (ctrl+o to expand)

● Li a spec, o plano, as tasks e o DECISIONS. Vou começar pela T-002
  (modelo.py).

● Bash(cat > reembolso/modelo.py <<'EOF'
      """Estruturas de dados do motor (plan §3)."""…)
  ⎿  ..
        [100%]
     2 passed in 0.02s
     … +2 lines (ctrl+o to expand)
  ⎿  Created reembolso\modelo.py (+70 -0)
       1 +"""Estruturas de dados do motor (plan §3)."""                  
       2 +                                                               
       3 +from dataclasses import dataclass                              
       4 +from datetime import date                                      
       5 +from decimal import Decimal                                    
       6 +from enum import StrEnum                                       
       7 +                                                               
       8 +                                                               
       9 +class Status(StrEnum):                                         
      10 +    """Status de um item da saída (spec §4)."""                
      11 +                                                               
      12 +    APROVADO = "aprovado"                                      
      13 +    LIMITADO = "limitado"                                      
      14 +    RECUSADO = "recusado"                                      
      15 +                                                               
      16 +                                                               
      17 +class Motivo(StrEnum):                                         
      18 +    """Códigos de motivo da saída (spec §4, tabela de motivos).
         +"""                                                            
      19 +                                                               
      20 +    DADOS_INVALIDOS = "DADOS_INVALIDOS"                        
      21 +    VALOR_NEGATIVO = "VALOR_NEGATIVO"                          
      22 +    FORA_DO_PERIODO = "FORA_DO_PERIODO"                        
      23 +    CATEGORIA_NAO_REEMBOLSAVEL = "CATEGORIA_NAO_REEMBOLSAVEL"  
      24 +    DUPLICATA = "DUPLICATA"                                    
      25 +    NOTA_FISCAL_AUSENTE = "NOTA_FISCAL_AUSENTE"                
      26 +    LIMITE_DIARIO = "LIMITE_DIARIO"                            
      27 +                                                               
      28 +                                                               
      29 +@dataclass(frozen=True)                                        
      30 +class Despesa:                                                 
      31 +    """Despesa que passou pela etapa 1 (RN-013), já normalizada
         + e arredondada."""                                             
      32 +                                                               
      33 +    posicao: int                                               
      34 +    id: str                                                    
      35 +    data: date                                                 
      36 +    categoria: str                                             
      37 +    fornecedor: str                                            
      38 +    tem_nota_fiscal: bool                                      
      39 +    valor_informado: Decimal                                   
      40 +    valor_considerado: Decimal                                 
     … 30 more lines (ctrl+o to expand)
  ⎿  Created tests\test_modelo.py (+17 -0)
       1 +from reembolso.modelo import Motivo, Status                    
       2 +                                                               
       3 +                                                               
       4 +def test_motivos_iguais_aos_codigos_da_spec():                 
       5 +    assert {m.value for m in Motivo} == {                      
       6 +        "DADOS_INVALIDOS",                                     
       7 +        "VALOR_NEGATIVO",                                      
       8 +        "FORA_DO_PERIODO",                                     
       9 +        "CATEGORIA_NAO_REEMBOLSAVEL",                          
      10 +        "DUPLICATA",                                           
      11 +        "NOTA_FISCAL_AUSENTE",                                 
      12 +        "LIMITE_DIARIO",                                       
      13 +    }                                                          
      14 +                                                               
      15 +                                                               
      16 +def test_status_iguais_aos_textos_da_spec():                   
      17 +    assert {s.value for s in Status} == {"aprovado", "limitado"
         +, "recusado"}                                                  

● Bash(cat > /tmp/fechar.sh <<'EOF'
      #!/bin/sh…)
  ⎿  warning: in the working copy of 'specs/001-motor-reembolso/tasks.md',
     LF will be replaced by CRLF the next time Git touches it
     warning: in the working copy of 'reembolso/modelo.py', LF will be repl
     … +5 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      30    - **Teste:** `tests/test_estrutura.py::test_pacote_importa`
      31    - **Commit:** 33ec69e
      32  
      33 -- [ ] **T-002** — `modelo.py`: dataclasses `Documento`, `Despes
         -a`, `Invalida`,                                                
      33 +- [x] **T-002** — `modelo.py`: dataclasses `Documento`, `Despes
         +a`, `Invalida`,                                                
      34    `Resultado` e enums `Status` e `Motivo`, com valores iguais a
          os textos da spec.
      35    - **Atende:** spec §4 (status e motivos), plan §3
      36    - **Aceite:** os sete motivos e os três status têm exatamente
           os textos da spec.

  Ran 1 shell command (ctrl+o to expand)

● T-003: normalização de texto.

● Bash(cat > reembolso/normalizacao.py <<'EOF'
      """Normalização de texto (RN-002) e arredondamento (RN-003)."""…)
  ⎿  .........
        [100%]
     9 passed in 0.03s
     … +2 lines (ctrl+o to expand)
  ⎿  Created reembolso\normalizacao.py (+13 -0)
       1 +"""Normalização de texto (RN-002) e arredondamento (RN-003)."""
       2 +                                                               
       3 +import unicodedata                                             
       4 +                                                               
       5 +                                                               
       6 +def normalizar_texto(texto: str) -> str:                       
       7 +    """Remove espaços das pontas, passa para minúsculas e remov
         +e acentos (RN-002, DT-007).                                    
       8 +                                                               
       9 +    Espaços internos e demais caracteres são mantidos.         
      10 +    """                                                        
      11 +    decomposto = unicodedata.normalize("NFD", texto.strip().low
         +er())                                                          
      12 +    sem_acentos = "".join(c for c in decomposto if unicodedata.
         +category(c) != "Mn")                                           
      13 +    return unicodedata.normalize("NFC", sem_acentos)           
  ⎿  Created tests\test_rn002_normalizacao.py (+32 -0)
       1 +import pytest                                                  
       2 +                                                               
       3 +from reembolso.normalizacao import normalizar_texto            
       4 +                                                               
       5 +                                                               
       6 +@pytest.mark.parametrize("categoria", ["ALIMENTACAO", " Aliment
         +ação ", "alimentacao"])                                        
       7 +def test_rn002_grafias_de_alimentacao_viram_alimentacao(categor
         +ia):                                                           
       8 +    assert normalizar_texto(categoria) == "alimentacao"        
       9 +                                                               
      10 +                                                               
      11 +def test_rn002_fornecedor_ignora_maiusculas():                 
      12 +    assert normalizar_texto("Bistro Central") == normalizar_tex
         +to("bistro central")                                           
      13 +                                                               
      14 +                                                               
      15 +def test_rn002_fornecedor_ignora_espacos_nas_pontas():         
      16 +    assert normalizar_texto("BISTRO CENTRAL ") == normalizar_te
         +xto("Bistro Central")                                          
      17 +                                                               
      18 +                                                               
      19 +def test_rn002_mantem_espacos_internos():                      
      20 +    assert normalizar_texto("  Bistro   Central  ") == "bistro 
         +  central"                                                     
      21 +                                                               
      22 +                                                               
      23 +def test_rn002_cedilha_vira_c():                               
      24 +    assert normalizar_texto("Açaí da Praça") == "acai da praca"
      25 +                                                               
      26 +                                                               
      27 +def test_rn002_maiusculas_acentuadas():                        
      28 +    assert normalizar_texto("ÁÉÍÓÚ ÂÊÔ ÃÕ À Ç") == "aeiou aeo a
         +o a c"                                                         
      29 +                                                               
      30 +                                                               
      31 +def test_rn002_mantem_outros_caracteres():                     
      32 +    assert normalizar_texto("transporte_urbano-2/x") == "transp
         +orte_urbano-2/x"                                               

● Bash(sh /tmp/fechar.sh T-003 "normaliza categoria e fornecedor removendo
      espacos, maiusculas e acentos" 2>/dev/null)
  ⎿  1e0e792 feat(T-003): normaliza categoria e fornecedor removendo espaco
     s, maiusculas e acentos
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      38      `::test_status_iguais_aos_textos_da_spec`
      39    - **Commit:**
      40  
      41 -- [ ] **T-003** — Normalização de texto em `normalizacao.py`: r
         -emove espaços das                                              
      41 +- [x] **T-003** — Normalização de texto em `normalizacao.py`: r
         +emove espaços das                                              
      42    pontas, passa para minúsculas e remove acentos. Mantém espaço
          s internos.
      43    - **Atende:** RN-002, AMB-013, DT-007
      44    - **Aceite:** `ALIMENTACAO`, ` Alimentação ` e `alimentacao` 
          → `alimentacao`;

● Bash(cat > reembolso/normalizacao.py <<'EOF'
      """Normalização de texto (RN-002) e arredondamento (RN-003)."""…)
  ⎿  ..................
        [100%]
     18 passed in 0.03s
     … +2 lines (ctrl+o to expand)
  ⎿  Updated reembolso\normalizacao.py (+17 -0)
       1  """Normalização de texto (RN-002) e arredondamento (RN-003)."""
       2  
       3  import unicodedata
       4 +from decimal import ROUND_HALF_UP, Context, Decimal            
       5 +                                                               
       6 +CENTAVO = Decimal("0.01")                                      
       7 +                                                               
       8 +# Precisão suficiente para quantizar qualquer valor da entrada 
         +sem InvalidOperation.                                          
       9 +_CONTEXTO = Context(prec=1000)                                 
      10  
      11  
      12  def normalizar_texto(texto: str) -> str:
     ...
      17      decomposto = unicodedata.normalize("NFD", texto.strip().low
          er())
      18      sem_acentos = "".join(c for c in decomposto if unicodedata.
          category(c) != "Mn")
      19      return unicodedata.normalize("NFC", sem_acentos)
      20 +                                                               
      21 +                                                               
      22 +def arredondar(valor: Decimal) -> Decimal:                     
      23 +    """Arredonda para centavos com a metade se afastando do zer
         +o (RN-003, DT-001).                                            
      24 +                                                               
      25 +    O zero negativo (-0.00) vira 0.00 (DT-005).                
      26 +    """                                                        
      27 +    arredondado = valor.quantize(CENTAVO, rounding=ROUND_HALF_U
         +P, context=_CONTEXTO)                                          
      28 +    if arredondado.is_zero():                                  
      29 +        return Decimal("0.00")                                 
      30 +    return arredondado                                         
  ⎿  Created tests\test_rn003_arredondamento.py (+43 -0)
       1 +from decimal import Decimal                                    
       2 +                                                               
       3 +import pytest                                                  
       4 +                                                               
       5 +from reembolso.normalizacao import arredondar                  
       6 +                                                               
       7 +                                                               
       8 +@pytest.mark.parametrize(                                      
       9 +    ("valor", "esperado"),                                     
      10 +    [                                                          
      11 +        ("33.333", "33.33"),                                   
      12 +        ("10.005", "10.01"),                                   
      13 +        ("-10.005", "-10.01"),                                 
      14 +        ("10.004", "10.00"),                                   
      15 +        ("72.5", "72.50"),                                     
      16 +        ("100", "100.00"),                                     
      17 +        ("-45.00", "-45.00"),                                  
      18 +    ],                                                         
      19 +    ids=[                                                      
      20 +        "d-011",                                               
      21 +        "metade_positiva",                                     
      22 +        "metade_negativa",                                     
      23 +        "abaixo_da_metade",                                    
      24 +        "uma_casa",                                            
      25 +        "inteiro",                                             
      26 +        "negativo_exato",                                      
      27 +    ],                                                         
      28 +)                                                              
      29 +def test_rn003_arredonda_para_centavos(valor, esperado):       
      30 +    resultado = arredondar(Decimal(valor))                     
      31 +    assert resultado == Decimal(esperado)                      
      32 +    assert str(resultado) == esperado                          
      33 +                                                               
      34 +                                                               
      35 +def test_rn003_negativo_que_arredonda_a_zero_vira_zero_sem_sina
         +l():                                                           
      36 +    resultado = arredondar(Decimal("-0.004"))                  
      37 +    assert resultado == Decimal("0")                           
      38 +    assert not resultado.is_signed()                           
      39 +    assert str(resultado) == "0.00"                            
      40 +                                                               
     … 3 more lines (ctrl+o to expand)

● Bash(sh /tmp/fechar.sh T-004 "arredonda valores para centavos com metade
      afastando do zero" 2>/dev/null)
  ⎿  1f7df07 feat(T-004): arredonda valores para centavos com metade afasta
     ndo do zero
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      46    - **Teste:** `tests/test_rn002_normalizacao.py`
      47    - **Commit:**
      48  
      49 -- [ ] **T-004** — Arredondamento para centavos com a metade se 
         -afastando do zero                                              
      49 +- [x] **T-004** — Arredondamento para centavos com a metade se 
         +afastando do zero                                              
      50    em `normalizacao.py`. `-0.00` vira `0.00`.
      51    - **Atende:** RN-003, AMB-012, DT-001
      52    - **Aceite:** 33,333 → 33,33; 10,005 → 10,01; −10,005 → −10,0
          1; −0,004 → 0,00,

● T-005: parse do JSON.

● Bash(cat > reembolso/entrada.py <<'EOF'
      """Leitura e validação da entrada (etapas 1 e 2 da spec §8; RN-013)."""…)
  ⎿  ......
        [100%]
     6 passed in 0.02s
     … +4 lines (ctrl+o to expand)
  ⎿  Created reembolso\entrada.py (+23 -0)
       1 +"""Leitura e validação da entrada (etapas 1 e 2 da spec §8; RN-
         +013)."""                                                       
       2 +                                                               
       3 +import json                                                    
       4 +from decimal import Decimal                                    
       5 +                                                               
       6 +                                                               
       7 +class EntradaInvalida(Exception):                              
       8 +    """Erro geral da RN-013: o documento inteiro é rejeitado e 
         +não há saída."""                                               
       9 +                                                               
      10 +                                                               
      11 +def _rejeitar_constante(nome: str):                            
      12 +    raise EntradaInvalida(f"documento não é JSON válido: litera
         +l {nome} não é permitido")                                     
      13 +                                                               
      14 +                                                               
      15 +def ler_json(texto: str) -> object:                            
      16 +    """Converte o texto em objetos Python, com números não inte
         +iros como Decimal (DT-001).                                    
      17 +                                                               
      18 +    `NaN`, `Infinity` e `-Infinity` são rejeitados (DT-003).   
      19 +    """                                                        
      20 +    try:                                                       
      21 +        return json.loads(texto, parse_float=Decimal, parse_con
         +stant=_rejeitar_constante)                                     
      22 +    except json.JSONDecodeError as erro:                       
      23 +        raise EntradaInvalida(f"documento não é JSON válido: {e
         +rro}") from erro                                               
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      56  
      57  ## Fase 2 — Entrada (RN-013)
      58  
      59 -- [ ] **T-005** — Parse do JSON em `entrada.py` com números lid
         -os como `Decimal`.                                             
      59 +- [x] **T-005** — Parse do JSON em `entrada.py` com números lid
         +os como `Decimal`.                                             
      60    JSON ilegível, `NaN` e `Infinity` levantam `EntradaInvalida`.
      61    - **Atende:** RN-013 (erro geral: documento ilegível), DT-001
          , DT-003
      62    - **Aceite:** documento não JSON, com `NaN` ou com `Infinity`
           → `EntradaInvalida`;
  ⎿  Created tests\test_rn013_dados_invalidos.py (+31 -0)
       1 +from decimal import Decimal                                    
       2 +                                                               
       3 +import pytest                                                  
       4 +                                                               
       5 +from reembolso.entrada import EntradaInvalida, ler_json        
       6 +                                                               
       7 +                                                               
       8 +def test_rn013_json_invalido_erro_geral():                     
       9 +    with pytest.raises(EntradaInvalida):                       
      10 +        ler_json('{"colaborador": ')                           
      11 +                                                               
      12 +                                                               
      13 +def test_rn013_nan_erro_geral():                               
      14 +    with pytest.raises(EntradaInvalida):                       
      15 +        ler_json('{"valor": NaN}')                             
      16 +                                                               
      17 +                                                               
      18 +@pytest.mark.parametrize("literal", ["Infinity", "-Infinity"]) 
      19 +def test_rn013_infinity_erro_geral(literal):                   
      20 +    with pytest.raises(EntradaInvalida):                       
      21 +        ler_json(f'{{"valor": {literal}}}')                    
      22 +                                                               
      23 +                                                               
      24 +def test_dt001_float_lido_como_decimal():                      
      25 +    valor = ler_json('{"valor": 33.333}')["valor"]             
      26 +    assert isinstance(valor, Decimal)                          
      27 +    assert valor == Decimal("33.333")                          
      28 +                                                               
      29 +                                                               
      30 +def test_dt001_metade_nao_sofre_erro_de_float():               
      31 +    assert ler_json('{"valor": 10.005}')["valor"] == Decimal("1
         +0.005")                                                        

● T-006: validação do documento (erro geral).

● Bash(cat > reembolso/entrada.py <<'EOF'
      """Leitura e validação da entrada (etapas 1 e 2 da spec §8; RN-013)."""…)
  ⎿  ...........................
        [100%]
     27 passed in 0.04s
     … +2 lines (ctrl+o to expand)
  ⎿  Updated reembolso\entrada.py (+68 -0)
       1  """Leitura e validação da entrada (etapas 1 e 2 da spec §8; RN-
          013)."""
       2  
       3  import json
       4 +import re                                                      
       5 +from dataclasses import dataclass                              
       6 +from datetime import date                                      
       7  from decimal import Decimal
       8  
       9 +_FORMATO_DATA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")      
      10 +                                                               
      11  
      12  class EntradaInvalida(Exception):
      13      """Erro geral da RN-013: o documento inteiro é rejeitado e 
          não há saída."""
      14  
      15  
      16 +@dataclass(frozen=True)                                        
      17 +class Cabecalho:                                               
      18 +    """Partes do documento validadas no nível geral (RN-013).""
         +"                                                              
      19 +                                                               
      20 +    colaborador: dict                                          
      21 +    periodo: dict                                              
      22 +    inicio: date                                               
      23 +    fim: date                                                  
      24 +    itens: list[dict]                                          
      25 +                                                               
      26 +                                                               
      27  def _rejeitar_constante(nome: str):
      28      raise EntradaInvalida(f"documento não é JSON válido: litera
          l {nome} não é permitido")
      29  
     ...
      37          return json.loads(texto, parse_float=Decimal, parse_con
          stant=_rejeitar_constante)
      38      except json.JSONDecodeError as erro:
      39          raise EntradaInvalida(f"documento não é JSON válido: {e
          rro}") from erro
      40 +                                                               
      41 +                                                               
      42 +def texto_preenchido(valor: object) -> bool:                   
      43 +    """Texto com ao menos um caractere que não é espaço (RN-013
         +)."""                                                          
      44 +    return isinstance(valor, str) and valor.strip() != ""      
      45 +                                                               
      46 +                                                               
      47 +def data_valida(valor: object) -> date | None:                 
     … 44 more lines (ctrl+o to expand)
  ⎿  Updated tests\test_rn013_dados_invalidos.py (+91 -1)
      1 +from datetime import date                                       
      2  from decimal import Decimal
      3  
      4  import pytest
      5  
      5 -from reembolso.entrada import EntradaInvalida, ler_json         
      6 +from reembolso.entrada import EntradaInvalida, ler_json, validar
        +_documento                                                      
      7  
      8  
      9  def test_rn013_json_invalido_erro_geral():
     ...
       30  
       31  def test_dt001_metade_nao_sofre_erro_de_float():
       32      assert ler_json('{"valor": 10.005}')["valor"] == Decimal("
           10.005")
       33 +                                                              
       34 +                                                              
       35 +def _documento(**alteracoes):                                 
       36 +    doc = {                                                   
       37 +        "colaborador": {"id": "c-0417", "nome": "Marina Volpi"
          +},                                                            
       38 +        "periodo": {"competencia": "2026-07", "inicio": "2026-
          +07-01", "fim": "2026-07-31"},                                 
       39 +        "despesas": [],                                       
       40 +    }                                                         
       41 +    for caminho, valor in alteracoes.items():                 
       42 +        alvo = doc                                            
       43 +        *pais, campo = caminho.split("__")                    
       44 +        for pai in pais:                                      
       45 +            alvo = alvo[pai]                                  
       46 +        if valor is _REMOVER:                                 
       47 +            del alvo[campo]                                   
       48 +        else:                                                 
       49 +            alvo[campo] = valor                               
       50 +    return doc                                                
       51 +                                                              
       52 +                                                              
       53 +_REMOVER = object()                                           
       54 +                                                              
       55 +                                                              
       56 +@pytest.mark.parametrize(                                     
       57 +    "alteracoes",                                             
       58 +    [                                                         
       59 +        {"periodo__fim": _REMOVER},                           
     … 62 more lines (ctrl+o to expand)

● Bash(sh /tmp/fechar.sh T-006 "valida colaborador, periodo e lista de despesas
      como erro geral" 2>/dev/null)
  ⎿  ab4c408 feat(T-006): valida colaborador, periodo e lista de despesas c
     omo erro geral
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      66      `::test_dt001_float_lido_como_decimal`
      67    - **Commit:**
      68  
      69 -- [ ] **T-006** — Validação do documento: `colaborador` e `peri
         -odo` são objetos,                                              
      69 +- [x] **T-006** — Validação do documento: `colaborador` e `peri
         +odo` são objetos,                                              
      70    `colaborador.id` é texto não vazio, `inicio` e `fim` são data
          s válidas
      71    (`AAAA-MM-DD` e existentes no calendário), `inicio ≤ fim`, `d
          espesas` é lista e
      72    todos os itens são objetos. Campos informativos e desconhecid
          os não são validados.

● T-007: validação por despesa.

● Bash(python - <<'EOF'
      p="reembolso/entrada.py"…)
  ⎿  ..............................................................
        [100%]
     62 passed in 0.07s
     … +2 lines (ctrl+o to expand)
  ⎿  Updated reembolso\entrada.py (+150 -91)
        1 -"""Leitura e validação da entrada (etapas 1 e 2 da spec §8; RN
          --013)."""                                                     
        2 -                                                              
        3 -import json                                                   
        4 -import re                                                     
        5 -from dataclasses import dataclass                             
        6 -from datetime import date                                     
        7 -from decimal import Decimal                                   
        8 -                                                              
        9 -_FORMATO_DATA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")     
       10 -                                                              
       11 -                                                              
       12 -class EntradaInvalida(Exception):                             
       13 -    """Erro geral da RN-013: o documento inteiro é rejeitado e
          - não há saída."""                                             
       14 -                                                              
       15 -                                                              
       16 -@dataclass(frozen=True)                                       
       17 -class Cabecalho:                                              
       18 -    """Partes do documento validadas no nível geral (RN-013)."
          -""                                                            
       19 -                                                              
       20 -    colaborador: dict                                         
       21 -    periodo: dict                                             
       22 -    inicio: date                                              
       23 -    fim: date                                                 
       24 -    itens: list[dict]                                         
       25 -                                                              
       26 -                                                              
       27 -def _rejeitar_constante(nome: str):                           
       28 -    raise EntradaInvalida(f"documento não é JSON válido: liter
          -al {nome} não é permitido")                                   
       29 -                                                              
       30 -                                                              
       31 -def ler_json(texto: str) -> object:                           
       32 -    """Converte o texto em objetos Python, com números não int
          -eiros como Decimal (DT-001).                                  
       33 -                                                              
       34 -    `NaN`, `Infinity` e `-Infinity` são rejeitados (DT-003).  
       35 -    """                                                       
       36 -    try:                                                      
       37 -        return json.loads(texto, parse_float=Decimal, parse_co
          -nstant=_rejeitar_constante)                                   
       38 -    except json.JSONDecodeError as erro:                      
       39 -        raise EntradaInvalida(f"documento não é JSON válido: {
          -erro}") from erro                                             
       40 -                                                              
     … 201 more lines (ctrl+o to expand)
  ⎿  Updated tests\test_rn013_dados_invalidos.py (+239 -121)
        1 -from datetime import date                                     
        2 -from decimal import Decimal                                   
        3 -                                                              
        4 -import pytest                                                 
        5 -                                                              
        6 -from reembolso.entrada import EntradaInvalida, ler_json, valid
          -ar_documento                                                  
        7 -                                                              
        8 -                                                              
        9 -def test_rn013_json_invalido_erro_geral():                    
       10 -    with pytest.raises(EntradaInvalida):                      
       11 -        ler_json('{"colaborador": ')                          
       12 -                                                              
       13 -                                                              
       14 -def test_rn013_nan_erro_geral():                              
       15 -    with pytest.raises(EntradaInvalida):                      
       16 -        ler_json('{"valor": NaN}')                            
       17 -                                                              
       18 -                                                              
       19 -@pytest.mark.parametrize("literal", ["Infinity", "-Infinity"])
       20 -def test_rn013_infinity_erro_geral(literal):                  
       21 -    with pytest.raises(EntradaInvalida):                      
       22 -        ler_json(f'{{"valor": {literal}}}')                   
       23 -                                                              
       24 -                                                              
       25 -def test_dt001_float_lido_como_decimal():                     
       26 -    valor = ler_json('{"valor": 33.333}')["valor"]            
       27 -    assert isinstance(valor, Decimal)                         
       28 -    assert valor == Decimal("33.333")                         
       29 -                                                              
       30 -                                                              
       31 -def test_dt001_metade_nao_sofre_erro_de_float():              
       32 -    assert ler_json('{"valor": 10.005}')["valor"] == Decimal("
          -10.005")                                                      
       33 -                                                              
       34 -                                                              
       35 -def _documento(**alteracoes):                                 
       36 -    doc = {                                                   
       37 -        "colaborador": {"id": "c-0417", "nome": "Marina Volpi"
          -},                                                            
       38 -        "periodo": {"competencia": "2026-07", "inicio": "2026-
          -07-01", "fim": "2026-07-31"},                                 
       39 -        "despesas": [],                                       
       40 -    }                                                         
     … 320 more lines (ctrl+o to expand)

● Bash(sh /tmp/fechar.sh T-007 "valida cada despesa e recusa com
      DADOS_INVALIDOS" 2>/dev/null)
  ⎿  0662169 feat(T-007): valida cada despesa e recusa com DADOS_INVALIDOS
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      78    - **Teste:** `tests/test_rn013_dados_invalidos.py::test_rn013
          _erro_geral_*`
      79    - **Commit:**
      80  
      81 -- [ ] **T-007** — Validação de cada despesa: falha produz `Inva
         -lida` com                                                      
      81 +- [x] **T-007** — Validação de cada despesa: falha produz `Inva
         +lida` com                                                      
      82    `DADOS_INVALIDOS`. `id` é nulo quando o problema está no `id`
          ; `valor_informado`
      83    é nulo quando o valor está ausente ou não é numérico; `bool` 
          não é aceito como
      84    número.

● T-008: montagem da Despesa válida e ler_documento.

  Ran 1 shell command (ctrl+o to expand)

● Teste mal escrito (o default=str serializa Decimal como texto). Corrijo o
  teste.

  Ran 1 shell command (ctrl+o to expand)

● Bash(.venv/Scripts/ruff check --fix -q . ; .venv/Scripts/ruff format -q . ;
      .venv/Scripts/python -m pytest -q && .venv/Scripts/ruff check . &&
      .venv/Scripts/ruff for…)
  ⎿  ......................................................................
     .. [ 82%]
     ...............
     … +6 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      91    - **Teste:** `tests/test_rn013_dados_invalidos.py::test_rn013
          _despesa_*`
      92    - **Commit:**
      93  
      94 -- [ ] **T-008** — Montagem da `Despesa` válida: posição (a part
         -ir de 1), categoria                                            
      94 +- [x] **T-008** — Montagem da `Despesa` válida: posição (a part
         +ir de 1), categoria                                            
      95    e fornecedor normalizados, `valor_informado` sem arredondamen
          to e
      96    `valor_considerado` arredondado.
      97    - **Atende:** RN-002, RN-003, spec §4 (posição)
  ⎿  Updated tests\test_rn013_dados_invalidos.py (+1 -2)
       1 +import json                                                    
       2  from datetime import date
       3  from decimal import Decimal
       4  
       5  import pytest
       6  
       6 -import json                                                    
       7 -                                                               
       7  from reembolso.entrada import (
       8      EntradaInvalida,
       9      ler_despesa,

● T-009: motor, tipos de etapa e justificativas.

  Read 1 file (ctrl+o to expand)
● Problema de quoting no heredoc; vou gravar os arquivos com a ferramenta Write.

  Read 2 files, ran 1 shell command (ctrl+o to expand)

● Update(reembolso\modelo.py)
  ⎿  Added 17 lines
      68      status: Status
      69      motivo: Motivo | None
      70      justificativa: str
      71 +                                                               
      72 +                                                               
      73 +@dataclass(frozen=True)                                        
      74 +class Recusa:                                                  
      75 +    """Decisão de uma etapa que recusa a despesa (spec §8).""" 
      76 +                                                               
      77 +    motivo: Motivo                                             
      78 +    justificativa: str                                         
      79 +                                                               
      80 +                                                               
      81 +@dataclass(frozen=True)                                        
      82 +class Corte:                                                   
      83 +    """Decisão de uma etapa em grupo que reduz o valor reembols
         +ável (spec §8, etapa 8)."""                                    
      84 +                                                               
      85 +    valor_reembolsavel: Decimal                                
      86 +    motivo: Motivo                                             
      87 +    justificativa: str                                         

● Write(reembolso\justificativas.py)
  ⎿  Wrote 20 lines to reembolso\justificativas.py
      1 """Textos das justificativas (spec §4, DT-008)."""
      2 
      3 from decimal import Decimal
      4 
      5 
      6 def reais(valor: Decimal) -> str:
      7     """Formata como `R$ 1.234,56`."""
      8     texto = f"{valor:,.2f}".replace(",", "_").replace(".", ",").r
        eplace("_", ".")
      9     return f"R$ {texto}"
     … +12 lines (ctrl+o to expand)

● Write(reembolso\motor.py)
  ⎿  Wrote 111 lines to reembolso\motor.py
       1 """Execução das etapas 3 a 8 da spec §8 sobre as despesas de um 
         documento."""
       2 
       3 from collections.abc import Callable, Sequence
       4 from dataclasses import dataclass
       6 
       7 from reembolso import justificativas
       8 from reembolso.modelo import (
       9     Corte,
      10     Despesa,
     … +123 lines (ctrl+o to expand)

● Write(tests\fabrica.py)
  ⎿  Wrote 50 lines to tests\fabrica.py
       1 """Construtores de objetos do modelo para os testes de regra (pl
         an §6)."""
       2 
       3 from datetime import date
       4 from decimal import Decimal
       6 from reembolso.modelo import Despesa, Documento, Invalida
       7 from reembolso.normalizacao import arredondar, normalizar_texto
       8 
       9 
      10 def despesa(
     … +46 lines (ctrl+o to expand)

● Write(tests\test_motor.py)
  ⎿  Wrote 112 lines to tests\test_motor.py
       1 from decimal import Decimal
       2 
       3 from fabrica import despesa, documento, invalida
       4 
       5 from reembolso.justificativas import reais
       6 from reembolso.modelo import Corte, Motivo, Recusa, Status
       7 from reembolso.motor import EmGrupo, PorItem, calcular
       8 
       9 
      10 def _recusa_posicao(posicao):
     … +110 lines (ctrl+o to expand)

● Bash(.venv/Scripts/ruff check --fix -q . ; .venv/Scripts/ruff format -q . ;
      .venv/Scripts/python -m pytest -q && .venv/Scripts/ruff check . &&
      .venv/Scripts/ruff for…)
  ⎿  E501 Line too long (104 > 100)
       --> tests\test_motor.py:27:101
        |
     … +17 lines (ctrl+o to expand)
  ⎿  Updated tests\test_motor.py (+3 -1)
      24  
      25  def _corta_para(valor):
      26      def regra(vivas, _doc):
      27 -        return {d.posicao: Corte(Decimal(valor), Motivo.LIMITE_
         -DIARIO, "corte (RN-008)") for d in vivas}                      
      27 +        return {                                               
      28 +            d.posicao: Corte(Decimal(valor), Motivo.LIMITE_DIAR
         +IO, "corte (RN-008)") for d in vivas                           
      29 +        }                                                      
      30  
      31      return regra
      32  

● Bash(sh /tmp/fechar.sh T-009 "cria motor com etapas por item e em grupo e
      justificativas" 2>/dev/null && git show --stat HEAD | tail -8)
  ⎿  12a6a4a feat(T-009): cria motor com etapas por item e em grupo e justi
     ficativas
     … +9 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      103  
      104  ## Fase 3 — Regras de negócio
      105  
      106 -- [ ] **T-009** — `motor.py`: lista `ETAPAS` (inicialmente vaz
          -ia), tipos `PorItem`                                          
      106 +- [x] **T-009** — `motor.py`: lista `ETAPAS` (inicialmente vaz
          +ia), tipos `PorItem`                                          
      107    e `EmGrupo`, lista de despesas vivas e status final (`aprova
           do` se
      108    `valor_reembolsavel == valor_considerado`, senão `limitado`)
           . Uma `Invalida`
      109    vira `Resultado` recusado com `DADOS_INVALIDOS`. Cria `justi
           ficativas.py` com a

● T-010: etapa de valor negativo.

● Write(reembolso\etapas.py)
  ⎿  Wrote 13 lines to reembolso\etapas.py
       1 """Uma função por etapa da seção 8 da spec (etapas 3 a 8)."""
       2 
       3 from reembolso import justificativas
       5 
       6 
       7 def valor_negativo(despesa: Despesa, _documento: Documento) -> R
         ecusa | None:
          é válido."""
       9     if despesa.valor_considerado < 0:
      10         return Recusa(
     … +6 lines (ctrl+o to expand)

● Update(reembolso\justificativas.py)
  ⎿  Added 4 lines
      13      return f"Dados inválidos: {detalhe} (RN-013)."
      14  
      15  
      16 +def valor_negativo(valor: Decimal) -> str:                     
      17 +    return f"Valor negativo ({reais(valor)}) não é reembolsável
         + e não abate outras despesas (RN-005)."                        
      18 +                                                               
      19 +                                                               
      20  def aprovado() -> str:
      21      return (
      22          "Despesa aprovada: passou por todas as regras e é reemb
          olsada integralmente "

● Update(reembolso\motor.py)
  ⎿  Added 1 line
       4  from dataclasses import dataclass
       5  from decimal import Decimal
       6  
       7 +from reembolso import etapas as regras                         
       8  from reembolso import justificativas
       9  from reembolso.modelo import (
      10      Corte,

● Update(reembolso\motor.py)
  ⎿  Added 3 lines, removed 1 line
      40  Etapa = PorItem | EmGrupo
      41  
      42  # Ordem das etapas 3 a 8 da spec §8. As etapas 1 e 2 acontecem 
          em entrada.py.
      43 -ETAPAS: list[Etapa] = []                                       
      43 +ETAPAS: list[Etapa] = [                                        
      44 +    PorItem(regras.valor_negativo),  # RN-005 → VALOR_NEGATIVO 
      45 +]                                                              
      46  
      47  
      48  def _decisoes(etapa: Etapa, vivas: list[Despesa], documento: Do
          cumento) -> dict:

● Write(tests\test_rn005_valor_negativo.py)
  ⎿  Wrote 39 lines to tests\test_rn005_valor_negativo.py
       1 from decimal import Decimal
       2 
       3 from fabrica import despesa, documento
       4 
       5 from reembolso.etapas import valor_negativo
       6 from reembolso.modelo import Motivo, Status
       7 from reembolso.motor import calcular
       8 
       9 
      10 def test_rn005_d009_estorno_recusado():
     … +32 lines (ctrl+o to expand)

● Bash(.venv/Scripts/ruff check --fix -q . ; .venv/Scripts/ruff format -q . ;
      .venv/Scripts/python -m pytest -q && .venv/Scripts/ruff check . &&
      .venv/Scripts/ruff for…)
  ⎿  E501 Line too long (102 > 100)
       --> reembolso\justificativas.py:17:101
        |
     … +14 lines (ctrl+o to expand)
  ⎿  Updated reembolso\justificativas.py (+3 -1)
      14  
      15  
      16  def valor_negativo(valor: Decimal) -> str:
      17 -    return f"Valor negativo ({reais(valor)}) não é reembolsável
         - e não abate outras despesas (RN-005)."                        
      17 +    return (                                                   
      18 +        f"Valor negativo ({reais(valor)}) não é reembolsável e 
         +não abate outras despesas (RN-005)."                           
      19 +    )                                                          
      20  
      21  
      22  def aprovado() -> str:
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      115      `::test_secao8_invalida_vira_dados_invalidos`, `::test_sec
           ao8_resultado_na_ordem_da_entrada`
      116    - **Commit:**
      117  
      118 -- [ ] **T-010** — Etapa de valor negativo.                    
      118 +- [x] **T-010** — Etapa de valor negativo.                    
      119    - **Atende:** RN-005, AMB-011
      120    - **Aceite:** d-009 (−45,00) → recusado, 0,00, `VALOR_NEGATI
           VO`; 0,00 → aprovado,
      121      0,00; −0,004 → aprovado, 0,00.

● T-011: etapa de período.

● Bash(python - <<'EOF'
      p="reembolso/justificativas.py"…)
  ⎿  ......................................................................
     .. [ 67%]
     ...................................
     … +6 lines (ctrl+o to expand)
  ⎿  Updated reembolso\etapas.py (+23 -13)
       1 -"""Uma função por etapa da seção 8 da spec (etapas 3 a 8)."""  
       2 -                                                               
       3 -from reembolso import justificativas                           
       4 -from reembolso.modelo import Despesa, Documento, Motivo, Recusa
       5 -                                                               
       6 -                                                               
       7 -def valor_negativo(despesa: Despesa, _documento: Documento) -> 
         -Recusa | None:                                                 
       8 -    """RN-005: valor considerado menor que zero é recusado; zer
         -o é válido."""                                                 
       9 -    if despesa.valor_considerado < 0:                          
      10 -        return Recusa(                                         
      11 -            Motivo.VALOR_NEGATIVO, justificativas.valor_negativ
         -o(despesa.valor_considerado)                                   
      12 -        )                                                      
      13 -    return None                                                
       1 +"""Uma função por etapa da seção 8 da spec (etapas 3 a 8)."""  
       2 +                                                               
       3 +from reembolso import justificativas                           
       4 +from reembolso.modelo import Despesa, Documento, Motivo, Recusa
       5 +                                                               
       6 +                                                               
       7 +def valor_negativo(despesa: Despesa, _documento: Documento) -> 
         +Recusa | None:                                                 
       8 +    """RN-005: valor considerado menor que zero é recusado; zer
         +o é válido."""                                                 
       9 +    if despesa.valor_considerado < 0:                          
      10 +        return Recusa(                                         
      11 +            Motivo.VALOR_NEGATIVO, justificativas.valor_negativ
         +o(despesa.valor_considerado)                                   
      12 +        )                                                      
      13 +    return None                                                
      14 +                                                               
      15 +                                                               
      16 +def periodo(despesa: Despesa, documento: Documento) -> Recusa |
         + None:                                                         
      17 +    """RN-004: a data deve estar entre início e fim, bordas inc
         +luídas; competência não é usada."""                            
      18 +    if documento.inicio <= despesa.data <= documento.fim:      
      19 +        return None                                            
      20 +    return Recusa(                                             
      21 +        Motivo.FORA_DO_PERIODO,                                
      22 +        justificativas.fora_do_periodo(despesa.data, documento.
         +inicio, documento.fim),                                        
      23 +    )                                                          
  ⎿  Updated reembolso\justificativas.py (+31 -26)
       1 -"""Textos das justificativas (spec §4, DT-008)."""             
       2 -                                                               
       3 -from decimal import Decimal                                    
       4 -                                                               
       5 -                                                               
       6 -def reais(valor: Decimal) -> str:                              
       7 -    """Formata como `R$ 1.234,56`."""                          
       8 -    texto = f"{valor:,.2f}".replace(",", "_").replace(".", ",")
         -.replace("_", ".")                                             
       9 -    return f"R$ {texto}"                                       
      10 -                                                               
      11 -                                                               
      12 -def dados_invalidos(detalhe: str) -> str:                      
      13 -    return f"Dados inválidos: {detalhe} (RN-013)."             
      14 -                                                               
      15 -                                                               
      16 -def valor_negativo(valor: Decimal) -> str:                     
      17 -    return (                                                   
      18 -        f"Valor negativo ({reais(valor)}) não é reembolsável e 
         -não abate outras despesas (RN-005)."                           
      19 -    )                                                          
      20 -                                                               
      21 -                                                               
      22 -def aprovado() -> str:                                         
      23 -    return (                                                   
      24 -        "Despesa aprovada: passou por todas as regras e é reemb
         -olsada integralmente "                                         
      25 -        "(RN-001, RN-004 a RN-008)."                           
      26 -    )                                                          
       1 +"""Textos das justificativas (spec §4, DT-008)."""             
       2 +                                                               
       3 +from datetime import date                                      
       4 +from decimal import Decimal                                    
       5 +                                                               
       6 +                                                               
       7 +def reais(valor: Decimal) -> str:                              
       8 +    """Formata como `R$ 1.234,56`."""                          
       9 +    texto = f"{valor:,.2f}".replace(",", "_").replace(".", ",")
         +.replace("_", ".")                                             
      10 +    return f"R$ {texto}"                                       
      11 +                                                               
      12 +                                                               
      13 +def dados_invalidos(detalhe: str) -> str:                      
      14 +    return f"Dados inválidos: {detalhe} (RN-013)."             
     … 17 more lines (ctrl+o to expand)
  ⎿  Updated reembolso\motor.py (+115 -114)
        1 -"""Execução das etapas 3 a 8 da spec §8 sobre as despesas de u
          -m documento."""                                               
        2 -                                                              
        3 -from collections.abc import Callable, Sequence                
        4 -from dataclasses import dataclass                             
        5 -from decimal import Decimal                                   
        6 -                                                              
        7 -from reembolso import etapas as regras                        
        8 -from reembolso import justificativas                          
        9 -from reembolso.modelo import (                                
       10 -    Corte,                                                    
       11 -    Despesa,                                                  
       12 -    Documento,                                                
       13 -    Invalida,                                                 
       14 -    Motivo,                                                   
       15 -    Recusa,                                                   
       16 -    Resultado,                                                
       17 -    Status,                                                   
       18 -)                                                             
       19 -                                                              
       20 -ZERO = Decimal("0.00")                                        
       21 -                                                              
       22 -                                                              
       23 -@dataclass(frozen=True)                                       
       24 -class PorItem:                                                
       25 -    """Etapa que decide sobre cada despesa isoladamente: `None
          -` (passa) ou `Recusa`."""                                     
       26 -                                                              
       27 -    regra: Callable[[Despesa, Documento], Recusa | None]      
       28 -                                                              
       29 -                                                              
       30 -@dataclass(frozen=True)                                       
       31 -class EmGrupo:                                                
       32 -    """Etapa que recebe todas as despesas vivas, em ordem de p
          -osição, e decide sobre o conjunto.                            
       33 -                                                              
       34 -    Devolve as decisões indexadas pela posição; despesas ausen
          -tes do dicionário passam.                                     
       35 -    """                                                       
       36 -                                                              
       37 -    regra: Callable[[list[Despesa], Documento], dict[int, Recu
          -sa | Corte]]                                                  
       38 -                                                              
       39 -                                                              
       40 -Etapa = PorItem | EmGrupo                                     
     … 189 more lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      122    - **Teste:** `tests/test_rn005_valor_negativo.py`
      123    - **Commit:**
      124  
      125 -- [ ] **T-011** — Etapa de período, com as bordas incluídas. `
          -competencia` não é                                            
      125 +- [x] **T-011** — Etapa de período, com as bordas incluídas. `
          +competencia` não é                                            
      126    usada.
      127    - **Atende:** RN-004, AMB-009
      128    - **Aceite:** d-008 (2026-04-15) → `FORA_DO_PERIODO`; data i
           gual a `inicio` e
  ⎿  Created tests\test_rn004_periodo.py (+35 -0)
       1 +from dataclasses import replace                                
       2 +from decimal import Decimal                                    
       3 +                                                               
       4 +import pytest                                                  
       5 +from fabrica import despesa, documento                         
       6 +                                                               
       7 +from reembolso.etapas import periodo                           
       8 +from reembolso.modelo import Motivo, Status                    
       9 +from reembolso.motor import calcular                           
      10 +                                                               
      11 +                                                               
      12 +def test_rn004_d008_antes_do_periodo_recusada():               
      13 +    d008 = despesa(1, id="d-008", data="2026-04-15", valor="41.
         +00")                                                           
      14 +    item = calcular(documento(d008))[0]                        
      15 +    assert item.status == Status.RECUSADO                      
      16 +    assert item.motivo == Motivo.FORA_DO_PERIODO               
      17 +    assert item.valor_reembolsavel == Decimal("0.00")          
      18 +    assert "RN-004" in item.justificativa                      
      19 +                                                               
      20 +                                                               
      21 +def test_rn004_depois_do_periodo_recusada():                   
      22 +    assert calcular(documento(despesa(1, data="2026-08-01")))[0
         +].motivo == Motivo.FORA_DO_PERIODO                             
      23 +                                                               
      24 +                                                               
      25 +@pytest.mark.parametrize(                                      
      26 +    "data", ["2026-07-01", "2026-07-31"], ids=["primeiro_dia", 
         +"d-014_ultimo_dia"]                                            
      27 +)                                                              
      28 +def test_rn004_bordas_incluidas(data):                         
      29 +    assert periodo(despesa(1, data=data), documento()) is None 
      30 +                                                               
      31 +                                                               
      32 +def test_rn004_competencia_divergente_nao_muda_resultado():    
      33 +    doc = documento(despesa(1, data="2026-07-10"), despesa(2, d
         +ata="2026-04-15"))                                             
      34 +    divergente = replace(doc, periodo={**doc.periodo, "competen
         +cia": "2026-04"})                                              
      35 +    assert calcular(divergente) == calcular(doc)               

● T-012: categoria e politica.py.

● Bash(cat > reembolso/politica.py <<'EOF'
      """Valores da política de reembolso, como dados (plan §4, DT-004)."""…)
  ⎿  ......................................................................
     .. [ 61%]
     .............................................
     … +5 lines (ctrl+o to expand)
  ⎿  Updated reembolso\etapas.py (+11 -1)
      1  """Uma função por etapa da seção 8 da spec (etapas 3 a 8)."""
      2  
      3 -from reembolso import justificativas                            
      3 +from reembolso import justificativas, politica                  
      4  from reembolso.modelo import Despesa, Documento, Motivo, Recusa
      5  
      6  
     ...
      21          Motivo.FORA_DO_PERIODO,
      22          justificativas.fora_do_periodo(despesa.data, documento.
          inicio, documento.fim),
      23      )
      24 +                                                               
      25 +                                                               
      26 +def categoria(despesa: Despesa, _documento: Documento) -> Recus
         +a | None:                                                      
      27 +    """RN-001: só categorias da lista fechada, comparadas após 
         +normalização (RN-002)."""                                      
      28 +    if despesa.categoria in politica.CATEGORIAS_REEMBOLSAVEIS: 
      29 +        return None                                            
      30 +    return Recusa(                                             
      31 +        Motivo.CATEGORIA_NAO_REEMBOLSAVEL,                     
      32 +        justificativas.categoria_nao_reembolsavel(despesa.categ
         +oria),                                                         
      33 +    )                                                          
  ⎿  Updated reembolso\justificativas.py (+4 -0)
      24      return f"Data {data} fora do período de {inicio} a {fim} (R
          N-004)."
      25  
      26  
      27 +def categoria_nao_reembolsavel(categoria: str) -> str:         
      28 +    return f"Categoria '{categoria}' não é reembolsável pela po
         +lítica (RN-001)."                                              
      29 +                                                               
      30 +                                                               
      31  def aprovado() -> str:
      32      return (
      33          "Despesa aprovada: passou por todas as regras e é reemb
          olsada integralmente "
  ⎿  Updated reembolso\motor.py (+1 -0)
      43  ETAPAS: list[Etapa] = [
      44      PorItem(regras.valor_negativo),  # RN-005 → VALOR_NEGATIVO
      45      PorItem(regras.periodo),  # RN-004 → FORA_DO_PERIODO
      46 +    PorItem(regras.categoria),  # RN-001 → CATEGORIA_NAO_REEMBO
         +LSAVEL                                                         
      47  ]
      48  
      49  
  ⎿  Created reembolso\politica.py (+4 -0)
      1 +"""Valores da política de reembolso, como dados (plan §4, DT-004
        +)."""                                                           
      2 +                                                                
      3 +# RN-001: lista fechada de categorias reembolsáveis, já normaliz
        +adas (RN-002).                                                  
      4 +CATEGORIAS_REEMBOLSAVEIS = frozenset({"alimentacao", "transporte
        +_urbano", "hospedagem"})                                        
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      131    - **Teste:** `tests/test_rn004_periodo.py`
      132    - **Commit:**
      133  
      134 -- [ ] **T-012** — Etapa de categoria + `CATEGORIAS_REEMBOLSAVE
          -IS` em `politica.py`.                                         
      134 +- [x] **T-012** — Etapa de categoria + `CATEGORIAS_REEMBOLSAVE
          +IS` em `politica.py`.                                         
      135    - **Atende:** RN-001, AMB-014
      136    - **Aceite:** d-005 (`coworking`) → recusado, 0,00, `CATEGOR
           IA_NAO_REEMBOLSAVEL`;
      137      `ALIMENTACAO` → aceita.
  ⎿  … 1 more file changed

● T-013: duplicatas.

● Bash(python - <<'EOF'
      p="reembolso/justificativas.py"…)
  ⎿  ......................................................................
     .. [ 57%]
     ......................................................
     … +4 lines (ctrl+o to expand)
  ⎿  Updated reembolso\etapas.py (+25 -0)
      1  """Uma função por etapa da seção 8 da spec (etapas 3 a 8)."""
      2  
      3 +from collections import defaultdict                             
      4 +                                                                
      5  from reembolso import justificativas, politica
      6  from reembolso.modelo import Despesa, Documento, Motivo, Recusa
      7  
     ...
      33          Motivo.CATEGORIA_NAO_REEMBOLSAVEL,
      34          justificativas.categoria_nao_reembolsavel(despesa.categ
          oria),
      35      )
      36 +                                                               
      37 +                                                               
      38 +def duplicatas(vivas: list[Despesa], _documento: Documento) -> 
         +dict[int, Recusa]:                                             
      39 +    """RN-006: agrupa por data, categoria, fornecedor e valor c
         +onsiderado e mantém uma por grupo.                             
      40 +                                                               
      41 +    Fica a de menor posição entre as que têm nota fiscal; se ne
         +nhuma tiver, a de menor                                        
      42 +    posição. `vivas` chega em ordem de posição.                
      43 +    """                                                        
      44 +    grupos: dict[tuple, list[Despesa]] = defaultdict(list)     
      45 +    for despesa in vivas:                                      
      46 +        chave = (despesa.data, despesa.categoria, despesa.forne
         +cedor, despesa.valor_considerado)                              
      47 +        grupos[chave].append(despesa)                          
      48 +                                                               
      49 +    recusas: dict[int, Recusa] = {}                            
      50 +    for grupo in grupos.values():                              
      51 +        com_nota = [d for d in grupo if d.tem_nota_fiscal]     
      52 +        mantida = (com_nota or grupo)[0]                       
      53 +        for despesa in grupo:                                  
      54 +            if despesa is not mantida:                         
      55 +                recusas[despesa.posicao] = Recusa(             
      56 +                    Motivo.DUPLICATA, justificativas.duplicata(
         +mantida.id)                                                    
      57 +                )                                              
      58 +    return recusas                                             
  ⎿  Updated reembolso\justificativas.py (+7 -0)
      28      return f"Categoria '{categoria}' não é reembolsável pela po
          lítica (RN-001)."
      29  
      30  
      31 +def duplicata(id_mantida: str) -> str:                         
      32 +    return (                                                   
      33 +        f"Duplicata de {id_mantida} (mesma data, categoria, for
         +necedor e valor); "                                            
      34 +        f"mantida {id_mantida} (RN-006)."                      
      35 +    )                                                          
      36 +                                                               
      37 +                                                               
      38  def aprovado() -> str:
      39      return (
      40          "Despesa aprovada: passou por todas as regras e é reemb
          olsada integralmente "
  ⎿  Updated reembolso\motor.py (+1 -0)
      44      PorItem(regras.valor_negativo),  # RN-005 → VALOR_NEGATIVO
      45      PorItem(regras.periodo),  # RN-004 → FORA_DO_PERIODO
      46      PorItem(regras.categoria),  # RN-001 → CATEGORIA_NAO_REEMBO
          LSAVEL
      47 +    EmGrupo(regras.duplicatas),  # RN-006 → DUPLICATA          
      48  ]
      49  
      50  
  ⎿  Created tests\test_rn006_duplicatas.py (+87 -0)
       1 +from decimal import Decimal                                    
       2 +                                                               
       3 +from fabrica import despesa, documento, invalida               
       4 +                                                               
       5 +from reembolso.modelo import Motivo, Status                    
       6 +from reembolso.motor import calcular                           
       7 +                                                               
       8 +                                                               
       9 +def _bistro(posicao, id, **campos):                            
      10 +    base = {"data": "2026-07-09", "fornecedor": "Bistro Central
         +", "valor": "54.90"}                                           
      11 +    return despesa(posicao, id=id, **{**base, **campos})       
      12 +                                                               
      13 +                                                               
      14 +def test_rn006_d006_d007_ambas_com_nota_mantem_a_primeira():   
      15 +    d006, d007 = calcular(documento(_bistro(1, "d-006"), _bistr
         +o(2, "d-007")))                                                
      16 +    assert d006.status == Status.APROVADO                      
      17 +    assert d006.valor_reembolsavel == Decimal("54.90")         
      18 +    assert d007.status == Status.RECUSADO                      
      19 +    assert d007.motivo == Motivo.DUPLICATA                     
      20 +    assert d007.valor_reembolsavel == Decimal("0.00")          
      21 +    assert "RN-006" in d007.justificativa                      
      22 +    assert "d-006" in d007.justificativa                       
      23 +                                                               
      24 +                                                               
      25 +def test_rn006_so_a_segunda_tem_nota_mantem_a_segunda():       
      26 +    primeira, segunda = calcular(                              
      27 +        documento(_bistro(1, "a", tem_nota_fiscal=False), _bist
         +ro(2, "b", tem_nota_fiscal=True))                              
      28 +    )                                                          
      29 +    assert primeira.motivo == Motivo.DUPLICATA                 
      30 +    assert "b" in primeira.justificativa                       
      31 +    assert segunda.status == Status.APROVADO                   
      32 +                                                               
      33 +                                                               
      34 +def test_rn006_nenhuma_com_nota_mantem_a_primeira():           
      35 +    primeira, segunda = calcular(                              
      36 +        documento(_bistro(1, "a", tem_nota_fiscal=False), _bist
         +ro(2, "b", tem_nota_fiscal=False))                             
      37 +    )                                                          
      38 +    assert primeira.status == Status.APROVADO                  
      39 +    assert segunda.motivo == Motivo.DUPLICATA                  
      40 +                                                               
     … 47 more lines (ctrl+o to expand)

● Reforço as checagens de id na justificativa (o "b" é fraco demais).

● Bash(python - <<'EOF'
      p="tests/test_rn006_duplicatas.py"…)  ⎿  30:    assert "d-b" in primeira.justificativa
     51:    assert all("d-b" in r.justificativa for r in (resultados[0], re
     sultados[2]))
     … +11 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      138    - **Teste:** `tests/test_rn001_categoria.py`
      139    - **Commit:**
      140  
      141 -- [ ] **T-013** — Etapa de duplicatas (mesma data, categoria n
          -ormalizada,                                                   
      141 +- [x] **T-013** — Etapa de duplicatas (mesma data, categoria n
          +ormalizada,                                                   
      142    fornecedor normalizado e `valor_considerado`). É mantida a d
           e menor posição
      143    entre as que têm nota; se nenhuma tiver nota, a de menor pos
           ição.
      144    - **Atende:** RN-006, AMB-010
  ⎿  Updated tests\test_rn006_duplicatas.py (+92 -87)
       1 -from decimal import Decimal                                    
       2 -                                                               
       3 -from fabrica import despesa, documento, invalida               
       4 -                                                               
       5 -from reembolso.modelo import Motivo, Status                    
       6 -from reembolso.motor import calcular                           
       7 -                                                               
       8 -                                                               
       9 -def _bistro(posicao, id, **campos):                            
      10 -    base = {"data": "2026-07-09", "fornecedor": "Bistro Central
         -", "valor": "54.90"}                                           
      11 -    return despesa(posicao, id=id, **{**base, **campos})       
      12 -                                                               
      13 -                                                               
      14 -def test_rn006_d006_d007_ambas_com_nota_mantem_a_primeira():   
      15 -    d006, d007 = calcular(documento(_bistro(1, "d-006"), _bistr
         -o(2, "d-007")))                                                
      16 -    assert d006.status == Status.APROVADO                      
      17 -    assert d006.valor_reembolsavel == Decimal("54.90")         
      18 -    assert d007.status == Status.RECUSADO                      
      19 -    assert d007.motivo == Motivo.DUPLICATA                     
      20 -    assert d007.valor_reembolsavel == Decimal("0.00")          
      21 -    assert "RN-006" in d007.justificativa                      
      22 -    assert "d-006" in d007.justificativa                       
      23 -                                                               
      24 -                                                               
      25 -def test_rn006_so_a_segunda_tem_nota_mantem_a_segunda():       
      26 -    primeira, segunda = calcular(                              
      27 -        documento(_bistro(1, "a", tem_nota_fiscal=False), _bist
         -ro(2, "b", tem_nota_fiscal=True))                              
      28 -    )                                                          
      29 -    assert primeira.motivo == Motivo.DUPLICATA                 
      30 -    assert "b" in primeira.justificativa                       
      31 -    assert segunda.status == Status.APROVADO                   
      32 -                                                               
      33 -                                                               
      34 -def test_rn006_nenhuma_com_nota_mantem_a_primeira():           
      35 -    primeira, segunda = calcular(                              
      36 -        documento(_bistro(1, "a", tem_nota_fiscal=False), _bist
         -ro(2, "b", tem_nota_fiscal=False))                             
      37 -    )                                                          
      38 -    assert primeira.status == Status.APROVADO                  
      39 -    assert segunda.motivo == Motivo.DUPLICATA                  
      40 -                                                               
     … 139 more lines (ctrl+o to expand)

● T-014: nota fiscal.

● Bash(python - <<'EOF'
      p="reembolso/politica.py"…)
  ⎿  ......................................................................
     .. [ 54%]
     ............................................................
     … +5 lines (ctrl+o to expand)
  ⎿  Updated reembolso\etapas.py (+10 -0)
      56                      Motivo.DUPLICATA, justificativas.duplicata(
          mantida.id)
      57                  )
      58      return recusas
      59 +                                                               
      60 +                                                               
      61 +def nota_fiscal(despesa: Despesa, _documento: Documento) -> Rec
         +usa | None:                                                    
      62 +    """RN-007: valor da própria despesa acima do limiar e sem n
         +ota é recusado inteiro."""                                     
      63 +    if despesa.valor_considerado > politica.LIMIAR_NOTA_FISCAL 
         +and not despesa.tem_nota_fiscal:                               
      64 +        return Recusa(                                         
      65 +            Motivo.NOTA_FISCAL_AUSENTE,                        
      66 +            justificativas.nota_fiscal_ausente(politica.LIMIAR_
         +NOTA_FISCAL),                                                  
      67 +        )                                                      
      68 +    return None                                                
  ⎿  Updated reembolso\justificativas.py (+4 -0)
      35      )
      36  
      37  
      38 +def nota_fiscal_ausente(limiar: Decimal) -> str:               
      39 +    return f"Valor acima de {reais(limiar)} sem nota fiscal (RN
         +-007)."                                                        
      40 +                                                               
      41 +                                                               
      42  def aprovado() -> str:
      43      return (
      44          "Despesa aprovada: passou por todas as regras e é reemb
          olsada integralmente "
  ⎿  Updated reembolso\motor.py (+1 -0)
      45      PorItem(regras.periodo),  # RN-004 → FORA_DO_PERIODO
      46      PorItem(regras.categoria),  # RN-001 → CATEGORIA_NAO_REEMBO
          LSAVEL
      47      EmGrupo(regras.duplicatas),  # RN-006 → DUPLICATA
      48 +    PorItem(regras.nota_fiscal),  # RN-007 → NOTA_FISCAL_AUSENT
         +E                                                              
      49  ]
      50  
      51  
  ⎿  Updated reembolso\politica.py (+9 -4)
      1 -"""Valores da política de reembolso, como dados (plan §4, DT-004
        -)."""                                                           
      2 -                                                                
      3 -# RN-001: lista fechada de categorias reembolsáveis, já normaliz
        -adas (RN-002).                                                  
      4 -CATEGORIAS_REEMBOLSAVEIS = frozenset({"alimentacao", "transporte
        -_urbano", "hospedagem"})                                        
      1 +"""Valores da política de reembolso, como dados (plan §4, DT-004
        +)."""                                                           
      2 +                                                                
      3 +from decimal import Decimal                                     
      4 +                                                                
      5 +# RN-001: lista fechada de categorias reembolsáveis, já normaliz
        +adas (RN-002).                                                  
      6 +CATEGORIAS_REEMBOLSAVEIS = frozenset({"alimentacao", "transporte
        +_urbano", "hospedagem"})                                        
      7 +                                                                
      8 +# RN-007: exige nota fiscal quando o valor considerado é estrita
        +mente maior que o limiar.                                       
      9 +LIMIAR_NOTA_FISCAL = Decimal("100.00")                          
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      149    - **Teste:** `tests/test_rn006_duplicatas.py`
      150    - **Commit:**
      151  
      152 -- [ ] **T-014** — Etapa de nota fiscal + `LIMIAR_NOTA_FISCAL` 
          -em `politica.py`.                                             
      152 +- [x] **T-014** — Etapa de nota fiscal + `LIMIAR_NOTA_FISCAL` 
          +em `politica.py`.                                             
      153    - **Atende:** RN-007, AMB-004, AMB-005
      154    - **Aceite:** d-003 (100,00, sem nota) → passa; d-004 (100,0
           1, sem nota) e d-013
      155      (690,00, sem nota) → recusado, 0,00, `NOTA_FISCAL_AUSENTE`
           ; 150,00 com nota →
  ⎿  … 1 more file changed

● T-015: limites por data e categoria.

  Ran 1 shell command (ctrl+o to expand)

● Mesmo problema de quoting do shell; separo em Write + script Python.

  Read 3 files, ran 1 shell command (ctrl+o to expand)

● Update(reembolso\politica.py)
  ⎿  Added 7 lines
       7  
       8  # RN-007: exige nota fiscal quando o valor considerado é estrit
          amente maior que o limiar.
       9  LIMIAR_NOTA_FISCAL = Decimal("100.00")
      10 +                                                               
      11 +# RN-008: limite da soma reembolsada por combinação de data e c
         +ategoria.                                                      
      12 +LIMITE_POR_DATA = {                                            
      13 +    "alimentacao": Decimal("60.00"),                           
      14 +    "transporte_urbano": Decimal("80.00"),                     
      15 +    "hospedagem": Decimal("250.00"),                           
      16 +}                                                              

● Update(reembolso\justificativas.py)
  ⎿  Added 6 lines
       3  from datetime import date
       4  from decimal import Decimal
       5  
       6 +_NOMES_CATEGORIA = {                                           
       7 +    "alimentacao": "alimentação",                              
       8 +    "transporte_urbano": "transporte urbano",                  
       9 +    "hospedagem": "hospedagem",                                
      10 +}                                                              
      11  
      12 +                                                               
      13  def reais(valor: Decimal) -> str:
      14      """Formata como `R$ 1.234,56`."""
      15      texto = f"{valor:,.2f}".replace(",", "_").replace(".", ",")
          .replace("_", ".")

● Update(reembolso\justificativas.py)
  ⎿  Added 8 lines
      45      return f"Valor acima de {reais(limiar)} sem nota fiscal (RN
          -007)."
      46  
      47  
      48 +def limite_diario(categoria: str, limite: Decimal, excedente: D
         +ecimal) -> str:                                                
      49 +    nome = _NOMES_CATEGORIA.get(categoria, categoria)          
      50 +    return (                                                   
      51 +        f"Limite diário de {nome} de {reais(limite)} aplicado; 
         +"                                                              
      52 +        f"excedente de {reais(excedente)} cortado (RN-008, RN-0
         +10)."                                                          
      53 +    )                                                          
      54 +                                                               
      55 +                                                               
      56  def aprovado() -> str:
      57      return (
      58          "Despesa aprovada: passou por todas as regras e é reemb
          olsada integralmente "

● Update(reembolso\etapas.py)
  ⎿  Added 2 lines, removed 1 line
       1  """Uma função por etapa da seção 8 da spec (etapas 3 a 8)."""
       2  
       3  from collections import defaultdict
       4 +from decimal import Decimal                                    
       5  
       6  from reembolso import justificativas, politica
       6 -from reembolso.modelo import Despesa, Documento, Motivo, Recusa
       7 +from reembolso.modelo import Corte, Despesa, Documento, Motivo,
         + Recusa                                                        
       8  
       9  
      10  def valor_negativo(despesa: Despesa, _documento: Documento) -> 
          Recusa | None:

● Update(reembolso\etapas.py)
  ⎿  Added 25 lines
      67              justificativas.nota_fiscal_ausente(politica.LIMIAR_
          NOTA_FISCAL),
      68          )
      69      return None
      70 +                                                               
      71 +                                                               
      72 +def limites_por_data(vivas: list[Despesa], _documento: Document
         +o) -> dict[int, Corte]:                                        
      73 +    """RN-008, RN-009, RN-010: limite por data e categoria, con
         +sumido na ordem da posição.                                    
      74 +                                                               
      75 +    Cada despesa recebe o menor valor entre o seu valor conside
         +rado e o saldo deixado                                         
      76 +    pelas anteriores; o excedente é cortado. `vivas` chega em o
         +rdem de posição.                                               
      77 +    """                                                        
      78 +    saldos: dict[tuple, Decimal] = {}                          
      79 +    cortes: dict[int, Corte] = {}                              
      80 +    for despesa in vivas:                                      
      81 +        limite = politica.LIMITE_POR_DATA[despesa.categoria]   
      82 +        chave = (despesa.data, despesa.categoria)              
      83 +        saldo = saldos.get(chave, limite)                      
      84 +        reembolsavel = min(despesa.valor_considerado, saldo)   
      85 +        saldos[chave] = saldo - reembolsavel                   
      86 +        if reembolsavel < despesa.valor_considerado:           
      87 +            cortes[despesa.posicao] = Corte(                   
      88 +                reembolsavel,                                  
      89 +                Motivo.LIMITE_DIARIO,                          
      90 +                justificativas.limite_diario(                  
      91 +                    despesa.categoria, limite, despesa.valor_co
         +nsiderado - reembolsavel                                       
      92 +                ),                                             
      93 +            )                                                  
      94 +    return cortes                                              

● Update(reembolso\motor.py)
  ⎿  Added 1 line
      46      PorItem(regras.categoria),  # RN-001 → CATEGORIA_NAO_REEMBO
          LSAVEL
      47      EmGrupo(regras.duplicatas),  # RN-006 → DUPLICATA
      48      PorItem(regras.nota_fiscal),  # RN-007 → NOTA_FISCAL_AUSENT
          E
      49 +    EmGrupo(regras.limites_por_data),  # RN-008, RN-009, RN-010
         + → LIMITE_DIARIO                                               
      50  ]
      51  
      52  

● Agora os três arquivos de teste da T-015.

● Write(tests\test_rn008_limites.py)
  ⎿  Wrote 87 lines to tests\test_rn008_limites.py
       1 from decimal import Decimal
       2 
       3 import pytest
       4 from fabrica import despesa, documento
       5 
       6 from reembolso.modelo import Motivo, Status
       7 from reembolso.motor import calcular
       8 
       9 
      10 @pytest.mark.parametrize(
     … +92 lines (ctrl+o to expand)

● Write(tests\test_rn009_distribuicao.py)
  ⎿  Wrote 57 lines to tests\test_rn009_distribuicao.py
       1 from decimal import Decimal
       2 
       3 from fabrica import despesa, documento
       4 
       5 from reembolso.modelo import Motivo, Status
       6 from reembolso.motor import calcular
       7 
       8 
       9 def test_rn009_d001_d002_consumo_pela_posicao():
      10     d001, d002 = calcular(
     … +51 lines (ctrl+o to expand)

● Write(tests\test_rn010_parcial.py)
  ⎿  Wrote 22 lines to tests\test_rn010_parcial.py
       1 from decimal import Decimal
       2 
       3 from fabrica import despesa, documento
       4 
       5 from reembolso.modelo import Motivo, Status
       7 
       8 
       9 def test_rn010_d014_reembolsada_ate_o_limite():
      10     d014 = despesa(1, id="d-014", data="2026-07-31", categoria="
         ALIMENTACAO", valor="61.00")
     … +13 lines (ctrl+o to expand)

● Simplifico o teste parametrizado (o desvio para hospedagem é desnecessário, a
  fábrica já usa nota fiscal).

● Update(tests\test_rn008_limites.py)
  ⎿  Removed 5 lines
      15      no_limite, acima = calcular(
      16          documento(
      17              despesa(1, data="2026-07-10", categoria=categoria, 
          valor=limite),
      18 -            despesa(2, data="2026-07-11", categoria=categoria, 
         -valor="99.00"),                                                
      19 -        )                                                      
      20 -        if categoria != "hospedagem"                           
      21 -        else documento(                                        
      22 -            despesa(1, data="2026-07-10", categoria=categoria, 
         -valor=limite),                                                 
      18              despesa(2, data="2026-07-11", categoria=categoria, 
          valor="999.00"),
      19          )
      20      )

● Bash(.venv/Scripts/ruff check --fix -q . ; .venv/Scripts/ruff format -q . ;
      .venv/Scripts/python -m pytest -q && .venv/Scripts/ruff check . &&
      .venv/Scripts/ruff for…)
  ⎿  E501 Line too long (106 > 100)
       --> tests\test_rn008_limites.py:69:101
        |
     … +18 lines (ctrl+o to expand)
  ⎿  Updated tests\test_rn008_limites.py (+3 -1)
      66  
      67  
      68  def test_rn008_d003_recebe_limite_inteiro_com_d004_recusada():
      69 -    r003, r004 = calcular(documento(_transporte(1, "d-003", "10
         -0.00"), _transporte(2, "d-004", "100.01")))                    
      69 +    r003, r004 = calcular(                                     
      70 +        documento(_transporte(1, "d-003", "100.00"), _transport
         +e(2, "d-004", "100.01"))                                       
      71 +    )                                                          
      72      assert r003.valor_reembolsavel == Decimal("80.00")
      73      assert r003.status == Status.LIMITADO
      74      assert r004.motivo == Motivo.NOTA_FISCAL_AUSENTE

● Bash(sh /tmp/fechar.sh T-015 "aplica limite por data e categoria na ordem da
      posicao" 2>/dev/null)
  ⎿  7b9463a feat(T-015): aplica limite por data e categoria na ordem da po
     sicao
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      157    - **Teste:** `tests/test_rn007_nota_fiscal.py`
      158    - **Commit:**
      159  
      160 -- [ ] **T-015** — Etapa de limites por data e categoria, com o
          - limite consumido na                                          
      160 +- [x] **T-015** — Etapa de limites por data e categoria, com o
          + limite consumido na                                          
      161    ordem das posições e o excedente cortado + `LIMITE_POR_DATA`
            em `politica.py`.
      162    - **Atende:** RN-008, RN-009, RN-010, AMB-001, AMB-002, AMB-
           003, AMB-008
      163    - **Aceite:** d-001 + d-002 → 60,00 + 0,00; d-010 (480,00) →
            250,00, `limitado`;

● T-016: justificativa de LIMITE_DIARIO com consumo e ids.

● Update(reembolso\justificativas.py)
  ⎿  Added 25 lines, removed 3 lines
      45      return f"Valor acima de {reais(limiar)} sem nota fiscal (RN
          -007)."
      46  
      47  
      48 -def limite_diario(categoria: str, limite: Decimal, excedente: D
         -ecimal) -> str:                                                
      48 +def _enumerar(ids: list[str]) -> str:                          
      49 +    if len(ids) == 1:                                          
      50 +        return ids[0]                                          
      51 +    return f"{', '.join(ids[:-1])} e {ids[-1]}"                
      52 +                                                               
      53 +                                                               
      54 +def limite_diario(                                             
      55 +    categoria: str,                                            
      56 +    limite: Decimal,                                           
      57 +    data: date,                                                
      58 +    consumido: Decimal,                                        
      59 +    consumidoras: list[str],                                   
      60 +    excedente: Decimal,                                        
      61 +) -> str:                                                      
      62 +    """Cita o limite e, se houver, o valor já consumido no dia 
         +e quem o consumiu (spec §4)."""                                
      63      nome = _NOMES_CATEGORIA.get(categoria, categoria)
      64 +    if not consumidoras:                                       
      65 +        return (                                               
      66 +            f"Limite diário de {nome} de {reais(limite)} aplica
         +do; "                                                          
      67 +            f"excedente de {reais(excedente)} cortado (RN-008, 
         +RN-010)."                                                      
      68 +        )                                                      
      69 +    por = f"por {_enumerar(consumidoras)} em {data}"           
      70 +    if consumido >= limite:                                    
      71 +        return f"Limite diário de {nome} de {reais(limite)} já 
         +consumido {por} (RN-008, RN-009)."                             
      72      return (
      51 -        f"Limite diário de {nome} de {reais(limite)} aplicado; 
         -"                                                              
      52 -        f"excedente de {reais(excedente)} cortado (RN-008, RN-0
         -10)."                                                          
      73 +        f"Limite diário de {nome} de {reais(limite)}, com {reai
         +s(consumido)} já consumido {por}; "                            
      74 +        f"excedente de {reais(excedente)} cortado (RN-008, RN-0
         +09, RN-010)."                                                  
      75      )
      76  
      77  

● Update(reembolso\etapas.py)
  ⎿  Added 13 lines, removed 5 lines
       75      Cada despesa recebe o menor valor entre o seu valor consid
           erado e o saldo deixado
       76      pelas anteriores; o excedente é cortado. `vivas` chega em 
           ordem de posição.
       77      """
       78 -    saldos: dict[tuple, Decimal] = {}                         
       78 +    consumos: dict[tuple, Decimal] = defaultdict(Decimal)     
       79 +    consumidoras: dict[tuple, list[str]] = defaultdict(list)  
       80      cortes: dict[int, Corte] = {}
       81      for despesa in vivas:
       82          limite = politica.LIMITE_POR_DATA[despesa.categoria]
       83          chave = (despesa.data, despesa.categoria)
       83 -        saldo = saldos.get(chave, limite)                     
       84 -        reembolsavel = min(despesa.valor_considerado, saldo)  
       85 -        saldos[chave] = saldo - reembolsavel                  
       84 +        consumido = consumos[chave]                           
       85 +        reembolsavel = min(despesa.valor_considerado, limite -
          + consumido)                                                   
       86          if reembolsavel < despesa.valor_considerado:
       87              cortes[despesa.posicao] = Corte(
       88                  reembolsavel,
       89                  Motivo.LIMITE_DIARIO,
       90                  justificativas.limite_diario(
       91 -                    despesa.categoria, limite, despesa.valor_c
          -onsiderado - reembolsavel                                     
       91 +                    despesa.categoria,                        
       92 +                    limite,                                   
       93 +                    despesa.data,                             
       94 +                    consumido,                                
       95 +                    list(consumidoras[chave]),                
       96 +                    despesa.valor_considerado - reembolsavel, 
       97                  ),
       98              )
       99 +        if reembolsavel > 0:                                  
      100 +            consumos[chave] = consumido + reembolsavel        
      101 +            consumidoras[chave].append(despesa.id)            
      102      return cortes

● Update(tests\test_rn009_distribuicao.py)  ⎿  Added 41 lines
      46      assert segunda.status == Status.LIMITADO
      47  
      48  
      49 +def test_rn009_justificativa_cita_despesa_que_consumiu():      
      50 +    _, d002 = calcular(                                        
      51 +        documento(                                             
      52 +            despesa(1, id="d-001", data="2026-07-03", valor="72
         +.50"),                                                         
      53 +            despesa(2, id="d-002", data="2026-07-03", valor="38
         +.00"),                                                         
      54 +        )                                                      
      55 +    )                                                          
      56 +    assert "R$ 60,00" in d002.justificativa                    
      57 +    assert "d-001" in d002.justificativa                       
      58 +    assert "RN-009" in d002.justificativa                      
      59 +                                                               
      60 +                                                               
      61 +def test_rn009_justificativa_cita_valor_consumido_e_todas_as_co
         +nsumidoras():                                                  
      62 +    *_, terceira = calcular(                                   
      63 +        documento(                                             
      64 +            despesa(1, id="h-1", data="2026-07-14", categoria="
         +hospedagem", valor="100.00"),                                  
      65 +            despesa(2, id="h-2", data="2026-07-14", categoria="
         +hospedagem", valor="100.00"),                                  
      66 +            despesa(3, id="h-3", data="2026-07-14", categoria="
         +hospedagem", valor="150.00"),                                  
      67 +        )                                                      
      68 +    )                                                          
      69 +    assert terceira.valor_reembolsavel == Decimal("50.00")     
      70 +    assert "R$ 250,00" in terceira.justificativa               
      71 +    assert "R$ 200,00" in terceira.justificativa               
      72 +    assert "h-1" in terceira.justificativa                     
      73 +    assert "h-2" in terceira.justificativa                     
      74 +    assert "RN-009" in terceira.justificativa                  
      75 +    assert "RN-010" in terceira.justificativa                  
      76 +                                                               
      77 +                                                               
      78 +def test_rn009_justificativa_nao_cita_despesa_que_nao_consumiu(
         +):                                                             
      79 +    *_, terceira = calcular(                                   
      80 +        documento(                                             
      81 +            despesa(1, id="a-1", data="2026-07-03", valor="60.0
         +0"),                                                           
      82 +            despesa(2, id="a-2", data="2026-07-03", valor="5.00
         +"),                                                            
      83 +            despesa(3, id="a-3", data="2026-07-03", valor="5.00
         +"),                                                            
      84 +        )                                                      
      85 +    )                                                          
      86 +    assert "a-1" in terceira.justificativa                     
      87 +    assert "a-2" not in terceira.justificativa                 
      88 +                                                               
      89 +                                                               
      90  def test_rn009_despesa_zero_depois_do_limite_consumido_e_aprova
          da():
      91      _, zero = calcular(
      92          documento(

● Bash(.venv/Scripts/ruff check --fix -q . ; .venv/Scripts/ruff format -q . ;
      .venv/Scripts/python -m pytest -q && .venv/Scripts/ruff check . &&
      .venv/Scripts/ruff for…)
  ⎿  ......................................................................
     .. [ 48%]
     ......................................................................
     … +8 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      168      `tests/test_rn010_parcial.py`
      169    - **Commit:**
      170  
      171 -- [ ] **T-016** — Justificativa de `LIMITE_DIARIO` com o limit
          -e, o valor já                                                 
      171 +- [x] **T-016** — Justificativa de `LIMITE_DIARIO` com o limit
          +e, o valor já                                                 
      172    consumido no dia e os `id` das despesas que o consumiram.
      173    - **Atende:** spec §4 (justificativa), RN-009
      174    - **Aceite:** a justificativa de d-002 cita R$ 60,00, d-001 
           e RN-009.

● T-017: testes de viagem (RN-011) e calendário (RN-012), só testes.

● Write(tests\test_rn011_viagem.py)
  ⎿  Wrote 71 lines to tests\test_rn011_viagem.py
      1 import json
      2 from collections import defaultdict
      3 from decimal import Decimal
      4 from pathlib import Path
      5 
      6 from reembolso.entrada import ler_documento
      7 from reembolso.modelo import Despesa
      8 from reembolso.motor import calcular
      9 from reembolso.politica import LIMITE_POR_DATA
     … +66 lines (ctrl+o to expand)

● Write(tests\test_rn012_calendario.py)
  ⎿  Wrote 27 lines to tests\test_rn012_calendario.py
      1 from datetime import date
      2 from decimal import Decimal
      3 
      4 import pytest
      5 from fabrica import despesa, documento
      6 
      7 from reembolso.modelo import Status
      8 from reembolso.motor import calcular
      9 
     … +19 lines (ctrl+o to expand)

● Bash(.venv/Scripts/ruff check --fix -q . ; .venv/Scripts/ruff format -q . ;
      .venv/Scripts/python -m pytest -q && .venv/Scripts/ruff check . &&
      .venv/Scripts/ruff for…)
  ⎿  ......................................................................
     .. [ 45%]
     ......................................................................
     … +8 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      175    - **Teste:** `tests/test_rn009_distribuicao.py::test_rn009_j
           ustificativa_cita_despesa_que_consumiu`
      176    - **Commit:**
      177  
      178 -- [ ] **T-017** — Testes das regras que determinam o que **não
          -** fazer: viagem e                                            
      178 +- [x] **T-017** — Testes das regras que determinam o que **não
          +** fazer: viagem e                                            
      179    dias do calendário (`test(T-017)`).
      180    - **Atende:** RN-011, RN-012, AMB-006, AMB-007, AMB-015
      181    - **Aceite:** d-003 ("Corrida aeroporto", 100,00) → limite d
           e 80,00, 80,00;

● T-018: saida.py e serialização.

● Write(reembolso\saida.py)
  ⎿  Wrote 62 lines to reembolso\saida.py
       1 """Montagem e serialização do documento de saída (spec §4, RN-00
         3, DT-005)."""
       2 
       3 import json
       4 from decimal import Decimal
       6 from reembolso.modelo import Documento, Resultado
       7 from reembolso.normalizacao import CENTAVO
       8 
       9 
      10 def _dinheiro(valor: Decimal | None) -> Decimal | None:
     … +63 lines (ctrl+o to expand)

● Write(tests\test_saida_serializacao.py)
  ⎿  Wrote 119 lines to tests\test_saida_serializacao.py
      1 import json
      2 from decimal import Decimal
      3 
      4 from fabrica import despesa, documento, invalida
      5 
      6 from reembolso.modelo import Motivo, Resultado, Status
      7 from reembolso.motor import calcular
      8 from reembolso.saida import montar_saida, serializar
      9 
     … +116 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● Bash(sh /tmp/fechar.sh T-018 "monta e serializa a saida com Decimal, duas
      casas e nulos" 2>/dev/null)
  ⎿  9560e22 feat(T-018): monta e serializa a saida com Decimal, duas casas
      e nulos
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      186  
      187  ## Fase 4 — Saída e CLI
      188  
      189 -- [ ] **T-018** — `saida.py` + encoder JSON: `valor_considerad
          -o`,                                                           
      189 +- [x] **T-018** — `saida.py` + encoder JSON: `valor_considerad
          +o`,                                                           
      190    `valor_reembolsavel` e `total_reembolsavel` com duas casas; 
           `valor_informado`
      191    sem quantizar; `null` onde a spec pede nulo; `Decimal` dentr
           o de `colaborador`
      192    e `periodo`; UTF-8 com `ensure_ascii=False`.

● T-019: CLI.

● Write(reembolso\cli.py)
  ⎿  Wrote 49 lines to reembolso\cli.py
      1 """Interface de linha de comando. Único módulo que toca disco, st
        dout e stderr (plan §2)."""
      2 
      3 import argparse
      4 import sys
      5 from pathlib import Path
      6 
      7 from reembolso.entrada import EntradaInvalida, ler_documento
      8 from reembolso.motor import calcular
      9 from reembolso.saida import montar_saida, serializar
     … +49 lines (ctrl+o to expand)

● Write(reembolso\__main__.py)
  ⎿  Added 1 line, removed 10 lines
       1 -import argparse                                                
       1  import sys
       2  
       3 +from reembolso.cli import main                                 
       4  
       5 -def main(argv: list[str] | None = None) -> int:                
       6 -    parser = argparse.ArgumentParser(                          
       7 -        prog="python -m reembolso",                            
       8 -        description="Motor de cálculo de reembolso de despesas 
         -corporativas.",                                                
       9 -    )                                                          
      10 -    parser.parse_args(argv)                                    
      11 -    return 0                                                   
      12 -                                                               
      13 -                                                               
       5  if __name__ == "__main__":
       6      sys.exit(main())

● Write(tests\test_cli.py)
  ⎿  Wrote 83 lines to tests\test_cli.py
       1 import json
       2 import subprocess
       3 import sys
       4 from decimal import Decimal
       5 from pathlib import Path
       6 
       7 RAIZ = Path(__file__).parent.parent
       8 EXEMPLO = RAIZ / "exemplos" / "despesas-exemplo.json"
       9 
      10 CONTEUDO_ANTERIOR = '{"conteudo": "anterior"}\n'
     … +81 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● No Windows o processo filho escreve stderr em cp1252; ajusto o teste para
  forçar UTF-8 no filho (PYTHONUTF8=1).

● Update(tests\test_cli.py)
  ⎿  Added 2 lines
      17          text=True,
      18          encoding="utf-8",
      19          cwd=RAIZ,
      20 +        # Mensagens têm acentos; sem isso, no Windows o stderr 
         +do filho sai em cp1252.                                        
      21 +        env={**os.environ, "PYTHONUTF8": "1"},                 
      22      )
      23  
      24  

● Update(tests\test_cli.py)
  ⎿  Added 1 line
      1  import json
      2 +import os                                                       
      3  import subprocess
      4  import sys
      5  from decimal import Decimal

  Ran 1 shell command (ctrl+o to expand)

● Bash(sh /tmp/fechar.sh T-019 "cria CLI calcular com erro geral em stderr e
      codigo 1" 2>/dev/null && .venv/Scripts/python -m reembolso calcular
      --input exemplos/despe…)
  ⎿  deb2843 feat(T-019): cria CLI calcular com erro geral em stderr e codi
     go 1
     exit=0
     … +71 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      198    - **Teste:** `tests/test_saida_serializacao.py`
      199    - **Commit:**
      200  
      201 -- [ ] **T-019** — CLI `calcular --input --output`: em erro ger
          -al, mensagem em                                               
      201 +- [x] **T-019** — CLI `calcular --input --output`: em erro ger
          +al, mensagem em                                               
      202    stderr, código 1 e arquivo de saída não criado nem sobrescri
           to; sucesso retorna
      203    0; argumentos inválidos retornam 2.
      204    - **Atende:** RN-013 (erro geral, "não gera saída"), DT-006

● Saída do exemplo bate com a §4 e a §9. T-020: teste de aceite.

● Write(tests\test_secao9_aceite_exemplo.py)
  ⎿  Wrote 66 lines to tests\test_secao9_aceite_exemplo.py
      1 import json
      2 from decimal import Decimal
      3 from pathlib import Path
      4 
      5 import pytest
      6 
      7 from reembolso.entrada import ler_documento
      8 from reembolso.motor import calcular
      9 from reembolso.saida import montar_saida, serializar
     … +60 lines (ctrl+o to expand)

● Bash(.venv/Scripts/ruff check --fix -q . ; .venv/Scripts/ruff format -q . ;
      .venv/Scripts/python -m pytest -q && .venv/Scripts/ruff check . &&
      .venv/Scripts/ruff for…)
  ⎿  ......................................................................
     .. [ 37%]
     ......................................................................
     … +7 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      211  
      212  ## Fase 5 — Casos de borda e aceite
      213  
      214 -- [ ] **T-020** — Aceite completo com `exemplos/despesas-exemp
          -lo.json`                                                      
      214 +- [x] **T-020** — Aceite completo com `exemplos/despesas-exemp
          +lo.json`                                                      
      215    (`test(T-020)`).
      216    - **Atende:** spec §9
      217    - **Aceite:** as 14 linhas (`valor_reembolsavel`, `status`, 
           `motivo`) batem com

● T-021: texto exato das justificativas da §4 e RN em todo item.
● Bash(cat >> tests/test_secao9_aceite_exemplo.py <<'EOF'…)
  ⎿  ......................................................................
     .. [ 36%]
     ......................................................................
     … +8 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      220    - **Teste:** `tests/test_secao9_aceite_exemplo.py`
      221    - **Commit:**
      222  
      223 -- [ ] **T-021** — Texto exato das justificativas dos exemplos 
          -da §4 e verificação                                           
      223 +- [x] **T-021** — Texto exato das justificativas dos exemplos 
          +da §4 e verificação                                           
      224    de que todo item cita uma RN.
      225    - **Atende:** spec §4 (exemplo), spec §9 (justificativa cita
            RN)
      226    - **Aceite:** d-001, d-002 e d-004 têm exatamente as justifi
           cativas da §4; todo
  ⎿  Updated tests\test_secao9_aceite_exemplo.py (+25 -0)
      1  import json
      2 +import re                                                       
      3  from decimal import Decimal
      4  from pathlib import Path
      5  
     ...
      65      entrada = json.loads(EXEMPLO.read_text(encoding="utf-8"))
      66      assert saida["colaborador"] == entrada["colaborador"]
      67      assert saida["periodo"] == entrada["periodo"]
      68 +                                                               
      69 +                                                               
      70 +JUSTIFICATIVAS_SECAO4 = {                                      
      71 +    "d-001": (                                                 
      72 +        "Limite diário de alimentação de R$ 60,00 aplicado; "  
      73 +        "excedente de R$ 12,50 cortado (RN-008, RN-010)."      
      74 +    ),                                                         
      75 +    "d-002": (                                                 
      76 +        "Limite diário de alimentação de R$ 60,00 já consumido 
         +por d-001 em 2026-07-03 "                                      
      77 +        "(RN-008, RN-009)."                                    
      78 +    ),                                                         
      79 +    "d-004": "Valor acima de R$ 100,00 sem nota fiscal (RN-007)
         +.",                                                            
      80 +}                                                              
      81 +                                                               
      82 +                                                               
      83 +@pytest.mark.parametrize("id_", list(JUSTIFICATIVAS_SECAO4))   
      84 +def test_justificativas_exemplo_secao4(saida, id_):            
      85 +    item = next(i for i in saida["itens"] if i["id"] == id_)   
      86 +    assert item["justificativa"] == JUSTIFICATIVAS_SECAO4[id_] 
      87 +                                                               
      88 +                                                               
      89 +def test_todo_item_cita_rn(saida):                             
      90 +    for item in saida["itens"]:                                
      91 +        assert re.search(r"RN-\d{3}", item["justificativa"]), i
         +tem["id"]                                                      

● T-022: tabela da §7 como teste parametrizado (37 casos).

● Write(tests\test_secao7_casos_de_borda.py)
  ⎿  Wrote 311 lines to tests\test_secao7_casos_de_borda.py
       1 """Tabela da seção 7 da spec: um caso por linha, com o nome da s
         pec como `id`."""
       2 
       3 import json
       4 from decimal import Decimal
       6 import pytest
       7 
       8 from reembolso.entrada import EntradaInvalida, ler_documento
       9 from reembolso.motor import calcular
      10 from reembolso.saida import montar_saida, serializar
     … +332 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● Todos passam. Confiro como os nomes aparecem no relatório do pytest:

  Ran 1 shell command (ctrl+o to expand)

● O pytest escapa os acentos (n\xe3o). Para os nomes aparecerem iguais aos da
  spec, ativo a opção do pytest que desliga esse escape.

● Update(pyproject.toml)
  ⎿  Added 2 lines
      17  
      18  [tool.pytest.ini_options]
      19  testpaths = ["tests"]
      20 +# Mostra os nomes dos casos da seção 7 da spec com acentos, sem
         + escapar (T-022).                                              
      21 +disable_test_id_escaping_and_forfeit_all_rights_to_community_su
         +pport = true                                                   
      22  
      23  [tool.ruff]
      24  target-version = "py312"

● Bash(.venv/Scripts/python -m pytest --collect-only -q
      tests/test_secao7_casos_de_borda.py | sed -n '5,7p'; .venv/Scripts/python
      -m pytest -q && .venv/Scripts/ruff ch…)
  ⎿  tests/test_secao7_casos_de_borda.py::test_secao7_caso_de_borda[Despesa
      recusada n�o consome limite]
     tests/test_secao7_casos_de_borda.py::test_secao7_caso_de_borda[Categor
     … +16 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      229      `::test_todo_item_cita_rn`
      230    - **Commit:**
      231  
      232 -- [ ] **T-022** — Tabela da §7 como teste parametrizado, com u
          -ma linha por caso e                                           
      232 +- [x] **T-022** — Tabela da §7 como teste parametrizado, com u
          +ma linha por caso e                                           
      233    o nome do caso como `id` (`test(T-022)`).
      234    - **Atende:** spec §7 (todas as RN citadas na tabela)
      235    - **Aceite:** os 37 casos da §7 passam e aparecem no relatór
           io do pytest com o

● T-023: invariantes (determinismo e descrição informativa).

● Write(tests\test_rn014_descricao.py)
  ⎿  Wrote 58 lines to tests\test_rn014_descricao.py
      1 import json
      2 from decimal import Decimal
      3 from pathlib import Path
      4 
      5 import pytest
      6 
      7 from reembolso.entrada import ler_documento
      8 from reembolso.motor import calcular
      9 from reembolso.saida import montar_saida, serializar
     … +56 lines (ctrl+o to expand)

● Bash(cat >> tests/test_secao9_aceite_exemplo.py <<'EOF'…)
  ⎿  ......................................................................
     .. [ 29%]
     ......................................................................
     … +8 lines (ctrl+o to expand)
  ⎿  Updated tests\test_rn014_descricao.py (+8 -2)
      41          lambda p, _d: p,
      42          lambda _p, _d: REMOVER,
      43      ],
      44 -    ids=["texto_qualquer", "indicios_de_viagem_e_diarias", "mai
         -usculas", "vazia", "numero",                                   
      45 -         "ausente"],                                           
      44 +    ids=[                                                      
      45 +        "texto_qualquer",                                      
      46 +        "indicios_de_viagem_e_diarias",                        
      47 +        "maiusculas",                                          
      48 +        "vazia",                                               
      49 +        "numero",                                              
      50 +        "ausente",                                             
      51 +    ],                                                         
      52  )
      53  def test_rn014_trocar_descricoes_nao_altera_decisoes(trocar):
      54      original = _decisoes(_com_descricoes(lambda _p, d: d["descr
          icao"]))
  ⎿  Updated tests\test_secao9_aceite_exemplo.py (+21 -0)
      1  import json
      2  import re
      3 +import subprocess                                               
      4 +import sys                                                      
      5  from decimal import Decimal
      6  from pathlib import Path
      7  
     ...
       91  def test_todo_item_cita_rn(saida):
       92      for item in saida["itens"]:
       93          assert re.search(r"RN-\d{3}", item["justificativa"]), 
           item["id"]
       94 +                                                              
       95 +                                                              
       96 +def _rodar_cli(saida_path):                                   
       97 +    return subprocess.run(                                    
       98 +        [sys.executable, "-m", "reembolso", "calcular", "--inp
          +ut", EXEMPLO, "--output", saida_path],                        
       99 +        capture_output=True,                                  
      100 +        cwd=EXEMPLO.parent.parent,                            
      101 +        check=True,                                           
      102 +    )                                                         
      103 +                                                              
      104 +                                                              
      105 +def test_determinismo(tmp_path):                              
      106 +    texto = EXEMPLO.read_text(encoding="utf-8")               
      107 +    assert _processar(texto) == _processar(texto)             
      108 +    # Processos separados: nenhuma ordem depende de hash ou es
          +tado do processo.                                             
      109 +    primeira, segunda = tmp_path / "1.json", tmp_path / "2.jso
          +n"                                                            
      110 +    _rodar_cli(primeira)                                      
      111 +    _rodar_cli(segunda)                                       
      112 +    assert primeira.read_bytes() == segunda.read_bytes()      

● Corrijo o nome do último teste (ele verifica que descrição diferente não
  impede a duplicata):

● Bash(sed -i 's/def test_rn014_descricoes_iguais_nao_criam_duplicata/def
      test_rn014_descricao_diferente_nao_impede_duplicata/; s/    # d-006 e
      d-007 têm a mesma descr…)
  ⎿  58:def test_rn014_descricao_diferente_nao_impede_duplicata():
     59:    # Trocar só a descrição de d-007 não desfaz a duplicata com d-0
     06 (RN-006).
     … +12 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      237    - **Teste:** `tests/test_secao7_casos_de_borda.py`
      238    - **Commit:**
      239  
      240 -- [ ] **T-023** — Invariantes: determinismo e descrição inform
          -ativa                                                         
      240 +- [x] **T-023** — Invariantes: determinismo e descrição inform
          +ativa                                                         
      241    (`test(T-023)`).
      242    - **Atende:** RN-014, spec §9, AMB-006, AMB-008, AMB-010
      243    - **Aceite:** duas execuções produzem saídas idênticas byte 
           a byte; trocar todas
  ⎿  Updated tests\test_rn014_descricao.py (+3 -3)
      55      assert _decisoes(_com_descricoes(trocar)) == original
      56  
      57  
      58 -def test_rn014_descricoes_iguais_nao_criam_duplicata():        
      59 -    # d-006 e d-007 têm a mesma descrição; trocar só a de d-007
         - mantém a duplicata (RN-006).                                  
      60 -    def trocar(posicao, despesa):                              
      58 +def test_rn014_descricao_diferente_nao_impede_duplicata():     
      59 +    # Trocar só a descrição de d-007 não desfaz a duplicata com
         + d-006 (RN-006).                                               
      60 +    def trocar(_posicao, despesa):                             
      61          return "Outra descrição" if despesa["id"] == "d-007" el
          se despesa["descricao"]
      62  
      63      decisoes = _decisoes(_com_descricoes(trocar))

● T-024: teste de rastreabilidade.

● Write(tests\test_rastreabilidade.py)
  ⎿  Wrote 39 lines to tests\test_rastreabilidade.py
       1 """Toda RN da spec tem um arquivo de teste `test_rnNNN_*.py` (pl
         an §6)."""
       2 
       4 from pathlib import Path
       5 
       6 TESTES = Path(__file__).parent
       7 SPEC = TESTES.parent / "specs" / "001-motor-reembolso" / "spec.m
       8 
       9 
      10 def rns_da_spec(texto: str) -> set[str]:
     … +32 lines (ctrl+o to expand)

● Bash(.venv/Scripts/ruff check --fix -q . ; .venv/Scripts/ruff format -q . ;
      .venv/Scripts/python -m pytest -q && .venv/Scripts/ruff check . &&
      .venv/Scripts/ruff for…)
  ⎿  ......................................................................
     .. [ 29%]
     ......................................................................
     … +9 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      246      `tests/test_secao9_aceite_exemplo.py::test_determinismo`
      247    - **Commit:**
      248  
      249 -- [ ] **T-024** — Teste de rastreabilidade: lê a `spec.md`, ex
          -trai os `RN-\d{3}` e                                          
      249 +- [x] **T-024** — Teste de rastreabilidade: lê a `spec.md`, ex
          +trai os `RN-\d{3}` e                                          
      250    falha se algum não tiver arquivo `test_rnNNN_*.py`. Fica por
            último porque só
      251    passa quando todas as RN têm teste.
      252    - **Atende:** plan §6

● T-025: README. Primeiro vejo o README atual.

  Searched for 1 pattern (ctrl+o to expand)

● O próprio README do desafio pede que ele seja substituído pelo README do
  projeto, que é o escopo da T-025. Vou escrever o novo README e validar o
  roteiro num clone limpo.

● Write(README.md)
  ⎿  Added 66 lines, removed 76 lines
        1 -# Desafio Prático — Spec Driven Development                   
        1 +# Motor de Cálculo de Reembolso                               
        2  
        3 -Aula bônus de SDD, fechando a trilha:                         
        3 +CLI que lê um JSON com as despesas de um colaborador em um per
          +íodo e gera um                                                
        4 +JSON com o valor reembolsável, o status e a justificativa de c
          +ada despesa,                                                  
        5 +seguindo as regras da spec.                                   
        6  
        5 -`AI Fluency` → `Claude 101` → `Claude Code 101` → `Building wi
          -th the Claude API` → `Claude Code in Action` → `Módulo SDD` → 
          -**Desafio**                                                   
        7 +Este repositório é a entrega do desafio de Spec Driven Develop
          +ment                                                          
        8 +(enunciado em [`DESAFIO.md`](DESAFIO.md)).                    
        9  
        7 -**Individual · 2 dias · Claude Code**                         
       10 +| Documento | Conteúdo |                                      
       11 +|---|---|                                                     
       12 +| [`specs/001-motor-reembolso/spec.md`](specs/001-motor-reembo
          +lso/spec.md) | O quê: regras de negócio (RN-001 a RN-014), amb
          +iguidades, casos de borda, aceite |                           
       13 +| [`specs/001-motor-reembolso/plan.md`](specs/001-motor-reembo
          +lso/plan.md) | O como: stack, arquitetura, decisões técnicas |
       14 +| [`specs/001-motor-reembolso/tasks.md`](specs/001-motor-reemb
          +olso/tasks.md) | Em que ordem: tasks T-001 a T-025, cada uma c
          +om o seu commit |                                             
       15 +| [`specs/001-motor-reembolso/DECISIONS.md`](specs/001-motor-r
          +eembolso/DECISIONS.md) | Log de mudanças da spec |            
       16  
        9 ----                                                           
       17 +## Requisitos                                                 
       18  
       11 -## Comece por aqui                                            
       19 +- Python 3.12 ou mais recente                                 
       20 +- Nenhuma dependência para rodar; `pytest` e `ruff` para desen
          +volvimento                                                    
       21  
       13 -1. **[`DESAFIO.md`](DESAFIO.md)** — o enunciado. Leia inteiro 
          -antes de escrever qualquer coisa.                             
       14 -2. **[`RUBRICA.md`](RUBRICA.md)** — como você é avaliado. É pú
          -blica de propósito; leia antes de começar.                    
       15 -3. **[`exemplos/despesas-exemplo.json`](exemplos/despesas-exem
          -plo.json)** — a entrada de referência. Não é decoração: percor
          -ra item por item antes de escrever a spec.                    
       16 -4. **[`FAQ.md`](FAQ.md)** — travou? Comece por aqui. **O instr
          -utor está fora durante o desafio**, então o FAQ é o canal de s
          -uporte.                                                       
       22 +## Instalação                                                 
       23  
       18 ----                                                           
       24 +```bash                                                       
       25 +python -m venv .venv                                          
       26 +.venv/bin/python -m pip install -e ".[dev]"        # Linux/mac
          +OS                                                            
       27 +.venv/Scripts/python -m pip install -e ".[dev]"    # Windows  
       28 +```                                                           
       29  
       20 -## Como participar                                            
       30 +Os comandos abaixo supõem o ambiente virtual ativado          
       31 +(`source .venv/bin/activate` ou `.venv\Scripts\activate`).    
       32  
       22 -**1. Faça um fork deste repositório.** Ele precisa ser público
          -, ou você não conseguirá compartilhar depois.                 
       33 +## Como rodar                                                 
       34  
       24 -**2. Clone o seu fork e prepare a estrutura de trabalho:**    
       25 -                                                              
       35  ```bash
       27 -git clone https://github.com/<seu-usuario>/sdd-desafio.git    
       28 -cd sdd-desafio                                                
       29 -cp template/CLAUDE.md .                                       
       30 -cp -r template/specs .                                        
       31 -cp -r template/docs .                                         
       32 -git add -A && git commit -m "chore: estrutura inicial a partir
          - do template"                                                 
       36 +python -m reembolso calcular --input exemplos/despesas-exemplo
          +.json --output resultado.json                                 
       37  ```
       38  
       35 -<details>                                                     
       36 -<summary>PowerShell</summary>                                 
       39 +- `--input`: documento de despesas no formato de              
       40 +  [`exemplos/despesas-exemplo.json`](exemplos/despesas-exemplo
          +.json) (spec §4).                                             
       41 +- `--output`: arquivo de resultado, em UTF-8. Para o exemplo, 
          +o                                                             
       42 +  `total_reembolsavel` é `585.43`.                            
       43  
       38 -```powershell                                                 
       39 -git clone https://github.com/<seu-usuario>/sdd-desafio.git    
       40 -cd sdd-desafio                                                
       41 -Copy-Item template\CLAUDE.md .                                
       42 -Copy-Item template\specs . -Recurse                           
       43 -Copy-Item template\docs . -Recurse                            
       44 -git add -A; git commit -m "chore: estrutura inicial a partir d
          -o template"                                                   
       45 -```                                                           
       46 -</details>                                                    
       44 +Códigos de saída:                                             
       45  
       48 -Os arquivos em `template/` são esqueletos com as perguntas que
          - cada documento precisa responder. Deixe a pasta `template/` o
          -nde está — ela serve de referência.                           
       46 +| Código | Situação |                                         
       47 +|---|---|                                                     
       48 +| 0 | Sucesso; o arquivo de saída foi gravado |               
       49 +| 1 | Erro geral da RN-013 (documento ilegível, sem período vá
          +lido etc.); mensagem em stderr, e o arquivo de saída não é cri
          +ado nem sobrescrito |                                         
       50 +| 2 | Argumentos de linha de comando inválidos |              
       51  
       50 -**3. Trabalhe no seu fork**, seguindo as três regras do jogo d
          -escritas no [`DESAFIO.md`](DESAFIO.md):                       
       52 +Uma despesa com dados inválidos não interrompe a execução: ela
          + sai recusada                                                 
       53 +com `DADOS_INVALIDOS` e as demais são calculadas normalmente. 
       54  
       52 -- Nenhum commit sem task                                      
       53 -- Explicação no chat que não está na spec é bug de spec       
       54 -- Interações exportadas (`/export`) e commitadas em `docs/sess
          -ions/`                                                        
       55 +## Como testar                                                
       56  
       56 -**4. No Dia 2, às 10h**, você recebe uma mudança de requisito 
          -pelo canal da turma. Ela é obrigatória e vale 20 pontos. Chegu
          -e nesse momento com o sistema base funcionando e testado.     
       57 +```bash                                                       
       58 +python -m pytest                                              
       59 +```                                                           
       60  
       58 -> Durante os dois dias o instrutor está de férias e não respon
          -de mensagens. Dúvida de processo: [`FAQ.md`](FAQ.md). Dúvida s
          -obre o que a política do RH significa não tem resposta — decid
          -ir isso é o exercício.                                        
       61 +Os testes seguem a spec: um arquivo `tests/test_rnNNN_*.py` po
          +r regra de                                                    
       62 +negócio, `tests/test_secao7_casos_de_borda.py` com um caso por
          + linha da tabela                                              
       63 +da seção 7, `tests/test_secao9_aceite_exemplo.py` com o aceite
          + do exemplo e                                                 
       64 +`tests/test_rastreabilidade.py`, que falha se alguma RN da spe
          +c ficar sem                                                   
       65 +arquivo de teste.                                             
       66  
       60 -**5. Entregue** enviando o link do seu fork no formulário. Pra
          -zo: **Dia 2, 18h**.                                           
       67 +## Lint e formatação                                          
       68  
       62 ----                                                           
       69 +```bash                                                       
       70 +ruff check .                                                  
       71 +ruff format .                                                 
       72 +```                                                           
       73  
       64 -## O que o seu fork precisa conter ao final                   
       74 +## Estrutura                                                  
       75  
       76  ```
       67 -seu-fork/                                                     
       68 -├── CLAUDE.md                     # convenções do projeto para
          - o agente                                                     
       69 -├── README.md                     # como rodar e como testar o
          - SEU projeto                                                  
       70 -├── specs/                                                    
       71 -│   └── 001-motor-reembolso/                                  
       72 -│       ├── spec.md               # o QUÊ e o PORQUÊ          
       73 -│       ├── plan.md               # o COMO                    
       74 -│       ├── tasks.md              # T-001..T-0NN, com critério
          - de aceite                                                    
       75 -│       └── DECISIONS.md          # log de mudanças de spec   
       76 -├── src/                                                      
       77 -├── tests/                                                    
       78 -└── docs/                                                     
       79 -    ├── sessions/                 # exports das suas conversas
          - com o Claude                                                 
       80 -    └── RELATORIO.md              # o relatório final         
       77 +reembolso/                                                    
       78 +  cli.py             argumentos, leitura e escrita de arquivo,
          + códigos de saída                                             
       79 +  entrada.py         JSON → Documento; validação da RN-013 (et
          +apas 1 e 2)                                                   
       80 +  normalizacao.py    normalização de texto (RN-002) e arredond
          +amento (RN-003)                                               
       81 +  politica.py        categorias, limites e limiar da nota fisc
          +al, como dados                                                
       82 +  etapas.py          uma função por etapa da seção 8 da spec  
       83 +  motor.py           ordem das etapas (ETAPAS) e execução     
       84 +  justificativas.py  textos das justificativas                
       85 +  saida.py           Resultado → JSON                         
       86 +  modelo.py          dataclasses e enums                      
       87 +tests/                                                        
       88 +exemplos/                                                     
       89 +specs/001-motor-reembolso/                                    
       90 +docs/sessions/       exports das sessões com o Claude Code    
       91  ```
       82 -                                                              
       83 -Sobre o `README.md`: substitua este arquivo pelo README do **s
          -eu** projeto — como rodar, como testar, o que você construiu. 
          -Um README que não permite rodar o projeto custa pontos.       
       84 -                                                              
       85 ----                                                           
       86 -                                                              
       87 -## Antes de começar, confirme que o `/export` funciona        
       88 -                                                              
       89 -Abra o Claude Code, troque duas mensagens, rode `/export` e co
          -nfirme que o arquivo foi gerado.                              
       90 -                                                              
       91 -Faça isso **agora**, não no Dia 2. Sem `docs/sessions/`, o cri
          -tério de relatório vale zero — e já aconteceu de gente que fez
          - tudo certo descobrir no último dia que não tinha registro nen
          -hum do trabalho.                                              
       92 -                                                              
       93 -Exporte ao final de **cada** sessão, nomeando `docs/sessions/0
          -1-descricao-curta.md`, `02-...`, e assim por diante.          
       94 -                                                              
       95 ----                                                           
       96 -                                                              
       97 -## O resumo em um parágrafo                                   
       98 -                                                              
       99 -Você vai receber uma política de reembolso escrita por um RH, 
          -com a redação ruim que uma política de RH real tem. Ela é ambí
          -gua em vários pontos, e você não tem acesso a ninguém para tir
          -ar dúvida. O trabalho não é implementar — é **especificar**: e
          -ncontrar cada ambiguidade, decidir explicitamente, justificar 
          -e registrar. O produto funcionando vale **10 dos 100 pontos**.
          - Os outros 90 estão na spec, na rastreabilidade `spec → tasks 
          -→ commits → testes`, na resposta à mudança de requisito do Dia
          - 2 e no relatório.                                            
      100 -                                                              
      101 -Isso é deliberado. Um projeto que roda perfeitamente com spec 
          -fraca tira nota baixa; um projeto com bug conhecido, spec impe
          -cável e trilha limpa tira nota alta.                          

● Bash(git add README.md && git stash -q 2>/dev/null; true; git stash pop -q;
      D=$(mktemp -d) && git clone -q . "$D/clone" && cp README.md
      "$D/clone/README.md" && cd "$…)
  ⎿  warning: in the working copy of 'README.md', LF will be replaced by CR
     LF the next time Git touches it
     … +9 lines (ctrl+o to expand)
  ⎿  Shell cwd was reset to 
     C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio
  ⎿  Updated README.md (+91 -91)
       1 -# Motor de Cálculo de Reembolso                                
       2 -                                                               
       3 -CLI que lê um JSON com as despesas de um colaborador em um perí
         -odo e gera um                                                  
       4 -JSON com o valor reembolsável, o status e a justificativa de ca
         -da despesa,                                                    
       5 -seguindo as regras da spec.                                    
       6 -                                                               
       7 -Este repositório é a entrega do desafio de Spec Driven Developm
         -ent                                                            
       8 -(enunciado em [`DESAFIO.md`](DESAFIO.md)).                     
       9 -                                                               
      10 -| Documento | Conteúdo |                                       
      11 -|---|---|                                                      
      12 -| [`specs/001-motor-reembolso/spec.md`](specs/001-motor-reembol
         -so/spec.md) | O quê: regras de negócio (RN-001 a RN-014), ambig
         -uidades, casos de borda, aceite |                              
      13 -| [`specs/001-motor-reembolso/plan.md`](specs/001-motor-reembol
         -so/plan.md) | O como: stack, arquitetura, decisões técnicas |  
      14 -| [`specs/001-motor-reembolso/tasks.md`](specs/001-motor-reembo
         -lso/tasks.md) | Em que ordem: tasks T-001 a T-025, cada uma com
         - o seu commit |                                                
      15 -| [`specs/001-motor-reembolso/DECISIONS.md`](specs/001-motor-re
         -embolso/DECISIONS.md) | Log de mudanças da spec |              
      16 -                                                               
      17 -## Requisitos                                                  
      18 -                                                               
      19 -- Python 3.12 ou mais recente                                  
      20 -- Nenhuma dependência para rodar; `pytest` e `ruff` para desenv
         -olvimento                                                      
      21 -                                                               
      22 -## Instalação                                                  
      23 -                                                               
      24 -```bash                                                        
      25 -python -m venv .venv                                           
      26 -.venv/bin/python -m pip install -e ".[dev]"        # Linux/macO
         -S                                                              
      27 -.venv/Scripts/python -m pip install -e ".[dev]"    # Windows   
      28 -```                                                            
      29 -                                                               
      30 -Os comandos abaixo supõem o ambiente virtual ativado           
      31 -(`source .venv/bin/activate` ou `.venv\Scripts\activate`).     
      32 -                                                               
      33 -## Como rodar                                                  
      34 -                                                               
      35 -```bash                                                        
      36 -python -m reembolso calcular --input exemplos/despesas-exemplo.
         -json --output resultado.json                                   
      37 -```                                                            
      38 -                                                               
      39 -- `--input`: documento de despesas no formato de               
      40 -  [`exemplos/despesas-exemplo.json`](exemplos/despesas-exemplo.
         -json) (spec §4).                                               
     … 142 more lines (ctrl+o to expand)
  ⎿  (timeout 6m 40s)

● O roteiro do README funcionou num clone limpo (exit 0, total 585.43, 245
  testes passando, lint ok). Confiro o estado e faço o commit da T-025.

● Bash(git status --short && git ls-files | grep -i egg; sh /tmp/fechar.sh T-025
      "README com instalacao, execucao da CLI, testes e lint" docs 2>/dev/null
      && git status…)
  ⎿   M README.md
     4223e05 docs(T-025): README com instalacao, execucao da CLI, testes e
     lint
      M README.md
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      257  
      258  ## Fase 6 — Finalização
      259  
      260 -- [ ] **T-025** — README: requisitos, instalação, como rodar a
          - CLI e como rodar os                                          
      260 +- [x] **T-025** — README: requisitos, instalação, como rodar a
          + CLI e como rodar os                                          
      261    testes e o lint (`docs(T-025)`).
      262    - **Atende:** DESAFIO (entrega), RUBRICA §5
      263    - **Aceite:** num clone limpo, seguir o README gera `resulta
           do.json` a partir do

● O commit da T-025 saiu só com o tasks.md (o README ficou fora do git add do
  meu script). Como o commit é local e acabou de ser criado, faço amend para que
  a task fique em um commit só.

  Ran 1 shell command (ctrl+o to expand)

● Confiro que cada commit tem o conteúdo certo e preencho os hashes no tasks.md,
  como foi feito na T-001:

  Ran 1 shell command (ctrl+o to expand)
● Bash(python - <<'EOF'
      import re, subprocess…)
  ⎿  warning: in the working copy of 'specs/001-motor-reembolso/tasks.md',
     LF will be replaced by CRLF the next time Git touches it
      specs/001-motor-reembolso/tasks.md | 48 +++++++++++++++++++----------
     … +26 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+24 -24)
      36    - **Aceite:** os sete motivos e os três status têm exatamente
           os textos da spec.
      37    - **Teste:** `tests/test_modelo.py::test_motivos_iguais_aos_c
          odigos_da_spec`,
      38      `::test_status_iguais_aos_textos_da_spec`
      39 -  - **Commit:**                                                
      39 +  - **Commit:** f207780                                        
      40  
      41  - [x] **T-003** — Normalização de texto em `normalizacao.py`: r
          emove espaços das
      42    pontas, passa para minúsculas e remove acentos. Mantém espaço
          s internos.
     ...
      44    - **Aceite:** `ALIMENTACAO`, ` Alimentação ` e `alimentacao` 
          → `alimentacao`;
      45      `Bistro Central` = `bistro central`; espaços internos manti
          dos; `ç` → `c`.
      46    - **Teste:** `tests/test_rn002_normalizacao.py`
      47 -  - **Commit:**                                                
      47 +  - **Commit:** 1e0e792                                        
      48  
      49  - [x] **T-004** — Arredondamento para centavos com a metade se 
          afastando do zero
      50    em `normalizacao.py`. `-0.00` vira `0.00`.
     ...
      52    - **Aceite:** 33,333 → 33,33; 10,005 → 10,01; −10,005 → −10,0
          1; −0,004 → 0,00,
      53      sem sinal.
      54    - **Teste:** `tests/test_rn003_arredondamento.py`
      55 -  - **Commit:**                                                
      55 +  - **Commit:** 1f7df07                                        
      56  
      57  ## Fase 2 — Entrada (RN-013)
      58  
     ...
      64    - **Teste:** `tests/test_rn013_dados_invalidos.py::test_rn013
          _json_invalido_erro_geral`,
      65      `::test_rn013_nan_erro_geral`, `::test_rn013_infinity_erro_
          geral`,
      66      `::test_dt001_float_lido_como_decimal`
      67 -  - **Commit:**                                                
      67 +  - **Commit:** fb3fd8d                                        
      68  
      69  - [x] **T-006** — Validação do documento: `colaborador` e `peri
          odo` são objetos,
      70    `colaborador.id` é texto não vazio, `inicio` e `fim` são data
          s válidas
     ...
      76      é lista ou item que não é objeto → `EntradaInvalida`. `peri
          odo.competencia` =
      77      `"julho"` e `despesas: []` → sem erro.
      78    - **Teste:** `tests/test_rn013_dados_invalidos.py::test_rn013
          _erro_geral_*`
      79 -  - **Commit:**                                                
      79 +  - **Commit:** ab4c408                                        
      80  
      81  - [x] **T-007** — Validação de cada despesa: falha produz `Inva
          lida` com
      82    `DADOS_INVALIDOS`. `id` é nulo quando o problema está no `id`
          ; `valor_informado`
     … 152 more lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● Terminei as tasks T-002 a T-025. Cada uma tem um commit próprio e foi marcada
  [x] no tasks.md dentro do próprio commit. Os 245 testes passam e o ruff check
  e o ruff format --check estão limpos.

  Commits: do f207780 (T-002) ao 8bb0338 (T-025). As tasks que só acrescentam
  testes (T-017, T-020 a T-024) usam test(...), e o README usa docs(T-025). No
  fim fiz mais um commit, docs(tasks): registra commits da T-002 a T-025, para
  preencher o campo Commit: de cada task, como foi feito na T-001. Nada foi
  enviado para o remoto.

  Resultado no exemplo: python -m reembolso calcular gera as 14 linhas da tabela
  da §9 e o total_reembolsavel de 585.43. As justificativas de d-001, d-002 e
  d-004 são idênticas às da §4. Também segui o README num clone limpo, e ele
  funcionou do começo ao fim.

  Decisões de negócio: não encontrei nenhuma fora da spec, então não precisei
  parar. Algumas escolhas de redação ficaram por minha conta, porque a spec só
  exige citar a RN, o id da despesa mantida e o limite consumido (DT-008). Vale
  você revisar:
  - os textos das justificativas que não aparecem na §4 (aprovado, duplicata,
    período, categoria, valor negativo, dados inválidos);
  - o caso de limite parcialmente consumido, como "…de R$ 250,00, com R$ 200,00
    já consumido por h-1 e h-2 em …; excedente de R$ 100,00 cortado (RN-008,
    RN-009, RN-010)";
  - o formato R$ 1.234,56.

  Escolhas técnicas a conferir:
  - T-009: criei os tipos Recusa e Corte em modelo.py. São o que as etapas
    devolvem ao motor; o plano não os nomeia.
  - Testes: criei tests/fabrica.py, com os construtores despesa(), invalida() e
    documento() que o plano §6 prevê.
  - T-022: para os 37 casos aparecerem no relatório do pytest com os nomes
    acentuados da spec, liguei no pyproject.toml a opção
    disable_test_id_escaping_and_forfeit_all_rights_to_community_support. Sem
    ela, um nome aparece como n\xe3o.
  - T-019: os testes da CLI rodam o processo com PYTHONUTF8=1. No Windows, o
    stderr com acentos chegava em cp1252 e quebrava a leitura no teste. A CLI lê
    a entrada como utf-8-sig, então um arquivo salvo com BOM também é aceito.
  - T-025: o primeiro commit saiu sem o README, porque meu script de commit não
    o incluía. Como o commit era local e recém-criado, corrigi com --amend.

  Não feito: conforme você pediu, não fiz /export nem registro de sessão em
  docs/sessions/. A Fase 7 (Envelope) só começa no Dia 2.

✻ Brewed for 16m 3s · done 15:36