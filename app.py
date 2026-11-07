"""Painel do Guardião do lote, com a identidade visual Gogroup. Rode: streamlit run app.py"""
import html
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "src"))
import decisoes_humanas as dh  # noqa: E402
from coletor import montar_planilha_mae  # noqa: E402
from guardiao import alertas_caixa, casos, conferir  # noqa: E402
from leitor_email import TOKEN  # noqa: E402

st.set_page_config(page_title="Guardião do lote · Gogroup", page_icon=str(RAIZ / "assets/g-gogroup.png"),
                   layout="wide", initial_sidebar_state="collapsed")

# Identidade Gogroup (brandbook): azul protagonista, Poppins, pílulas, cantos arredondados.
# Atenção: o Streamlit quebra o <style> se houver linha em branco dentro dele.
st.markdown("""
<style>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap");
:root{ --azul:#2659a5; --azul-escuro:#1d4683; --azul-claro:#3dbfef; --azul-bg:#eef3fa; --limao:#d7d900;
  --rosa:#e61782; --vermelho:#e5273c; --amarelo:#f8ae13; --texto:#1f2430; --texto-2:#5b6272;
  --borda:#e3e7ee; --fundo:#f4f6f9; --branco:#ffffff; }
html, body, .stApp, .stApp *:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded){
  font-family:'Poppins', sans-serif !important; }
.stApp{ background:var(--fundo); color:var(--texto); }
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stSidebarCollapsedControl"]{ display:none; }
.block-container{ padding:0 2rem 3rem; max-width:1320px; }
.barra{ background:var(--branco); border-bottom:1px solid var(--borda); margin:0 -2rem 0; padding:14px 2rem;
  display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap; }
.barra img{ height:30px; display:block; }
.barra .dir{ display:flex; align-items:center; gap:12px; flex-wrap:wrap; color:var(--texto-2); font-size:.85rem; }
.pilula{ display:inline-flex; align-items:center; gap:6px; background:var(--azul); color:#fff; font-weight:600;
  font-size:.7rem; letter-spacing:.08em; text-transform:uppercase; padding:6px 14px; border-radius:999px; white-space:nowrap; }
.chip{ display:inline-flex; align-items:center; gap:7px; background:var(--fundo); border:1px solid var(--borda);
  color:var(--texto); font-weight:500; font-size:.8rem; padding:5px 12px; border-radius:999px; white-space:nowrap; }
.ponto{ width:8px; height:8px; border-radius:50%; display:inline-block; }
.cabeca{ display:flex; align-items:flex-end; justify-content:space-between; gap:16px; flex-wrap:wrap; margin:26px 0 18px; }
.cabeca h1{ font-size:1.55rem; font-weight:700; margin:0; padding:0; color:var(--texto); line-height:1.3; }
.cabeca .sub{ color:var(--texto-2); font-size:.9rem; margin-top:2px; }
.kpis{ display:grid; grid-template-columns:repeat(4, minmax(0,1fr)); gap:16px; margin-bottom:26px; }
@media (max-width:1100px){ .kpis{ grid-template-columns:repeat(2, minmax(0,1fr)); } }
.kpi{ background:var(--branco); border-radius:18px; padding:18px; display:flex; gap:16px; align-items:center;
  box-shadow:0 1px 2px rgba(16,24,40,.06); border:1px solid var(--borda); min-width:0; }
.kpi .ic{ flex:0 0 56px; height:56px; border-radius:16px; display:flex; align-items:center; justify-content:center; }
.kpi .ic svg{ width:28px; height:28px; }
.kpi .txt{ min-width:0; }
.kpi .rot{ color:var(--texto-2); font-size:.8rem; font-weight:500; }
.kpi .val{ color:var(--texto); font-size:clamp(1.15rem, 1.45vw, 1.75rem); font-weight:800; line-height:1.15; font-variant-numeric:tabular-nums; white-space:nowrap; }
.kpi .det{ color:var(--texto-2); font-size:.78rem; }
.painel{ background:var(--branco); border:1px solid var(--borda); border-radius:18px; padding:20px 22px; margin-bottom:18px;
  box-shadow:0 1px 2px rgba(16,24,40,.06); }
.painel h3{ font-size:1.02rem; font-weight:600; margin:0 0 2px; padding:0; color:var(--texto); }
.painel .nota{ color:var(--texto-2); font-size:.82rem; margin:0 0 12px; }
.tabela-wrap{ overflow:auto; max-height:560px; border:1px solid var(--borda); border-radius:12px; }
table.t{ width:100%; border-collapse:collapse; font-size:.85rem; }
table.t th{ position:sticky; top:0; background:#f8f9fb; color:var(--texto-2); font-weight:600; text-align:left;
  padding:10px 12px; border-bottom:1px solid var(--borda); white-space:nowrap; z-index:1; }
table.t td{ padding:10px 12px; border-bottom:1px solid #eef0f4; vertical-align:top; color:var(--texto); }
table.t tr:last-child td{ border-bottom:none; }
table.t .num{ text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }
table.t .forte{ font-weight:700; }
table.t .sec{ color:var(--texto-2); font-size:.78rem; }
.selo{ display:inline-flex; align-items:center; gap:5px; font-weight:600; font-size:.72rem; padding:3px 10px;
  border-radius:999px; white-space:nowrap; }
.selo.fraude{ background:#fde9ec; color:#a3162a; } .selo.erro{ background:#fff3dc; color:#7a4d00; }
.selo.dup{ background:var(--azul-bg); color:var(--azul-escuro); } .selo.ok{ background:#e6f6ef; color:#0f6b4a; }
.selo.neutro{ background:#eceef2; color:#3c4250; }
.caso{ display:grid; grid-template-columns:minmax(0,1fr) auto; gap:6px 24px; padding:18px 0; border-top:1px solid #eef0f4; }
.caso:first-of-type{ border-top:none; }
.caso .forn{ font-weight:600; font-size:1rem; margin:6px 0 2px; }
.caso .tit{ color:var(--texto-2); font-size:.78rem; word-break:break-word; }
.caso .mot{ font-size:.88rem; margin:8px 0 0; }
.caso .din{ text-align:right; }
.caso .din .v{ font-weight:800; font-size:1.45rem; font-variant-numeric:tabular-nums; white-space:nowrap; }
.caso .din .q{ color:var(--texto-2); font-size:.78rem; }
.caso .acao{ grid-column:1 / -1; font-size:.82rem; color:var(--texto-2); }
.evid{ border-left:3px solid var(--rosa); background:#fdf0f6; padding:8px 12px; font-size:.83rem; color:#5a0f35; margin-top:8px; }
.resolvido{ color:#0f6b4a; font-weight:600; font-size:.82rem; }
.barra-total{ display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap;
  background:var(--azul); color:#fff; border-radius:14px; padding:14px 18px; margin-bottom:14px; }
.barra-total .r{ font-size:.82rem; opacity:.9; } .barra-total .v{ font-size:1.6rem; font-weight:800; font-variant-numeric:tabular-nums; }
.vazio{ text-align:center; padding:30px; color:var(--texto-2); }
div[data-testid="stSegmentedControl"] button, div[data-testid="stButtonGroup"] button{ border-radius:999px !important; font-weight:600; }
.stButton button{ border-radius:999px; font-weight:600; white-space:nowrap; }
.stButton button[kind="primary"]{ background:var(--rosa); border-color:var(--rosa); color:#fff; }
.stButton button[kind="primary"]:hover{ background:#c4116d; border-color:#c4116d; color:#fff; }
.stButton button:focus-visible{ outline:3px solid var(--azul-claro); outline-offset:2px; }
.stDownloadButton button{ border-radius:999px; font-weight:600; background:#fff; color:var(--azul); border:1px solid var(--azul); }
div[data-testid="stSelectbox"] label, div[data-testid="stTextInput"] label{ font-size:.78rem; color:var(--texto-2); }
</style>
""", unsafe_allow_html=True)


