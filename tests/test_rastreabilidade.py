"""Toda RN da spec tem um arquivo de teste `test_rnNNN_*.py` (plan §6)."""

import re
from pathlib import Path

TESTES = Path(__file__).parent
SPEC = TESTES.parent / "specs" / "001-motor-reembolso" / "spec.md"


def rns_da_spec(texto: str) -> set[str]:
    return set(re.findall(r"RN-\d{3}", texto))


def rns_sem_teste(rns: set[str], arquivos: list[str]) -> set[str]:
    cobertas = set()
    for nome in arquivos:
        encontrado = re.fullmatch(r"test_rn(\d{3})_\w+\.py", nome)
        if encontrado:
            cobertas.add(f"RN-{encontrado.group(1)}")
    return rns - cobertas


def _arquivos_de_teste() -> list[str]:
    return [p.name for p in TESTES.glob("test_rn*.py")]


def test_rastreabilidade_spec_tem_rn001_a_rn014():
    assert rns_da_spec(SPEC.read_text(encoding="utf-8")) == {f"RN-{n:03d}" for n in range(1, 15)}


def test_rastreabilidade_toda_rn_tem_arquivo_de_teste():
    rns = rns_da_spec(SPEC.read_text(encoding="utf-8"))
    assert rns_sem_teste(rns, _arquivos_de_teste()) == set()


def test_rastreabilidade_remover_um_arquivo_faz_falhar():
    rns = rns_da_spec(SPEC.read_text(encoding="utf-8"))
    arquivos = [a for a in _arquivos_de_teste() if not a.startswith("test_rn007_")]
    assert rns_sem_teste(rns, arquivos) == {"RN-007"}
