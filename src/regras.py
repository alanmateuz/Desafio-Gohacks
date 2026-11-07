"""Regras determinísticas do guardião do lote (código, não IA).

Cada regra vem de dados/parametros.md ou dados/politicas.csv. Nada aqui chama a IA.
"""
import re
from datetime import datetime, timedelta

DECISOES = {"liberar", "retirar", "acionar"}
CAMPOS_BANCARIOS = {"banco", "agencia", "conta", "chave_pix"}
JANELA_TROCA_BANCARIA = timedelta(days=30)  # politicas.csv: "alterados há menos de 30 dias"
RENATA = "PS01"  # coordenadora de CP: fraude, duplicidade, erro de lançamento


def normalizar_nf(numero: str) -> str:
    """'000011045' -> '11045'; '11079-1' -> '11079'; '36495/1' -> '36495'; vazio -> ''."""
    texto = str(numero or "").strip()
    if texto.lower() == "nan":
        return ""
    texto = re.split(r"[-/]", texto)[0]
    texto = re.sub(r"\D", "", texto)
    return texto.lstrip("0")


def troca_bancaria_sem_confirmacao(alteracoes: list[dict], referencia: datetime) -> dict | None:
    """Devolve a alteração bancária mais recente nos últimos 30 dias que NÃO tem confirmação
    registrada. Só o registro do ERP vale; texto de e-mail nunca confirma nada."""
    suspeitas = []
    for alt in alteracoes:
        if alt.get("campo") not in CAMPOS_BANCARIOS:
            continue
        quando = datetime.fromisoformat(str(alt["data_hora"]))
        if referencia - quando > JANELA_TROCA_BANCARIA or quando > referencia:
            continue
        if str(alt.get("confirmacao_registrada", "")).strip().lower() != "sim":
            suspeitas.append(alt)
    return max(suspeitas, key=lambda a: a["data_hora"]) if suspeitas else None


def chave_duplicidade(fornecedor_id: str, numero_nf: str, parcela: str) -> tuple | None:
    """Mesmo fornecedor + mesma NF normalizada + mesma parcela. Sem NF não dá para comparar."""
    nf = normalizar_nf(numero_nf)
    if not nf:
        return None
    return (fornecedor_id, nf, str(parcela).strip())


def avaliar(titulo: dict) -> list[dict]:
    """Aplica as regras a uma linha da planilha mãe. Devolve a lista de violações."""
    violacoes = []
    troca = titulo.get("troca_bancaria_suspeita")
    if troca and titulo.get("forma_pagamento") in {"ted", "pix"}:
        violacoes.append({
            "regra": "troca_bancaria_sem_confirmacao",
            "acionar": RENATA,
            "fato": f"{troca['campo']} alterado em {troca['data_hora'][:10]} por {troca['alterado_por']}"
                    f" (origem: {troca['origem']}) sem confirmação registrada",
        })
    if titulo.get("duplicado_de"):
        violacoes.append({
            "regra": "duplicidade",
            "acionar": RENATA,
            "fato": f"mesma NF {titulo['nf_normalizada']} parcela {titulo['parcela']} já está em "
                    f"{titulo['duplicado_de']}",
        })
    return violacoes


def validar_saida(saida: dict) -> list[str]:
    """Confere a saída do guardião (e, na camada 2, da IA). Lista vazia = saída válida."""
    erros = []
    if saida.get("decisao") not in DECISOES:
        erros.append("decisao_invalida")
    if not saida.get("motivo"):
        erros.append("sem_motivo")
    if saida.get("decisao") != "liberar" and not saida.get("regras_violadas"):
        erros.append("retirada_sem_regra")
    return erros