def brl(v: float) -> str:
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def e(t) -> str:
    return html.escape(str(t if t is not None else ""))


ICONES = {  # ícones simples, brancos, decorativos (aria-hidden)
    "banco": '<path d="M3 10h18M5 10v8m4-8v8m6-8v8m4-8v8M3 20h18M12 3l9 5H3z" />',
    "escudo": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "alerta": '<path d="M12 8v5m0 3h.01"/><circle cx="12" cy="12" r="9"/>',
    "pessoa": '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
}


def kpi(icone: str, cor: str, rotulo: str, valor: str, detalhe: str) -> str:
    svg = (f'<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" '
           f'stroke-linejoin="round" aria-hidden="true">{ICONES[icone]}</svg>')
    return (f'<div class="kpi"><div class="ic" style="background:{cor}">{svg}</div><div class="txt">'
            f'<div class="rot">{e(rotulo)}</div><div class="val">{e(valor)}</div><div class="det">{e(detalhe)}</div>'
            f'</div></div>')


def tabela(linhas: list[dict], colunas: list[tuple], altura: int = 560) -> str:
    """colunas: (chave, título, classe). Valores já vêm escapados quando contêm HTML (chaves terminadas em _html)."""
    cab = "".join(f'<th class="{c}">{e(t)}</th>' for _, t, c in colunas)
    corpo = ""
    for l in linhas:
        corpo += "<tr>" + "".join(
            f'<td class="{c}">{l[k] if k.endswith("_html") else e(l[k])}</td>' for k, _, c in colunas) + "</tr>"
    return (f'<div class="tabela-wrap" style="max-height:{altura}px"><table class="t"><thead><tr>{cab}</tr></thead>'
            f'<tbody>{corpo}</tbody></table></div>')


