"""Regras determinísticas do guardião do lote (código, não IA).

Cada regra vem de dados/parametros.md ou dados/politicas.csv. Nada aqui chama a IA.
"""
import re
from datetime import datetime, timedelta

DECISOES = {"liberar", "retirar", "acionar"}
CAMPOS_BANCARIOS = {"banco", "agencia", "conta", "chave_pix"}
JANELA_TROCA_BANCARIA = timedelta(days=30)  # politicas.csv: "alterados há menos de 30 dias"
RENATA = "PS01"  # coordenadora de CP: fraude, duplicidade, erro de lançamento
APROVADOR = "aprovador"
TOLERANCIA_DUPLICATA = 0.10  # politicas.csv tres_vias.titulo_x_duplicata (vai para config na camada 4)
ALCADA_ANALISTA = 5000.0  # politicas.csv alcadas.analista_cp.*_ate


def brl(v: float) -> str:
    """R$ no formato brasileiro: 90.873,80."""
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


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


SUSPEITAS = {
    "dominio_parecido": "domínio parecido com o do cadastro",
    "remetente_fora_do_cadastro": "remetente fora do cadastro",
    "tentativa_de_instruir_agente": "texto tenta dar ordem ao agente",
}


def _fato_email(e: dict) -> str:
    fato = (f"o pedido veio de {e['remetente']} ({SUSPEITAS.get(e.get('suspeita'), e.get('suspeita'))})"
            f" em {str(e.get('data_hora', ''))[:10]}, e-mail {e['comunicacao_id']}")
    if e.get("tenta_instruir_agente") and e.get("trecho"):
        fato += f"; o texto tenta instruir o robô: \"{e['trecho']}\""
    return fato


def aprovacao_necessaria(valor: float) -> str | None:
    """Quem precisa aprovar no lote (alçadas de politicas.csv). Não retém: a aprovação é em lote."""
    if valor > 50000:
        return "PS03"
    if valor > ALCADA_ANALISTA:
        return APROVADOR
    return None


def _vazio(valor) -> bool:
    return valor is None or valor == "" or (isinstance(valor, float) and valor != valor)


def avaliar(titulo: dict) -> list[dict]:
    """Aplica as regras a uma linha da planilha mãe. Devolve as violações em ordem de prioridade:
    a primeira define a ação e o caso. Cada violação traz a ação proposta (ferramentas.csv)."""
    violacoes = []
    valor = float(titulo.get("valor") or 0)
    forma = titulo.get("forma_pagamento")

    troca = titulo.get("troca_bancaria_suspeita")
    if troca and forma in {"ted", "pix"}:
        violacoes.append({
            "regra": "troca_bancaria_sem_confirmacao",
            "decisao": "retirar", "acao": "reverter_alteracao_cadastro", "acionar": RENATA,
            "fato": f"{troca['campo']} alterado em {troca['data_hora'][:10]} por {troca['alterado_por']}"
                    f" (origem: {troca['origem']}) sem confirmação registrada",
        })

    raiz_boleto, raiz_forn = titulo.get("raiz_beneficiario_boleto"), titulo.get("raiz_fornecedor")
    if forma == "boleto" and raiz_boleto and raiz_forn and raiz_boleto != raiz_forn:
        violacoes.append({
            "regra": "boleto_beneficiario_diferente",
            "decisao": "retirar", "acao": "contatar_fornecedor", "acionar": RENATA,
            "fato": f"boleto em nome do CNPJ {titulo.get('cnpj_beneficiario_boleto')}, que não é do "
                    f"fornecedor (raiz {raiz_forn})",
        })

    if titulo.get("duplicado_de"):
        violacoes.append({
            "regra": "duplicidade",
            "decisao": "retirar", "acao": "cancelar_titulo",
            "acionar": RENATA if valor > ALCADA_ANALISTA else None,
            "fato": f"mesma NF {titulo['nf_normalizada']} parcela {titulo['parcela']} já está em "
                    f"{titulo['duplicado_de']}",
        })

    tem_nf = bool(titulo.get("nf_normalizada"))
    if tem_nf and not titulo.get("chave_nf"):
        if titulo.get("nf_outro_fornecedor"):
            violacoes.append({
                "regra": "nf_de_outro_fornecedor",
                "decisao": "retirar", "acao": "corrigir_lancamento", "acionar": APROVADOR,
                "fato": f"a NF {titulo['nf_normalizada']} não é deste fornecedor; é de "
                        f"{titulo['nf_outro_fornecedor']}",
            })
        else:
            violacoes.append({
                "regra": "sem_nf_no_portal",
                "decisao": "acionar", "acao": "retirar_do_lote", "acionar": RENATA,
                "fato": f"a NF {titulo['nf_normalizada']} não existe no portal para este fornecedor",
            })

    if titulo.get("fracionado_com"):
        violacoes.append({
            "regra": "fracionamento_alcada",
            "decisao": "retirar", "acao": "solicitar_aprovacao", "acionar": APROVADOR,
            "fato": f"títulos da mesma NF no mesmo dia somam acima da alçada do analista "
                    f"(com {titulo['fracionado_com']}); dividir para caber na alçada é proibido",
        })

    # Evidência dos e-mails (IA lê, código decide): só REFORÇA uma regra que já disparou
    regras_disparadas = {v["regra"] for v in violacoes}
    for e in titulo.get("emails_suspeitos") or []:
        if "troca_bancaria_sem_confirmacao" in regras_disparadas and e.get("pede_troca_bancaria"):
            violacoes.append({
                "regra": "pedido_troca_por_email_suspeito",
                "decisao": "retirar", "acao": "reverter_alteracao_cadastro", "acionar": RENATA,
                "fato": _fato_email(e),
            })
        elif "boleto_beneficiario_diferente" in regras_disparadas and e.get("suspeita") in {
                "remetente_fora_do_cadastro", "dominio_parecido"}:
            violacoes.append({
                "regra": "boleto_de_email_fora_do_cadastro",
                "decisao": "retirar", "acao": "contatar_fornecedor", "acionar": RENATA,
                "fato": _fato_email(e),
            })

    vdup = titulo.get("valor_duplicata")
    # arredonda para centavos: 1000.10 - 1000.00 dá 0.1000000000000227 em ponto flutuante
    diferenca = round(abs(valor - float(vdup)), 2) if not _vazio(vdup) else 0.0
    if diferenca > TOLERANCIA_DUPLICATA:
        violacoes.append({
            "regra": "valor_diferente_duplicata",
            "decisao": "retirar", "acao": "corrigir_lancamento",
            "acionar": APROVADOR if diferenca > ALCADA_ANALISTA else None,
            "fato": f"título de {brl(valor)}, mas a duplicata da parcela {titulo['parcela']} é de "
                    f"{brl(float(vdup))} (diferença de {brl(diferenca)})",
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
