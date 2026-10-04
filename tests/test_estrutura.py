import importlib


def test_pacote_importa():
    assert importlib.import_module("reembolso") is not None
    assert importlib.import_module("reembolso.__main__") is not None