PESSOAS = {"PS01": "Renata Paiva (coord. contas a pagar)", "PS03": "Helena Duarte (diretora financeira)",
           "PS08": "Lívia Campos (jurídico)", "aprovador": "Aprovador (Cláudia ou Renata)"}
ACAO_BOTAO = {"reverter_alteracao_cadastro": "Aprovar reversão da conta", "cancelar_titulo": "Aprovar cancelamento",
              "corrigir_lancamento": "Aprovar correção", "contatar_fornecedor": "Confirmar e bloquear boleto",
              "solicitar_aprovacao": "Aprovar valor somado", "retirar_do_lote": "Manter fora do lote"}
ACAO_TEXTO = {"reverter_alteracao_cadastro": "voltar para a conta anterior e pagar no prazo (aprovação dupla)",
              "cancelar_titulo": "cancelar o título duplicado",
              "corrigir_lancamento": "corrigir o lançamento e pagar o valor certo",
              "contatar_fornecedor": "confirmar o boleto com o fornecedor pelo canal do cadastro",
              "solicitar_aprovacao": "pedir aprovação do valor somado",
              "retirar_do_lote": "tirar do lote até alguém conferir"}
SELO = {"troca_bancaria_sem_confirmacao": ("fraude", "⚠ Fraude · conta trocada"),
        "boleto_beneficiario_diferente": ("fraude", "⚠ Fraude · boleto falso"),
        "duplicidade": ("dup", "⧉ Pagamento em dobro"),
        "valor_diferente_duplicata": ("erro", "≠ Valor diferente da nota"),
        "nf_de_outro_fornecedor": ("erro", "↔ Fornecedor errado"),
        "sem_nf_no_portal": ("erro", "? NF não encontrada"),
        "fracionamento_alcada": ("erro", "÷ Valor dividido")}
APROV = {"PS03": "Diretora", "aprovador": "Aprovador", "": "Analista"}


@st.cache_data(show_spinner="Conferindo a fila e lendo a caixa de e-mail…")
def carregar():
    df = conferir(montar_planilha_mae())
    caixa = df.attrs.get("caixa", pd.DataFrame())
    al = alertas_caixa(df)
    df.attrs = {}
    return df, caixa, al


