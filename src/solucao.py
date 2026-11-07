"""Guardião do lote. O eval/run.py chama resolver(titulo) para cada caso.

Camada 1: regras de troca bancária e duplicidade + motivo em modo simulado (sem IA).
"""
from ia import escrever_motivo
from regras import avaliar, validar_saida


def resolver(titulo: dict) -> dict:
    # Dado faltando: não dá para conferir, então nunca libera
    if not titulo.get("titulo_id") or not titulo.get("fornecedor_id"):
        return {"decisao": "acionar", "regras_violadas": ["dado_faltando"], "acionar": "PS01",
                "motivo": "Título sem identificação ou sem fornecedor; não é possível conferir."}

    # 1. Código para regra
    violacoes = avaliar(titulo)
    if not violacoes:
        saida = {"decisao": "liberar", "regras_violadas": [], "acionar": None,
                 "motivo": "Nenhuma regra violada."}
    else:
        saida = {
            "decisao": "retirar",
            "regras_violadas": [v["regra"] for v in violacoes],
            "acionar": violacoes[0]["acionar"],
            # 2. IA para linguagem (simulada na camada 1): só escreve, não decide
            "motivo": escrever_motivo(titulo, violacoes),
        }

    # 3. Confere a saída antes de usar; inválida vai para a pessoa
    if validar_saida(saida):
        return {"decisao": "acionar", "regras_violadas": ["saida_invalida"], "acionar": "PS01",
                "motivo": "Saída do guardião inválida; revisar manualmente."}
    return saida
