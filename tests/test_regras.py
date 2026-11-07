"""Testes das regras determinísticas do guardião. Rode: pytest -q
Versão mínima da camada 1; o /testes (avaliador) amplia com o gabarito do Mateus."""
import pathlib
import sys
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
from regras import chave_duplicidade, normalizar_nf, troca_bancaria_sem_confirmacao, validar_saida

REF = datetime(2026, 11, 2, 8, 0)


def test_nf_com_zeros_e_serie_viram_a_mesma():
    assert normalizar_nf("000011045") == normalizar_nf("11045") == normalizar_nf("11045-1") == "11045"
    assert normalizar_nf("36495/1") == "36495"
    assert normalizar_nf("") == ""


def test_parcelas_diferentes_nao_sao_duplicidade():
    assert chave_duplicidade("FP4615", "1234", "1/2") != chave_duplicidade("FP4615", "1234", "2/2")


def test_sem_nf_nao_compara_duplicidade():
    assert chave_duplicidade("FP4615", "", "1/1") is None


def test_troca_bancaria_sem_confirmacao_e_pega():
    alt = {"campo": "conta", "data_hora": "2026-10-30 16:05:00", "confirmacao_registrada": "não"}
    assert troca_bancaria_sem_confirmacao([alt], REF) == alt


def test_troca_confirmada_ou_antiga_nao_e_suspeita():
    confirmada = {"campo": "conta", "data_hora": "2026-10-20 14:10:00", "confirmacao_registrada": "sim"}
    antiga = {"campo": "conta", "data_hora": "2026-08-01 10:00:00", "confirmacao_registrada": "não"}
    email = {"campo": "email", "data_hora": "2026-10-30 10:00:00", "confirmacao_registrada": "não"}
    assert troca_bancaria_sem_confirmacao([confirmada, antiga, email], REF) is None


def test_saida_invalida_e_barrada():
    assert "decisao_invalida" in validar_saida({"decisao": "talvez", "motivo": "x"})
    assert "retirada_sem_regra" in validar_saida({"decisao": "retirar", "motivo": "x", "regras_violadas": []})