df, caixa, alertas = carregar()
decisoes = dh.carregar()
lotes = df.drop_duplicates("lote_remessa").sort_values(["data_prevista", "horario_fechamento"]).lote_remessa.tolist()
info = df.drop_duplicates("lote_remessa").set_index("lote_remessa")


def nome_lote(l: str) -> str:
    if l == "fila":
        return "Fila inteira · 03/11 a 13/11"
    r = info.loc[l]
    return f"{r.banco_pagador} · {pd.to_datetime(r.data_prevista).strftime('%d/%m')} · fecha às {r.horario_fechamento}"


# ---------- Barra superior (logo + lote + status da IA)
logo_b64 = __import__("base64").b64encode((RAIZ / "assets/logo-gogroup.png").read_bytes()).decode()
cor_ia, txt_ia = ("#1d9e75", "IA ativa · Jev") if TOKEN else ("#f8ae13", "IA em modo simulado")
st.markdown(f"""<div class="barra"><div style="display:flex;align-items:center;gap:16px">
  <img src="data:image/png;base64,{logo_b64}" alt="Gogroup"><span class="pilula">Guardião do lote</span></div>
  <div class="dir">Contas a pagar · referência 02/11/2026 08:00
  <span class="chip"><span class="ponto" style="background:{cor_ia}"></span>{txt_ia}</span></div></div>""",
            unsafe_allow_html=True)

# ---------- Cabeçalho da tela + seletor de lote
c1, c2 = st.columns([3, 1.3], vertical_alignment="bottom")
with c2:
    escolha = st.selectbox("Lote de remessa", ["fila"] + lotes, index=1, format_func=nome_lote)
vis = df if escolha == "fila" else df[df.lote_remessa == escolha]
cs = casos(vis)


def decisao_efetiva(c):
    if c.caso_id in decisoes:
        return decisoes[c.caso_id]
    if not c.acionar:
        return {"decisao": "aprovar", "quem": "Agente (alçada do analista)", "quando": "automático"}
    return None


cs["efetiva"] = [decisao_efetiva(c) for c in cs.itertuples()]
cs["volta"] = [dh.volta_ao_lote(c.acao, c.efetiva) for c in cs.itertuples()]
voltam = set(t.strip() for c in cs[cs.volta].itertuples() for t in c.titulos.split(","))
seguem = vis[(vis.decisao == "liberar") | vis.titulo_id.isin(voltam)]
retidos = vis[(vis.decisao != "liberar") & ~vis.titulo_id.isin(voltam)]
pendentes = cs[cs.efetiva.isna()]
al_vis = alertas if escolha == "fila" else alertas.iloc[0:0]
alertas_pend = [a for a in al_vis.itertuples() if f"alerta:{a.alerta}:{a.fornecedor}" not in decisoes] if len(al_vis) else []
n_pend = len(pendentes) + len(alertas_pend)

with c1:
    st.markdown(f"""<div class="cabeca" style="margin-bottom:0"><div><h1>{e(nome_lote(escolha))}</h1>
      <div class="sub">{len(vis)} títulos conferidos antes do envio ao banco · {brl(vis.valor.sum())} na fila</div></div></div>""",
                unsafe_allow_html=True)
st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

# ---------- KPIs (o dinheiro em destaque)
st.markdown('<div class="kpis">'
            + kpi("banco", "#2659a5", "Vai ao banco", brl(seguem.valor.sum()), f"{len(seguem)} títulos liberados")
            + kpi("escudo", "#e5273c", "Protegido (fora do lote)", brl(retidos.valor.sum()), f"{len(retidos)} títulos retidos")
            + kpi("alerta", "#f8ae13", "Precisa da sua decisão", f"{n_pend} caso(s)",
                  brl(pendentes.valor.sum()) + " aguardando")
            + kpi("pessoa", "#3dbfef", "Pessoas acionadas", str((cs.acionar != "").sum() + len(al_vis)),
                  f"{(cs.acionar == '').sum()} casos resolvidos pelo agente")
            + "</div>", unsafe_allow_html=True)

