"""Normalização de texto (RN-002) e arredondamento (RN-003)."""

import unicodedata


def normalizar_texto(texto: str) -> str:
    """Remove espaços das pontas, passa para minúsculas e remove acentos (RN-002, DT-007).

    Espaços internos e demais caracteres são mantidos.
    """
    decomposto = unicodedata.normalize("NFD", texto.strip().lower())
    sem_acentos = "".join(c for c in decomposto if unicodedata.category(c) != "Mn")
    return unicodedata.normalize("NFC", sem_acentos)
