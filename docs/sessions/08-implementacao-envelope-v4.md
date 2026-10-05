 ▐▛███▛█   Claude Code v2.1.289
▝▜██████▀  Opus 5.5 · API Usage Billing
 ▝▝   ▝▝   C:\Learning\AI\AnthropicAcademy\Desafio\sdd-desafio


> leia o CLAUDE.md a spec 2.1 o plan 2.0 o tasks.md e o DECISIONS.md            
                                                                                
  agora implemente as tasks da fase 7 começando na t-026 e siga em ordem        
                                                                                
  pra cada task:                                                                
  faz só o que ela pede                                                         
  roda os testes relacionados                                                   
  roda o lint                                                                   
  se passar marca [x]                                                           
  faz um commit separado referenciando a task                                   
  depois vai pra proxima                                                        
                                                                                
  nao junta duas tasks no mesmo commit                                          
  nao muda regra da spec por conta propria                                      
  se achar alguma decisao de negocio faltando para e me avisa                   
                                                                                
  pode fazer varias tasks nessa mesma sessao                                    
  nao faz export entre as tasks                                                 
  nao faz push ainda                                                            
                                                                                
  vai ate onde conseguir                                                        

  Read 4 files, ran 3 shell commands (ctrl+o to expand)

● Li a spec 2.1, o plan 2.0, o tasks.md e o DECISIONS.md, e agora estou lendo o
  código e os testes atuais antes de começar a T-026.

  Ran 3 shell commands (ctrl+o to expand)

● Antes de começar a T-026, vou commitar separadamente (local, sem push) os
  documentos pendentes — spec 2.1, plan 2.0, tasks (Fase 7), DECISIONS (D-003) e
  exemplos/envelope/ — para evitar que esse diff seja incluído no commit da
  tarefa.

  Ran 1 shell command (ctrl+o to expand)

● Agora a T-026 (modelo).