# ---------- Navegação (uma seção por vez, sem menu lateral)
VISTAS = [f"Exceções ({n_pend})", "Lote final", "Caixa de e-mail", "Planilha mãe", "Resumo da fila"]
vista = st.segmented_control("Seção", VISTAS, default=VISTAS[0], label_visibility="collapsed") or VISTAS[0]
st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ================= EXCEÇÕES
if vista.startswith("Exceções"):
    ordem = cs.assign(p=cs.efetiva.isna()).sort_values(["p", "valor"], ascending=[False, False])
    with st.container(border=True):
        st.markdown('<h3 style="font-size:1.02rem;font-weight:600;margin:0">Exceções do lote</h3>'
                    '<div style="color:#5b6272;font-size:.82rem;margin:2px 0 4px">Um caso por fornecedor e problema. '
                    'O agente propõe a ação; quem tem a alçada decide. O que for aprovado volta ao lote quando faz sentido.'
                    '</div>', unsafe_allow_html=True)
        if cs.empty:
            st.markdown('<div class="vazio">✓ Nenhuma exceção neste lote: todos os títulos passaram nas regras.</div>',
                        unsafe_allow_html=True)
        for c in ordem.itertuples():
            regra = c.caso_id.split(":", 1)[1]
            classe, selo = SELO.get(regra, ("erro", regra))
            tits = [t.strip() for t in c.titulos.split(",")]
            lista = ", ".join(tits[:5]) + (f" e mais {len(tits) - 5}" if len(tits) > 5 else "")
            motivo, _, evid = c.motivo.partition(" Evidência:")
            quem = PESSOAS.get(c.acionar, "Agente, dentro da alçada do analista")
            efe = c.efetiva
            estado = ""
            if efe:
                efeito = "volta ao lote" if dh.volta_ao_lote(c.acao, efe) else "fica fora do lote"
                verbo = "Liberado" if efe["decisao"] == "liberar" else "Ação aprovada"
                estado = f'<div class="resolvido">✓ {verbo} por {e(efe["quem"])} ({e(efe["quando"])}) · {efeito}</div>'
            evid_html = f'<div class="evid"><b>Evidência na caixa de e-mail:</b> {e(evid.strip())}</div>' if evid else ""
            st.markdown(f"""<div class="caso"><div><span class="selo {classe}">{selo}</span>
              <div class="forn">{e(c.fornecedor)}</div><div class="tit">{c.qtd} título(s): {e(lista)}</div>
              <div class="mot">{e(motivo)}</div>{evid_html}</div>
              <div class="din"><div class="v">{brl(c.valor)}</div><div class="q">{c.qtd} título(s)</div></div>
              <div class="acao"><b>Ação proposta:</b> {ACAO_TEXTO.get(c.acao, c.acao)} · <b>Quem decide:</b> {e(quem)}
              {estado}</div></div>""", unsafe_allow_html=True)
            b1, b2, _ = st.columns([1.25, 1.1, 3])
            if not efe:
                if b1.button(ACAO_BOTAO.get(c.acao, "Aprovar ação"), key=f"a-{c.caso_id}", type="primary",
                             use_container_width=True):
                    dh.registrar(c.caso_id, "aprovar", quem.split(" (")[0])
                    st.rerun()
                if b2.button("Liberar mesmo assim", key=f"l-{c.caso_id}", use_container_width=True,
                             help="Falso alarme: o título volta ao lote como está"):
                    dh.registrar(c.caso_id, "liberar", quem.split(" (")[0])
                    st.rerun()
            elif c.caso_id in decisoes and b1.button("Desfazer decisão", key=f"d-{c.caso_id}", use_container_width=True):
                dh.desfazer(c.caso_id)
                st.rerun()
    if len(al_vis):
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown('<h3 style="font-size:1.02rem;font-weight:600;margin:0">Alertas da caixa de e-mail</h3>'
                        '<div style="color:#5b6272;font-size:.82rem;margin:2px 0 4px">Não seguram nenhum título; '
                        'avisam quem precisa agir.</div>', unsafe_allow_html=True)
            for a in al_vis.itertuples():
                chave = f"alerta:{a.alerta}:{a.fornecedor}"
                nome = "⚠ Phishing na caixa" if a.alerta == "phishing_na_caixa" else "⚠ Tentativa de instruir o agente"
                ok = chave in decisoes
                st.markdown(f"""<div class="caso"><div><span class="selo fraude">{nome}</span>
                  <div class="forn">{e(a.fornecedor if a.fornecedor != '—' else 'Remetentes fora do cadastro')}</div>
                  <div class="mot">{e(a.motivo)}</div></div><div class="din"><div class="q">E-mails</div>
                  <div class="tit">{e(a.emails)}</div></div>
                  <div class="acao"><b>Quem é avisado:</b> {e(PESSOAS.get(a.acionar, a.acionar))}
                  {'<div class="resolvido">✓ Ciente</div>' if ok else ''}</div></div>""", unsafe_allow_html=True)
                if not ok and st.button("Marcar como ciente", key=f"c-{chave}"):
                    dh.registrar(chave, "ciente", PESSOAS.get(a.acionar, a.acionar).split(" (")[0])
                    st.rerun()

