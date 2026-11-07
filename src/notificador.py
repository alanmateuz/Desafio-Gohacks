"""Avisa a equipe dos casos que esperam decisão: 1 mensagem por pessoa, sem repetir.

Uso: python src/notificador.py            # mostra o que seria enviado
     python src/notificador.py --enviar   # envia

- Código para regra: quem recebe, o motivo e a ação vêm das regras e do config/equipe.json.
  A IA não escreve nada na mensagem.
- Só o que espera uma pessoa: o que o agente resolve dentro da alçada do analista não é enviado.
- Sem repetir: só vai caso novo ou cujo valor mudou desde o último envio com sucesso.
- 3 modos pelo .env: SLACK_BOT_TOKEN (DM, com SLACK_ID_<pessoa>), SLACK_WEBHOOK_URL (um canal)
  ou simulado. Todo envio fica registrado em dados/outbox_slack.jsonl (é o histórico do chat).
- Até 2 tentativas por mensagem; se falhar, fica como "falhou" e volta a ser enviada na próxima vez.
"""
import json
import os
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")
CONFIG = json.loads((RAIZ / "config" / "equipe.json").read_text(encoding="utf-8"))
PESSOAS = CONFIG["pessoas"]
ACAO_TEXTO = CONFIG["acao_texto"]
OUTBOX = RAIZ / "dados" / "outbox_slack.jsonl"
TENTATIVAS = 2
DECIDIDO = ("aprovar", "liberar", "manter")


def modo() -> str:
    if os.getenv("SLACK_BOT_TOKEN"):
        return "slack"
    if os.getenv("SLACK_WEBHOOK_URL"):
        return "webhook"
    return "simulado"


def brl(v: float) -> str:
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def montar_itens(casos, alertas, decisoes: dict) -> list[dict]:
    """Casos e alertas que esperam uma pessoa (sem decisão humana registrada)."""
    itens = []
    for c in casos.itertuples():
        d = (decisoes.get(c.caso_id) or {}).get("decisao")
        if d in DECIDIDO:
            continue
        pessoa = c.acionar or ("PS01" if d == "revisar" else "")  # ação automática desfeita volta à coordenação
        if not pessoa:
            continue  # dentro da alçada: o agente resolve sozinho
        motivo = str(c.motivo).partition(" Evidência:")[0]
        itens.append({"chave": c.caso_id, "pessoa": pessoa, "fornecedor": c.fornecedor, "valor": round(float(c.valor), 2),
                      "qtd": int(c.qtd), "motivo": motivo, "acao": ACAO_TEXTO.get(c.acao, c.acao)})
    for a in (alertas.itertuples() if len(alertas) else []):
        chave = f"alerta:{a.alerta}:{a.fornecedor}"
        if (decisoes.get(chave) or {}).get("decisao"):
            continue
        forn = a.fornecedor if a.fornecedor != "—" else "Caixa de e-mail · remetentes desconhecidos"
        itens.append({"chave": chave, "pessoa": a.acionar, "fornecedor": forn, "valor": 0.0, "qtd": 0,
                      "motivo": a.motivo, "acao": ACAO_TEXTO.get(a.acao, a.acao)})
    return itens


def historico() -> list[dict]:
    if not OUTBOX.exists():
        return []
    return [json.loads(l) for l in OUTBOX.read_text(encoding="utf-8").splitlines() if l.strip()]


def ja_avisados() -> dict:
    """chave do caso -> valor do último aviso entregue (ou simulado)."""
    out = {}
    for m in historico():
        if m["status"] in ("enviado", "simulado"):
            for i in m["itens"]:
                out[i["chave"]] = i["valor"]
    return out


def novos(itens: list[dict]) -> list[dict]:
    av = ja_avisados()
    return [i for i in itens if i["chave"] not in av or abs(av[i["chave"]] - i["valor"]) > 0.005]


def por_pessoa(itens: list[dict]) -> dict:
    grupos = {}
    for i in itens:
        grupos.setdefault(i["pessoa"], []).append(i)
    return grupos


