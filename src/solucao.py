"""Guardião do lote. O eval/run.py chama resolver(titulo) para cada caso.

Camada 1.1: 6 regras em código, ação proposta por caso e motivo em modo simulado (sem IA).
"""
from ia import escrever_motivo
from regras import avaliar, validar_saida


def resolver(titulo: dict) -> dict:
    # Dado faltando: não dá para conferir, então nunca libera
    if not titulo.get("titulo_id") or not titulo.get("fornecedor_id"):
        return {"decisao": "acionar", "regras_violadas": ["dado_faltando"], "acao": "retirar_do_lote",
                "acionar": "PS01", "caso_id": "sem_fornecedor:dado_faltando",
                "motivo": "Título sem identificação ou sem fornecedor; não é possível conferir."}

    # 1. Código para regra
    violacoes = avaliar(titulo)
    if not violacoes:
        saida = {"decisao": "liberar", "regras_violadas": [], "acao": None, "acionar": None,
                 "caso_id": None, "motivo": "Nenhuma regra violada."}
    else:
        principal = violacoes[0]  # a de maior prioridade define a ação e o caso
        saida = {
            "decisao": principal["decisao"],
            "regras_violadas": [v["regra"] for v in violacoes],
            "acao": principal["acao"],
            "acionar": next((v["acionar"] for v in violacoes if v["acionar"]), None),
            "caso_id": f"{titulo['fornecedor_id']}:{principal['regra']}",
            # 2. IA para linguagem (simulada): só escreve, não decide
            "motivo": escrever_motivo(titulo, violacoes),
        }

    # 3. Confere a saída antes de usar; inválida vai para a pessoa
    if validar_saida(saida):
        return {"decisao": "acionar", "regras_violadas": ["saida_invalida"], "acao": "retirar_do_lote",
                "acionar": "PS01", "caso_id": f"{titulo['fornecedor_id']}:saida_invalida",
                "motivo": "Saída do guardião inválida; revisar manualmente."}
    return saida
