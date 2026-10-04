from reembolso.modelo import Motivo, Status


def test_motivos_iguais_aos_codigos_da_spec():
    assert {m.value for m in Motivo} == {
        "DADOS_INVALIDOS",
        "VALOR_NEGATIVO",
        "FORA_DO_PERIODO",
        "CATEGORIA_NAO_REEMBOLSAVEL",
        "DUPLICATA",
        "NOTA_FISCAL_AUSENTE",
        "LIMITE_DIARIO",
    }


def test_status_iguais_aos_textos_da_spec():
    assert {s.value for s in Status} == {"aprovado", "limitado", "recusado"}