# ================= LOTE FINAL
elif vista == "Lote final":
    acao_tit = {t.strip(): (c.acao, c.efetiva) for c in cs[cs.volta].itertuples() for t in c.titulos.split(",")}
    linhas, total = [], 0.0
    for t in seguem.sort_values("valor", ascending=False).itertuples():
        acao, efe = acao_tit.get(t.titulo_id, (None, None))
        valor, destino, nota = t.valor, t.destino_pagamento, ""
        if efe and efe["decisao"] == "aprovar" and acao == "reverter_alteracao_cadastro" and t.destino_anterior:
            destino, nota = t.destino_anterior, '<span class="selo ok">↺ Conta revertida</span>'
        elif (efe and efe["decisao"] == "aprovar" and acao == "corrigir_lancamento" and pd.notna(t.valor_duplicata)
              and "valor_diferente_duplicata" in t.regras_violadas):
            valor, nota = float(t.valor_duplicata), '<span class="selo ok">✓ Valor corrigido</span>'
        elif efe:
            nota = '<span class="selo neutro">Liberado por decisão</span>'
        total += valor
        linhas.append({"titulo_id": t.titulo_id, "forn": t.razao_social, "venc": pd.to_datetime(t.vencimento).strftime("%d/%m"),
                       "destino": destino, "aprov": APROV.get(t.aprovacao, ""), "obs_html": nota,
                       "valor": brl(valor), "lote": t.lote_remessa, "_v": valor})
    st.markdown(f"""<div class="barra-total"><div><div class="r">Total a enviar ao banco</div>
      <div class="v">{brl(total)}</div></div><div class="r">{len(linhas)} títulos ·
      {sum(1 for l in linhas if l['aprov'] == 'Aprovador')} com aprovador · {sum(1 for l in linhas if l['aprov'] == 'Diretora')}
      com a diretora</div></div>""", unsafe_allow_html=True)
    if len(pendentes):
        st.warning(f"{len(pendentes)} caso(s) sem decisão ficam fora deste lote até alguém decidir.")
    with st.container(border=True):
        st.markdown(tabela(linhas, [("titulo_id", "Título", ""), ("forn", "Fornecedor", ""), ("venc", "Vence", "num"),
                                    ("destino", "Destino do pagamento", ""), ("aprov", "Aprovação", ""),
                                    ("obs_html", "Situação", ""), ("valor", "Valor", "num forte")]),
                    unsafe_allow_html=True)
        csv = pd.DataFrame([{k: v for k, v in l.items() if not k.endswith("_html") and k != "_v"} for l in linhas])
        st.download_button("Baixar planilha do lote (CSV)", csv.to_csv(index=False).encode("utf-8-sig"),
                           file_name=f"lote_final_{escolha}.csv", mime="text/csv")
    st.caption("Dados fictícios do evento: correções aprovadas ainda precisariam ser lançadas no ERP.")

