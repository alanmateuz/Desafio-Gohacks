"""Caixa de e-mail da área: liga cada e-mail a um fornecedor (código) e lê o texto (IA, Jev).

Código para regra:
- quem é o fornecedor (endereço/domínio do cadastro, nome, CNPJ citado);
- se o remetente está FORA do cadastro ou usa domínio PARECIDO (embalartte × embalarte);
- conta bancária citada no texto (padrão de texto).
IA para linguagem: pede troca de conta? tenta dar ordem ao agente? tipo do e-mail?
"""
import re
from difflib import SequenceMatcher
from pathlib import Path

import pandas as pd

from leitor_email import ler_email

DADOS = Path(__file__).resolve().parent.parent / "dados"
GRATUITOS = {"gmail.com", "outlook.com", "hotmail.com", "yahoo.com", "yahoo.com.br", "uol.com.br",
             "bol.com.br", "icloud.com", "live.com"}
RE_CONTA = re.compile(r"(?:c/c|conta)\s*:?\s*(\d{4,10}-?\d?)", re.IGNORECASE)
RE_CNPJ = re.compile(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}")


def _dominio(endereco: str) -> str:
    return str(endereco or "").split("@")[-1].strip().lower()


def _raiz(cnpj: str) -> str:
    return re.sub(r"\D", "", str(cnpj or ""))[:8]


def _parecido(a: str, b: str) -> bool:
    """Domínios quase iguais mas diferentes (1–2 letras trocadas)."""
    return a != b and SequenceMatcher(None, a, b).ratio() >= 0.9


def carregar_caixa(com_ia: bool = True) -> pd.DataFrame:
    msgs = pd.read_csv(DADOS / "comunicacoes_fornecedores.csv", dtype=str, keep_default_na=False)
    forn = pd.read_csv(DADOS / "fornecedores.csv", dtype=str, keep_default_na=False)
    alts = pd.read_csv(DADOS / "alteracoes_cadastro.csv", dtype=str, keep_default_na=False)

    # Endereços aceitos por fornecedor: o cadastro atual + os anteriores (antes de trocas de e-mail)
    enderecos = {}
    for fid, e in zip(forn.fornecedor_id, forn.email_cadastrado):
        enderecos.setdefault(fid, set()).add(e.strip().lower())
    for _, a in alts[alts.campo == "email"].iterrows():
        enderecos.setdefault(a.fornecedor_id, set()).add(a.valor_anterior.strip().lower())
    por_endereco = {e: f for f, es in enderecos.items() for e in es}
    por_dominio = {_dominio(e): f for f, es in enderecos.items() for e in es
                   if _dominio(e) not in GRATUITOS}
    por_raiz = {_raiz(c): f for f, c in zip(forn.fornecedor_id, forn.cnpj)}
    nomes = {f: n.lower() for f, n in zip(forn.fornecedor_id, forn.nome_fantasia) if len(n) >= 5}

    linhas = []
    for m in msgs.to_dict("records"):
        rem = m["remetente"].strip().lower()
        dom = _dominio(rem)
        texto_total = f"{m['assunto']} {m['nome_remetente']} {m['texto']} {m['anexos']}".lower()
        fid, como = "", ""
        if rem in por_endereco:
            fid, como = por_endereco[rem], "endereco_cadastro"
        elif dom in por_dominio:
            fid, como = por_dominio[dom], "dominio_cadastro"
        else:
            parecido = next((d for d in por_dominio if _parecido(dom, d)), None)
            if parecido:
                fid, como = por_dominio[parecido], "dominio_parecido"
            else:
                fid = next((f for f, n in nomes.items() if n in texto_total), "")
                if not fid:
                    fid = next((por_raiz[_raiz(c)] for c in RE_CNPJ.findall(texto_total)
                                if _raiz(c) in por_raiz), "")
                como = "fora_do_cadastro" if fid else "desconhecido"
        conta = RE_CONTA.search(m["texto"])
        lido = ler_email(m["remetente"], m["assunto"], m["texto"]) if com_ia else {"erro": "sem_ia"}
        linhas.append({
            "comunicacao_id": m["comunicacao_id"], "data_hora": m["data_hora"], "remetente": rem,
            "assunto": m["assunto"], "texto": m["texto"], "fornecedor_id": fid, "vinculo": como,
            "conta_citada": conta.group(1) if conta else "",
            "pede_troca_bancaria": lido.get("pede_troca_bancaria"),
            "tenta_instruir_agente": lido.get("tenta_instruir_agente"),
            "tipo": lido.get("tipo", ""), "confianca": lido.get("confianca"),
            "revisar_ia": bool(lido.get("revisar")), "erro_ia": lido.get("erro", ""),
            "custo_usd": lido.get("custo_usd", 0.0),
        })
    return pd.DataFrame(linhas)


def suspeita_do_email(e: dict) -> str:
    """Motivo de suspeita de um e-mail, decidido pelo código (a IA só alimenta)."""
    if e["vinculo"] == "dominio_parecido":
        return "dominio_parecido"
    if e["vinculo"] == "fora_do_cadastro":
        return "remetente_fora_do_cadastro"
    if e["vinculo"] == "desconhecido" and (e["tipo"] == "phishing" or e["revisar_ia"]):
        return "remetente_desconhecido"
    if e["tenta_instruir_agente"]:
        return "tentativa_de_instruir_agente"
    return ""


def trecho_suspeito(texto: str) -> str:
    """Primeira frase que fala com robô/IA ou manda pular a conferência (para mostrar como evidência)."""
    for frase in re.split(r"(?<=[.!?])\s+", texto or ""):
        if re.search(r"rob[ôo]|assistente|\bIA\b|sem conferir|n[ãa]o (é|e) necess|j[áa] foi validad|"
                     r"sem a confer|pr[ée]-aprovad", frase, re.IGNORECASE):
            return frase.strip()
    return ""
