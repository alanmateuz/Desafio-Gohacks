"""Testes das regras determinísticas. Rode: pytest -q
Cada teste = uma regra confirmada pelo Mateus. Troque pelos do desafio."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from regras import tem_termo_proibido, validar_saida


def test_termo_proibido_e_detectado():
    assert tem_termo_proibido("Garantimos o resultado")


def test_saida_sem_decisao_valida_e_barrada():
    assert "decisao_invalida" in validar_saida({"decisao": "talvez", "motivo": "x"})