# ================= CAIXA DE E-MAIL
elif vista == "Caixa de e-mail":
    if caixa.empty:
        st.markdown('<div class="painel vazio">Caixa de e-mail não carregada.</div>', unsafe_allow_html=True)
    else:
        sus = caixa[caixa.suspeita != ""]
        st.markdown('<div class="kpis">'
                    + kpi("banco", "#2659a5", "E-mails lidos pela IA", str(len(caixa)), "01/10 a 02/11")
                    + kpi("escudo", "#e5273c", "Suspeitos (regra do código)", str(len(sus)), "domínio ou remetente")
                    + kpi("alerta", "#f8ae13", "Em revisão humana", str(int(caixa.revisar_ia.sum())), "confiança abaixo de 0,7")
                    + kpi("pessoa", "#3dbfef", "Custo da 1ª leitura", "US$ 0,0059", "depois fica em cache")
                    + "</div>", unsafe_allow_html=True)
        filtro = st.segmented_control("Mostrar", ["Suspeitos", "Em revisão", "Todos"], default="Suspeitos")
        base = sus if filtro in (None, "Suspeitos") else (caixa[caixa.revisar_ia] if filtro == "Em revisão" else caixa)
        rot = {"dominio_parecido": "Domínio parecido com o do cadastro", "remetente_fora_do_cadastro": "Fora do cadastro",
               "remetente_desconhecido": "Remetente desconhecido", "tentativa_de_instruir_agente": "Tenta dar ordem ao agente"}
        linhas = [{"data": r.data_hora[:16].replace("2026-", "").replace("-", "/"), "rem": r.remetente, "ass": r.assunto,
                   "tipo": r.tipo or "falha de leitura",
                   "troca": {True: "Sim", False: "Não"}.get(r.pede_troca_bancaria, "—"),
                   "ordem": {True: "Sim", False: "Não"}.get(r.tenta_instruir_agente, "—"),
                   "conf": f"{r.confianca:.2f}" if pd.notna(r.confianca) else "—",
                   "sus_html": f'<span class="selo fraude">{e(rot[r.suspeita])}</span>' if r.suspeita else ""}
                  for r in base.itertuples()]
        with st.container(border=True):
            st.markdown(tabela(linhas, [("data", "Data", ""), ("rem", "Remetente", ""), ("ass", "Assunto", ""),
                                        ("tipo", "Tipo (IA)", ""), ("troca", "Pede troca de conta (IA)", ""),
                                        ("ordem", "Ordem ao agente (IA)", ""), ("conf", "Confiança", "num"),
                                        ("sus_html", "Suspeita (código)", "")], altura=520), unsafe_allow_html=True)
        st.caption("A IA só lê o texto. Quem decide se um e-mail é suspeito é o código (endereço e domínio do cadastro). "
                   "O texto de um e-mail nunca libera um pagamento.")

