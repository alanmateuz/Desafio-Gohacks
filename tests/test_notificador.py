"""Avisos para a equipe: 1 mensagem por pessoa, só o que espera decisão, sem repetir."""
import pathlib
import sys

import pandas as pd
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import notificador as nt  # noqa: E402


def _casos():
    return pd.DataFrame([
        {"caso_id": "F1:troca_bancaria_sem_confirmacao", "fornecedor": "Embalarte", "acionar": "PS01",
         "valor": 194440.08, "qtd": 25, "acao": "reverter_alteracao_cadastro", "motivo": "Conta trocada. Evidência: x"},
        {"caso_id": "F2:duplicidade", "fornecedor": "Maciez", "acionar": "", "valor": 4750.0, "qtd": 1,
         "acao": "cancelar_titulo", "motivo": "Título em dobro."},
        {"caso_id": "F3:valor_diferente_duplicata", "fornecedor": "Polyfilm", "acionar": "aprovador",
         "valor": 48380.0, "qtd": 1, "acao": "corrigir_lancamento", "motivo": "Zero a mais."},
        {"caso_id": "F4:sem_nf_no_portal", "fornecedor": "Cartonart", "acionar": "PS01", "valor": 900.0, "qtd": 1,
         "acao": "retirar_do_lote", "motivo": "NF não encontrada."},
    ])


ALERTAS = pd.DataFrame([{"alerta": "phishing_na_caixa", "fornecedor": "—", "acao": "abrir_incidente",
                         "acionar": "PS08", "motivo": "2 e-mails de golpe."}])


@pytest.fixture(autouse=True)
def outbox_temporario(tmp_path, monkeypatch):
    monkeypatch.setattr(nt, "OUTBOX", tmp_path / "outbox.jsonl")
    for v in ("SLACK_BOT_TOKEN", "SLACK_WEBHOOK_URL"):
        monkeypatch.delenv(v, raising=False)


def test_uma_mensagem_por_pessoa_e_so_o_que_espera_decisao():
    itens = nt.montar_itens(_casos(), ALERTAS, {})
    grupos = nt.por_pessoa(itens)
    assert set(grupos) == {"PS01", "aprovador", "PS08"}  # Maciez (alçada do analista) não vai
    assert len(grupos["PS01"]) == 2
    assert "Evidência" not in grupos["PS01"][0]["motivo"]


def test_caso_ja_decidido_nao_e_avisado():
    itens = nt.montar_itens(_casos(), ALERTAS, {"F1:troca_bancaria_sem_confirmacao": {"decisao": "manter"},
                                                "alerta:phishing_na_caixa:—": {"decisao": "ciente"}})
    chaves = {i["chave"] for i in itens}
    assert "F1:troca_bancaria_sem_confirmacao" not in chaves and not any(c.startswith("alerta") for c in chaves)


def test_acao_automatica_desfeita_volta_para_a_coordenacao():
    itens = nt.montar_itens(_casos(), ALERTAS.iloc[0:0], {"F2:duplicidade": {"decisao": "revisar"}})
    assert any(i["chave"] == "F2:duplicidade" and i["pessoa"] == "PS01" for i in itens)


def test_nao_repete_e_reenvia_quando_o_valor_muda():
    itens = nt.montar_itens(_casos(), ALERTAS, {})
    primeira = nt.enviar(itens)
    assert len(primeira) == 3 and all(r["status"] == "simulado" for r in primeira)
    assert nt.enviar(itens) == []  # nada novo
    itens[0]["valor"] += 1000
    reenvio = nt.enviar(itens)
    assert len(reenvio) == 1 and len(reenvio[0]["itens"]) == 1
    assert len(nt.historico()) == 4