● Bash(python - <<'EOF'
      from pathlib import Path…)
  ⎿  warning: in the working copy of 'reembolso/modelo.py', LF will be repl
     aced by CRLF the next time Git touches it
     warning: in the working copy of 'tests/test_modelo.py', LF will be rep
     … +13 lines (ctrl+o to expand)
  ⎿  Updated reembolso\modelo.py (+11 -1)
      18      """Códigos de motivo da saída (spec §4, tabela de motivos).
          """
      19  
      20      DADOS_INVALIDOS = "DADOS_INVALIDOS"
      21 +    COTACAO_INDISPONIVEL = "COTACAO_INDISPONIVEL"              
      22      VALOR_NEGATIVO = "VALOR_NEGATIVO"
      23      FORA_DO_PERIODO = "FORA_DO_PERIODO"
      24      CATEGORIA_NAO_REEMBOLSAVEL = "CATEGORIA_NAO_REEMBOLSAVEL"
     ...
      29  
      30  @dataclass(frozen=True)
      31  class Despesa:
      31 -    """Despesa que passou pela etapa 1 (RN-013), já normalizada
         - e arredondada."""                                             
      32 +    """Despesa que passou pela etapa 1 (RN-013), já normalizada
         + e arredondada.                                                
      33 +                                                               
      34 +    `valor_informado` está na moeda da despesa; `valor_consider
         +ado`, em reais (RN-018).                                       
      35 +    """                                                        
      36  
      37      posicao: int
      38      id: str
     ...
      42      tem_nota_fiscal: bool
      43      valor_informado: Decimal
      44      valor_considerado: Decimal
      45 +    moeda: str = "BRL"  # normalizada (RN-017)                 
      46 +    taxa_cambio: Decimal | None = None  # como está no document
         +o de câmbio; None em BRL                                       
      47 +    data_cotacao: date | None = None  # data da taxa usada; Non
         +e em BRL                                                       
      48  
      49  
      50  @dataclass(frozen=True)
     ...
      75      status: Status
      76      motivo: Motivo | None
      77      justificativa: str
      78 +    moeda: str | None = "BRL"                                  
      79 +    taxa_cambio: Decimal | None = None                         
      80 +    data_cotacao: date | None = None                           
      81  
      82  
      83  @dataclass(frozen=True)
  ⎿  Updated tests\test_modelo.py (+1 -0)
       4  def test_motivos_iguais_aos_codigos_da_spec():
       5      assert {m.value for m in Motivo} == {
       6          "DADOS_INVALIDOS",
       7 +        "COTACAO_INDISPONIVEL",                                
       8          "VALOR_NEGATIVO",
       9          "FORA_DO_PERIODO",
      10          "CATEGORIA_NAO_REEMBOLSAVEL",

● Testes da T-026 passam (as 3 falhas de rastreabilidade já existiam antes: a
  spec 2.x tem RN-015 a RN-018, e isso só fecha na T-041). Marco e commito.

● Bash(cat > /tmp/marcar.py <<'EOF'
      import sys…)
  ⎿  warning: in the working copy of 'reembolso/modelo.py', LF will be repl
     aced by CRLF the next time Git touches it
     warning: in the working copy of 'specs/001-motor-reembolso/tasks.md',
     … +5 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      292  
      293  ### 7.1 — Modelo e documentos de entrada
      294  
      295 -- [ ] **T-026** — `modelo.py`: motivo `COTACAO_INDISPONIVEL`; 
          -`Despesa` ganha                                               
      295 +- [x] **T-026** — `modelo.py`: motivo `COTACAO_INDISPONIVEL`; 
          +`Despesa` ganha                                               
      296    `moeda`, `taxa_cambio` e `data_cotacao`; `Resultado` ganha `
           moeda`,
      297    `taxa_cambio` e `data_cotacao`. Valores padrão (`BRL`, nulo,
            nulo) mantêm as
      298    despesas da v3 como estão.

● Vou adicionar a função ler_politica ao politica.py, mantendo as constantes por
  ora (serão removidas na T-031), e incluir normalizar_moeda (DT-007) para
  tratar a moeda_base.

  Searched for 1 pattern (ctrl+o to expand)

● Bash(sed -i 's/\b_numero(/numero(/g' reembolso/entrada.py && python - <<'EOF'
      from pathlib import Path…)
  ⎿  Updated reembolso\entrada.py (+4 -4)
       94      return Cabecalho(colaborador, periodo, inicio, fim, itens)
       95  
       96  
       97 -def _numero(valor: object) -> Decimal | None:                 
       97 +def numero(valor: object) -> Decimal | None:                  
       98      """Valor numérico como Decimal; `bool` não é número (DT-00
           2)."""
       99      if isinstance(valor, bool):
      100          return None
     ...
      126      problemas.append(_problema_texto(item, "fornecedor"))
      127      if "valor" not in item:
      128          problemas.append("valor ausente")
      129 -    elif _numero(item["valor"]) is None:                      
      129 +    elif numero(item["valor"]) is None:                       
      130          problemas.append("valor não é numérico")
      131      if "tem_nota_fiscal" not in item:
      132          problemas.append("tem_nota_fiscal ausente")
     ...
      146      return Invalida(
      147          posicao=posicao,
      148          id=item["id"] if _problema_texto(item, "id") is None e
           lse None,
      149 -        valor_informado=_numero(item.get("valor")),           
      149 +        valor_informado=numero(item.get("valor")),            
      150          detalhe="; ".join(problemas),
      151      )
      152  
     ...
      156      invalida = validar_despesa(item, posicao)
      157      if invalida is not None:
      158          return invalida
      159 -    valor_informado = _numero(item["valor"])                  
      159 +    valor_informado = numero(item["valor"])                   
      160      return Despesa(
      161          posicao=posicao,
      162          id=item["id"],
  ⎿  Updated reembolso\normalizacao.py (+6 -1)
      1 -"""Normalização de texto (RN-002) e arredondamento (RN-003).""" 
      1 +"""Normalização de texto (RN-002), de moeda (RN-017) e arredonda
        +mento (RN-003)."""                                              
      2  
      3  import unicodedata
      4  from decimal import ROUND_HALF_UP, Context, Decimal
     ...
      19      return unicodedata.normalize("NFC", sem_acentos)
      20  
      21  
      22 +def normalizar_moeda(codigo: str) -> str:                      
      23 +    """Remove espaços das pontas e passa para maiúsculas (RN-01
         +7, DT-007)."""                                                 
      24 +    return codigo.strip().upper()                              
      25 +                                                               
      26 +                                                               
      27  def arredondar(valor: Decimal) -> Decimal:
      28      """Arredonda para centavos com a metade se afastando do zer
          o (RN-003, DT-001).
      29  
  ⎿  Updated reembolso\politica.py (+103 -1)
       1 -"""Valores da política de reembolso, como dados (plan §4, DT-00
         -4)."""                                                         
       1 +"""Documento de política de reembolso (RN-015) e valores da pol
         +ítica, como dados (plan §4)."""                                
       2  
       3 +from dataclasses import dataclass                              
       4  from decimal import Decimal
       5  
       6 +from reembolso.entrada import EntradaInvalida, ler_json, numero
         +, texto_preenchido                                             
       7 +from reembolso.normalizacao import normalizar_moeda, normalizar
         +_texto                                                         
       8 +                                                               
       9  # RN-001: lista fechada de categorias reembolsáveis, já normali
          zadas (RN-002).
      10  CATEGORIAS_REEMBOLSAVEIS = frozenset({"alimentacao", "transport
          e_urbano", "hospedagem"})
      11  
     ...
       18      "transporte_urbano": Decimal("80.00"),
       19      "hospedagem": Decimal("250.00"),
       20  }
       21 +                                                              
       22 +MOEDA_BASE = "BRL"                                            
       23 +PERIODICIDADES = frozenset({"dia", "diaria"})                 
       24 +                                                              
       25 +                                                              
       26 +@dataclass(frozen=True)                                       
       27 +class Centro:                                                 
       28 +    """Tabela de um centro de custo do documento de política."
          +""                                                            
       29 +                                                              
       30 +    codigo: str  # grafia da chave no documento (AMB-038)     
       31 +    limites: dict[str, Decimal]  # categoria normalizada → lim
          +ite                                                           
       32 +                                                              
       33 +                                                              
       34 +@dataclass(frozen=True)                                       
       35 +class Politica:                                               
       36 +    """Documento de política validado (RN-015)."""            
       37 +                                                              
       38 +    moeda_base: str                                           
       39 +    limiar_nota_fiscal: Decimal                               
       40 +    padrao: dict[str, Decimal]  # categoria normalizada → limi
          +te                                                            
       41 +    centros: dict[str, Centro]  # chave normalizada → Centro  
       42 +                                                              
       43 +                                                              
       44 +def _erro(mensagem: str) -> EntradaInvalida:                  
       45 +    return EntradaInvalida(f"documento de política inválido: {
          +mensagem}")                                                   
     … 73 more lines (ctrl+o to expand)

● Bash(python - <<'EOF'
      from pathlib import Path…)
  ⎿  1 file reformatted, 11 files left unchanged
     ......................................................................
     .. [ 59%]
     … +5 lines (ctrl+o to expand)
  ⎿  Updated reembolso\politica.py (+5 -1)
      115  
      116  def ler_politica(texto: str) -> Politica:
      117      """Texto JSON → `Politica`. Levanta `EntradaInvalida` nos 
           casos de erro geral (RN-015)."""
      118 -    return validar_politica(ler_json(texto))                  
      118 +    try:                                                      
      119 +        dados = ler_json(texto)                               
      120 +    except EntradaInvalida as erro:                           
      121 +        raise _erro(str(erro)) from erro                      
      122 +    return validar_politica(dados)                            
  ⎿  Created tests\test_rn015_politica.py (+200 -0)
        1 +import copy                                                   
        2 +import json                                                   
        3 +from decimal import Decimal                                   
        4 +from pathlib import Path                                      
        5 +                                                              
        6 +import pytest                                                 
        7 +                                                              
        8 +from reembolso.entrada import EntradaInvalida                 
        9 +from reembolso.politica import ler_politica                   
       10 +                                                              
       11 +POLITICA_V4 = Path(__file__).parent.parent / "exemplos" / "env
          +elope" / "politica-v4.json"                                   
       12 +                                                              
       13 +_REMOVER = object()                                           
       14 +                                                              
       15 +                                                              
       16 +def _politica(**alteracoes):                                  
       17 +    """Política pequena e válida; `alteracoes` usa `__` como s
          +eparador de caminho."""                                       
       18 +    doc = {                                                   
       19 +        "versao": "teste",                                    
       20 +        "moeda_base": "BRL",                                  
       21 +        "padrao": {                                           
       22 +            "alimentacao": {"limite": 60.00, "periodicidade": 
          +"dia"},                                                       
       23 +            "hospedagem": {"limite": 250.00, "periodicidade": 
          +"diaria"},                                                    
       24 +        },                                                    
       25 +        "centros_custo": {                                    
       26 +            "CC-ADM": {"alimentacao": {"limite": 45.00, "perio
          +dicidade": "dia"}},                                           
       27 +        },                                                    
       28 +        "nota_fiscal_obrigatoria_acima_de": 100.00,           
       29 +    }                                                         
       30 +    doc = copy.deepcopy(doc)                                  
       31 +    for caminho, valor in alteracoes.items():                 
       32 +        alvo = doc                                            
       33 +        *pais, campo = caminho.split("__")                    
       34 +        for pai in pais:                                      
       35 +            alvo = alvo[pai]                                  
       36 +        if valor is _REMOVER:                                 
       37 +            del alvo[campo]                                   
       38 +        else:                                                 
       39 +            alvo[campo] = valor                               
       40 +    return json.dumps(doc, ensure_ascii=False)                
     … 160 more lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● Bash(python /tmp/marcar.py T-027 && git add reembolso/entrada.py
      reembolso/normalizacao.py reembolso/politica.py
      tests/test_rn015_politica.py specs/001-motor-reembol…)
  ⎿  warning: in the working copy of 'reembolso/entrada.py', LF will be rep
     laced by CRLF the next time Git touches it
     warning: in the working copy of 'reembolso/normalizacao.py', LF will b
     … +9 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      303      (atualizado para oito motivos)
      304    - **Commit:**
      305  
      306 -- [ ] **T-027** — Leitura e validação do documento de política
          - (`politica.py`                                               
      306 +- [x] **T-027** — Leitura e validação do documento de política
          + (`politica.py`                                               
      307    passa a ler `politica-v4.json` e devolver um objeto `Politic
           a`). Chaves de
      308    categoria e de centro de custo e o valor de `periodicidade` 
           normalizados pela
      309    RN-002; `moeda_base` normalizada pela RN-017. A grafia origi
           nal de cada chave

● T-028 — política aplicável por centro de custo, Origem e
  justificativas.origem, além de centro_custo no Documento.

● Bash(python - <<'EOF'
      from pathlib import Path…)
  ⎿  warning: in the working copy of 'reembolso/entrada.py', LF will be rep
     laced by CRLF the next time Git touches it
     warning: in the working copy of 'reembolso/justificativas.py', LF will
     … +87 lines (ctrl+o to expand)
  ⎿  Updated reembolso\entrada.py (+6 -1)
      25      inicio: date
      26      fim: date
      27      itens: list[dict]
      28 +    centro_custo: str | None                                   
      29  
      30  
      31  def _rejeitar_constante(nome: str):
     ...
      75  
      76      if not texto_preenchido(colaborador.get("id")):
      77          raise EntradaInvalida("colaborador.id ausente, vazio ou
           não é texto")
      78 +    centro_custo = colaborador.get("centro_custo")             
      79 +    if "centro_custo" in colaborador and not isinstance(centro_
         +custo, str):                                                   
      80 +        raise EntradaInvalida("colaborador.centro_custo não é t
         +exto")                                                         
      81  
      82      inicio = data_valida(periodo.get("inicio"))
      83      if inicio is None:
     ...
       95          if not isinstance(item, dict):
       96              raise EntradaInvalida(f"item {posicao} de despesas
            não é objeto")
       97  
       94 -    return Cabecalho(colaborador, periodo, inicio, fim, itens)
       98 +    return Cabecalho(colaborador, periodo, inicio, fim, itens,
          + centro_custo)                                                
       99  
      100  
      101  def numero(valor: object) -> Decimal | None:
     ...
      184          despesas=[
      185              ler_despesa(item, posicao) for posicao, item in en
           umerate(cabecalho.itens, start=1)
      186          ],
      187 +        centro_custo=cabecalho.centro_custo,                  
      188      )
  ⎿  Updated reembolso\justificativas.py (+15 -0)
       3  from datetime import date
       4  from decimal import Decimal
       5  
       6 +from reembolso.politica import Origem, TipoOrigem              
       7 +                                                               
       8  _NOMES_CATEGORIA = {
       9      "alimentacao": "alimentação",
      10      "transporte_urbano": "transporte urbano",
     ...
      18      return f"R$ {texto}"
      19  
      20  
      21 +def origem(origem: Origem) -> str:                             
      22 +    """Política de onde veio a entrada da categoria (RN-016, DT
         +-011)."""                                                      
      23 +    match origem.tipo:                                         
      24 +        case TipoOrigem.PADRAO:                                
      25 +            return "política padrão"                           
      26 +        case TipoOrigem.CENTRO:                                
      27 +            return f"centro de custo {origem.codigo}"          
      28 +        case TipoOrigem.HERDADA:                               
      29 +            return f"centro de custo {origem.codigo} usando lim
         +ite herdado da política padrão"                                
      30 +        case TipoOrigem.NAO_CADASTRADO:                        
      31 +            return f"política padrão; centro de custo {origem.c
         +odigo} não cadastrado"                                         
      32 +                                                               
      33 +                                                               
      34  def dados_invalidos(detalhe: str) -> str:
      35      return f"Dados inválidos: {detalhe} (RN-013)."
      36  
  ⎿  Updated reembolso\modelo.py (+1 -0)
      64      inicio: date
      65      fim: date
      66      despesas: list[Despesa | Invalida]
      67 +    centro_custo: str | None = None  # como veio (já validado c
         +omo texto); None se ausente                                    
      68  
      69  
      70  @dataclass(frozen=True)
  ⎿  Updated reembolso\politica.py (+57 -1)
      1 -"""Documento de política de reembolso (RN-015) e valores da polí
        -tica, como dados (plan §4)."""                                  
      1 +"""Documento de política (RN-015), política aplicável por centro
        + de custo (RN-016) e                                            
      2 +valores da política, como dados (plan §4)."""                   
      3  
      4  from dataclasses import dataclass
      5  from decimal import Decimal
      6 +from enum import Enum                                           
      7  
      8  from reembolso.entrada import EntradaInvalida, ler_json, numero,
          texto_preenchido
      9  from reembolso.normalizacao import normalizar_moeda, normalizar_
         texto
     ...
      122      except EntradaInvalida as erro:
      123          raise _erro(str(erro)) from erro
      124      return validar_politica(dados)
      125 +                                                              
      126 +                                                              
      127 +class TipoOrigem(Enum):                                       
      128 +    """De qual tabela veio a entrada de uma categoria (RN-016)
          +."""                                                          
      129 +                                                              
      130 +    PADRAO = "padrao"  # centro de custo ausente ou vazio     
      131 +    CENTRO = "centro"  # centro cadastrado; categoria na tabel
          +a do centro ou em nenhuma                                     
      132 +    HERDADA = "herdada"  # centro cadastrado; categoria só na 
          +padrão                                                        
      133 +    NAO_CADASTRADO = "nao_cadastrado"  # centro informado e nã
          +o cadastrado                                                  
      134 +                                                              
      135 +                                                              
      136 +@dataclass(frozen=True)                                       
      137 +class Origem:                                                 
      138 +    tipo: TipoOrigem                                          
      139 +    codigo: str | None  # código a citar na justificativa (AMB
          +-038, AMB-040)                                                
      140 +                                                              
      141 +                                                              
      142 +@dataclass(frozen=True)                                       
      143 +class PoliticaAplicavel:                                      
      144 +    """Política escolhida para todas as despesas do documento 
          +(RN-016)."""                                                  
      145 +                                                              
      146 +    limiar_nota_fiscal: Decimal                               
      147 +    padrao: dict[str, Decimal]                                
      148 +    centro: Centro | None = None                              
      149 +    nao_cadastrado: str | None = None  # código do centro info
          +rmado e não cadastrado                                        
      150 +                                                              
      151 +    def regra(self, categoria: str) -> tuple[Decimal | None, O
          +rigem]:                                                       
     … 27 more lines (ctrl+o to expand)

● Percebi que o teste antigo de campos informativos/desconhecidos usa
  centro_custo: null, mas pela spec 2.1 (RN-013/RN-016) isso agora conta como
  erro geral. Vou seguir a leitura literal, atualizar esse teste e registrar a
  mudança no resumo final.

● Bash(python - <<'EOF'
      from pathlib import Path…)
  ⎿  All checks passed!
     FAILED tests/test_rastreabilidade.py::test_rastreabilidade_spec_tem_rn
     001_a_rn014
     … +5 lines (ctrl+o to expand)
  ⎿  Updated tests\test_rn013_dados_invalidos.py (+15 -1)
      81          {"despesas": _REMOVER},
      82          {"despesas": {"id": "d-001"}},
      83          {"despesas": [{"id": "d-001"}, "d-002"]},
      84 +        {"colaborador__centro_custo": 42},                     
      85 +        {"colaborador__centro_custo": None},                   
      86      ],
      87      ids=[
      88          "sem_periodo_fim",
     ...
      101          "sem_despesas",
      102          "despesas_nao_lista",
      103          "item_nao_objeto",
      104 +        "centro_custo_numerico",                              
      105 +        "centro_custo_nulo",                                  
      106      ],
      107  )
      108  def test_rn013_erro_geral_documento_invalido(alteracoes):
     ...
      126  
      127  
      128  def test_rn013_erro_geral_nao_ocorre_com_campos_informativos_e
           _desconhecidos():
      125 -    doc = _documento(colaborador__nome=123, colaborador__centr
          -o_custo=None, extra={"x": 1})                                 
      129 +    doc = _documento(colaborador__nome=123, extra={"x": 1})   
      130      validar_documento(doc)
      131  
      132  
      133 +def test_rn013_erro_geral_nao_ocorre_com_centro_custo_texto_au
          +sente_ou_vazio():                                             
      134 +    assert validar_documento(_documento(colaborador__centro_cu
          +sto="  ")).centro_custo == "  "                               
      135 +    assert validar_documento(_documento()).centro_custo is Non
          +e                                                             
      136 +                                                              
      137 +                                                              
      138 +def test_rn013_centro_custo_chega_ao_documento_como_veio():   
      139 +    texto = json.dumps(_documento(colaborador__centro_custo=" 
          +cc-comercial "))                                              
      140 +    assert ler_documento(texto).centro_custo == " cc-comercial
          + "                                                            
      141 +                                                              
      142 +                                                              
      143  def test_rn013_erro_geral_nao_ocorre_com_inicio_igual_ao_fim()
           :
      144      validar_documento(_documento(periodo__inicio="2026-07-31")
           )
      145  
  ⎿  Created tests\test_rn016_politica_aplicavel.py (+112 -0)
        1 +from decimal import Decimal                                   
        2 +from pathlib import Path                                      
        3 +                                                              
        4 +import pytest                                                 
        5 +                                                              
        6 +from reembolso import justificativas                          
        7 +from reembolso.politica import Origem, TipoOrigem, ler_politic
          +a, politica_aplicavel                                         
        8 +                                                              
        9 +POLITICA_V4 = ler_politica(                                   
       10 +    (Path(__file__).parent.parent / "exemplos" / "envelope" / 
          +"politica-v4.json").read_text(                                
       11 +        encoding="utf-8"                                      
       12 +    )                                                         
       13 +)                                                             
       14 +                                                              
       15 +                                                              
       16 +def _regra(centro_custo, categoria):                          
       17 +    return politica_aplicavel(POLITICA_V4, centro_custo).regra
          +(categoria)                                                   
       18 +                                                              
       19 +                                                              
       20 +@pytest.mark.parametrize("centro_custo", [None, "", "  "], ids
          +=["ausente", "vazio", "espacos"])                             
       21 +def test_rn016_sem_centro_usa_padrao(centro_custo):           
       22 +    assert _regra(centro_custo, "alimentacao") == (           
       23 +        Decimal("60.00"),                                     
       24 +        Origem(TipoOrigem.PADRAO, None),                      
       25 +    )                                                         
       26 +                                                              
       27 +                                                              
       28 +@pytest.mark.parametrize("centro_custo", ["CC-COMERCIAL", " cc
          +-comercial ", "Cc-Comercial"])                                
       29 +def test_rn016_centro_cadastrado_com_grafia_do_documento(centr
          +o_custo):                                                     
       30 +    assert _regra(centro_custo, "alimentacao") == (           
       31 +        Decimal("90.00"),                                     
       32 +        Origem(TipoOrigem.CENTRO, "CC-COMERCIAL"),            
       33 +    )                                                         
       34 +                                                              
       35 +                                                              
       36 +def test_rn016_centro_nao_cadastrado_usa_padrao():            
       37 +    assert _regra("CC-SUPORTE-N2", "hospedagem") == (         
       38 +        Decimal("250.00"),                                    
       39 +        Origem(TipoOrigem.NAO_CADASTRADO, "CC-SUPORTE-N2"),   
       40 +    )                                                         
     … 72 more lines (ctrl+o to expand)

● Bash(git status --short && python /tmp/marcar.py T-028 && git add reembolso
      tests specs/001-motor-reembolso/tasks.md ':!reembolso/docs' && git commit
      -q -m "feat(T-0…)
  ⎿   M reembolso/entrada.py
      M reembolso/justificativas.py
      M reembolso/modelo.py
     … +15 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      326    - **Teste:** `tests/test_rn015_politica.py`
      327    - **Commit:**
      328  
      329 -- [ ] **T-028** — Política aplicável: `politica_aplicavel(poli
          -tica, centro_custo)`                                          
      329 +- [x] **T-028** — Política aplicável: `politica_aplicavel(poli
          +tica, centro_custo)`                                          
      330    devolve uma `PoliticaAplicavel` cujo `regra(categoria)` dá o
            limite (ou `None`
      331    se a categoria não consta) e a `Origem(tipo, codigo)` daquel
           a categoria. O
      332    `tipo` é `PADRAO`, `CENTRO`, `HERDADA` ou `NAO_CADASTRADO`. 
           Com o centro

● T-029 — leitura e validação do documento de câmbio (sem a busca de cotação,
  que é da T-034).

● Bash(cat > reembolso/cambio.py <<'EOF'
      """Documento de câmbio (RN-018)."""…)
  ⎿  All checks passed!
     FAILED tests/test_rastreabilidade.py::test_rastreabilidade_spec_tem_rn
     001_a_rn014
     … +5 lines (ctrl+o to expand)
  ⎿  Created reembolso\cambio.py (+75 -0)
       1 +"""Documento de câmbio (RN-018)."""                            
       2 +                                                               
       3 +from dataclasses import dataclass                              
       4 +from datetime import date                                      
       5 +from decimal import Decimal                                    
       6 +                                                               
       7 +from reembolso.entrada import EntradaInvalida, data_valida, ler
         +_json, numero, texto_preenchido                                
       8 +from reembolso.normalizacao import normalizar_moeda            
       9 +                                                               
      10 +                                                               
      11 +@dataclass(frozen=True)                                        
      12 +class Cambio:                                                  
      13 +    """Documento de câmbio validado (RN-018)."""               
      14 +                                                               
      15 +    moeda_base: str                                            
      16 +    taxas: dict[str, list[tuple[date, Decimal]]]  # moeda → (da
         +ta, taxa), ordenado por data                                   
      17 +                                                               
      18 +                                                               
      19 +def _erro(mensagem: str) -> EntradaInvalida:                   
      20 +    return EntradaInvalida(f"documento de câmbio inválido: {men
         +sagem}")                                                       
      21 +                                                               
      22 +                                                               
      23 +def _taxas_da_data(chave: str, taxas: object) -> dict[str, Deci
         +mal]:                                                          
      24 +    """Taxas de uma data, com código normalizado (RN-017); taxa
         + deve ser número > 0."""                                       
      25 +    if not isinstance(taxas, dict):                            
      26 +        raise _erro(f"taxas.{chave} não é objeto")             
      27 +    lidas = {}                                                 
      28 +    for moeda, taxa in taxas.items():                          
      29 +        convertida = numero(taxa)                              
      30 +        if convertida is None:                                 
      31 +            raise _erro(f"taxas.{chave}.{moeda} não é número") 
      32 +        if convertida <= 0:                                    
      33 +            raise _erro(f"taxas.{chave}.{moeda} é menor ou igua
         +l a zero")                                                     
      34 +        lidas[normalizar_moeda(moeda)] = convertida            
      35 +    if len(lidas) != len(taxas):                               
      36 +        raise _erro(f"taxas.{chave} tem moedas iguais depois da
         + normalização")                                                
      37 +    return lidas                                               
      38 +                                                               
      39 +                                                               
      40 +def validar_cambio(dados: object, moeda_base_politica: str) -> 
         +Cambio:                                                        
     … 35 more lines (ctrl+o to expand)
  ⎿  Created tests\test_rn018_cambio.py (+125 -0)
        1 +import copy                                                   
        2 +import json                                                   
        3 +from datetime import date                                     
        4 +from decimal import Decimal                                   
        5 +from pathlib import Path                                      
        6 +                                                              
        7 +import pytest                                                 
        8 +                                                              
        9 +from reembolso.cambio import ler_cambio                       
       10 +from reembolso.entrada import EntradaInvalida                 
       11 +                                                              
       12 +CAMBIO = Path(__file__).parent.parent / "exemplos" / "envelope
          +" / "cambio.json"                                             
       13 +                                                              
       14 +_REMOVER = object()                                           
       15 +                                                              
       16 +                                                              
       17 +def _cambio(**alteracoes):                                    
       18 +    """Câmbio pequeno e válido; `alteracoes` usa `__` como sep
          +arador de caminho."""                                         
       19 +    doc = copy.deepcopy(                                      
       20 +        {                                                     
       21 +            "moeda_base": "BRL",                              
       22 +            "fonte": "teste",                                 
       23 +            "taxas": {                                        
       24 +                "2026-07-13": {"USD": 5.42, "EUR": 5.91},     
       25 +                "2026-07-14": {"USD": 5.44},                  
       26 +            },                                                
       27 +        }                                                     
       28 +    )                                                         
       29 +    for caminho, valor in alteracoes.items():                 
       30 +        alvo = doc                                            
       31 +        *pais, campo = caminho.split("__")                    
       32 +        for pai in pais:                                      
       33 +            alvo = alvo[pai]                                  
       34 +        if valor is _REMOVER:                                 
       35 +            del alvo[campo]                                   
       36 +        else:                                                 
       37 +            alvo[campo] = valor                               
       38 +    return json.dumps(doc)                                    
       39 +                                                              
       40 +                                                              
     … 85 more lines (ctrl+o to expand)

● Bash(python /tmp/marcar.py T-029 && git add reembolso/cambio.py
      tests/test_rn018_cambio.py specs/001-motor-reembolso/tasks.md && git
      commit -q -m "feat(T-029): le e…)
  ⎿  warning: in the working copy of 'specs/001-motor-reembolso/tasks.md',
     LF will be replaced by CRLF the next time Git touches it
     warning: in the working copy of 'reembolso/cambio.py', LF will be repl
     … +157 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      361      `centro_custo` numérico)
      362    - **Commit:**
      363  
      364 -- [ ] **T-029** — Leitura e validação do documento de câmbio (
          -`cambio.py` →                                                 
      364 +- [x] **T-029** — Leitura e validação do documento de câmbio (
          +`cambio.py` →                                                 
      365    objeto `Cambio`), opcional. Quando informado, é sempre valid
           ado. Códigos de
      366    moeda normalizados pela RN-017. Erro → `EntradaInvalida`. Ai
           nda não é usado
      367    pelo motor.

● T-030 — campo moeda da despesa. Até a T-034, despesa em moeda estrangeira
  continua com valor_considerado arredondado como hoje ("sem mudar o resultado
  de nenhuma despesa").

● Bash(python - <<'EOF'
      from pathlib import Path…)
  ⎿  All checks passed!
     tests\test_rastreabilidade.py:28: AssertionError
     =========================== short test summary info ==================
     … +4 lines (ctrl+o to expand)
  ⎿  Updated reembolso\entrada.py (+8 -3)
       7  from decimal import Decimal
       8  
       9  from reembolso.modelo import Despesa, Documento, Invalida
      10 -from reembolso.normalizacao import arredondar, normalizar_texto
      10 +from reembolso.normalizacao import arredondar, normalizar_moeda
         +, normalizar_texto                                             
      11  
      12  _FORMATO_DATA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
      13  
     ...
      136          problemas.append("tem_nota_fiscal ausente")
      137      elif not isinstance(item["tem_nota_fiscal"], bool):
      138          problemas.append("tem_nota_fiscal não é verdadeiro/fal
           so")
      139 +    if "moeda" in item:                                       
      140 +        problemas.append(_problema_texto(item, "moeda"))      
      141      return [p for p in problemas if p is not None]
      142  
      143  
      144  def validar_despesa(item: dict, posicao: int) -> Invalida | No
           ne:
      145      """Devolve `Invalida` se a despesa tiver erro da RN-013, o
           u `None` se for válida.
      146  
      145 -    Campos informativos (`descricao`) e desconhecidos não são 
          -lidos.                                                        
      147 +    `moeda` é opcional; presente, deve ser texto não vazio (RN
          +-017). Campos informativos                                    
      148 +    (`descricao`) e desconhecidos não são lidos.              
      149      """
      150      problemas = _problemas(item)
      151      if not problemas:
     ...
      159  
      160  
      161  def ler_despesa(item: dict, posicao: int) -> Despesa | Invalid
           a:
      159 -    """Etapas 1 e 2 da spec §8: valida (RN-013), normaliza (RN
          --002) e arredonda (RN-003)."""                                
      162 +    """Etapas 1 e 2 da spec §8: valida (RN-013, RN-017), norma
          +liza (RN-002, RN-017) e                                       
      163 +    arredonda (RN-003). Sem `moeda`, a moeda é `BRL` (RN-017).
          +"""                                                           
      164      invalida = validar_despesa(item, posicao)
      165      if invalida is not None:
      166          return invalida
     ...
      174          tem_nota_fiscal=item["tem_nota_fiscal"],
      175          valor_informado=valor_informado,
      176          valor_considerado=arredondar(valor_informado),
      177 +        moeda=normalizar_moeda(item.get("moeda", "BRL")),     
      178      )
      179  
     … 1 more lines (ctrl+o to expand)
  ⎿  Updated reembolso\motor.py (+2 -0)
      66          status=Status.RECUSADO,
      67          motivo=recusa.motivo,
      68          justificativa=recusa.justificativa,
      69 +        moeda=getattr(despesa, "moeda", None),  # nula em DADOS
         +_INVALIDOS (RN-013)                                            
      70      )
      71  
      72  
     ...
      86          status=status,
      87          motivo=motivo,
      88          justificativa=texto,
      89 +        moeda=despesa.moeda,                                   
      90      )
      91  
      92  
  ⎿  Updated tests\test_rn013_dados_invalidos.py (+1 -1)
      245  
      246  
      247  def test_rn013_despesa_campo_desconhecido_e_ignorado():
      248 -    assert validar_despesa(_despesa(moeda="USD"), posicao=1) i
          -s None                                                        
      248 +    assert validar_despesa(_despesa(projeto="X"), posicao=1) i
          +s None                                                        
      249  
      250  
      251  def test_rn013_despesa_descricao_malformada_e_ignorada():
  ⎿  Created tests\test_rn017_moeda.py (+80 -0)
       1 +import json                                                    
       2 +from decimal import Decimal                                    
       3 +                                                               
       4 +import pytest                                                  
       5 +                                                               
       6 +from reembolso.entrada import ler_despesa, ler_documento       
       7 +from reembolso.modelo import Despesa, Invalida, Motivo         
       8 +from reembolso.motor import calcular                           
       9 +from reembolso.normalizacao import normalizar_moeda            
      10 +                                                               
      11 +_REMOVER = object()                                            
      12 +                                                               
      13 +                                                               
      14 +def _despesa(**alteracoes):                                    
      15 +    item = {                                                   
      16 +        "id": "e-010",                                         
      17 +        "data": "2026-07-27",                                  
      18 +        "categoria": "alimentacao",                            
      19 +        "fornecedor": "Bistro Central",                        
      20 +        "valor": Decimal("88.00"),                             
      21 +        "tem_nota_fiscal": True,                               
      22 +    }                                                          
      23 +    for campo, valor in alteracoes.items():                    
      24 +        if valor is _REMOVER:                                  
      25 +            del item[campo]                                    
      26 +        else:                                                  
      27 +            item[campo] = valor                                
      28 +    return item                                                
      29 +                                                               
      30 +                                                               
      31 +def test_rn017_moeda_ausente_e_brl():                          
      32 +    despesa = ler_despesa(_despesa(), posicao=1)               
      33 +    assert isinstance(despesa, Despesa)                        
      34 +    assert despesa.moeda == "BRL"                              
      35 +                                                               
      36 +                                                               
      37 +@pytest.mark.parametrize("moeda, esperada", [(" usd ", "USD"), 
         +("eur", "EUR"), ("BRL", "BRL")])                               
      38 +def test_rn017_moeda_normalizada(moeda, esperada):             
      39 +    assert ler_despesa(_despesa(moeda=moeda), posicao=1).moeda 
         +== esperada                                                    
      40 +                                                               
     … 40 more lines (ctrl+o to expand)

● Bash(python /tmp/marcar.py T-030 && git add reembolso tests
      specs/001-motor-reembolso/tasks.md ':!reembolso/docs' && git commit -q -m
      "feat(T-030): le e normaliza a…)  ⎿  warning: in the working copy of 'reembolso/entrada.py', LF will be rep
     laced by CRLF the next time Git touches it
     warning: in the working copy of 'reembolso/motor.py', LF will be repla
     … +265 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      375    - **Teste:** `tests/test_rn018_cambio.py::test_rn018_documen
           to_*`
      376    - **Commit:**
      377  
      378 -- [ ] **T-030** — Campo `moeda` da despesa: ausente → `BRL`; t
          -exto normalizado                                              
      378 +- [x] **T-030** — Campo `moeda` da despesa: ausente → `BRL`; t
          +exto normalizado                                              
      379    (pontas e maiúsculas); vazio ou não texto → `DADOS_INVALIDOS
           ` com `moeda` nulo.
      380    Qualquer código não vazio é aceito. Revisa a T-007, onde `mo
           eda` era ignorada.
      381    - **Atende:** RN-017, RN-013 (erro em uma despesa), AMB-024

● T-031 é a troca de assinatura (Contexto), com política externa no motor e na
  CLI. Primeiro vejo todos os pontos que chamam calcular e as etapas.

  Searched for 1 pattern, ran 1 shell command (ctrl+o to expand)

● Agora escrevo o código de produção da T-031.

  Ran 1 shell command (ctrl+o to expand)

● O heredoc falhou no shell; vou gravar o script num arquivo e executar.

  Ran 1 shell command (ctrl+o to expand)

● Write(~\AppData\Local\Temp\t031.py)
  ⎿  Wrote 254 lines to
     ..\..\..\..\..\Users\Remakker\AppData\Local\Temp\t031.py
       1 from pathlib import Path
       2 
       3 
       4 def editar(caminho, *trocas):
       5     p = Path(caminho)
       6     s = p.read_text(encoding="utf-8")
       7     for old, new in trocas:
       8         assert old in s, (caminho, old[:60])
       9         s = s.replace(old, new)
      10     p.write_text(s, encoding="utf-8", newline="\n")
     … +312 lines (ctrl+o to expand)

● Bash(python /tmp/t031.py && grep -n "Documento" reembolso/motor.py
      reembolso/etapas.py; .venv/Scripts/ruff check reembolso)
  ⎿  reembolso/motor.py:14:    Documento,
     reembolso/motor.py:97:    documento: Documento,
     reembolso/etapas.py:9:from reembolso.modelo import Corte, Despesa, Doc
     … +3 lines (ctrl+o to expand)
  ⎿  Updated reembolso\cli.py (+17 -7)
       6  
       7  from reembolso.entrada import EntradaInvalida, ler_documento
       8  from reembolso.motor import calcular
       9 +from reembolso.politica import ler_politica, politica_aplicavel
      10  from reembolso.saida import montar_saida, serializar
      11  
      12  
     ...
      20          "calcular", help="calcula o reembolso de um documento d
          e despesas"
      21      )
      22      calcular_.add_argument("--input", required=True, type=Path,
           help="JSON de despesas")
      23 +    # Não é obrigatório no argparse: a falta da política é erro
         + geral, código 1 (DT-006).                                     
      24 +    calcular_.add_argument("--politica", type=Path, help="JSON 
         +da política de reembolso")                                     
      25      calcular_.add_argument("--output", required=True, type=Path
          , help="JSON de resultado")
      26      return parser
      27  
      28  
      26 -def _calcular(entrada: Path) -> str:                           
      29 +def _ler(caminho: Path) -> str:                                
      30      try:
      28 -        texto = entrada.read_text(encoding="utf-8-sig")        
      31 +        return caminho.read_text(encoding="utf-8-sig")         
      32      except (OSError, UnicodeDecodeError) as erro:
      30 -        raise EntradaInvalida(f"não foi possível ler {entrada}:
         - {erro}") from erro                                            
      31 -    documento = ler_documento(texto)                           
      32 -    return serializar(montar_saida(documento, calcular(document
         -o)))                                                           
      33 +        raise EntradaInvalida(f"não foi possível ler {caminho}:
         + {erro}") from erro                                            
      34 +                                                               
      35 +                                                               
      36 +def _calcular(entrada: Path, politica: Path | None) -> str:    
      37 +    documento = ler_documento(_ler(entrada))                   
      38 +    if politica is None:                                       
      39 +        raise EntradaInvalida("documento de política não inform
         +ado (--politica)")                                             
      40 +    # Até a T-038, o fluxo real usa a política padrão, sem esco
         +lher por centro de custo.                                      
      41 +    aplicavel = politica_aplicavel(ler_politica(_ler(politica))
         +, None)                                                        
      42 +    return serializar(montar_saida(documento, calcular(document
         +o, aplicavel)))                                                
      43  
      44  
      45  def main(argv: list[str] | None = None) -> int:
      36 -    """Sucesso: 0. Erro geral da RN-013: mensagem em stderr, 1,
         - sem saída (DT-006).                                           
      46 +    """Sucesso: 0. Erro geral (RN-013, RN-015): mensagem em std
         +err, 1, sem saída (DT-006).                                    
     … 10 more lines (ctrl+o to expand)
  ⎿  Updated reembolso\etapas.py (+30 -17)
       1 -"""Uma função por etapa da seção 8 da spec (etapas 3 a 8)."""  
       1 +"""Uma função por etapa da seção 8 da spec."""                 
       2  
       3  from collections import defaultdict
       4 +from dataclasses import dataclass                              
       5  from decimal import Decimal
       6  
       6 -from reembolso import justificativas, politica                 
       7 +from reembolso import justificativas                           
       8 +from reembolso.cambio import Cambio                            
       9  from reembolso.modelo import Corte, Despesa, Documento, Motivo,
           Recusa
      10 +from reembolso.politica import PoliticaAplicavel               
      11  
      12  
      10 -def valor_negativo(despesa: Despesa, _documento: Documento) -> 
         -Recusa | None:                                                 
      13 +@dataclass(frozen=True)                                        
      14 +class Contexto:                                                
      15 +    """O que toda etapa recebe além das despesas (DT-009)."""  
      16 +                                                               
      17 +    documento: Documento                                       
      18 +    politica: PoliticaAplicavel                                
      19 +    cambio: Cambio | None = None                               
      20 +                                                               
      21 +                                                               
      22 +def valor_negativo(despesa: Despesa, _contexto: Contexto) -> Re
         +cusa | None:                                                   
      23      """RN-005: valor considerado menor que zero é recusado; zer
          o é válido."""
      24      if despesa.valor_considerado < 0:
      25          return Recusa(
     ...
      28      return None
      29  
      30  
      19 -def periodo(despesa: Despesa, documento: Documento) -> Recusa |
         - None:                                                         
      31 +def periodo(despesa: Despesa, contexto: Contexto) -> Recusa | N
         +one:                                                           
      32      """RN-004: a data deve estar entre início e fim, bordas inc
          luídas; competência não é usada."""
      33 +    documento = contexto.documento                             
      34      if documento.inicio <= despesa.data <= documento.fim:
      35          return None
      36      return Recusa(
     ...
      39      )
      40  
     … 53 more lines (ctrl+o to expand)
  ⎿  Updated reembolso\motor.py (+20 -11)
      1 -"""Execução das etapas 3 a 8 da spec §8 sobre as despesas de um 
        -documento."""                                                   
      1 +"""Execução das etapas da spec §8 sobre as despesas de um docume
        +nto."""                                                         
      2  
      3  from collections.abc import Callable, Sequence
      4  from dataclasses import dataclass
     ...
       6  
       7  from reembolso import etapas as regras
       8  from reembolso import justificativas
       9 +from reembolso.cambio import Cambio                            
      10 +from reembolso.etapas import Contexto                          
      11  from reembolso.modelo import (
      12      Corte,
      13      Despesa,
     ...
      18      Resultado,
      19      Status,
      20  )
      21 +from reembolso.politica import PoliticaAplicavel               
      22  
      23  ZERO = Decimal("0.00")
      24  
     ...
      27  class PorItem:
      28      """Etapa que decide sobre cada despesa isoladamente: `None`
           (passa) ou `Recusa`."""
      29  
      27 -    regra: Callable[[Despesa, Documento], Recusa | None]       
      30 +    regra: Callable[[Despesa, Contexto], Recusa | None]        
      31  
      32  
      33  @dataclass(frozen=True)
     ...
      37      Devolve as decisões indexadas pela posição; despesas ausent
          es do dicionário passam.
      38      """
      39  
      37 -    regra: Callable[[list[Despesa], Documento], dict[int, Recus
         -a | Corte]]                                                    
      40 +    regra: Callable[[list[Despesa], Contexto], dict[int, Recusa
         + | Corte]]                                                     
      41  
      42  
      43  Etapa = PorItem | EmGrupo
      44  
      42 -# Ordem das etapas 3 a 8 da spec §8. As etapas 1 e 2 acontecem 
         -em entrada.py.                                                 
      45 +# Ordem das etapas da spec §8. As etapas 1 e 2 acontecem em ent
         +rada.py.                                                       
      46  ETAPAS: list[Etapa] = [
     … 46 more lines (ctrl+o to expand)
  ⎿  Updated reembolso\politica.py (+4 -15)
      1 -"""Documento de política (RN-015), política aplicável por centro
        - de custo (RN-016) e                                            
      2 -valores da política, como dados (plan §4)."""                   
      1 +"""Documento de política (RN-015) e política aplicável por centr
        +o de custo (RN-016).                                            
      2 +                                                                
      3 +Os valores da política não estão no código: vêm do documento inf
        +ormado (plan §4, DT-004).                                       
      4 +"""                                                             
      5  
      6  from dataclasses import dataclass
      7  from decimal import Decimal
     ...
      10  from reembolso.entrada import EntradaInvalida, ler_json, numero
          , texto_preenchido
      11  from reembolso.normalizacao import normalizar_moeda, normalizar
          _texto
      12  
      11 -# RN-001: lista fechada de categorias reembolsáveis, já normali
         -zadas (RN-002).                                                
      12 -CATEGORIAS_REEMBOLSAVEIS = frozenset({"alimentacao", "transport
         -e_urbano", "hospedagem"})                                      
      13 -                                                               
      14 -# RN-007: exige nota fiscal quando o valor considerado é estrit
         -amente maior que o limiar.                                     
      15 -LIMIAR_NOTA_FISCAL = Decimal("100.00")                         
      16 -                                                               
      17 -# RN-008: limite da soma reembolsada por combinação de data e c
         -ategoria.                                                      
      18 -LIMITE_POR_DATA = {                                            
      19 -    "alimentacao": Decimal("60.00"),                           
      20 -    "transporte_urbano": Decimal("80.00"),                     
      21 -    "hospedagem": Decimal("250.00"),                           
      22 -}                                                              
      23 -                                                               
      13  MOEDA_BASE = "BRL"
      14  PERIODICIDADES = frozenset({"dia", "diaria"})
      15  

● Agora a parte mecânica dos testes: fabrica.politica_aplicavel() /
  fabrica.contexto() e as chamadas de calcular informando a política.

● Write(~\AppData\Local\Temp\t031_testes.py)
  ⎿  Wrote 82 lines to
     ..\..\..\..\..\Users\Remakker\AppData\Local\Temp\t031_testes.py
       1 """Troca mecânica das chamadas de `calcular` e das etapas nos te
         stes (T-031)."""
       2 
       3 import re
       4 from pathlib import Path
       6 TESTES = Path("tests")
       7 
       8 
       9 def _fecha(s: str, abre: int) -> int:
      10     nivel = 0
     … +76 lines (ctrl+o to expand)

● Bash(python /tmp/t031_testes.py && git diff tests | grep "^[-+]" | grep -v
      "^+++\|^---" | head -60)
  ⎿  alterado: tests\test_motor.py
     alterado: tests\test_rn001_categoria.py
     alterado: tests\test_rn004_periodo.py
     … +94 lines (ctrl+o to expand)
  ⎿  Updated tests\test_motor.py (+10 -20)
      1  from decimal import Decimal
      2  
      3 -from fabrica import despesa, documento, invalida                
      3 +from fabrica import despesa, documento, invalida, politica_aplic
        +avel                                                            
      4  
      5  from reembolso.justificativas import reais
      6  from reembolso.modelo import Corte, Motivo, Recusa, Status
     ...
      33  
      34  def test_secao8_recusada_nao_chega_a_etapa_seguinte():
      35      vistas = []
      36 -    resultados = calcular(                                     
      37 -        documento(despesa(1), despesa(2), despesa(3)),         
      38 -        [PorItem(_recusa_posicao(2)), EmGrupo(_registra(vistas)
         -)],                                                            
      39 -    )                                                          
      36 +    resultados = calcular(documento(despesa(1), despesa(2), des
         +pesa(3)), politica_aplicavel(), etapas=[PorItem(_recusa_posicao
         +(2)), EmGrupo(_registra(vistas))])                             
      37      assert vistas == [1, 3]
      38      assert resultados[1].status == Status.RECUSADO
      39      assert resultados[1].motivo == Motivo.VALOR_NEGATIVO
     ...
      45      def recusa_todas(_d, _doc):
      46          return Recusa(Motivo.FORA_DO_PERIODO, "teste (RN-004)")
      47  
      51 -    resultados = calcular(                                     
      52 -        documento(despesa(1)), [PorItem(_recusa_posicao(1)), Po
         -rItem(recusa_todas)]                                           
      53 -    )                                                          
      48 +    resultados = calcular(documento(despesa(1)), politica_aplic
         +avel(), etapas=[PorItem(_recusa_posicao(1)), PorItem(recusa_tod
         +as)])                                                          
      49      assert resultados[0].motivo == Motivo.VALOR_NEGATIVO
      50  
      51  
      52  def test_secao8_invalida_vira_dados_invalidos():
      53      vistas = []
      59 -    resultados = calcular(                                     
      60 -        documento(invalida(1, valor="50.00"), despesa(2)), [EmG
         -rupo(_registra(vistas))]                                       
      61 -    )                                                          
      54 +    resultados = calcular(documento(invalida(1, valor="50.00"),
         + despesa(2)), politica_aplicavel(), etapas=[EmGrupo(_registra(v
         +istas))])                                                      
      55      item = resultados[0]
      56      assert vistas == [2]
      57      assert item.status == Status.RECUSADO
     ...
      64  
      65  
      66  def test_secao8_invalida_com_id_nulo():
     … 42 more lines (ctrl+o to expand)
  ⎿  Updated tests\test_rn001_categoria.py (+4 -4)
      1  from decimal import Decimal
      2  
      3  import pytest
      4 -from fabrica import despesa, documento                          
      4 +from fabrica import despesa, documento, politica_aplicavel, cont
        +exto                                                            
      5  
      6  from reembolso.etapas import categoria
      7  from reembolso.modelo import Motivo, Status
     ...
      10  
      11  def test_rn001_d005_coworking_recusada():
      12      d005 = despesa(1, id="d-005", categoria="coworking", valor=
          "89.00")
      13 -    item = calcular(documento(d005))[0]                        
      13 +    item = calcular(documento(d005), politica_aplicavel())[0]  
      14      assert item.status == Status.RECUSADO
      15      assert item.motivo == Motivo.CATEGORIA_NAO_REEMBOLSAVEL
      16      assert item.valor_reembolsavel == Decimal("0.00")
     ...
      21      "nome", ["alimentacao", "transporte_urbano", "hospedagem", 
          "ALIMENTACAO", " Alimentação "]
      22  )
      23  def test_rn001_categorias_reembolsaveis_aceitas(nome):
      24 -    assert categoria(despesa(1, categoria=nome), documento()) i
         -s None                                                         
      24 +    assert categoria(despesa(1, categoria=nome), contexto()) is
         + None                                                          
      25  
      26  
      27  @pytest.mark.parametrize("nome", ["transporte", "transporte urb
          ano", "hotel", "alimentacao_extra"])
      28  def test_rn001_lista_fechada_nao_aceita_parecidas(nome):
      29 -    assert categoria(despesa(1, categoria=nome), documento()).m
         -otivo == (                                                     
      29 +    assert categoria(despesa(1, categoria=nome), contexto()).mo
         +tivo == (                                                      
      30          Motivo.CATEGORIA_NAO_REEMBOLSAVEL
      31      )
  ⎿  Updated tests\test_rn004_periodo.py (+5 -5)
      2  from decimal import Decimal
      3  
      4  import pytest
      5 -from fabrica import despesa, documento                          
      5 +from fabrica import despesa, documento, politica_aplicavel, cont
        +exto                                                            
      6  
      7  from reembolso.etapas import periodo
      8  from reembolso.modelo import Motivo, Status
     ...
      11  
      12  def test_rn004_d008_antes_do_periodo_recusada():
      13      d008 = despesa(1, id="d-008", data="2026-04-15", valor="41.
          00")
      14 -    item = calcular(documento(d008))[0]                        
      14 +    item = calcular(documento(d008), politica_aplicavel())[0]  
      15      assert item.status == Status.RECUSADO
      16      assert item.motivo == Motivo.FORA_DO_PERIODO
      17      assert item.valor_reembolsavel == Decimal("0.00")
     ...
      19  
      20  
      21  def test_rn004_depois_do_periodo_recusada():
      22 -    assert calcular(documento(despesa(1, data="2026-08-01")))[0
         -].motivo == Motivo.FORA_DO_PERIODO                             
      22 +    assert calcular(documento(despesa(1, data="2026-08-01")), p
         +olitica_aplicavel())[0].motivo == Motivo.FORA_DO_PERIODO       
      23  
      24  
      25  @pytest.mark.parametrize(
      26      "data", ["2026-07-01", "2026-07-31"], ids=["primeiro_dia", 
          "d-014_ultimo_dia"]
      27  )
      28  def test_rn004_bordas_incluidas(data):
      29 -    assert periodo(despesa(1, data=data), documento()) is None 
      29 +    assert periodo(despesa(1, data=data), contexto()) is None  
      30  
      31  
      32  def test_rn004_competencia_divergente_nao_muda_resultado():
      33      doc = documento(despesa(1, data="2026-07-10"), despesa(2, d
          ata="2026-04-15"))
      34      divergente = replace(doc, periodo={**doc.periodo, "competen
          cia": "2026-04"})
      35 -    assert calcular(divergente) == calcular(doc)               
      35 +    assert calcular(divergente, politica_aplicavel()) == calcul
         +ar(doc, politica_aplicavel())                                  
  ⎿  Updated tests\test_rn005_valor_negativo.py (+6 -6)
      1  from decimal import Decimal
      2  
      3 -from fabrica import despesa, documento                          
      3 +from fabrica import despesa, documento, politica_aplicavel, cont
        +exto                                                            
      4  
      5  from reembolso.etapas import valor_negativo
      6  from reembolso.modelo import Motivo, Status
     ...
       9  
      10  def test_rn005_d009_estorno_recusado():
      11      d009 = despesa(1, id="d-009", categoria="transporte_urbano"
          , valor="-45.00")
      12 -    item = calcular(documento(d009))[0]                        
      12 +    item = calcular(documento(d009), politica_aplicavel())[0]  
      13      assert item.status == Status.RECUSADO
      14      assert item.motivo == Motivo.VALOR_NEGATIVO
      15      assert item.valor_reembolsavel == Decimal("0.00")
     ...
      18  
      19  
      20  def test_rn005_valor_zero_aprovado():
      21 -    item = calcular(documento(despesa(1, valor="0.00")))[0]    
      21 +    item = calcular(documento(despesa(1, valor="0.00")), politi
         +ca_aplicavel())[0]                                             
      22      assert item.status == Status.APROVADO
      23      assert item.motivo is None
      24      assert item.valor_reembolsavel == Decimal("0.00")
      25  
      26  
      27  def test_rn005_negativo_que_arredonda_a_zero_aprovado():
      28 -    item = calcular(documento(despesa(1, valor="-0.004")))[0]  
      28 +    item = calcular(documento(despesa(1, valor="-0.004")), poli
         +tica_aplicavel())[0]                                           
      29      assert item.status == Status.APROVADO
      30      assert item.valor_considerado == Decimal("0.00")
      31      assert item.valor_reembolsavel == Decimal("0.00")
      32  
      33  
      34  def test_rn005_etapa_recusa_menos_um_centavo():
      35 -    assert valor_negativo(despesa(1, valor="-0.01"), documento(
         -)).motivo == Motivo.VALOR_NEGATIVO                             
      35 +    assert valor_negativo(despesa(1, valor="-0.01"), contexto()
         +).motivo == Motivo.VALOR_NEGATIVO                              
      36  
      37  
      38  def test_rn005_etapa_passa_positivo():
      39 -    assert valor_negativo(despesa(1, valor="0.01"), documento()
         -) is None                                                      
     … 1 more lines (ctrl+o to expand)
  ⎿  Updated tests\test_rn006_duplicatas.py (+13 -23)
      1  from decimal import Decimal
      2  
      3 -from fabrica import despesa, documento, invalida                
      3 +from fabrica import despesa, documento, invalida, politica_aplic
        +avel                                                            
      4  
      5  from reembolso.modelo import Motivo, Status
      6  from reembolso.motor import calcular
     ...
      12  
      13  
      14  def test_rn006_d006_d007_ambas_com_nota_mantem_a_primeira():
      15 -    d006, d007 = calcular(documento(_bistro(1, "d-006"), _bistr
         -o(2, "d-007")))                                                
      15 +    d006, d007 = calcular(documento(_bistro(1, "d-006"), _bistr
         +o(2, "d-007")), politica_aplicavel())                          
      16      assert d006.status == Status.APROVADO
      17      assert d006.valor_reembolsavel == Decimal("54.90")
      18      assert d007.status == Status.RECUSADO
     ...
      23  
      24  
      25  def test_rn006_so_a_segunda_tem_nota_mantem_a_segunda():
      26 -    primeira, segunda = calcular(                              
      27 -        documento(_bistro(1, "d-a", tem_nota_fiscal=False), _bi
         -stro(2, "d-b", tem_nota_fiscal=True))                          
      28 -    )                                                          
      26 +    primeira, segunda = calcular(documento(_bistro(1, "d-a", te
         +m_nota_fiscal=False), _bistro(2, "d-b", tem_nota_fiscal=True)),
         + politica_aplicavel())                                         
      27      assert primeira.motivo == Motivo.DUPLICATA
      28      assert "d-b" in primeira.justificativa
      29      assert segunda.status == Status.APROVADO
      30  
      31  
      32  def test_rn006_nenhuma_com_nota_mantem_a_primeira():
      35 -    primeira, segunda = calcular(                              
      36 -        documento(                                             
      33 +    primeira, segunda = calcular(documento(                    
      34              _bistro(1, "d-a", tem_nota_fiscal=False), _bistro(2
          , "d-b", tem_nota_fiscal=False)
      38 -        )                                                      
      39 -    )                                                          
      35 +        ), politica_aplicavel())                               
      36      assert primeira.status == Status.APROVADO
      37      assert segunda.motivo == Motivo.DUPLICATA
      38  
      39  
      40  def test_rn006_entre_varias_com_nota_mantem_a_de_menor_posicao(
          ):
     … 56 more lines (ctrl+o to expand)
  ⎿  … 11 more files changed

● Agora a fabrica, o teste da RN-011 que usava a constante e os testes novos da
  T-031.

● Write(~\AppData\Local\Temp\t031_b.py)
  ⎿  Wrote 214 lines to
     ..\..\..\..\..\Users\Remakker\AppData\Local\Temp\t031_b.py
       1 from pathlib import Path
       2 
       3 
       4 def editar(caminho, *trocas):
       5     p = Path(caminho)
       6     s = p.read_text(encoding="utf-8")
       7     for old, new in trocas:
       8         assert old in s, (caminho, old[:60])
       9         s = s.replace(old, new)
      10     p.write_text(s, encoding="utf-8", newline="\n")
     … +221 lines (ctrl+o to expand)

● Bash(python /tmp/t031_b.py && head -12 tests/test_rn008_limites.py)
  ⎿  from decimal import Decimal

     import pytest
     … +10 lines (ctrl+o to expand)
  ⎿  Updated tests\fabrica.py (+30 -0)
       1  """Construtores de objetos do modelo para os testes de regra (p
          lan §6)."""
       2  
       3 +import json                                                    
       4  from datetime import date
       5  from decimal import Decimal
       6 +from pathlib import Path                                       
       7  
       8 +from reembolso.cambio import Cambio                            
       9 +from reembolso.etapas import Contexto                          
      10  from reembolso.modelo import Despesa, Documento, Invalida
      11  from reembolso.normalizacao import arredondar, normalizar_texto
      12 +from reembolso.politica import PoliticaAplicavel, ler_politica 
      13 +from reembolso.politica import politica_aplicavel as _politica_
         +aplicavel                                                      
      14 +                                                               
      15 +POLITICA_V4 = Path(__file__).parent.parent / "exemplos" / "enve
         +lope" / "politica-v4.json"                                     
      16  
      17  
      18  def despesa(
     ...
      56          fim=date.fromisoformat(fim),
      57          despesas=list(despesas),
      58      )
      59 +                                                               
      60 +                                                               
      61 +def politica_aplicavel(                                        
      62 +    centro_custo: str | None = None, documento: dict | None = N
         +one                                                            
      63 +) -> PoliticaAplicavel:                                        
      64 +    """Política aplicável lida de `politica-v4.json` ou de `doc
         +umento`; padrão por padrão."""                                 
      65 +    if documento is None:                                      
      66 +        texto = POLITICA_V4.read_text(encoding="utf-8")        
      67 +    else:                                                      
      68 +        texto = json.dumps(documento)                          
      69 +    return _politica_aplicavel(ler_politica(texto), centro_cust
         +o)                                                             
      70 +                                                               
      71 +                                                               
      72 +def contexto(                                                  
      73 +    doc: Documento | None = None,                              
      74 +    politica: PoliticaAplicavel | None = None,                 
      75 +    cambio: Cambio | None = None,                              
      76 +) -> Contexto:                                                 
      77 +    """Contexto para chamar uma etapa diretamente (DT-009).""" 
     … 3 more lines (ctrl+o to expand)
  ⎿  Updated tests\test_motor.py (+21 -0)
      2  
      3  from fabrica import despesa, documento, invalida, politica_aplic
         avel
      4  
      5 +from reembolso.etapas import Contexto                           
      6  from reembolso.justificativas import reais
      7  from reembolso.modelo import Corte, Motivo, Recusa, Status
      8  from reembolso.motor import EmGrupo, PorItem, calcular
     ...
      103      assert reais(Decimal("60")) == "R$ 60,00"
      104      assert reais(Decimal("12.5")) == "R$ 12,50"
      105      assert reais(Decimal("1234.56")) == "R$ 1.234,56"
      106 +                                                              
      107 +                                                              
      108 +def test_dt009_etapas_recebem_contexto():                     
      109 +    recebidos = []                                            
      110 +                                                              
      111 +    def por_item(d, ctx):                                     
      112 +        recebidos.append(ctx)                                 
      113 +                                                              
      114 +    def em_grupo(vivas, ctx):                                 
      115 +        recebidos.append(ctx)                                 
      116 +        return {}                                             
      117 +                                                              
      118 +    doc = documento(despesa(1))                               
      119 +    politica = politica_aplicavel("CC-COMERCIAL")             
      120 +    calcular(doc, politica, etapas=[PorItem(por_item), EmGrupo
          +(em_grupo)])                                                  
      121 +    assert len(recebidos) == 2                                
      122 +    assert all(isinstance(ctx, Contexto) for ctx in recebidos)
      123 +    assert all(ctx.documento is doc for ctx in recebidos)     
      124 +    assert all(ctx.politica is politica for ctx in recebidos) 
      125 +    assert all(ctx.cambio is None for ctx in recebidos)       
  ⎿  Updated tests\test_rn007_nota_fiscal.py (+18 -0)
      47      assert nota_fiscal(_transporte(1, "y", "100.005"), contexto
          ()) is not None
      48  
      49  
      50 +def test_rn007_limiar_vem_do_documento():                      
      51 +    politica = politica_aplicavel(                             
      52 +        documento={                                            
      53 +            "moeda_base": "BRL",                               
      54 +            "padrao": {"transporte_urbano": {"limite": 500, "pe
         +riodicidade": "dia"}},                                         
      55 +            "centros_custo": {},                               
      56 +            "nota_fiscal_obrigatoria_acima_de": 150.00,        
      57 +        }                                                      
      58 +    )                                                          
      59 +    passa = _transporte(1, "a", "120.00")                      
      60 +    recusada = _transporte(1, "b", "150.01")                   
      61 +    assert nota_fiscal(passa, contexto(politica=politica)) is N
         +one                                                            
      62 +    assert nota_fiscal(recusada, contexto(politica=politica)).m
         +otivo == Motivo.NOTA_FISCAL_AUSENTE                            
      63 +    item = calcular(documento(passa), politica)[0]             
      64 +    assert item.status == Status.APROVADO                      
      65 +    assert item.valor_reembolsavel == Decimal("120.00")        
      66 +                                                               
      67 +                                                               
      68  def test_rn007_usa_valor_da_despesa_e_nao_a_soma_do_dia():
      69      # Duas despesas de 60,00 sem nota no mesmo dia somam 120,00
          , mas nenhuma passa de 100,00.
      70      resultados = calcular(documento(_transporte(1, "a", "60.00"
          ), _transporte(2, "b", "60.00", tem_nota_fiscal=True)), politic
          a_aplicavel())
  ⎿  Updated tests\test_rn008_limites.py (+66 -0)
       74      assert r009.motivo == Motivo.VALOR_NEGATIVO
       75      assert com_estorno == sem_estorno
       76      assert com_estorno.valor_reembolsavel == Decimal("80.00")
       77 +                                                              
       78 +                                                              
       79 +def _politica(alimentacao="60.00", periodicidade="dia"):      
       80 +    return politica_aplicavel(                                
       81 +        documento={                                           
       82 +            "moeda_base": "BRL",                              
       83 +            "padrao": {                                       
       84 +                "alimentacao": {"limite": alimentacao, "period
          +icidade": periodicidade},                                     
       85 +                "hospedagem": {"limite": 250, "periodicidade":
          + "diaria"},                                                   
       86 +            },                                                
       87 +            "centros_custo": {},                              
       88 +            "nota_fiscal_obrigatoria_acima_de": 100,          
       89 +        }                                                     
       90 +    )                                                         
       91 +                                                              
       92 +                                                              
       93 +def _numeros(politica_json: dict) -> dict:                    
       94 +    return json.loads(json.dumps(politica_json), parse_float=D
          +ecimal)                                                       
       95 +                                                              
       96 +                                                              
       97 +def test_rn008_limite_vem_do_documento():                     
       98 +    politica = politica_aplicavel(                            
       99 +        documento={                                           
      100 +            "moeda_base": "BRL",                              
      101 +            "padrao": {"alimentacao": {"limite": 70.00, "perio
          +dicidade": "dia"}},                                           
      102 +            "centros_custo": {},                              
      103 +            "nota_fiscal_obrigatoria_acima_de": 100.00,       
      104 +        }                                                     
      105 +    )                                                         
      106 +    primeira, segunda = calcular(                             
      107 +        documento(                                            
      108 +            despesa(1, data="2026-07-03", valor="50.00"),     
      109 +            despesa(2, data="2026-07-03", valor="50.00"),     
      110 +        ),                                                    
      111 +        politica,                                             
      112 +    )                                                         
      113 +    assert primeira.valor_reembolsavel == Decimal("50.00")    
     … 29 more lines (ctrl+o to expand)
  ⎿  Updated tests\test_rn011_viagem.py (+4 -3)
       8  from reembolso.entrada import ler_documento
       9  from reembolso.modelo import Despesa
      10  from reembolso.motor import calcular
      11 -from reembolso.politica import LIMITE_POR_DATA                 
      11  
      12  EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas
          -exemplo.json"
      13  
     ...
      67      for despesa, resultado in zip(documento.despesas, resultado
          s, strict=True):
      68          assert isinstance(despesa, Despesa)
      69          soma[(despesa.data, despesa.categoria)] += resultado.va
          lor_reembolsavel
      70 +    politica = politica_aplicavel()                            
      71      for (_, categoria), total in soma.items():
      72 -        if categoria in LIMITE_POR_DATA:                       
      73 -            assert total <= LIMITE_POR_DATA[categoria]         
      72 +        limite, _ = politica.regra(categoria)                  
      73 +        if limite is not None:                                 
      74 +            assert total <= limite                             

● Deixei dois helpers sem uso (_politica, _numeros) no test_rn008; vou
  removê-los.

● Bash(python - <<'PY'
      from pathlib import Path…)
  ⎿  E501 Line too long (160 > 100)
       --> tests\test_motor.py:37:101
        |
     … +170 lines (ctrl+o to expand)
  ⎿  Updated tests\fabrica.py (+1 -3)
      75      cambio: Cambio | None = None,
      76  ) -> Contexto:
      77      """Contexto para chamar uma etapa diretamente (DT-009)."""
      78 -    return Contexto(                                           
      79 -        doc or documento(), politica or politica_aplicavel(), c
         -ambio                                                          
      80 -    )                                                          
      78 +    return Contexto(doc or documento(), politica or politica_ap
         +licavel(), cambio)                                             
  ⎿  Updated tests\test_motor.py (+26 -6)
      34  
      35  def test_secao8_recusada_nao_chega_a_etapa_seguinte():
      36      vistas = []
      37 -    resultados = calcular(documento(despesa(1), despesa(2), des
         -pesa(3)), politica_aplicavel(), etapas=[PorItem(_recusa_posicao
         -(2)), EmGrupo(_registra(vistas))])                             
      37 +    resultados = calcular(                                     
      38 +        documento(despesa(1), despesa(2), despesa(3)),         
      39 +        politica_aplicavel(),                                  
      40 +        etapas=[PorItem(_recusa_posicao(2)), EmGrupo(_registra(
         +vistas))],                                                     
      41 +    )                                                          
      42      assert vistas == [1, 3]
      43      assert resultados[1].status == Status.RECUSADO
      44      assert resultados[1].motivo == Motivo.VALOR_NEGATIVO
     ...
      50      def recusa_todas(_d, _doc):
      51          return Recusa(Motivo.FORA_DO_PERIODO, "teste (RN-004)")
      52  
      49 -    resultados = calcular(documento(despesa(1)), politica_aplic
         -avel(), etapas=[PorItem(_recusa_posicao(1)), PorItem(recusa_tod
         -as)])                                                          
      53 +    resultados = calcular(                                     
      54 +        documento(despesa(1)),                                 
      55 +        politica_aplicavel(),                                  
      56 +        etapas=[PorItem(_recusa_posicao(1)), PorItem(recusa_tod
         +as)],                                                          
      57 +    )                                                          
      58      assert resultados[0].motivo == Motivo.VALOR_NEGATIVO
      59  
      60  
      61  def test_secao8_invalida_vira_dados_invalidos():
      62      vistas = []
      55 -    resultados = calcular(documento(invalida(1, valor="50.00"),
         - despesa(2)), politica_aplicavel(), etapas=[EmGrupo(_registra(v
         -istas))])                                                      
      63 +    resultados = calcular(                                     
      64 +        documento(invalida(1, valor="50.00"), despesa(2)),     
      65 +        politica_aplicavel(),                                  
      66 +        etapas=[EmGrupo(_registra(vistas))],                   
      67 +    )                                                          
      68      item = resultados[0]
      69      assert vistas == [2]
      70      assert item.status == Status.RECUSADO
     ...
      81  
      82  
      83  def test_secao8_resultado_na_ordem_da_entrada():
      72 -    resultados = calcular(documento(despesa(1), invalida(2), de
         -spesa(3), despesa(4)), politica_aplicavel(), etapas=[PorItem(_r
         -ecusa_posicao(3))])                                            
      84 +    resultados = calcular(                                     
     … 27 more lines (ctrl+o to expand)
  ⎿  Updated tests\test_rn001_categoria.py (+1 -1)
      1  from decimal import Decimal
      2  
      3  import pytest
      4 -from fabrica import despesa, documento, politica_aplicavel, cont
        -exto                                                            
      4 +from fabrica import contexto, despesa, documento, politica_aplic
        +avel                                                            
      5  
      6  from reembolso.etapas import categoria
      7  from reembolso.modelo import Motivo, Status
  ⎿  Updated tests\test_rn004_periodo.py (+5 -2)
      2  from decimal import Decimal
      3  
      4  import pytest
      5 -from fabrica import despesa, documento, politica_aplicavel, cont
        -exto                                                            
      5 +from fabrica import contexto, despesa, documento, politica_aplic
        +avel                                                            
      6  
      7  from reembolso.etapas import periodo
      8  from reembolso.modelo import Motivo, Status
     ...
      19  
      20  
      21  def test_rn004_depois_do_periodo_recusada():
      22 -    assert calcular(documento(despesa(1, data="2026-08-01")), p
         -olitica_aplicavel())[0].motivo == Motivo.FORA_DO_PERIODO       
      22 +    assert (                                                   
      23 +        calcular(documento(despesa(1, data="2026-08-01")), poli
         +tica_aplicavel())[0].motivo                                    
      24 +        == Motivo.FORA_DO_PERIODO                              
      25 +    )                                                          
      26  
      27  
      28  @pytest.mark.parametrize(
  ⎿  Updated tests\test_rn005_valor_negativo.py (+1 -1)
      1  from decimal import Decimal
      2  
      3 -from fabrica import despesa, documento, politica_aplicavel, cont
        -exto                                                            
      3 +from fabrica import contexto, despesa, documento, politica_aplic
        +avel                                                            
      4  
      5  from reembolso.etapas import valor_negativo
      6  from reembolso.modelo import Motivo, Status
  ⎿  … 10 more files changed

● Lint ok depois do ruff format. Falta o test_cli.py: passar --politica e
  incluir os testes de política ausente, inexistente e inválida.

● Write(~\AppData\Local\Temp\t031_cli.py)
  ⎿  Wrote 89 lines to
     ..\..\..\..\..\Users\Remakker\AppData\Local\Temp\t031_cli.py
       1 from pathlib import Path
       2 
       3 p = Path("tests/test_cli.py")
       4 s = p.read_text(encoding="utf-8")
       5 
       6 
       7 def trocar(old, new, count=1):
       8     global s
       9     assert s.count(old) == count, (old, s.count(old))
      10     s = s.replace(old, new)
     … +90 lines (ctrl+o to expand)

● Bash(python /tmp/t031_cli.py && .venv/Scripts/ruff format . -q;
      .venv/Scripts/ruff check . && .venv/Scripts/ruff format --check . &&
      .venv/Scripts/python -m pytest -…)
  ⎿  All checks passed!
     39 files already formatted
     =========================== short test summary info ==================
     … +12 lines (ctrl+o to expand)
  ⎿  Updated tests\test_cli.py (+67 -6)
       7  
       8  RAIZ = Path(__file__).parent.parent
       9  EXEMPLO = RAIZ / "exemplos" / "despesas-exemplo.json"
      10 +POLITICA = RAIZ / "exemplos" / "envelope" / "politica-v4.json" 
      11  
      12  CONTEUDO_ANTERIOR = '{"conteudo": "anterior"}\n'
      13  
     ...
      34  
      35  def test_cli_exemplo_gera_arquivo(tmp_path):
      36      saida = tmp_path / "resultado.json"
      36 -    processo = _rodar("calcular", "--input", EXEMPLO, "--output
         -", saida)                                                      
      37 +    processo = _rodar("calcular", "--input", EXEMPLO, "--politi
         +ca", POLITICA, "--output", saida)                              
      38      assert processo.returncode == 0, processo.stderr
      39      resultado = json.loads(saida.read_text(encoding="utf-8"), p
          arse_float=Decimal)
      40      assert len(resultado["itens"]) == 14
     ...
      44  def test_dt006_erro_geral_nao_sobrescreve_saida(tmp_path):
      45      saida = tmp_path / "resultado.json"
      46      saida.write_text(CONTEUDO_ANTERIOR, encoding="utf-8")
      46 -    processo = _rodar("calcular", "--input", _sem_periodo_fim(t
         -mp_path), "--output", saida)                                   
      47 +    processo = _rodar(                                         
      48 +        "calcular", "--input", _sem_periodo_fim(tmp_path), "--p
         +olitica", POLITICA, "--output", saida                          
      49 +    )                                                          
      50      assert processo.returncode == 1
      51      assert saida.read_text(encoding="utf-8") == CONTEUDO_ANTERI
          OR
      52  
      53  
      54  def test_dt006_erro_geral_nao_cria_saida(tmp_path):
      55      saida = tmp_path / "resultado.json"
      53 -    processo = _rodar("calcular", "--input", _sem_periodo_fim(t
         -mp_path), "--output", saida)                                   
      56 +    processo = _rodar(                                         
      57 +        "calcular", "--input", _sem_periodo_fim(tmp_path), "--p
         +olitica", POLITICA, "--output", saida                          
      58 +    )                                                          
      59      assert processo.returncode == 1
      60      assert not saida.exists()
      61  
      62  
      63  def test_dt006_erro_geral_retorna_1_e_escreve_stderr(tmp_path):
      64      saida = tmp_path / "resultado.json"
      60 -    processo = _rodar("calcular", "--input", _sem_periodo_fim(t
         -mp_path), "--output", saida)                                   
      65 +    processo = _rodar(                                         
     … 78 more lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● Update(tests\test_secao9_aceite_exemplo.py)
  ⎿  Added 12 lines, removed 1 line
       96  
       97  def _rodar_cli(saida_path):
       98      return subprocess.run(
       99 -        [sys.executable, "-m", "reembolso", "calcular", "--inp
          -ut", EXEMPLO, "--output", saida_path],                        
       99 +        [                                                     
      100 +            sys.executable,                                   
      101 +            "-m",                                             
      102 +            "reembolso",                                      
      103 +            "calcular",                                       
      104 +            "--input",                                        
      105 +            EXEMPLO,                                          
      106 +            "--politica",                                     
      107 +            POLITICA,                                         
      108 +            "--output",                                       
      109 +            saida_path,                                       
      110 +        ],                                                    
      111          capture_output=True,
      112          cwd=EXEMPLO.parent.parent,
      113          check=True,

● Update(tests\test_secao9_aceite_exemplo.py)
  ⎿  Added 1 line
      13  from reembolso.saida import montar_saida, serializar
      14  
      15  EXEMPLO = Path(__file__).parent.parent / "exemplos" / "despesas
          -exemplo.json"
      16 +POLITICA = Path(__file__).parent.parent / "exemplos" / "envelop
         +e" / "politica-v4.json"                                        
      17  
      18  # Tabela da seção 9 da spec: id, valor_reembolsavel, status, mo
          tivo.
      19  TABELA_SECAO9 = [

  Ran 1 shell command (ctrl+o to expand)

● Suíte verde, tirando a falha conhecida da rastreabilidade (é da T-041).
  Confiro rapidamente o diff da CLI e da fábrica antes de commitar.

  Ran 1 shell command (ctrl+o to expand)

● Bash(python /tmp/marcar.py T-031 && git add reembolso tests
      specs/001-motor-reembolso/tasks.md ':!reembolso/docs' && git commit -q -m
      "feat(T-031): le a politica ext…)
  ⎿  warning: in the working copy of 'reembolso/cli.py', LF will be replace
     d by CRLF the next time Git touches it
     warning: in the working copy of 'reembolso/etapas.py', LF will be repl
     … +82 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      389  
      390  ### 7.2 — Regras com política externa e câmbio
      391  
      392 -- [ ] **T-031** — Política externa no motor e na CLI:         
      392 +- [x] **T-031** — Política externa no motor e na CLI:         
      393    `calcular(documento, politica, cambio=None, etapas=None)` mo
           nta um
      394    `Contexto(documento, politica, cambio)` e o passa a todas as
            etapas no lugar
      395    do `Documento` (troca mecânica de assinatura de todas as eta
           pas, num único

● T-032 — etapa de categoria pela política aplicável (limite 0 recusa;
  justificativa cita a origem).
  Searched for 1 pattern (ctrl+o to expand)

● Write(~\AppData\Local\Temp\t032.py)
  ⎿  Wrote 205 lines to
     ..\..\..\..\..\Users\Remakker\AppData\Local\Temp\t032.py
       1 from pathlib import Path
       2 
       3 
       4 def editar(caminho, *trocas):
       5     p = Path(caminho)
       6     s = p.read_text(encoding="utf-8")
       7     for old, new in trocas:
       8         assert old in s, (caminho, old[:60])
       9         s = s.replace(old, new)
      10     p.write_text(s, encoding="utf-8", newline="\n")
     … +230 lines (ctrl+o to expand)

● Bash(python /tmp/t032.py && .venv/Scripts/ruff format . -q; .venv/Scripts/ruff
      check . && .venv/Scripts/ruff format --check . && .venv/Scripts/python -m
      pytest -q 2>…)
  ⎿  All checks passed!
     39 files already formatted
     =========================== short test summary info ==================
     … +4 lines (ctrl+o to expand)
  ⎿  Updated reembolso\etapas.py (+8 -4)
      40  
      41  
      42  def categoria(despesa: Despesa, contexto: Contexto) -> Recusa |
           None:
      43 -    """RN-001: só categorias que constam da política aplicável,
         - comparadas após normalização."""                              
      44 -    limite, _origem = contexto.politica.regra(despesa.categoria
         -)                                                              
      45 -    if limite is not None:                                     
      43 +    """RN-001, RN-016: reembolsável só se consta da política ap
         +licável com limite maior que zero.                             
      44 +                                                               
      45 +    Comparada após normalização (RN-002); limite 0 é "não reemb
         +olsável" (AMB-022), e o texto                                  
      46 +    de `observacao` não é usado.                               
      47 +    """                                                        
      48 +    limite, origem = contexto.politica.regra(despesa.categoria)
      49 +    if limite is not None and limite > 0:                      
      50          return None
      51      return Recusa(
      52          Motivo.CATEGORIA_NAO_REEMBOLSAVEL,
      49 -        justificativas.categoria_nao_reembolsavel(despesa.categ
         -oria),                                                         
      53 +        justificativas.categoria_nao_reembolsavel(despesa.categ
         +oria, origem),                                                 
      54      )
      55  
      56  
  ⎿  Updated reembolso\justificativas.py (+6 -2)
      45      return f"Data {data} fora do período de {inicio} a {fim} (R
          N-004)."
      46  
      47  
      48 -def categoria_nao_reembolsavel(categoria: str) -> str:         
      49 -    return f"Categoria '{categoria}' não é reembolsável pela po
         -lítica (RN-001)."                                              
      48 +def categoria_nao_reembolsavel(categoria: str, politica: Origem
         +) -> str:                                                      
      49 +    """Cita a política aplicada (spec §4, RN-016)."""          
      50 +    return (                                                   
      51 +        f"Categoria '{categoria}' não é reembolsável pela polít
         +ica aplicada "                                                 
      52 +        f"({origem(politica)}) (RN-001, RN-016)."              
      53 +    )                                                          
      54  
      55  
      56  def duplicata(id_mantida: str) -> str:
  ⎿  Updated tests\test_rn001_categoria.py (+115 -0)
      15      assert item.motivo == Motivo.CATEGORIA_NAO_REEMBOLSAVEL
      16      assert item.valor_reembolsavel == Decimal("0.00")
      17      assert "RN-001" in item.justificativa
      18 +    assert "política padrão" in item.justificativa             
      19  
      20  
      21  @pytest.mark.parametrize(
     ...
       30      assert categoria(despesa(1, categoria=nome), contexto()).m
           otivo == (
       31          Motivo.CATEGORIA_NAO_REEMBOLSAVEL
       32      )
       33 +                                                              
       34 +                                                              
       35 +def _recusa(centro_custo, nome, politica=None):               
       36 +    politica = politica or politica_aplicavel(centro_custo)   
       37 +    return categoria(despesa(1, categoria=nome), contexto(poli
          +tica=politica))                                               
       38 +                                                              
       39 +                                                              
       40 +def test_rn001_d010_hospedagem_com_limite_zero_recusada():    
       41 +    d010 = despesa(1, id="d-010", data="2026-07-14", categoria
          +="hospedagem", valor="480.00")                                
       42 +    item = calcular(documento(d010), politica_aplicavel("CC-EN
          +G-PLATAFORMA"))[0]                                            
       43 +    assert item.status == Status.RECUSADO                     
       44 +    assert item.motivo == Motivo.CATEGORIA_NAO_REEMBOLSAVEL   
       45 +    assert item.valor_reembolsavel == Decimal("0.00")         
       46 +    assert "RN-001" in item.justificativa                     
       47 +    assert "centro de custo CC-ENG-PLATAFORMA" in item.justifi
          +cativa                                                        
       48 +                                                              
       49 +                                                              
       50 +def test_rn001_d013_limite_zero_vem_antes_da_nota_fiscal():   
       51 +    d013 = despesa(1, id="d-013", categoria="hospedagem", valo
          +r="690.00", tem_nota_fiscal=False)                            
       52 +    item = calcular(documento(d013), politica_aplicavel("CC-EN
          +G-PLATAFORMA"))[0]                                            
       53 +    assert item.motivo == Motivo.CATEGORIA_NAO_REEMBOLSAVEL   
       54 +                                                              
       55 +                                                              
       56 +def test_rn001_f003_representacao_na_padrao_recusada():       
       57 +    recusa = _recusa("CC-SUPORTE-N2", "representacao")        
       58 +    assert recusa.motivo == Motivo.CATEGORIA_NAO_REEMBOLSAVEL 
       59 +    assert "política padrão; centro de custo CC-SUPORTE-N2 não
          + cadastrado" in recusa.justificativa                          
       60 +                                                              
       61 +                                                              
       62 +def test_rn001_e001_representacao_no_comercial_passa():       
     … 84 more lines (ctrl+o to expand)

● Bash(python /tmp/marcar.py T-032 && git add reembolso tests
      specs/001-motor-reembolso/tasks.md ':!reembolso/docs' && git commit -q -m
      "feat(T-032): recusa categoria…)
  ⎿  warning: in the working copy of 'reembolso/etapas.py', LF will be repl
     aced by CRLF the next time Git touches it
     warning: in the working copy of 'reembolso/justificativas.py', LF will
     … +169 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      420      `::test_rn015_politica_invalida_nao_sobrescreve_saida`
      421    - **Commit:**
      422  
      423 -- [ ] **T-032** — Etapa de categoria pela política aplicável: 
          -reembolsável só se                                            
      423 +- [x] **T-032** — Etapa de categoria pela política aplicável: 
          +reembolsável só se                                            
      424    consta da tabela efetiva com limite maior que zero; limite 0
           ,00 →
      425    `CATEGORIA_NAO_REEMBOLSAVEL`; `observacao` ignorada. A justi
           ficativa cita a
      426    origem da categoria (T-028). Revisa a T-012.

● Encontrei o limite diário aplicável na tabela efetiva e vou justificar o valor
  de LIMITE_DIARIO com base na origem, seguindo o formato dos exemplos da §4
  (ex.: "Limite diário de alimentação de R$ 75,00 (centro de custo
  CC-ENG-PLATAFORMA), com...").

  Searched for 1 pattern (ctrl+o to expand)

● Write(~\AppData\Local\Temp\t033.py)
  ⎿  Wrote 286 lines to
     ..\..\..\..\..\Users\Remakker\AppData\Local\Temp\t033.py
       1 from pathlib import Path
       2 
       3 
       4 def editar(caminho, *trocas):
       5     p = Path(caminho)
       6     s = p.read_text(encoding="utf-8")
       7     for old, new in trocas:
       8         assert old in s, (caminho, old[:60])
       9         s = s.replace(old, new)
      10     p.write_text(s, encoding="utf-8", newline="\n")
     … +320 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● Estou na T-033: o código já está aplicado, e falta corrigir os imports do
  test_rn011_viagem.py, onde nomes locais conflitam com os da fabrica.

● Bash(python - <<'PY'
      from pathlib import Path…)
  ⎿  All checks passed!
     39 files already formatted
     E         Use -v to get more diff
     … +7 lines (ctrl+o to expand)
  ⎿  Updated tests\test_rn011_viagem.py (+6 -7)
       3  from decimal import Decimal
       4  from pathlib import Path
       5  
       6 -from fabrica import despesa, politica_aplicavel                
       7 -from fabrica import documento as doc_                          
       6 +from fabrica import despesa, documento, politica_aplicavel     
       7  
       8  from reembolso.entrada import ler_documento
       9  from reembolso.modelo import Despesa
     ...
      61  
      62  
      63  def test_rn011_exemplo_nenhuma_despesa_acima_da_tabela_da_rn008
          ():
      65 -    documento = ler_documento(EXEMPLO.read_text(encoding="utf-8
         -"))                                                            
      66 -    resultados = calcular(documento, politica_aplicavel())     
      64 +    lido = ler_documento(EXEMPLO.read_text(encoding="utf-8"))  
      65 +    resultados = calcular(lido, politica_aplicavel())          
      66      soma: dict[tuple, Decimal] = defaultdict(Decimal)
      68 -    for despesa, resultado in zip(documento.despesas, resultado
         -s, strict=True):                                               
      69 -        assert isinstance(despesa, Despesa)                    
      70 -        soma[(despesa.data, despesa.categoria)] += resultado.va
         -lor_reembolsavel                                               
      67 +    for lida, resultado in zip(lido.despesas, resultados, stric
         +t=True):                                                       
      68 +        assert isinstance(lida, Despesa)                       
      69 +        soma[(lida.data, lida.categoria)] += resultado.valor_re
         +embolsavel                                                     
      70      politica = politica_aplicavel()
      71      for (_, categoria), total in soma.items():
      72          limite, _ = politica.regra(categoria)

● Bash(python /tmp/marcar.py T-033 && git add reembolso tests
      specs/001-motor-reembolso/tasks.md ':!reembolso/docs' && git commit -q -m
      "feat(T-033): aplica limites da…)
  ⎿  warning: in the working copy of 'reembolso/etapas.py', LF will be repl
     aced by CRLF the next time Git touches it
     warning: in the working copy of 'reembolso/justificativas.py', LF will
     … +26 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      443    - **Teste:** `tests/test_rn001_categoria.py`
      444    - **Commit:**
      445  
      446 -- [ ] **T-033** — Etapa de limites pela tabela efetiva, inclui
          -ndo                                                           
      446 +- [x] **T-033** — Etapa de limites pela tabela efetiva, inclui
          +ndo                                                           
      447    `representacao` como categoria independente, e justificativa
            de
      448    `LIMITE_DIARIO` citando a origem do limite. O acréscimo em v
           iagem do documento
      449    não é aplicado. Revisa a T-015 e a T-016.

● T-034 — etapa de conversão (etapa 3 da §8). Começo pelo caso "Campo
  desconhecido" da §7 e pelos pontos do motor que vou mexer.

  Ran 1 shell command (ctrl+o to expand)

● Write(~\AppData\Local\Temp\t034.py)
  ⎿  Wrote 282 lines to
     ..\..\..\..\..\Users\Remakker\AppData\Local\Temp\t034.py
       1 from pathlib import Path
       2 
       3 
       4 def editar(caminho, *trocas):
       5     p = Path(caminho)
       7     for old, new in trocas:
       8         assert s.count(old) == 1, (caminho, old[:70], s.count(ol
         d))
       9         s = s.replace(old, new)
      10     p.write_text(s, encoding="utf-8", newline="\n")
     … +317 lines (ctrl+o to expand)

● Bash(python /tmp/t034.py && .venv/Scripts/ruff format . -q; .venv/Scripts/ruff
      check . ; .venv/Scripts/python -m pytest -q 2>&1 | tail -6)
  ⎿  I001 [*] Import block is un-sorted or un-formatted
      --> reembolso\modelo.py:3:1
       |
     … +25 lines (ctrl+o to expand)
  ⎿  Updated reembolso\cambio.py (+13 -0)
      1  """Documento de câmbio (RN-018)."""
      2  
      3 +from bisect import bisect_right                                 
      4  from dataclasses import dataclass
      5  from datetime import date
      6  from decimal import Decimal
     ...
      16      moeda_base: str
      17      taxas: dict[str, list[tuple[date, Decimal]]]  # moeda → (da
          ta, taxa), ordenado por data
      18  
      19 +    def cotacao(self, moeda: str, data: date) -> tuple[Decimal,
         + date] | None:                                                 
      20 +        """Taxa da moeda na data ou, sem ela, na data anterior 
         +mais próxima (RN-018).                                         
      21 +                                                               
      22 +        `None` se não houver taxa dessa moeda nem na data nem a
         +ntes dela.                                                     
      23 +        """                                                    
      24 +        lista = self.taxas.get(moeda, [])                      
      25 +        indice = bisect_right([d for d, _ in lista], data)     
      26 +        if indice == 0:                                        
      27 +            return None                                        
      28 +        data_cotacao, taxa = lista[indice - 1]                 
      29 +        return taxa, data_cotacao                              
      30 +                                                               
      31  
      32  def _erro(mensagem: str) -> EntradaInvalida:
      33      return EntradaInvalida(f"documento de câmbio inválido: {men
          sagem}")
  ⎿  Updated reembolso\entrada.py (+7 -3)
       6  from datetime import date
       7  from decimal import Decimal
       8  
       9 -from reembolso.modelo import Despesa, Documento, Invalida      
       9 +from reembolso.modelo import MOEDA_BASE, Despesa, Documento, In
         +valida                                                         
      10  from reembolso.normalizacao import arredondar, normalizar_moeda
          , normalizar_texto
      11  
      12  _FORMATO_DATA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
     ...
      165      if invalida is not None:
      166          return invalida
      167      valor_informado = numero(item["valor"])
      168 +    moeda = normalizar_moeda(item.get("moeda", MOEDA_BASE))   
      169 +    # Em BRL a conversão é a identidade (RN-003); as demais mo
          +edas são convertidas na                                       
      170 +    # etapa 3, que preenche `valor_considerado` (DT-010).     
      171 +    considerado = arredondar(valor_informado) if moeda == MOED
          +A_BASE else None                                              
      172      return Despesa(
      173          posicao=posicao,
      174          id=item["id"],
     ...
      177          fornecedor=normalizar_texto(item["fornecedor"]),
      178          tem_nota_fiscal=item["tem_nota_fiscal"],
      179          valor_informado=valor_informado,
      176 -        valor_considerado=arredondar(valor_informado),        
      177 -        moeda=normalizar_moeda(item.get("moeda", "BRL")),     
      180 +        valor_considerado=considerado,                        
      181 +        moeda=moeda,                                          
      182      )
      183  
      184  
  ⎿  Updated reembolso\etapas.py (+29 -2)
       1  """Uma função por etapa da seção 8 da spec."""
       2  
       3  from collections import defaultdict
       4 -from dataclasses import dataclass                              
       4 +from dataclasses import dataclass, replace                     
       5  from decimal import Decimal
       6  
       7  from reembolso import justificativas
       8  from reembolso.cambio import Cambio
       9 -from reembolso.modelo import Corte, Despesa, Documento, Motivo,
         - Recusa                                                        
       9 +from reembolso.modelo import MOEDA_BASE, Corte, Despesa, Docume
         +nto, Motivo, Recusa                                            
      10 +from reembolso.normalizacao import arredondar                  
      11  from reembolso.politica import PoliticaAplicavel
      12  
      13  
     ...
      20      cambio: Cambio | None = None
      21  
      22  
      23 +def conversao(despesa: Despesa, contexto: Contexto) -> Despesa 
         +| Recusa:                                                      
      24 +    """RN-018, RN-003: converte para reais pela taxa da data da
         + despesa ou da anterior mais                                   
      25 +    próxima e arredonda o produto uma única vez.               
      26 +                                                               
      27 +    Em BRL a despesa passa sem consultar o câmbio. Sem taxa, ou
         + sem documento de câmbio,                                      
      28 +    é recusada com `COTACAO_INDISPONIVEL` e `valor_considerado`
         + fica nulo.                                                    
      29 +    """                                                        
      30 +    if despesa.moeda == MOEDA_BASE:                            
      31 +        return despesa                                         
      32 +    cotacao = (                                                
      33 +        None if contexto.cambio is None else contexto.cambio.co
         +tacao(despesa.moeda, despesa.data)                             
      34 +    )                                                          
      35 +    if cotacao is None:                                        
      36 +        return Recusa(                                         
      37 +            Motivo.COTACAO_INDISPONIVEL,                       
      38 +            justificativas.cotacao_indisponivel(despesa.moeda, 
         +despesa.data),                                                 
      39 +        )                                                      
      40 +    taxa, data_cotacao = cotacao                               
      41 +    return replace(                                            
      42 +        despesa,                                               
      43 +        valor_considerado=arredondar(despesa.valor_informado * 
         +taxa),                                                         
      44 +        taxa_cambio=taxa,                                      
     … 7 more lines (ctrl+o to expand)
  ⎿  Updated reembolso\justificativas.py (+5 -0)
      36      return f"Dados inválidos: {detalhe} (RN-013)."
      37  
      38  
      39 +def cotacao_indisponivel(moeda: str, data: date) -> str:       
      40 +    """Cita a moeda e a data da despesa (spec §4)."""          
      41 +    return f"Sem cotação de {moeda} em {data} nem em data anter
         +ior (RN-018)."                                                 
      42 +                                                               
      43 +                                                               
      44  def valor_negativo(valor: Decimal) -> str:
      45      return (
      46          f"Valor negativo ({reais(valor)}) não é reembolsável e 
          não abate outras despesas (RN-005)."
  ⎿  Updated reembolso\modelo.py (+5 -2)
       6  from enum import StrEnum
       7  
       8  
       9 +MOEDA_BASE = "BRL"  # moeda dos limites e de `valor_considerado
         +` (RN-015, RN-018)                                             
      10 +                                                               
      11 +                                                               
      12  class Status(StrEnum):
      13      """Status de um item da saída (spec §4)."""
      14  
     ...
      44      fornecedor: str
      45      tem_nota_fiscal: bool
      46      valor_informado: Decimal
      44 -    valor_considerado: Decimal                                 
      45 -    moeda: str = "BRL"  # normalizada (RN-017)                 
      47 +    valor_considerado: Decimal | None  # None até a etapa 3 em 
         +moeda estrangeira (DT-010)                                     
      48 +    moeda: str = MOEDA_BASE  # normalizada (RN-017)            
      49      taxa_cambio: Decimal | None = None  # como está no document
          o de câmbio; None em BRL
      50      data_cotacao: date | None = None  # data da taxa usada; Non
          e em BRL
      51  
  ⎿  … 4 more files changed

● Código da conversão aplicado e a suíte continua verde. Agora os testes da
  T-034.

● Write(~\AppData\Local\Temp\t034_testes.py)
  ⎿  Wrote 272 lines to
     ..\..\..\..\..\Users\Remakker\AppData\Local\Temp\t034_testes.py
       1 from pathlib import Path
       2 
       3 
       4 def acrescentar(caminho, texto):
       5     with open(caminho, "a", encoding="utf-8", newline="\n") as f
       6         f.write(texto)
       7 
       8 
       9 def editar(caminho, *trocas):
      10     p = Path(caminho)
     … +295 lines (ctrl+o to expand)

● Bash(python /tmp/t034_testes.py && .venv/Scripts/ruff check --fix -q . ;
      .venv/Scripts/ruff format . -q; .venv/Scripts/ruff check . &&
      .venv/Scripts/ruff format --ch…)
  ⎿  E501 Line too long (102 > 100)
       --> tests\test_rn003_arredondamento.py:52:101
        |
     … +19 lines (ctrl+o to expand)
  ⎿  Updated reembolso\modelo.py (+0 -1)
       5  from decimal import Decimal
       6  from enum import StrEnum
       7  
       8 -                                                               
       8  MOEDA_BASE = "BRL"  # moeda dos limites e de `valor_considerado
          ` (RN-015, RN-018)
       9  
      10  
  ⎿  Updated tests\test_motor.py (+24 -2)
       1  from decimal import Decimal
       2  
       3 -from fabrica import despesa, documento, invalida, politica_apli
         -cavel                                                          
       3 +from fabrica import cambio, despesa, documento, invalida, polit
         +ica_aplicavel                                                  
       4  
       5  from reembolso.etapas import Contexto
       6  from reembolso.justificativas import reais
       7  from reembolso.modelo import Corte, Motivo, Recusa, Status
       8 -from reembolso.motor import EmGrupo, PorItem, calcular         
       8 +from reembolso.motor import ETAPAS, Conversao, EmGrupo, PorItem
         +, calcular                                                     
       9  
      10  
      11  def _recusa_posicao(posicao):
     ...
      143      assert all(ctx.documento is doc for ctx in recebidos)
      144      assert all(ctx.politica is politica for ctx in recebidos)
      145      assert all(ctx.cambio is None for ctx in recebidos)
      146 +                                                              
      147 +                                                              
      148 +def test_dt010_conversao_e_a_primeira_etapa():                
      149 +    assert isinstance(ETAPAS[0], Conversao)                   
      150 +    assert not any(isinstance(etapa, Conversao) for etapa in E
          +TAPAS[1:])                                                    
      151 +                                                              
      152 +                                                              
      153 +def test_dt010_nenhuma_despesa_chega_a_etapa_4_sem_valor_consi
          +derado():                                                     
      154 +    vistas = []                                               
      155 +    calcular(                                                 
      156 +        documento(                                            
      157 +            despesa(1, data="2026-07-14", valor="22.00", moeda
          +="EUR"),                                                      
      158 +            despesa(2, data="2026-07-21", valor="55.00", moeda
          +="GBP"),                                                      
      159 +            despesa(3, data="2026-07-18", valor="47.20"),     
      160 +        ),                                                    
      161 +        politica_aplicavel(),                                 
      162 +        cambio(),                                             
      163 +        etapas=[ETAPAS[0], EmGrupo(lambda vivas, _ctx: vistas.
          +extend(vivas) or {})],                                        
      164 +    )                                                         
      165 +    assert [d.posicao for d in vistas] == [1, 3]              
      166 +    assert all(d.valor_considerado is not None for d in vistas
          +)                                                             
      167 +    assert vistas[0].valor_considerado == Decimal("130.46")   
  ⎿  Updated tests\test_rn003_arredondamento.py (+11 -0)
      1  from decimal import Decimal
      2  
      3  import pytest
      4 +from fabrica import cambio, contexto, despesa                   
      5  
      6 +from reembolso.etapas import conversao                          
      7  from reembolso.normalizacao import arredondar
      8  
      9  
     ...
      43  
      44  def test_rn003_valor_muito_grande_nao_falha():
      45      assert arredondar(Decimal("1E+40")) == Decimal("1E+40")
      46 +                                                               
      47 +                                                               
      48 +def test_rn003_arredonda_uma_vez_depois_da_conversao():        
      49 +    d = despesa(1, data="2026-07-13", valor="33.333", moeda="US
         +D")                                                            
      50 +    convertida = conversao(d, contexto(cambio=cambio()))       
      51 +    assert convertida.valor_considerado == Decimal("180.66")   
      52 +    assert convertida.valor_considerado != arredondar(         
      53 +        arredondar(Decimal("33.333")) * Decimal("5.42")        
      54 +    )                                                          
  ⎿  Updated tests\test_rn018_cambio.py (+172 -1)
       5  from pathlib import Path
       6  
       7  import pytest
       8 +from fabrica import cambio, contexto, despesa, documento, polit
         +ica_aplicavel                                                  
       9  
      10  from reembolso.cambio import ler_cambio
      10 -from reembolso.entrada import EntradaInvalida                  
      11 +from reembolso.entrada import EntradaInvalida, ler_despesa     
      12 +from reembolso.etapas import conversao                         
      13 +from reembolso.modelo import Despesa, Motivo, Recusa, Status   
      14 +from reembolso.motor import calcular                           
      15  
      16  CAMBIO = Path(__file__).parent.parent / "exemplos" / "envelope"
           / "cambio.json"
      17  
     ...
      127  
      128  def test_rn018_documento_moeda_base_comparada_apos_normalizaca
           o():
      129      assert ler_cambio(_cambio(moeda_base=" brl "), "BRL").moed
           a_base == "BRL"
      130 +                                                              
      131 +                                                              
      132 +@pytest.mark.parametrize(                                     
      133 +    ("moeda", "data", "taxa", "data_cotacao"),                
      134 +    [                                                         
      135 +        ("EUR", "2026-07-14", "5.93", "2026-07-14"),          
      136 +        ("EUR", "2026-07-18", "5.96", "2026-07-17"),          
      137 +        ("EUR", "2026-07-19", "5.96", "2026-07-17"),          
      138 +        ("USD", "2026-07-20", "5.50", "2026-07-20"),          
      139 +        ("USD", "2026-07-31", "5.51", "2026-07-28"),          
      140 +    ],                                                        
      141 +    ids=["data_exata", "sabado", "domingo", "segunda", "lacuna
          +_no_fim_do_mes"],                                             
      142 +)                                                             
      143 +def test_rn018_cotacao_usa_data_anterior_mais_proxima(moeda, d
          +ata, taxa, data_cotacao):                                     
      144 +    assert cambio().cotacao(moeda, date.fromisoformat(data)) =
          += (                                                           
      145 +        Decimal(taxa),                                        
      146 +        date.fromisoformat(data_cotacao),                     
      147 +    )                                                         
      148 +                                                              
      149 +                                                              
      150 +@pytest.mark.parametrize(                                     
      151 +    ("moeda", "data"),                                        
      152 +    [("USD", "2026-07-10"), ("GBP", "2026-07-21"), ("USD", "20
          +26-07-12")],                                                  
     … 144 more lines (ctrl+o to expand)

● Tudo verde (419), lint ok. Commit da T-034.

● Bash(python /tmp/marcar.py T-034 && git add reembolso tests
      specs/001-motor-reembolso/tasks.md ':!reembolso/docs' && git commit -q -m
      "feat(T-034): converte para rea…)
  ⎿  warning: in the working copy of 'reembolso/cambio.py', LF will be repl
     aced by CRLF the next time Git touches it
     warning: in the working copy of 'reembolso/entrada.py', LF will be rep
     … +20 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      468      `tests/test_rn010_parcial.py`, `tests/test_rn011_viagem.py
           `
      469    - **Commit:**
      470  
      471 -- [ ] **T-034** — Etapa de conversão (etapa 3 da §8, antes de 
          -valor negativo):                                              
      471 +- [x] **T-034** — Etapa de conversão (etapa 3 da §8, antes de 
          +valor negativo):                                              
      472    novo tipo de etapa `Conversao` em `motor.py`, primeiro item 
           de `ETAPAS`, que
      473    devolve a `Despesa` com `valor_considerado`, `taxa_cambio` e
            `data_cotacao`
      474    preenchidos (ela substitui a da lista viva) ou uma recusa.

● T-035 — só teste: nota fiscal comparada com o valor já convertido.

● Bash(python - <<'PY'
      from pathlib import Path…)
  ⎿  All checks passed!
     39 files already formatted
     ..........
     … +2 lines (ctrl+o to expand)
  ⎿  Updated tests\test_rn007_nota_fiscal.py (+42 -1)
      1  from decimal import Decimal
      2  
      3  import pytest
      4 -from fabrica import contexto, despesa, documento, politica_aplic
        -avel                                                            
      4 +from fabrica import cambio, contexto, despesa, documento, politi
        +ca_aplicavel                                                    
      5  
      6  from reembolso.etapas import nota_fiscal
      7  from reembolso.modelo import Motivo, Status
     ...
       75          politica_aplicavel(),
       76      )
       77      assert all(r.motivo != Motivo.NOTA_FISCAL_AUSENTE for r in
            resultados)
       78 +                                                              
       79 +                                                              
       80 +def _estrangeira(id, categoria, data, valor, moeda):          
       81 +    item = calcular(                                          
       82 +        documento(                                            
       83 +            despesa(                                          
       84 +                1,                                            
       85 +                id=id,                                        
       86 +                data=data,                                    
       87 +                categoria=categoria,                          
       88 +                valor=valor,                                  
       89 +                moeda=moeda,                                  
       90 +                tem_nota_fiscal=False,                        
       91 +            )                                                 
       92 +        ),                                                    
       93 +        politica_aplicavel("CC-COMERCIAL"),                   
       94 +        cambio(),                                             
       95 +    )[0]                                                      
       96 +    return item                                               
       97 +                                                              
       98 +                                                              
       99 +def test_rn007_compara_valor_convertido_e005_recusada():      
      100 +    item = _estrangeira("e-005", "transporte_urbano", "2026-07
          +-20", "40.00", "USD")                                         
      101 +    assert item.valor_considerado == Decimal("220.00")        
      102 +    assert item.status == Status.RECUSADO                     
      103 +    assert item.motivo == Motivo.NOTA_FISCAL_AUSENTE          
      104 +    assert item.valor_reembolsavel == Decimal("0.00")         
      105 +                                                              
      106 +                                                              
     … 12 more lines (ctrl+o to expand)

● Bash(sed -i 's/^def _estrangeira(id, categoria, data, valor, moeda):$/def
      _estrangeira(id, categoria, data, valor, moeda):/'
      tests/test_rn007_nota_fiscal.py && pytho…)
  ⎿  warning: in the working copy of 'specs/001-motor-reembolso/tasks.md',
     LF will be replaced by CRLF the next time Git touches it
     warning: in the working copy of 'tests/test_rn007_nota_fiscal.py', LF
     … +30 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      504      `tests/test_secao7_casos_de_borda.py` (linha "Campo descon
           hecido")
      505    - **Commit:**
      506  
      507 -- [ ] **T-035** — Nota fiscal comparada com o valor convertido
          - para reais                                                   
      507 +- [x] **T-035** — Nota fiscal comparada com o valor convertido
          + para reais                                                   
      508    (`test(T-035)`; a T-034 já entrega `valor_considerado` em re
           ais).
      509    - **Atende:** RN-007, AMB-028
      510    - **Aceite:** e-005 (40,00 USD × 5,50 = 220,00, sem nota) → 
           recusado,

● T-036 — chave de duplicatas com moeda e valor original arredondado.

● Bash(python - <<'PY'
      from pathlib import Path…)
  ⎿  All checks passed!
     39 files already formatted
     =========================== short test summary info ==================
     … +4 lines (ctrl+o to expand)
  ⎿  Updated reembolso\etapas.py (+10 -3)
       82  
       83  
       84  def duplicatas(vivas: list[Despesa], _contexto: Contexto) -> d
           ict[int, Recusa]:
       85 -    """RN-006: agrupa por data, categoria, fornecedor e valor 
          -considerado e mantém uma por grupo.                           
       85 +    """RN-006: agrupa por data, categoria, fornecedor, moeda e
          + valor informado arredondado na                               
       86 +    moeda original, e mantém uma por grupo (DT-013).          
       87  
       88      Fica a de menor posição entre as que têm nota fiscal; se n
           enhuma tiver, a de menor
       88 -    posição. `vivas` chega em ordem de posição.               
       89 +    posição. `vivas` chega em ordem de posição e já sem as rec
          +usadas nas etapas 3 a 6.                                      
       90      """
       91      grupos: dict[tuple, list[Despesa]] = defaultdict(list)
       92      for despesa in vivas:
       92 -        chave = (despesa.data, despesa.categoria, despesa.forn
          -ecedor, despesa.valor_considerado)                            
       93 +        chave = (                                             
       94 +            despesa.data,                                     
       95 +            despesa.categoria,                                
       96 +            despesa.fornecedor,                               
       97 +            despesa.moeda,                                    
       98 +            arredondar(despesa.valor_informado),              
       99 +        )                                                     
      100          grupos[chave].append(despesa)
      101  
      102      recusas: dict[int, Recusa] = {}
  ⎿  Updated reembolso\justificativas.py (+1 -1)
      61  
      62  def duplicata(id_mantida: str) -> str:
      63      return (
      64 -        f"Duplicata de {id_mantida} (mesma data, categoria, for
         -necedor e valor); "                                            
      64 +        f"Duplicata de {id_mantida} (mesma data, categoria, for
         +necedor, moeda e valor); "                                     
      65          f"mantida {id_mantida} (RN-006)."
      66      )
      67  
  ⎿  Updated tests\test_rn006_duplicatas.py (+41 -1)
      1  from decimal import Decimal
      2  
      3 -from fabrica import despesa, documento, invalida, politica_aplic
        -avel                                                            
      3 +from fabrica import cambio, despesa, documento, invalida, politi
        +ca_aplicavel                                                    
      4  
      5  from reembolso.modelo import Motivo, Status
      6  from reembolso.motor import calcular
     ...
      101      )
      102      assert resultados[0].motivo == Motivo.DADOS_INVALIDOS
      103      assert resultados[1].status == Status.APROVADO
      104 +                                                              
      105 +                                                              
      106 +def _taberna(posicao, id, valor="22.00", moeda="EUR"):        
      107 +    return despesa(                                           
      108 +        posicao, id=id, data="2026-07-14", fornecedor="Taberna
          + do Chiado", valor=valor, moeda=moeda                         
      109 +    )                                                         
      110 +                                                              
      111 +                                                              
      112 +def _calcular(*despesas):                                     
      113 +    return calcular(documento(*despesas), politica_aplicavel("
          +CC-COMERCIAL"), cambio())                                     
      114 +                                                              
      115 +                                                              
      116 +def test_rn006_mesma_moeda_estrangeira_e_duplicata():         
      117 +    _, segunda = _calcular(_taberna(1, "e-a"), _taberna(2, "e-
          +b"))                                                          
      118 +    assert segunda.status == Status.RECUSADO                  
      119 +    assert segunda.motivo == Motivo.DUPLICATA                 
      120 +    assert "e-a" in segunda.justificativa                     
      121 +                                                              
      122 +                                                              
      123 +def test_rn006_mesmo_valor_em_reais_e_moedas_diferentes_nao_e_
          +duplicata():                                                  
      124 +    eur, brl = _calcular(_taberna(1, "e-a"), _taberna(2, "e-b"
          +, valor="130.46", moeda="BRL"))                               
      125 +    assert eur.valor_considerado == brl.valor_considerado == D
          +ecimal("130.46")                                              
      126 +    assert brl.motivo != Motivo.DUPLICATA                     
      127 +                                                              
      128 +                                                              
      129 +def test_rn006_mesmo_valor_original_e_moedas_diferentes_nao_e_
          +duplicata():                                                  
      130 +    _, usd = _calcular(_taberna(1, "e-a"), _taberna(2, "e-b", 
          +moeda="USD"))                                                 
      131 +    assert usd.motivo != Motivo.DUPLICATA                     
      132 +                                                              
      133 +                                                              
     … 10 more lines (ctrl+o to expand)

● Bash(python /tmp/marcar.py T-036 && git add reembolso tests
      specs/001-motor-reembolso/tasks.md ':!reembolso/docs' && git commit -q -m
      "feat(T-036): duplicatas exigem…)  ⎿  warning: in the working copy of 'reembolso/etapas.py', LF will be repl
     aced by CRLF the next time Git touches it
     warning: in the working copy of 'reembolso/justificativas.py', LF will
     … +122 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      514    - **Teste:** `tests/test_rn007_nota_fiscal.py::test_rn007_co
           mpara_valor_convertido_*`
      515    - **Commit:**
      516  
      517 -- [ ] **T-036** — Duplicatas exigem a mesma moeda e o mesmo va
          -lor informado                                                 
      517 +- [x] **T-036** — Duplicatas exigem a mesma moeda e o mesmo va
          +lor informado                                                 
      518    arredondado para centavos na moeda original (em `BRL`, o pró
           prio
      519    `valor_considerado`). Despesas recusadas por `COTACAO_INDISP
           ONIVEL` não entram
      520    no grupo. Revisa a T-013.

● T-037 — saída com moeda, taxa_cambio e data_cotacao, na ordem da §4.

● Bash(python - <<'PY'
      from pathlib import Path…)
  ⎿  All checks passed!
     39 files already formatted
     =========================== short test summary info ==================
     … +4 lines (ctrl+o to expand)
  ⎿  Updated reembolso\saida.py (+6 -0)
      13  
      14  
      15  def _item(resultado: Resultado) -> dict:
      16 +    """Campos na ordem da tabela da spec §4. `valor_informado` 
         +e `taxa_cambio` saem como vieram,                              
      17 +    sem quantizar; `data_cotacao`, como texto `AAAA-MM-DD` (DT-
         +005)."""                                                       
      18 +    data_cotacao = resultado.data_cotacao                      
      19      return {
      20          "id": resultado.id,
      21          "valor_informado": resultado.valor_informado,
      22 +        "moeda": resultado.moeda,                              
      23 +        "taxa_cambio": resultado.taxa_cambio,                  
      24 +        "data_cotacao": None if data_cotacao is None else data_
         +cotacao.isoformat(),                                           
      25          "valor_considerado": _dinheiro(resultado.valor_consider
          ado),
      26          "valor_reembolsavel": _dinheiro(resultado.valor_reembol
          savel),
      27          "status": resultado.status.value,
  ⎿  Updated tests\test_saida_serializacao.py (+43 -1)
      1  import json
      2 +from datetime import date                                       
      3  from decimal import Decimal
      4  
      4 -from fabrica import despesa, documento, invalida, politica_aplic
        -avel                                                            
      5 +from fabrica import cambio, despesa, documento, invalida, politi
        +ca_aplicavel                                                    
      6  
      7  from reembolso.modelo import Motivo, Resultado, Status
      8  from reembolso.motor import calcular
     ...
      59      assert item["id"] is None
      60      assert item["valor_informado"] is None
      61      assert item["valor_considerado"] is None
      62 +    assert item["moeda"] is None                               
      63 +    assert item["taxa_cambio"] is None                         
      64 +    assert item["data_cotacao"] is None                        
      65      assert item["valor_reembolsavel"] == 0
      66      assert item["motivo"] == Motivo.DADOS_INVALIDOS.value
      67  
     ...
      110      assert list(item) == [
      111          "id",
      112          "valor_informado",
      113 +        "moeda",                                              
      114 +        "taxa_cambio",                                        
      115 +        "data_cotacao",                                       
      116          "valor_considerado",
      117          "valor_reembolsavel",
      118          "status",
     ...
      125      texto = _texto(_resultado(), _resultado(id="d-002"))
      126      assert json.loads(texto)["itens"][1]["id"] == "d-002"
      127      assert texto.startswith('{\n  "colaborador": {\n    "id": 
           "c-0417"')
      128 +                                                              
      129 +                                                              
      130 +def test_dt005_moeda_e_cotacao_em_brl():                      
      131 +    resultados = calcular(documento(despesa(1, valor="47.20"))
          +, politica_aplicavel())                                       
      132 +    texto = _texto(*resultados)                               
      133 +    item = json.loads(texto)["itens"][0]                      
      134 +    assert item["moeda"] == "BRL"                             
      135 +    assert item["taxa_cambio"] is None                        
      136 +    assert item["data_cotacao"] is None                       
      137 +                                                              
     … 25 more lines (ctrl+o to expand)

● Bash(python /tmp/marcar.py T-037 && git add reembolso tests
      specs/001-motor-reembolso/tasks.md ':!reembolso/docs' && git commit -q -m
      "feat(T-037): emite moeda, taxa…)
  ⎿  warning: in the working copy of 'reembolso/saida.py', LF will be repla
     ced by CRLF the next time Git touches it
     warning: in the working copy of 'specs/001-motor-reembolso/tasks.md',
     … +93 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      527    - **Teste:** `tests/test_rn006_duplicatas.py`
      528    - **Commit:**
      529  
      530 -- [ ] **T-037** — Saída com os campos novos, na ordem da §4: `
          -moeda`,                                                       
      530 +- [x] **T-037** — Saída com os campos novos, na ordem da §4: `
          +moeda`,                                                       
      531    `taxa_cambio` (como está no documento, sem quantizar) e `dat
           a_cotacao`
      532    (`AAAA-MM-DD`); `valor_considerado` nulo também em `COTACAO_
           INDISPONIVEL`;
      533    `moeda` nula em `DADOS_INVALIDOS`. Revisa a T-018.

● Vou revisar as linhas da §7 reescritas pela spec 2.0 antes de implementar o
  fluxo completo da T-038: --cambio, política por centro de custo, atualização
  dos testes afetados da v3, e ajustes no README e CLAUDE.md.

  Ran 1 shell command (ctrl+o to expand)

● Write(~\AppData\Local\Temp\t038.py)
  ⎿  Wrote 377 lines to
     ..\..\..\..\..\Users\Remakker\AppData\Local\Temp\t038.py
       1 from pathlib import Path
       2 
       3 
       4 def editar(caminho, *trocas):
       5     p = Path(caminho)
       7     for old, new in trocas:
       8         assert s.count(old) == 1, (caminho, old[:70], s.count(ol
         d))
       9         s = s.replace(old, new)
      10     p.write_text(s, encoding="utf-8", newline="\n")
     … +448 lines (ctrl+o to expand)

● Bash(python /tmp/t038.py && .venv/Scripts/ruff check --fix -q . ;
      .venv/Scripts/ruff format . -q; .venv/Scripts/ruff check . &&
      .venv/Scripts/ruff format --check . &…)
  ⎿  All checks passed!
     39 files already formatted
     E         'RN-016'
     … +9 lines (ctrl+o to expand)
  ⎿  Updated CLAUDE.md (+1 -1)
      36  
      37  - Linguagem: Python 3.12+ (sem dependências de runtime; pytest 
          e ruff como dev)
      38  - Instalar: `python -m venv .venv` e `.venv/Scripts/python -m p
          ip install -e ".[dev]"`
      39 -- Rodar: `python -m reembolso calcular --input despesas.json --
         -output resultado.json`                                         
      39 +- Rodar: `python -m reembolso calcular --input despesas.json --
         +politica politica.json [--cambio cambio.json] --output resultad
         +o.json`                                                        
      40  - Testes: `python -m pytest`
      41  - Lint/format: `ruff check .` · `ruff format .`
      42  
  ⎿  Updated README.md (+19 -5)
      33  ## Como rodar
      34  
      35  ```bash
      36 -python -m reembolso calcular --input exemplos/despesas-exemplo.
         -json --output resultado.json                                   
      36 +python -m reembolso calcular --input exemplos/despesas-exemplo.
         +json \                                                         
      37 +  --politica exemplos/envelope/politica-v4.json --output result
         +ado.json                                                       
      38 +                                                               
      39 +python -m reembolso calcular --input exemplos/envelope/despesas
         +-envelope.json \                                               
      40 +  --politica exemplos/envelope/politica-v4.json --cambio exempl
         +os/envelope/cambio.json \                                      
      41 +  --output resultado.json                                      
      42  ```
      43  
      44  - `--input`: documento de despesas no formato de
      40 -  [`exemplos/despesas-exemplo.json`](exemplos/despesas-exemplo.
         -json) (spec §4).                                               
      41 -- `--output`: arquivo de resultado, em UTF-8. Para o exemplo, o
      42 -  `total_reembolsavel` é `585.43`.                             
      45 +  [`exemplos/despesas-exemplo.json`](exemplos/despesas-exemplo.
         +json) ou                                                       
      46 +  [`exemplos/envelope/despesas-envelope.json`](exemplos/envelop
         +e/despesas-envelope.json)                                      
      47 +  (spec §4).                                                   
      48 +- `--politica`: documento de política, obrigatório, no formato 
         +de                                                             
      49 +  [`exemplos/envelope/politica-v4.json`](exemplos/envelope/poli
         +tica-v4.json) (RN-015). A                                      
      50 +  tabela aplicada é escolhida pelo `colaborador.centro_custo` (
         +RN-016).                                                       
      51 +- `--cambio`: documento de câmbio no formato de                
      52 +  [`exemplos/envelope/cambio.json`](exemplos/envelope/cambio.js
         +on); só é necessário com                                       
      53 +  despesa em moeda estrangeira (RN-018). Sem ele, essas despesa
         +s saem recusadas com                                           
      54 +  `COTACAO_INDISPONIVEL`.                                      
      55 +- `--output`: arquivo de resultado, em UTF-8. Para o primeiro c
         +omando, o                                                      
      56 +  `total_reembolsavel` é `351.43`.                             
      57  
      58  Códigos de saída:
      59  
      60  | Código | Situação |
      61  |---|---|
      62  | 0 | Sucesso; o arquivo de saída foi gravado |
      49 -| 1 | Erro geral da RN-013 (documento ilegível, sem período vál
         -ido etc.); mensagem em stderr, e o arquivo de saída não é criad
         -o nem sobrescrito |                                            
      63 +| 1 | Erro geral (RN-013, RN-015, RN-018): documento de despesa
         +s, de política ou de câmbio ilegível ou inválido, política não 
         +informada etc.; mensagem em stderr, e o arquivo de saída não é 
         +criado nem sobrescrito |                                       
      64  | 2 | Argumentos de linha de comando inválidos |
      65  
      66  Uma despesa com dados inválidos não interrompe a execução: ela 
          sai recusada
  ⎿  Updated reembolso\cli.py (+17 -6)
       4  import sys
       5  from pathlib import Path
       6  
       7 +from reembolso.cambio import ler_cambio                        
       8  from reembolso.entrada import EntradaInvalida, ler_documento
       9  from reembolso.motor import calcular
      10  from reembolso.politica import ler_politica, politica_aplicavel
     ...
      23      calcular_.add_argument("--input", required=True, type=Path,
           help="JSON de despesas")
      24      # Não é obrigatório no argparse: a falta da política é erro
           geral, código 1 (DT-006).
      25      calcular_.add_argument("--politica", type=Path, help="JSON 
          da política de reembolso")
      26 +    calcular_.add_argument(                                    
      27 +        "--cambio", type=Path, help="JSON de câmbio; só necessá
         +rio com moeda estrangeira"                                     
      28 +    )                                                          
      29      calcular_.add_argument("--output", required=True, type=Path
          , help="JSON de resultado")
      30      return parser
      31  
     ...
      37          raise EntradaInvalida(f"não foi possível ler {caminho}:
           {erro}") from erro
      38  
      39  
      36 -def _calcular(entrada: Path, politica: Path | None) -> str:    
      40 +def _calcular(entrada: Path, politica: Path | None, cambio: Pat
         +h | None) -> str:                                              
      41 +    """Lê e valida despesas, política e câmbio, nessa ordem (DT
         +-006), e calcula.                                              
      42 +                                                               
      43 +    O câmbio vem por último porque compara a `moeda_base` com a
         + da política. Sem câmbio,                                      
      44 +    as despesas em moeda estrangeira são recusadas com `COTACAO
         +_INDISPONIVEL` (RN-018).                                       
      45 +    """                                                        
      46      documento = ler_documento(_ler(entrada))
      47      if politica is None:
      48          raise EntradaInvalida("documento de política não inform
          ado (--politica)")
      40 -    # Até a T-038, o fluxo real usa a política padrão, sem esco
         -lher por centro de custo.                                      
      41 -    aplicavel = politica_aplicavel(ler_politica(_ler(politica))
         -, None)                                                        
      42 -    return serializar(montar_saida(documento, calcular(document
         -o, aplicavel)))                                                
      49 +    lida = ler_politica(_ler(politica))                        
      50 +    taxas = None if cambio is None else ler_cambio(_ler(cambio)
         +, lida.moeda_base)                                             
      51 +    aplicavel = politica_aplicavel(lida, documento.centro_custo
         +)                                                              
      52 +    return serializar(montar_saida(documento, calcular(document
         +o, aplicavel, taxas)))                                         
      53  
      54  
      55  def main(argv: list[str] | None = None) -> int:
      46 -    """Sucesso: 0. Erro geral (RN-013, RN-015): mensagem em std
         -err, 1, sem saída (DT-006).                                    
     … 12 more lines (ctrl+o to expand)
  ⎿  Updated tests\test_cli.py (+113 -1)
       8  RAIZ = Path(__file__).parent.parent
       9  EXEMPLO = RAIZ / "exemplos" / "despesas-exemplo.json"
      10  POLITICA = RAIZ / "exemplos" / "envelope" / "politica-v4.json"
      11 +CAMBIO = RAIZ / "exemplos" / "envelope" / "cambio.json"        
      12  
      13  CONTEUDO_ANTERIOR = '{"conteudo": "anterior"}\n'
      14  
     ...
      39      assert processo.returncode == 0, processo.stderr
      40      resultado = json.loads(saida.read_text(encoding="utf-8"), p
          arse_float=Decimal)
      41      assert len(resultado["itens"]) == 14
      41 -    assert resultado["total_reembolsavel"] == Decimal("585.43")
      42 +    assert resultado["total_reembolsavel"] == Decimal("351.43")
      43  
      44  
      45  def test_dt006_erro_geral_nao_sobrescreve_saida(tmp_path):
     ...
       97  
       98  
       99  def test_dt006_argumentos_invalidos_retornam_2(tmp_path):
      100 +    saida = tmp_path / "resultado.json"                       
      101      assert _rodar("calcular", "--input", EXEMPLO).returncode =
           = 2
      102 +    assert _rodar("calcular", "--politica", POLITICA, "--outpu
          +t", saida).returncode == 2                                    
      103 +    desconhecido = _rodar(                                    
      104 +        "calcular", "--input", EXEMPLO, "--politica", POLITICA
          +, "--output", saida, "--extra", "x"                           
      105 +    )                                                         
      106 +    assert desconhecido.returncode == 2                       
      107      assert _rodar().returncode == 2
      108      assert _rodar("outro").returncode == 2
      109 +    assert not saida.exists()                                 
      110  
      111  
      112  def test_rn015_sem_politica_retorna_1_e_nao_cria_saida(tmp_pat
           h):
     ...
      153      assert processo.returncode == 1
      154      assert "política" in processo.stderr
      155      assert saida.read_text(encoding="utf-8") == CONTEUDO_ANTER
           IOR
      156 +                                                              
      157 +                                                              
      158 +def _exemplo_com(tmp_path, **colaborador):                    
      159 +    dados = json.loads(EXEMPLO.read_text(encoding="utf-8"))   
      160 +    for campo, valor in colaborador.items():                  
      161 +        if valor is None:                                     
     … 98 more lines (ctrl+o to expand)
  ⎿  Updated tests\test_secao7_casos_de_borda.py (+17 -6)
      74  TRANSP_0706 = {"data": "2026-07-06", "categoria": "transporte_u
          rbano", "fornecedor": "TaxiApp"}
      75  BISTRO = {"data": "2026-07-09", "fornecedor": "Bistro Central",
           "valor": Decimal("54.90")}
      76  HOSP_0714 = {"data": "2026-07-14", "categoria": "hospedagem"}
      77 +ENG = {"centro_custo": "CC-ENG-PLATAFORMA"}                    
      78 +COMERCIAL = {"centro_custo": "CC-COMERCIAL"}                   
      79  
      80  CASOS = [
      81      pytest.param(
      82          doc(
      83              d("d-001", **ALIM_0703, valor=Decimal("72.50")),
      84              d("d-002", **ALIM_0703, valor=Decimal("38.00")),
      85 +            colaborador=ENG,                                   
      86          ),
      84 -        [limitado("60.00"), limitado("0.00")],                 
      87 +        [aprovado("72.50"), limitado("2.50")],                 
      88          id="Duas despesas no mesmo dia somam acima do limite",
      89      ),
      90      pytest.param(
     ...
      169          id="Arredondamento na metade",
      170      ),
      171      pytest.param(
      169 -        doc(d("d-010", **HOSP_0714, descricao="Hotel Rio - 2 d
          -iarias", valor=Decimal("480.00"))),                           
      170 -        [limitado("250.00")],                                 
      172 +        doc(                                                  
      173 +            d("e-007", **HOSP_0714, descricao="Hotel Londres -
          + 3 noites", valor=Decimal("1200.00")),                        
      174 +            colaborador=COMERCIAL,                            
      175 +        ),                                                    
      176 +        [limitado("400.00")],                                 
      177          id="Hospedagem com várias diárias na descrição",
      178      ),
      179      pytest.param(
     ...
      190          id="Hospedagem sem nota acima de 100",
      191      ),
      192      pytest.param(
      187 -        doc(d("d-014", data="2026-07-31", categoria="ALIMENTAC
          -AO", valor=Decimal("61.00"))),                                
      188 -        [limitado("60.00")],                                  
      193 +        doc(                                                  
      194 +            d("d-014", data="2026-07-31", categoria="ALIMENTAC
          +AO", valor=Decimal("61.00")),                                 
      195 +            colaborador=ENG,                                  
      196 +        ),                                                    
     … 14 more lines (ctrl+o to expand)
  ⎿  … 1 more file changed

● Testes verdes. Vou ajustar a tabela de documentos e o README (incluindo
  cambio.py e removendo as constantes antigas de politica.py), e rodar a CLI
  real nos três exemplos para conferir os totais.

● Bash(python - <<'PY'
      from pathlib import Path…)
  ⎿  rc=0
     Traceback (most recent call last):
       File "<string>", line 2, in <module>
     … +15 lines (ctrl+o to expand)
  ⎿  Updated README.md (+5 -4)
       9  
      10  | Documento | Conteúdo |
      11  |---|---|
      12 -| [`specs/001-motor-reembolso/spec.md`](specs/001-motor-reembol
         -so/spec.md) | O quê: regras de negócio (RN-001 a RN-014), ambig
         -uidades, casos de borda, aceite |                              
      12 +| [`specs/001-motor-reembolso/spec.md`](specs/001-motor-reembol
         +so/spec.md) | O quê: regras de negócio (RN-001 a RN-018), ambig
         +uidades, casos de borda, aceite |                              
      13  | [`specs/001-motor-reembolso/plan.md`](specs/001-motor-reembol
          so/plan.md) | O como: stack, arquitetura, decisões técnicas |
      14 -| [`specs/001-motor-reembolso/tasks.md`](specs/001-motor-reembo
         -lso/tasks.md) | Em que ordem: tasks T-001 a T-025, cada uma com
         - o seu commit |                                                
      14 +| [`specs/001-motor-reembolso/tasks.md`](specs/001-motor-reembo
         +lso/tasks.md) | Em que ordem: tasks T-001 a T-041, cada uma com
         + o seu commit |                                                
      15  | [`specs/001-motor-reembolso/DECISIONS.md`](specs/001-motor-re
          embolso/DECISIONS.md) | Log de mudanças da spec |
      16  
      17  ## Requisitos
     ...
      91  reembolso/
      92    cli.py             argumentos, leitura e escrita de arquivo, 
          códigos de saída
      93    entrada.py         JSON → Documento; validação da RN-013 (eta
          pas 1 e 2)
      94 -  normalizacao.py    normalização de texto (RN-002) e arredonda
         -mento (RN-003)                                                 
      95 -  politica.py        categorias, limites e limiar da nota fisca
         -l, como dados                                                  
      94 +  normalizacao.py    normalização de texto (RN-002), moeda (RN-
         +017) e arredondamento (RN-003)                                 
      95 +  politica.py        documento de política (RN-015) e política 
         +aplicável (RN-016)                                             
      96 +  cambio.py          documento de câmbio e busca da cotação (RN
         +-018)                                                          
      97    etapas.py          uma função por etapa da seção 8 da spec
      98    motor.py           ordem das etapas (ETAPAS) e execução
      99    justificativas.py  textos das justificativas

  Ran 1 shell command (ctrl+o to expand)

● A CLI real bate exatamente com as três tabelas da §9 (351,43 · 1.143,26 ·
  373,76). Commito a T-038.

● Bash(.venv/Scripts/python -m pytest -q 2>&1 | tail -2; python /tmp/marcar.py
      T-038 && git add reembolso tests README.md CLAUDE.md
      specs/001-motor-reembolso/tasks.md…)
  ⎿  FAILED tests/test_rastreabilidade.py::test_rastreabilidade_spec_tem_rn
     001_a_rn014
     1 failed, 436 passed in 3.54s
     … +13 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      544  
      545  ### 7.3 — Integração, aceite e rastreabilidade
      546  
      547 -- [ ] **T-038** — Fluxo real completo: a CLI ganha `--cambio` 
          -(opcional) e passa                                            
      547 +- [x] **T-038** — Fluxo real completo: a CLI ganha `--cambio` 
          +(opcional) e passa                                            
      548    a escolher a política pelo `colaborador.centro_custo` (T-028
           ). Ordem de
      549    leitura: despesas, política, câmbio (o câmbio compara `moeda
           _base` com a
      550    política). Sem `--cambio`, o motor recebe `cambio=None`. No 
           mesmo

● T-039 — completar a tabela da §7 até os 71 casos, com os nomes da spec. Leio o
  arquivo de testes inteiro para adaptar o harness (política e câmbio
  variáveis).

  Ran 1 shell command (ctrl+o to expand)

● Vou ajustar o harness para chamar cli.main usando arquivos temporários,
  cobrindo os 34 novos casos com política e câmbio variáveis, incluindo
  "política ausente" e "câmbio inválido" pelo fluxo real.

● Write(~\AppData\Local\Temp\t039.py)
  ⎿  Wrote 474 lines to
     ..\..\..\..\..\Users\Remakker\AppData\Local\Temp\t039.py
       1 from pathlib import Path
       2 
       3 p = Path("tests/test_secao7_casos_de_borda.py")
       4 s = p.read_text(encoding="utf-8")
       5 
       6 
       7 def trocar(old, new):
       8     global s
       9     assert s.count(old) == 1, (old[:70], s.count(old))
      10     s = s.replace(old, new)
     … +515 lines (ctrl+o to expand)

● Corrijo no script uma linha que ficou torta (o if False no caso de câmbio
  inválido) e tiro o capsys sem uso.

  Ran 1 shell command (ctrl+o to expand)

● Sobrou uma linha longa (string literal); quebro em duas partes.

● Bash(python - <<'PY'
      from pathlib import Path…)
  ⎿  All checks passed!
     39 files already formatted
     ......................................................................
     … +2 lines (ctrl+o to expand)
  ⎿  Updated tests\test_secao7_casos_de_borda.py (+3 -1)
      394          [
      395              limitado(
      396                  "250.00",
      397 -                justificativa_cita="centro de custo CC-ADM usa
          -ndo limite herdado da política padrão",                       
      397 +                justificativa_cita=(                          
      398 +                    "centro de custo CC-ADM usando limite herd
          +ado da política padrão"                                       
      399 +                ),                                            
      400              )
      401          ],
      402          id="Categoria ausente na tabela do centro",

● Os 71 passaram de primeira. Confiro se os nomes batem exatamente com a spec e
  faço uma mutação rápida para garantir que o harness detecta erro de verdade.

  Ran 1 shell command (ctrl+o to expand)

● As diferenças são só de encoding do console (cp1252). Repito com UTF-8 para
  confirmar; a mutação falhou nos dois casos alterados, como deveria.

  Ran 1 shell command (ctrl+o to expand)

● Bash(python /tmp/marcar.py T-039 && git add
      tests/test_secao7_casos_de_borda.py specs/001-motor-reembolso/tasks.md &&
      git commit -q -m "test(T-039): cobre os 71 caso…)
  ⎿  warning: in the working copy of 'specs/001-motor-reembolso/tasks.md',
     LF will be replaced by CRLF the next time Git touches it
     warning: in the working copy of 'tests/test_secao7_casos_de_borda.py',
     … +3 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      578      argumento desconhecido)
      579    - **Commit:**
      580  
      581 -- [ ] **T-039** — Casos novos da §7 da spec 2.1 na tabela para
          -metrizada, com o                                              
      581 +- [x] **T-039** — Casos novos da §7 da spec 2.1 na tabela para
          +metrizada, com o                                              
      582    nome do caso como `id` (`test(T-039)`).
      583    - **Atende:** spec §7 (casos de RN-001, RN-006, RN-007, RN-0
           13, RN-015 a
      584      RN-018 e seção 8 incluídos nas specs 2.0 e 2.1), AMB-037, 
           AMB-038, AMB-039,

● T-040 — aceite dos dois documentos do envelope pela CLI.

● Write(tests\test_secao9_aceite_envelope.py)
  ⎿  Wrote 161 lines to tests\test_secao9_aceite_envelope.py
      1 """Aceite da seção 9 da spec para os dois documentos do envelope,
         pela CLI."""
      2 
      3 import json
      4 import os
      5 import re
      6 import subprocess
      7 import sys
      8 from decimal import Decimal
      9 from pathlib import Path
     … +185 lines (ctrl+o to expand)

  Ran 1 shell command (ctrl+o to expand)

● Bug do teste: json.dumps(default=str) grava Decimal como texto. Uso o
  serializar do projeto, que escreve Decimal como número.
● Bash(python - <<'PY'
      from pathlib import Path…)
  ⎿  All checks passed!
     40 files already formatted
     =========================== short test summary info ==================
     … +4 lines (ctrl+o to expand)
  ⎿  Updated tests\test_secao9_aceite_envelope.py (+3 -1)
      10  
      11  import pytest
      12  
      13 +from reembolso.saida import serializar                         
      14 +                                                               
      15  RAIZ = Path(__file__).parent.parent
      16  ENVELOPE = RAIZ / "exemplos" / "envelope"
      17  POLITICA = ENVELOPE / "politica-v4.json"
     ...
      155      for posicao, despesa in enumerate(dados["despesas"]):
      156          despesa["descricao"] = f"Viagem a Londres, 3 noites, h
           otel {posicao}"
      157      trocada = tmp_path / "trocada.json"
      156 -    trocada.write_text(json.dumps(dados, default=str), encodin
          -g="utf-8")                                                    
      158 +    trocada.write_text(serializar(dados), encoding="utf-8")   
      159  
      160      def decisoes(saida):
      161          return [(i["valor_reembolsavel"], i["status"], i["moti
           vo"]) for i in saida["itens"]]

● Bash(python /tmp/marcar.py T-040 && git add
      tests/test_secao9_aceite_envelope.py specs/001-motor-reembolso/tasks.md &&
      git commit -q -m "test(T-040): cobre o aceite…)
  ⎿  warning: in the working copy of 'specs/001-motor-reembolso/tasks.md',
     LF will be replaced by CRLF the next time Git touches it
     warning: in the working copy of 'tests/test_secao9_aceite_envelope.py'
     … +3 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      593      `::test_secao7_tem_71_casos`
      594    - **Commit:**
      595  
      596 -- [ ] **T-040** — Aceite dos dois documentos do envelope pela 
          -CLI, com                                                      
      596 +- [x] **T-040** — Aceite dos dois documentos do envelope pela 
          +CLI, com                                                      
      597    `politica-v4.json` e `cambio.json` (`test(T-040)`).
      598    - **Atende:** spec §9 (envelope), spec §4 (Exemplo 2), RN-01
           4, RN-016,
      599      AMB-019, AMB-038

● T-041 — rastreabilidade (RN-001 a RN-018) e tabela de Cobertura do tasks.md.

● Write(~\AppData\Local\Temp\t041.py)
  ⎿  Wrote 117 lines to
     ..\..\..\..\..\Users\Remakker\AppData\Local\Temp\t041.py
       1 from pathlib import Path
       2 
       3 
       4 def editar(caminho, *trocas):
       5     p = Path(caminho)
       7     for old, new in trocas:
       8         assert s.count(old) == 1, (caminho, old[:70], s.count(ol
         d))
       9         s = s.replace(old, new)
      10     p.write_text(s, encoding="utf-8", newline="\n")
     … +145 lines (ctrl+o to expand)

● Bash(python /tmp/t041.py && .venv/Scripts/python - <<'PY'
      import re…)
  ⎿  faltando na cobertura: [] | extras: []
     arquivos citados inexistentes: []
     All checks passed!
     … +10 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+50 -23)
      632  
      633  | Regra da spec | Task | Teste |
      634  |---|---|---|
      635 -| RN-001 | T-012 | `test_rn001_categoria.py` |                
      636 -| RN-002 | T-003, T-008 | `test_rn002_normalizacao.py` |      
      637 -| RN-003 | T-004, T-008, T-018 | `test_rn003_arredondamento.py
          -`, `test_saida_serializacao.py` |                             
      635 +| RN-001 | T-012, T-032 | `test_rn001_categoria.py` |         
      636 +| RN-002 | T-003, T-008, T-027, T-028 | `test_rn002_normalizac
          +ao.py`, `test_rn015_politica.py`, `test_rn016_politica_aplicav
          +el.py` |                                                      
      637 +| RN-003 | T-004, T-008, T-018, T-034, T-037 | `test_rn003_arr
          +edondamento.py`, `test_saida_serializacao.py` |               
      638  | RN-004 | T-011 | `test_rn004_periodo.py` |
      639 -| RN-005 | T-010 | `test_rn005_valor_negativo.py` |           
      640 -| RN-006 | T-013 | `test_rn006_duplicatas.py` |               
      641 -| RN-007 | T-014 | `test_rn007_nota_fiscal.py` |              
      642 -| RN-008 | T-015 | `test_rn008_limites.py` |                  
      643 -| RN-009 | T-015, T-016 | `test_rn009_distribuicao.py` |      
      644 -| RN-010 | T-015 | `test_rn010_parcial.py` |                  
      645 -| RN-011 | T-017 | `test_rn011_viagem.py` |                   
      646 -| RN-012 | T-017 | `test_rn012_calendario.py` |               
      647 -| RN-013 | T-005, T-006, T-007, T-019 | `test_rn013_dados_inva
          -lidos.py`, `test_cli.py` |                                    
      648 -| RN-014 | T-023 | `test_rn014_descricao.py` |                
      639 +| RN-005 | T-010, T-034 | `test_rn005_valor_negativo.py`, `tes
          +t_rn018_cambio.py` |                                          
      640 +| RN-006 | T-013, T-036 | `test_rn006_duplicatas.py` |        
      641 +| RN-007 | T-014, T-031, T-035 | `test_rn007_nota_fiscal.py` |
      642 +| RN-008 | T-015, T-031, T-033 | `test_rn008_limites.py` |    
      643 +| RN-009 | T-015, T-016, T-033 | `test_rn009_distribuicao.py` 
          +|                                                             
      644 +| RN-010 | T-015, T-033 | `test_rn010_parcial.py` |           
      645 +| RN-011 | T-017, T-033 | `test_rn011_viagem.py` |            
      646 +| RN-012 | T-017, T-034 | `test_rn012_calendario.py`, `test_rn
          +018_cambio.py` |                                              
      647 +| RN-013 | T-005, T-006, T-007, T-019, T-028, T-030, T-031, T-
          +038 | `test_rn013_dados_invalidos.py`, `test_rn017_moeda.py`, 
          +`test_cli.py` |                                               
      648 +| RN-014 | T-023, T-040 | `test_rn014_descricao.py`, `test_sec
          +ao9_aceite_envelope.py` |                                     
      649 +| RN-015 | T-027, T-031 | `test_rn015_politica.py`, `test_cli.
          +py` |                                                         
      650 +| RN-016 | T-028, T-032, T-033, T-038, T-040 | `test_rn016_pol
          +itica_aplicavel.py`, `test_rn001_categoria.py`, `test_rn008_li
          +mites.py`, `test_cli.py`, `test_secao9_aceite_envelope.py` |  
      651 +| RN-017 | T-030 | `test_rn017_moeda.py` |                    
      652 +| RN-018 | T-029, T-034, T-038 | `test_rn018_cambio.py`, `test
          +_cli.py` |                                                    
      653  | AMB-001 | T-015 | `test_rn008_limites.py` |
      654  | AMB-002 | T-015 | `test_rn009_distribuicao.py` |
      655  | AMB-003 | T-015 | `test_rn010_parcial.py` |
      656  | AMB-004 | T-014 | `test_rn007_nota_fiscal.py` |
      653 -| AMB-005 | T-014 | `test_rn007_nota_fiscal.py` |             
      654 -| AMB-006 | T-017, T-023 | `test_rn011_viagem.py`, `test_rn014
          -_descricao.py` |                                              
     … 48 more lines (ctrl+o to expand)
  ⎿  Updated tests\test_rastreabilidade.py (+4 -4)
      24      return [p.name for p in TESTES.glob("test_rn*.py")]
      25  
      26  
      27 -def test_rastreabilidade_spec_tem_rn001_a_rn014():             
      28 -    assert rns_da_spec(SPEC.read_text(encoding="utf-8")) == {f"
         -RN-{n:03d}" for n in range(1, 15)}                             
      27 +def test_rastreabilidade_spec_tem_rn001_a_rn018():             
      28 +    assert rns_da_spec(SPEC.read_text(encoding="utf-8")) == {f"
         +RN-{n:03d}" for n in range(1, 19)}                             
      29  
      30  
      31  def test_rastreabilidade_toda_rn_tem_arquivo_de_teste():
     ...
      35  
      36  def test_rastreabilidade_remover_um_arquivo_faz_falhar():
      37      rns = rns_da_spec(SPEC.read_text(encoding="utf-8"))
      38 -    arquivos = [a for a in _arquivos_de_teste() if not a.starts
         -with("test_rn007_")]                                           
      39 -    assert rns_sem_teste(rns, arquivos) == {"RN-007"}          
      38 +    arquivos = [a for a in _arquivos_de_teste() if a != "test_r
         +n018_cambio.py"]                                               
      39 +    assert rns_sem_teste(rns, arquivos) == {"RN-018"}          

● Suíte 100% verde (487). Removendo o test_rn018_cambio.py, a rastreabilidade
  falha como deveria, e a Cobertura tem todas as RN e AMB da spec. Commit da
  T-041.

● Bash(python /tmp/marcar.py T-041 && git add tests/test_rastreabilidade.py
      specs/001-motor-reembolso/tasks.md && git commit -q -m "test(T-041): exige
      teste de RN-001…)
  ⎿  warning: in the working copy of 'specs/001-motor-reembolso/tasks.md',
     LF will be replaced by CRLF the next time Git touches it
     warning: in the working copy of 'tests/test_rastreabilidade.py', LF wi
     … +26 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+1 -1)
      611    - **Teste:** `tests/test_secao9_aceite_envelope.py`
      612    - **Commit:**
      613  
      614 -- [ ] **T-041** — Rastreabilidade: o teste exige `test_rnNNN_*
          -.py` de RN-001 a                                              
      614 +- [x] **T-041** — Rastreabilidade: o teste exige `test_rnNNN_*
          +.py` de RN-001 a                                              
      615    RN-018; a tabela de Cobertura deste arquivo ganha RN-015 a R
           N-018, AMB-018 a
      616    AMB-036 e as tasks da Fase 7 nas linhas revistas. Fica por ú
           ltimo porque só
      617    passa quando RN-015 a RN-018 têm teste.

● Concluí a Fase 7 inteira: as 16 tasks (T-026 a T-041) estão marcadas [x], cada
  uma no seu commit. Não houve push nem export.

  Estado final: python -m pytest passa com 487 testes, ruff check . e ruff 
  format --check . passam sem erro. Rodei a CLI de verdade nos três exemplos e
  os totais batem com a §9: 351,43 (exemplo original), 1.143,26 (envelope) e
  373,76 (centro de custo desconhecido).

  O que você precisa saber:

  1. Commitei os seus documentos pendentes antes de começar. A spec 2.1, o plan
     2.0, a Fase 7 do tasks.md, a D-003 e exemplos/envelope/ ainda não estavam
     commitados. Sem isso, o primeiro [x] levaria todo esse diff para dentro do
     commit da T-026. Fiz quatro commits docs(spec|plan|tasks) antes dela. Se
     preferir outra divisão, dá para refazer, já que nada foi enviado.
  2. Decisão de leitura literal (T-028): "centro_custo": null virou erro geral.
     A spec diz "presente e não é texto → erro geral", e null está presente e
     não é texto. Um teste antigo tratava esse caso como campo informativo, e eu
     o mudei. Se a intenção era tratar null como ausente, isso é decisão de
     negócio e precisa entrar na spec.
  3. Divisão entre T-031 e T-032. A T-031 manda remover as constantes, mas a
     etapa de categoria dependia delas. Por isso, na T-031 a etapa de categoria
     passou a consultar a política, com efeito idêntico na política padrão. O
     limite zero e a origem na justificativa ficaram para a T-032.
  4. Textos intermediários de justificativa. Na T-033, a justificativa de limite
     passou a citar a origem. Até a T-038, os testes de texto exato da v3
     conferiram a versão com "(política padrão)". A T-038 trocou esses testes
     pelos textos exatos dos Exemplos 1 e 2 da §4.
  5. Mudanças além do texto literal das tasks:
     - A T-038 pedia só o comando no README; aproveitei e atualizei também as
       faixas de RN e de tasks e a lista de módulos (cambio.py), que estavam
       desatualizadas.
     - Na T-039, o harness da §7 passou a rodar pelo cli.main com arquivos
       temporários. Assim os casos de política ausente e câmbio inválido testam
       o fluxo real.
     - O texto da justificativa de COTACAO_INDISPONIVEL é meu: "Sem cotação de
       GBP em 2026-07-21 nem em data anterior (RN-018)". A spec só exige que ela
       cite a moeda e a data.

  Pendências que deixei de propósito:
  - O campo Commit: de cada task no tasks.md está vazio. Antes, os hashes eram
    registrados num commit docs(tasks) separado; faço esse commit se quiser.
  - O arquivo reembolso/docs/sessions/07-planejamento-envelope-v4.md não está
    commitado e fica num lugar estranho: as outras sessões estão em
    docs/sessions/. Não mexi nele.

✻ Crunched for 19m 31s · done 23:15

> mantem centro_custo null como erro geral                                      
                                                                                
  agora faz so o fechamento da rastreabilidade                                  
                                                                                
  preenche o campo Commit das tasks T-026 ate T-041 com os hashes dos commits   
  correspondentes                                                               
                                                                                
  move o arquivo                                                                
  reembolso/docs/sessions/07-planejamento-envelope-v4.md                        
  para                                                                          
  docs/sessions/07-planejamento-envelope-v4.md                                  
                                                                                
  nao mexe no codigo nem na spec plan ou decisions, faz um commit separado so   
  desse fechamento de docs/tasks                                                
                                                                                
  nao faz push ainda                                                            
                                                                                
  no final me mostra o hash desse commit e o git status                         

  Ran 1 shell command (ctrl+o to expand)

● O destino está livre e há exatamente 16 campos Commit: vazios. Preencho cada
  um a partir do git log pelo (T-0NN) do assunto.

● Bash(git log --format="%h %s" 3ef0e3c..HEAD | grep -E
      "\(T-0(2[6-9]|3[0-9]|4[01])\)" > /tmp/hashes.txt && wc -l <
      /tmp/hashes.txt && python - <<'PY'
      import re…)
  ⎿  16
     warning: in the working copy of 'specs/001-motor-reembolso/tasks.md',
     LF will be replaced by CRLF the next time Git touches it
     … +32 lines (ctrl+o to expand)
  ⎿  Updated specs\001-motor-reembolso\tasks.md (+16 -16)
      301      `COTACAO_INDISPONIVEL` existe; a suíte da v3 continua pass
           ando sem alteração.
      302    - **Teste:** `tests/test_modelo.py::test_motivos_iguais_aos_
           codigos_da_spec`
      303      (atualizado para oito motivos)
      304 -  - **Commit:**                                               
      304 +  - **Commit:** 18b151f                                       
      305  
      306  - [x] **T-027** — Leitura e validação do documento de política
            (`politica.py`
      307    passa a ler `politica-v4.json` e devolver um objeto `Politic
           a`). Chaves de
     ...
      324      `"acrescimo_em_viagem_percentual": "x"`,
      325      `versao`, `vigencia` e `observacao` com qualquer valor.
      326    - **Teste:** `tests/test_rn015_politica.py`
      327 -  - **Commit:**                                               
      327 +  - **Commit:** 0726363                                       
      328  
      329  - [x] **T-028** — Política aplicável: `politica_aplicavel(poli
           tica, centro_custo)`
      330    devolve uma `PoliticaAplicavel` cujo `regra(categoria)` dá o
            limite (ou `None`
     ...
      359      `justificativas.origem`),
      360      `tests/test_rn013_dados_invalidos.py::test_rn013_erro_gera
           l_*` (caso
      361      `centro_custo` numérico)
      362 -  - **Commit:**                                               
      362 +  - **Commit:** f185c37                                       
      363  
      364  - [x] **T-029** — Leitura e validação do documento de câmbio (
           `cambio.py` →
      365    objeto `Cambio`), opcional. Quando informado, é sempre valid
           ado. Códigos de
     ...
      373      data. Sem erro: `fonte` e `observacao` com qualquer valor;
            `" usd "` lido como
      374      `USD`.
      375    - **Teste:** `tests/test_rn018_cambio.py::test_rn018_documen
           to_*`
      376 -  - **Commit:**                                               
      376 +  - **Commit:** 3acc4e8                                       
      377  
      378  - [x] **T-030** — Campo `moeda` da despesa: ausente → `BRL`; t
           exto normalizado
      379    (pontas e maiúsculas); vazio ou não texto → `DADOS_INVALIDOS
           ` com `moeda` nulo.
     ...
      385      usar `"projeto": "X"`.
      386    - **Teste:** `tests/test_rn017_moeda.py`,
      387      `tests/test_rn013_dados_invalidos.py::test_rn013_despesa_c
           ampo_desconhecido_e_ignorado`
      388 -  - **Commit:**                                               
      388 +  - **Commit:** f0a2bcf                                       
      389  
      390  ### 7.2 — Regras com política externa e câmbio
      391  
     … 88 more lines (ctrl+o to expand)

● Hashes preenchidos na ordem T-026 → T-041. Agora movo o arquivo de sessão e
  faço um único commit só com os dois arquivos.

● Bash(mv reembolso/docs/sessions/07-planejamento-envelope-v4.md
      docs/sessions/07-planejamento-envelope-v4.md && rmdir
      reembolso/docs/sessions reembolso/docs && git ad…)
  ⎿  warning: in the working copy of 'specs/001-motor-reembolso/tasks.md',
     LF will be replaced by CRLF the next time Git touches it
     warning: in the working copy of 'docs/sessions/07-planejamento-envelop
     … +12 lines (ctrl+o to expand)
  ⎿  2 files changed (binary, mode only or too large to show)

● Fiz o fechamento da rastreabilidade num único commit, sem push. Mantive
  centro_custo: null como erro geral, como você pediu.

  Hash do commit: 0f6b03b — docs(tasks): registra commits da T-026 a T-041 e 
  move sessao 07 para docs/sessions

  O commit tem só dois arquivos:
  - tasks.md: os 16 campos Commit: da T-026 até a T-041 estão preenchidos com os
    hashes dos commits de cada task. Antes, conferi que cada task tem
    exatamente um commit.
  - Sessão 07: o arquivo foi movido de reembolso/docs/sessions/ para
    docs/sessions/07-planejamento-envelope-v4.md. A pasta reembolso/docs/, que
    ficou vazia, foi removida. O arquivo ainda não estava no git, então ele
    entra no histórico já no lugar novo.

  Código, spec, plan e DECISIONS não foram alterados.

  git status:
  On branch main
  Your branch is ahead of 'origin/main' by 21 commits.
    (use "git push" to publish your local commits)

  nothing to commit, working tree clean

✻ Worked for 33s · done 23:22