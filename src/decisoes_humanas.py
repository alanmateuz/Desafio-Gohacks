"""Decisões das pessoas sobre os casos (camada 3). Guardadas em dados/decisoes_humanas.json.

Cada caso tem uma ação proposta pelo agente. A pessoa pode:
- "aprovar": concorda com a ação (cancelar, reverter conta, corrigir valor, bloquear boleto);
- "liberar": falso alarme, o título volta ao lote como está.
O efeito no lote final é calculado aqui, em código, para ficar auditável.
"""
import json
from datetime import datetime
from pathlib import Path

ARQUIVO = Path(__file__).resolve().parent.parent / "dados" / "decisoes_humanas.json"

# Depois de "aprovar", o título volta ao lote? (cancelar e contatar o fornecedor: não)
VOLTA_AO_LOTE_SE_APROVADO = {
    "reverter_alteracao_cadastro": True,   # paga na conta anterior, no prazo
    "corrigir_lancamento": True,           # paga o valor/fornecedor corrigido
    "solicitar_aprovacao": True,
    "cancelar_titulo": False,              # duplicado sai de vez
    "contatar_fornecedor": False,          # espera confirmação pelo canal do cadastro
    "retirar_do_lote": False,
}


def carregar() -> dict:
    try:
        return json.loads(ARQUIVO.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def registrar(caso_id: str, decisao: str, quem: str) -> None:
    dados = carregar()
    dados[caso_id] = {"decisao": decisao, "quem": quem,
                      "quando": datetime.now().strftime("%d/%m %H:%M")}
    ARQUIVO.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")


def desfazer(caso_id: str) -> None:
    dados = carregar()
    dados.pop(caso_id, None)
    ARQUIVO.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")


def volta_ao_lote(acao: str, decisao: dict | None) -> bool:
    if not decisao:
        return False
    if decisao["decisao"] == "liberar":
        return True
    return VOLTA_AO_LOTE_SE_APROVADO.get(acao, False)