def texto(pessoa: str, itens: list[dict]) -> str:
    nome = PESSOAS.get(pessoa, {}).get("nome", pessoa)
    total = sum(i["valor"] for i in itens)
    linhas = [f"Olá, {nome.split()[0]}! O GoGuardian segurou {len(itens)} caso(s) que precisam da sua decisão"
              + (f" ({brl(total)})." if total else ".")]
    for i in itens:
        valor = f" · *{brl(i['valor'])}*" + (f" ({i['qtd']} títulos)" if i["qtd"] > 1 else "") if i["valor"] else ""
        linhas.append(f"• *{i['fornecedor']}*{valor}\n   Motivo: {i['motivo']}\n   Ação proposta: {i['acao']}")
    linhas.append(f"Decida no painel: {CONFIG['painel_url']}")
    return "\n".join(linhas)


def _post(url: str, corpo: dict, token: str = "") -> None:
    req = urllib.request.Request(url, data=json.dumps(corpo).encode(), method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8",
                                          "User-Agent": "guardiao-do-lote/1.0",
                                          **({"Authorization": f"Bearer {token}"} if token else {})})
    with urllib.request.urlopen(req, timeout=15) as r:
        resp = r.read().decode()
    if token and not json.loads(resp).get("ok"):
        raise RuntimeError(json.loads(resp).get("error", "erro do Slack"))


def _entregar(m: str, pessoa: str, msg: str) -> str:
    if m == "simulado":
        return "simulado"
    slack_id = os.getenv(f"SLACK_ID_{pessoa}", "")
    for tentativa in range(TENTATIVAS):
        try:
            if m == "slack":
                if not slack_id:
                    return "sem_id"
                _post("https://slack.com/api/chat.postMessage", {"channel": slack_id, "text": msg},
                      os.environ["SLACK_BOT_TOKEN"])
            else:
                marca = f"<@{slack_id}> " if slack_id else f"*Para {PESSOAS.get(pessoa, {}).get('nome', pessoa)}:* "
                _post(os.environ["SLACK_WEBHOOK_URL"], {"text": marca + msg})
            return "enviado"
        except Exception:  # noqa: BLE001 — rede/Slack fora: tenta de novo e depois desiste
            time.sleep(1 + tentativa)
    return "falhou"


def enviar(itens: list[dict]) -> list[dict]:
    """Envia os itens novos, 1 mensagem por pessoa. Devolve as mensagens registradas."""
    m = modo()
    registros = []
    for pessoa, grupo in por_pessoa(novos(itens)).items():
        msg = texto(pessoa, grupo)
        registros.append({"quando": datetime.now().strftime("%d/%m %H:%M"), "pessoa": pessoa, "modo": m,
                          "status": _entregar(m, pessoa, msg), "texto": msg, "itens": grupo})
    if registros:
        OUTBOX.parent.mkdir(exist_ok=True)
        with OUTBOX.open("a", encoding="utf-8") as f:
            for r in registros:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return registros


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    import decisoes_humanas as dh
    from coletor import montar_planilha_mae
    from guardiao import alertas_caixa, casos, conferir
    df = conferir(montar_planilha_mae())
    itens = montar_itens(casos(df), alertas_caixa(df), dh.carregar())
    pend = novos(itens)
    print(f"Modo: {modo()} · {len(itens)} caso(s) esperando decisão · {len(pend)} ainda não avisado(s)\n")
    if "--enviar" in sys.argv:
        for r in enviar(itens):
            print(f"[{r['status']}] {PESSOAS.get(r['pessoa'], {}).get('nome', r['pessoa'])}: {len(r['itens'])} caso(s)")
    else:
        for pessoa, grupo in por_pessoa(pend).items():
            print(f"--- para {PESSOAS.get(pessoa, {}).get('nome', pessoa)}\n{texto(pessoa, grupo)}\n")


if __name__ == "__main__":
    main()
