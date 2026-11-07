"""Regras determinísticas (código, não IA). Troque pelas regras do desafio no dia.

Exemplo: uma mensagem com termo proibido nunca pode ser aprovada automaticamente.
"""
import re

DECISOES = {"aprovar", "revisar"}
TERMOS_PROIBIDOS = re.compile(r"garantimos|reembolso|cura", re.IGNORECASE)


def tem_termo_proibido(texto: str) -> bool:
    return bool(TERMOS_PROIBIDOS.search(texto or ""))


def validar_saida(saida: dict) -> list[str]:
    """Confere a saída da IA antes de usar. Lista vazia = saída válida."""
    erros = []
    if saida.get("decisao") not in DECISOES:
        erros.append("decisao_invalida")
    if not saida.get("motivo"):
        erros.append("sem_motivo")
    return erros
