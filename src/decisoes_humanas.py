"""Decisões das pessoas sobre casos e títulos (camada 3). Guardadas em dados/decisoes_humanas.json.

"CRUD" das suspeitas, sempre auditável (quem e quando):
- casos: "aprovar" a ação proposta, "liberar" (falso alarme), "manter" fora do lote, "revisar" (desfaz uma
  ação automática do agente e devolve o caso para uma pessoa); nota e responsável opcionais;
- manuais: retirar qualquer título do lote com motivo (suspeita criada por uma pessoa) e devolvê-lo depois.
O efeito no lote final é calculado aqui, em código.
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


def _agora() -> str:
    return datetime.now().strftime("%d/%m %H:%M")


def _ler() -> dict:
    try:
        dados = json.loads(ARQUIVO.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {}
    if "casos" not in dados:  # formato antigo: {caso_id: {...}}
        dados = {"casos": {k: v for k, v in dados.items() if isinstance(v, dict)}, "manuais": {}}
    dados.setdefault("manuais", {})
    return dados


def _gravar(dados: dict) -> None:
    ARQUIVO.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")


def carregar() -> dict:
    """Decisões por caso (compatível com a versão anterior)."""
    return _ler()["casos"]


def registrar(caso_id: str, decisao: str, quem: str, nota: str = "", responsavel: str = "") -> None:
    dados = _ler()
    anterior = dados["casos"].get(caso_id, {})
    dados["casos"][caso_id] = {"decisao": decisao, "quem": quem, "quando": _agora(),
                               "nota": nota or anterior.get("nota", ""),
                               "responsavel": responsavel or anterior.get("responsavel", "")}
    _gravar(dados)


def anotar(caso_id: str, nota: str, responsavel: str, quem: str) -> None:
    """Atualiza nota/responsável sem mudar a decisão (ou sem decidir ainda)."""
    dados = _ler()
    atual = dados["casos"].get(caso_id, {"decisao": "", "quem": "", "quando": ""})
    atual.update({"nota": nota, "responsavel": responsavel, "anotado_por": quem, "anotado_em": _agora()})
    dados["casos"][caso_id] = atual
    _gravar(dados)


def desfazer(caso_id: str) -> None:
    dados = _ler()
    dados["casos"].pop(caso_id, None)
    _gravar(dados)


def manuais() -> dict:
    return _ler()["manuais"]


def retirar_manual(titulo_id: str, motivo: str, quem: str) -> None:
    dados = _ler()
    dados["manuais"][titulo_id] = {"motivo": motivo, "quem": quem, "quando": _agora()}
    _gravar(dados)


def devolver_manual(titulo_id: str) -> None:
    dados = _ler()
    dados["manuais"].pop(titulo_id, None)
    _gravar(dados)


def volta_ao_lote(acao: str, decisao: dict | None) -> bool:
    if not decisao or not decisao.get("decisao"):
        return False
    if decisao["decisao"] == "liberar":
        return True
    if decisao["decisao"] in ("manter", "revisar"):
        return False
    return VOLTA_AO_LOTE_SE_APROVADO.get(acao, False)