# ================= PLANILHA MÃE
elif vista == "Planilha mãe":
    f1, f2, f3 = st.columns([2, 1, 1])
    busca = f1.text_input("Buscar fornecedor, título ou NF", placeholder="ex.: Embalarte, TP432130, 20329")
    so = f2.selectbox("Decisão", ["Todas", "Seguem", "Fora do lote"])
    forma = f3.selectbox("Forma de pagamento", ["Todas", "ted", "boleto", "pix"])
    mae = vis.copy()
    if busca:
        b = busca.lower()
        mae = mae[mae.razao_social.str.lower().str.contains(b, regex=False) | mae.titulo_id.str.lower().str.contains(b, regex=False)
                  | mae.nf_normalizada.astype(str).str.contains(b, regex=False)]
    if so != "Todas":
        mae = mae[(mae.decisao == "liberar") if so == "Seguem" else (mae.decisao != "liberar")]
    if forma != "Todas":
        mae = mae[mae.forma_pagamento == forma]
    with st.container(border=True):
        st.dataframe(pd.DataFrame({
            "Título": mae.titulo_id, "Fornecedor": mae.razao_social, "NF digitada": mae.numero_nf_digitado,
            "Parcela": mae.parcela, "Valor": mae.valor, "Duplicata": mae.valor_duplicata,
            "Vence": pd.to_datetime(mae.vencimento).dt.strftime("%d/%m"), "Forma": mae.forma_pagamento,
            "Decisão": mae.decisao.map({"liberar": "✓ Segue", "retirar": "✕ Fora", "acionar": "? Acionar"}),
            "Regras": mae.regras_violadas, "Aprovação": mae.aprovacao.map(APROV), "Lote": mae.lote_remessa,
        }), hide_index=True, use_container_width=True, height=520, column_config={
            "Fornecedor": st.column_config.TextColumn(width="large"),
            "Regras": st.column_config.TextColumn(width="large"),
            "Valor": st.column_config.NumberColumn(format="R$ %.2f", width="small"),
            "Duplicata": st.column_config.NumberColumn(format="R$ %.2f", width="small"),
            "Título": st.column_config.TextColumn(width="small"), "Parcela": st.column_config.TextColumn(width="small"),
            "Vence": st.column_config.TextColumn(width="small"), "Forma": st.column_config.TextColumn(width="small")})
        st.caption(f"{len(mae)} de {len(vis)} títulos · ERP, Compras, portal NF-e, DDA e caixa de e-mail cruzados")

# ================= RESUMO DA FILA
else:
    tudo = casos(df)
    nomes = {k: v[1] for k, v in SELO.items()}
    por_regra = (tudo.assign(r=tudo.caso_id.str.split(":").str[1]).groupby("r")
                 .agg(valor=("valor", "sum"), qtd=("qtd", "sum")).sort_values("valor", ascending=False))
    l1, l2 = st.columns(2)
    with l1:
        with st.container(border=True):
            st.markdown('<h3 style="font-size:1.02rem;font-weight:600;margin:0">Dinheiro protegido por tipo de problema</h3>'
                        '<div class="nota" style="color:#5b6272;font-size:.82rem;margin-bottom:10px">Fila inteira, 03/11 a 13/11</div>',
                        unsafe_allow_html=True)
            st.markdown(tabela([{"tipo_html": f'<span class="selo {SELO.get(r, ("erro", r))[0]}">{e(nomes.get(r, r))}</span>',
                                 "qtd": int(row.qtd), "valor": brl(row.valor)} for r, row in por_regra.iterrows()],
                               [("tipo_html", "Problema", ""), ("qtd", "Títulos", "num"), ("valor", "Valor", "num forte")],
                               altura=420), unsafe_allow_html=True)
    with l2:
        with st.container(border=True):
            st.markdown('<h3 style="font-size:1.02rem;font-weight:600;margin:0">Próximos fechamentos</h3>'
                        '<div class="nota" style="color:#5b6272;font-size:.82rem;margin-bottom:10px">O que vai ao banco em cada lote</div>',
                        unsafe_allow_html=True)
            linhas = []
            for l in lotes:
                g = df[df.lote_remessa == l]
                r = g[g.decisao != "liberar"]
                rl = info.loc[l]
                curto = (f"{rl.banco_pagador.replace('Banco ', '')} · "
                         f"{pd.to_datetime(rl.data_prevista).strftime('%d/%m')} · {rl.horario_fechamento}")
                linhas.append({"lote": curto, "tit": len(g), "ret_html":
                               f'<span class="selo fraude">{len(r)} retidos</span>' if len(r) else '<span class="selo ok">✓ limpo</span>',
                               "valor": brl(g.valor.sum())})
            st.markdown(tabela(linhas, [("lote", "Lote", ""), ("tit", "Títulos", "num"), ("ret_html", "Situação", ""),
                                        ("valor", "Valor na fila", "num forte")], altura=420), unsafe_allow_html=True)
