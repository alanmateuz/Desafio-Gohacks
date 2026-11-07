"""Teste de integração na fila real (dados/ do evento): os 6 furos da verificação das 11:10."""
import pathlib
import sys

import pytest

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))
pytestmark = pytest.mark.skipif(not (RAIZ / "dados" / "agenda_remessa.csv").exists(),
                                reason="bases do evento não baixadas em dados/")


@pytest.fixture(scope="module")
def fila():
    from coletor import montar_planilha_mae
    from guardiao import conferir
    return conferir(montar_planilha_mae()).set_index("titulo_id")


@pytest.mark.parametrize("titulo, regra", [
    ("TP431459", "valor_diferente_duplicata"),      # zero a mais, R$ 48.380 x 4.838
    ("TP431775", "valor_diferente_duplicata"),      # zero a mais, R$ 90.873,80
    ("TP431946", "nf_de_outro_fornecedor"),         # Cartonart x Gráfica Cartonar
    ("TP432337", "nf_de_outro_fornecedor"),         # Polyfilm x Polifilm
    ("TP431754", "boleto_beneficiario_diferente"),  # 2ª via falsa da Pigmentos Aquarela
    ("TP432130", "troca_bancaria_sem_confirmacao"),  # Embalarte, R$ 96.480
    ("TP430006", "duplicidade"),                     # Maciez NF 20329
])
def test_furo_e_retido(fila, titulo, regra):
    assert fila.loc[titulo, "decisao"] != "liberar"
    assert regra in fila.loc[titulo, "regras_violadas"]


def test_parcelas_legitimas_seguem(fila):
    for titulo in ["TP431762", "TP431763", "TP429834"]:
        assert "duplicidade" not in fila.loc[titulo, "regras_violadas"]


def test_embalarte_vira_um_caso_so(fila):
    assert fila[fila.fornecedor_id == "FP4615"].caso_id.nunique() == 1


def test_contagem_esperada(fila):
    assert (fila.decisao != "liberar").sum() == 49
    lote = fila[fila.lote_remessa == "RM20261103-MER"]
    assert (lote.decisao != "liberar").sum() == 7


def test_ia_nunca_libera_o_que_as_regras_seguraram(fila):
    """Segurança: com ou sem a leitura da IA, nenhum título retido pelas regras passa a ser liberado."""
    from coletor import montar_planilha_mae
    from guardiao import conferir
    sem_ia = conferir(montar_planilha_mae(com_ia=False)).set_index("titulo_id")
    retidos_sem_ia = set(sem_ia[sem_ia.decisao != "liberar"].index)
    retidos_com_ia = set(fila[fila.decisao != "liberar"].index)
    assert retidos_sem_ia <= retidos_com_ia


def test_evidencia_dos_emails_nos_golpes(fila):
    assert "pedido_troca_por_email_suspeito" in fila.loc["TP432130", "regras_violadas"]
    assert "embalartte" in fila.loc["TP432130", "motivo"]
    assert "boleto_de_email_fora_do_cadastro" in fila.loc["TP431754", "regras_violadas"]


def test_alertas_da_caixa(fila):
    from guardiao import alertas_caixa
    al = alertas_caixa(fila)
    assert set(al.alerta) == {"phishing_na_caixa", "tentativa_de_instruir_agente"}
    assert "EM570998" in al[al.alerta == "phishing_na_caixa"].emails.iloc[0]  # falso cartório que o Jev erra


def test_alcada_vira_aprovacao_no_lote(fila):
    assert (fila.aprovacao == "PS03").sum() == 19


def test_reversao_paga_na_conta_anterior(fila):
    """Se a reversão da Embalarte for aprovada, o destino é a conta de antes da troca, não a do golpista."""
    assert fila.loc["TP432130", "destino_anterior"] == "ted 774/7166/9517944-5"
    assert "905" in fila.loc["TP432130", "destino_pagamento"]
