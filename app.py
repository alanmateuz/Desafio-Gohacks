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

# ---------- Identidade Gogroup (brandbook): azul protagonista, Poppins, pílulas e cantos arredondados
st.markdown("""
<style>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;800&display=swap");
:root{
  --azul:#2659a5; --azul-escuro:#1d4683; --azul-claro:#3dbfef; --azul-bg:#eef3fa;
  --limao:#d7d900; --rosa:#e61782; --vermelho:#e5273c; --amarelo:#f8ae13;
  --texto:#1f2430; --texto-2:#5b6272; --borda:#e3e7ee; --fundo:#ffffff; --fundo-2:#f6f7f9;
}
html, body, .stApp, .stApp *:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded) {
  font-family:'Poppins', sans-serif !important; }
.stApp{ background:var(--fundo); color:var(--texto); }
#MainMenu, footer, header[data-testid="stHeader"]{ visibility:hidden; height:0; }
.block-container{ padding-top:1.6rem; max-width:1240px; }
h1,h2,h3{ font-family:'Poppins',sans-serif; color:var(--texto); }
.topo{ display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap;
       padding-bottom:18px; border-bottom:1px solid var(--borda); margin-bottom:22px; }
.topo-esq{ display:flex; align-items:center; gap:18px; }
.pilula{ display:inline-block; background:var(--azul); color:#fff; font-weight:600; font-size:.72rem;
         letter-spacing:.08em; text-transform:uppercase; padding:6px 14px; border-radius:999px; }
.pilula.clara{ background:var(--azul-bg); color:var(--azul); }
.meta{ color:var(--texto-2); font-size:.82rem; text-align:right; line-height:1.5; }
.status-ia{ display:inline-flex; align-items:center; gap:6px; font-weight:600; }
.ponto{ width:8px; height:8px; border-radius:50%; display:inline-block; }
.heroi{ display:grid; grid-template-columns: 1.3fr 1fr; gap:18px; margin-bottom:18px; }
@media (max-width: 900px){ .heroi{ grid-template-columns:1fr; } }
.bloco-azul{ background:var(--azul); color:#fff; border-radius:28px; padding:26px 28px; }
.bloco-azul h2{ color:#fff; font-weight:800; font-size:1.7rem; margin:10px 0 6px; line-height:1.2; }
.bloco-azul p{ color:#dfe8f6; margin:0; font-size:.92rem; }
.bloco-limao{ background:var(--limao); color:#2b2c00; border-radius:28px; padding:24px 26px; }
.bloco-limao .rotulo{ font-weight:600; font-size:.78rem; letter-spacing:.06em; text-transform:uppercase; }
.bloco-limao .grande{ font-weight:800; font-size:2.1rem; line-height:1.1; margin:6px 0 2px; }
.bloco-limao p{ margin:0; font-size:.88rem; }
.kpis{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin:6px 0 26px; }
@media (max-width: 900px){ .kpis{ grid-template-columns:repeat(2,1fr); } }
.kpi{ border:1px solid var(--borda); border-radius:20px; padding:16px 18px; background:var(--fundo); }
.kpi .rotulo{ color:var(--texto-2); font-size:.8rem; font-weight:500; }
.kpi .valor{ font-weight:800; font-size:1.65rem; color:var(--texto); font-variant-numeric:tabular-nums; }
.kpi .sub{ color:var(--texto-2); font-size:.8rem; font-variant-numeric:tabular-nums; }
.kpi.destaque{ border-color:var(--azul); }
.kpi.destaque .valor{ color:var(--azul); }
.stTabs [data-baseweb="tab-list"]{ gap:8px; border-bottom:none; }
.stTabs [data-baseweb="tab"]{ background:var(--fundo-2); border-radius:999px; padding:8px 18px; height:auto;
       font-weight:600; color:var(--texto-2); }
.stTabs [aria-selected="true"]{ background:var(--azul) !important; color:#fff !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"]{ display:none; }
.caso{ border:1px solid var(--borda); border-radius:22px; padding:18px 22px; margin:12px 0 6px; background:#fff; }
.caso.feito{ background:var(--fundo-2); }
.caso-topo{ display:flex; justify-content:space-between; align-items:flex-start; gap:12px; flex-wrap:wrap; }
.caso h4{ margin:6px 0 2px; font-weight:600; font-size:1.05rem; color:var(--texto); }
.caso .valor{ font-weight:800; font-size:1.25rem; color:var(--texto); font-variant-numeric:tabular-nums; }
.caso .motivo{ margin:10px 0 8px; font-size:.92rem; color:var(--texto); }
.caso .linha{ color:var(--texto-2); font-size:.82rem; }
.evidencia{ border-left:4px solid var(--rosa); background:#fdf0f6; padding:8px 12px; border-radius:0;
            margin:8px 0; font-size:.86rem; color:#5a0f35; }
.selo{ display:inline-flex; align-items:center; gap:6px; font-weight:600; font-size:.74rem; padding:4px 10px;
       border-radius:999px; letter-spacing:.02em; }
.selo.fraude{ background:#fde9ec; color:#a3162a; }
.selo.erro{ background:#fff3dc; color:#7a4d00; }
.selo.dup{ background:var(--azul-bg); color:var(--azul-escuro); }
.selo.ok{ background:#e9f7fd; color:#0b5f80; }
.selo.feito{ background:#eceef2; color:#3c4250; }
.stButton button{ border-radius:999px; font-weight:600; padding:.45rem 1.1rem; border:1px solid var(--borda); }
.stButton button[kind="primary"]{ background:var(--rosa); border-color:var(--rosa); color:#fff; }
.stButton button[kind="primary"]:hover{ background:#c4116d; border-color:#c4116d; }
.stButton button:focus-visible{ outline:3px solid var(--azul-claro); outline-offset:2px; }
.stDownloadButton button{ border-radius:999px; font-weight:600; background:var(--azul); color:#fff; border:none; }
.vazio{ text-align:center; padding:34px; color:var(--texto-2); border:1px dashed var(--borda); border-radius:22px; }
.secao{ font-weight:600; color:var(--texto); margin:8px 0 2px; font-size:1.05rem; }
.nota{ color:var(--texto-2); font-size:.84rem; margin-bottom:6px; }
</style>
""", unsafe_allow_html=True)


def brl(v: float) -> str:
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


PESSOAS = {"PS01": "Renata Paiva · coord. contas a pagar", "PS03": "Helena Duarte · diretora financeira",
           "PS08": "Lívia Campos · jurídico", "aprovador": "Aprovador (Cláudia ou Renata)", "": ""}
ACAO_BOTAO = {
    "reverter_alteracao_cadastro": "Aprovar reversão da conta",
    "cancelar_titulo": "Aprovar cancelamento",
    "corrigir_lancamento": "Aprovar correção",
    "contatar_fornecedor": "Confirmar suspeita e bloquear",
    "solicitar_aprovacao": "Aprovar valor somado",
    "retirar_do_lote": "Manter fora do lote",
}
ACAO_TEXTO = {
    "reverter_alteracao_cadastro": "voltar para a conta anterior e pagar no prazo (aprovação dupla)",
    "cancelar_titulo": "cancelar o título duplicado",
    "corrigir_lancamento": "corrigir o lançamento e pagar o valor certo",
    "contatar_fornecedor": "confirmar o boleto com o fornecedor pelo canal do cadastro",
    "solicitar_aprovacao": "pedir aprovação do valor somado",
    "retirar_do_lote": "tirar do lote até alguém conferir",
}
SELO = {
    "troca_bancaria_sem_confirmacao": ("fraude", "⚠ Suspeita de fraude · conta trocada"),
    "boleto_beneficiario_diferente": ("fraude", "⚠ Suspeita de fraude · boleto"),
    "duplicidade": ("dup", "⧉ Pagamento em dobro"),
    "valor_diferente_duplicata": ("erro", "≠ Valor diferente da nota"),
    "nf_de_outro_fornecedor": ("erro", "↔ Fornecedor errado"),
    "sem_nf_no_portal": ("erro", "? NF não encontrada"),
    "fracionamento_alcada": ("erro", "÷ Valor dividido"),
}


@st.cache_data(show_spinner="Conferindo a fila e lendo a caixa de e-mail…")
def carregar():
    df = conferir(montar_planilha_mae())
    caixa = df.attrs.get("caixa", pd.DataFrame())
    al = alertas_caixa(df)
    df.attrs = {}
    return df, caixa, al


df, caixa, alertas = carregar()
decisoes = dh.carregar()

# ---------- Topo
ia_ativa = bool(TOKEN)
cor_ia, txt_ia = ("#1d9e75", "IA ativa · Jev (AI Proxy)") if ia_ativa else ("#f8ae13", "IA em modo simulado")
c_logo, c_meta = st.columns([1, 1])
with c_logo:
    st.image(str(RAIZ / "assets/logo-gogroup.png"), width=150)
with c_meta:
    st.markdown(f"""<div class="meta"><span class="pilula">Guardião do lote</span><br>
      Contas a pagar · referência 02/11/2026 08:00<br>
      <span class="status-ia"><span class="ponto" style="background:{cor_ia}"></span>{txt_ia}</span></div>""",
                unsafe_allow_html=True)
st.markdown('<div style="border-bottom:1px solid var(--borda);margin:4px 0 20px"></div>', unsafe_allow_html=True)

# ---------- Lote
lotes = (df.drop_duplicates("lote_remessa").sort_values(["data_prevista", "horario_fechamento"]).lote_remessa.tolist())
rotulo_lote = {l: f"{df[df.lote_remessa == l].banco_pagador.iloc[0]} · "
                  f"{pd.to_datetime(df[df.lote_remessa == l].data_prevista.iloc[0]).strftime('%d/%m')} · "
                  f"fecha às {df[df.lote_remessa == l].horario_fechamento.iloc[0]}" for l in lotes}
opcoes = ["Fila inteira (03/11 a 13/11)"] + lotes
escolha = st.selectbox("Lote de remessa", opcoes, index=1,
                       format_func=lambda o: o if o.startswith("Fila") else rotulo_lote[o])
vis = df if escolha.startswith("Fila") else df[df.lote_remessa == escolha]
cs = casos(vis)


def decisao_efetiva(c) -> dict | None:
    if c.caso_id in decisoes:
        return decisoes[c.caso_id]
    if not c.acionar:  # dentro da alçada do analista: o agente resolve sozinho
        return {"decisao": "aprovar", "quem": "Agente (alçada do analista)", "quando": "automático"}
    return None


cs["efetiva"] = [decisao_efetiva(c) for c in cs.itertuples()]
cs["volta"] = [dh.volta_ao_lote(c.acao, c.efetiva) for c in cs.itertuples()]
voltam = set(t.strip() for c in cs[cs.volta].itertuples() for t in c.titulos.split(","))
seguem = vis[(vis.decisao == "liberar") | vis.titulo_id.isin(voltam)]
retidos = vis[(vis.decisao != "liberar") & ~vis.titulo_id.isin(voltam)]
pendentes = cs[cs.efetiva.isna()]
al_vis = alertas if escolha.startswith("Fila") else alertas.iloc[0:0]
alertas_pend = [a for a in al_vis.itertuples() if f"alerta:{a.alerta}:{a.fornecedor}" not in decisoes] \
    if len(al_vis) else []
indevido = retidos.valor.sum()

# ---------- Herói (color blocking do brandbook)
titulo_lote = "Fila inteira" if escolha.startswith("Fila") else rotulo_lote[escolha]
st.markdown(f"""<div class="heroi">
  <div class="bloco-azul"><span class="pilula clara">Próximo envio</span>
    <h2>{html.escape(titulo_lote)}</h2>
    <p>{len(vis)} títulos conferidos antes do envio ao banco · {brl(vis.valor.sum())}</p></div>
  <div class="bloco-limao"><div class="rotulo">Precisa da sua decisão</div>
    <div class="grande">{len(pendentes) + len(alertas_pend)} caso(s)</div>
    <p>{"Nada pendente: o lote pode ser assinado." if not len(pendentes) + len(alertas_pend)
        else "Veja a aba Exceções antes de assinar o lote."}</p></div>
</div>""", unsafe_allow_html=True)

n_pessoas = (cs.acionar != "").sum() + len(al_vis)
st.markdown(f"""<div class="kpis">
  <div class="kpi"><div class="rotulo">Seguem para o banco</div><div class="valor">{len(seguem)}</div>
    <div class="sub">{brl(seguem.valor.sum())}</div></div>
  <div class="kpi destaque"><div class="rotulo">Seguros fora do lote</div><div class="valor">{len(retidos)}</div>
    <div class="sub">{brl(indevido)}</div></div>
  <div class="kpi"><div class="rotulo">Casos encontrados</div><div class="valor">{len(cs)}</div>
    <div class="sub">{(cs.acionar == '').sum()} resolvidos pelo agente</div></div>
  <div class="kpi"><div class="rotulo">Pessoas acionadas</div><div class="valor">{n_pessoas}</div>
    <div class="sub">1 aviso por caso, não por título</div></div>
</div>""", unsafe_allow_html=True)

aba_exc, aba_caixa, aba_mae, aba_lote = st.tabs(
    [f"Exceções ({len(pendentes) + len(alertas_pend)})", "Caixa de e-mail", "Planilha mãe", "Lote final"])

# ---------- Exceções
with aba_exc:
    if cs.empty and not len(al_vis):
        st.markdown('<div class="vazio">✓ Nenhuma exceção neste lote. Todos os títulos passaram nas regras.</div>',
                    unsafe_allow_html=True)
    ordem = cs.assign(pend=cs.efetiva.isna()).sort_values(["pend", "valor"], ascending=[False, False])
    for c in ordem.itertuples():
        regra_principal = c.caso_id.split(":", 1)[1]
        classe, selo = SELO.get(regra_principal, ("erro", regra_principal))
        efe = c.efetiva
        feito = efe is not None
        titulos = [t.strip() for t in c.titulos.split(",")]
        evid = ""
        for linha in vis[vis.titulo_id == titulos[0]].motivo:
            if "o pedido veio de" in linha:
                trecho = linha.split("Evidência:", 1)[-1].strip()
                evid = f'<div class="evidencia"><b>Evidência da caixa de e-mail</b><br>{html.escape(trecho)}</div>'
        motivo = c.motivo.split(" Evidência:")[0]
        quem = PESSOAS.get(c.acionar, c.acionar) or "Agente, dentro da alçada do analista"
        status = ""
        if feito:
            efeito = ("volta ao lote" if dh.volta_ao_lote(c.acao, efe) else "fica fora do lote")
            verbo = "Liberado" if efe["decisao"] == "liberar" else "Ação aprovada"
            status = (f'<span class="selo feito">✓ {verbo} por {html.escape(efe["quem"])} · '
                      f'{html.escape(efe["quando"])} · {efeito}</span>')
        lista = ", ".join(titulos[:6]) + (f" e mais {len(titulos) - 6}" if len(titulos) > 6 else "")
        st.markdown(f"""<div class="caso {'feito' if feito else ''}">
          <div class="caso-topo"><div><span class="selo {classe}">{selo}</span>
            <h4>{html.escape(c.fornecedor)}</h4>
            <div class="linha">{c.qtd} título(s): {html.escape(lista)}</div></div>
            <div class="valor">{brl(c.valor)}</div></div>
          <div class="motivo">{html.escape(motivo)}</div>{evid}
          <div class="linha"><b>Ação proposta:</b> {ACAO_TEXTO.get(c.acao, c.acao)} · <b>Quem decide:</b> {html.escape(quem)}</div>
          <div style="margin-top:8px">{status}</div></div>""", unsafe_allow_html=True)
        b1, b2, _ = st.columns([1.4, 1.2, 3])
        if not feito:
            if b1.button(ACAO_BOTAO.get(c.acao, "Aprovar ação"), key=f"a-{c.caso_id}", type="primary"):
                dh.registrar(c.caso_id, "aprovar", quem.split(" ·")[0])
                st.rerun()
            if b2.button("Liberar mesmo assim", key=f"l-{c.caso_id}",
                         help="Falso alarme: o título volta ao lote como está"):
                dh.registrar(c.caso_id, "liberar", quem.split(" ·")[0])
                st.rerun()
        elif c.caso_id in decisoes:
            if b1.button("Desfazer decisão", key=f"d-{c.caso_id}"):
                dh.desfazer(c.caso_id)
                st.rerun()

    if len(al_vis):
        st.markdown('<div class="secao" style="margin-top:22px">Alertas da caixa de e-mail</div>'
                    '<div class="nota">Não seguram nenhum título. Avisam quem precisa agir.</div>',
                    unsafe_allow_html=True)
        for a in al_vis.itertuples():
            chave = f"alerta:{a.alerta}:{a.fornecedor}"
            nome = "⚠ Phishing na caixa" if a.alerta == "phishing_na_caixa" else "⚠ Tentativa de instruir o agente"
            ok = chave in decisoes
            st.markdown(f"""<div class="caso {'feito' if ok else ''}"><span class="selo fraude">{nome}</span>
              <h4>{html.escape(a.fornecedor if a.fornecedor != '—' else 'Remetentes fora do cadastro')}</h4>
              <div class="motivo">{html.escape(a.motivo)}</div>
              <div class="linha"><b>E-mails:</b> {html.escape(a.emails)} · <b>Quem é avisado:</b> {PESSOAS.get(a.acionar, a.acionar)}</div>
              {'<div style="margin-top:8px"><span class="selo feito">✓ Ciente</span></div>' if ok else ''}</div>""",
                        unsafe_allow_html=True)
            if not ok and st.button("Marcar como ciente", key=f"c-{chave}"):
                dh.registrar(chave, "ciente", PESSOAS.get(a.acionar, a.acionar).split(" ·")[0])
                st.rerun()

# ---------- Caixa de e-mail
with aba_caixa:
    if caixa.empty:
        st.markdown('<div class="vazio">Caixa de e-mail não carregada.</div>', unsafe_allow_html=True)
    else:
        suspeitos = caixa[caixa.suspeita != ""]
        revisar = caixa[caixa.revisar_ia & (caixa.suspeita == "")]
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("E-mails lidos pela IA", len(caixa))
        k2.metric("Suspeitos (regra do código)", len(suspeitos))
        k3.metric("Em revisão (confiança < 0,7)", int(caixa.revisar_ia.sum()))
        k4.metric("Custo desta execução", f"US$ {caixa.custo_usd.sum():.4f}",
                  help="Leituras já feitas ficam em cache e não custam de novo. "
                       "A 1ª leitura dos 246 e-mails custou US$ 0,0059 (projeto/decisoes.md).")
        filtro = st.radio("Mostrar", ["Suspeitos", "Em revisão", "Todos"], horizontal=True)
        base = suspeitos if filtro == "Suspeitos" else (caixa[caixa.revisar_ia] if filtro == "Em revisão" else caixa)
        rot = {"dominio_parecido": "Domínio parecido com o do cadastro",
               "remetente_fora_do_cadastro": "Remetente fora do cadastro",
               "remetente_desconhecido": "Remetente desconhecido",
               "tentativa_de_instruir_agente": "Tenta dar ordem ao agente", "": "—"}
        st.dataframe(pd.DataFrame({
            "Data": base.data_hora.str[:16], "Remetente": base.remetente, "Assunto": base.assunto,
            "Tipo (IA)": base.tipo.replace({"": "falha de leitura"}),
            "Pede troca de conta (IA)": base.pede_troca_bancaria.map({True: "Sim", False: "Não"}).fillna("—"),
            "Ordem ao agente (IA)": base.tenta_instruir_agente.map({True: "Sim", False: "Não"}).fillna("—"),
            "Confiança": base.confianca, "Suspeita (código)": base.suspeita.map(rot),
        }), hide_index=True, use_container_width=True,
            column_config={"Confiança": st.column_config.ProgressColumn(min_value=0, max_value=1, format="%.2f")})
        st.markdown('<div class="nota">A IA só lê o texto. Quem decide se um e-mail é suspeito é o código '
                    '(endereço e domínio do cadastro); o texto de um e-mail nunca libera um pagamento.</div>',
                    unsafe_allow_html=True)

# ---------- Planilha mãe
with aba_mae:
    st.markdown('<div class="nota">Uma linha por título da fila, com ERP, Compras, portal NF-e, DDA e '
                'caixa de e-mail cruzados.</div>', unsafe_allow_html=True)
    f1, f2 = st.columns([2, 1])
    busca = f1.text_input("Buscar fornecedor, título ou NF", placeholder="ex.: Embalarte, TP432130, 20329")
    so = f2.selectbox("Decisão", ["Todas", "Seguem", "Fora do lote"])
    mae = vis.copy()
    if busca:
        b = busca.lower()
        mae = mae[mae.razao_social.str.lower().str.contains(b, regex=False)
                  | mae.titulo_id.str.lower().str.contains(b, regex=False)
                  | mae.nf_normalizada.astype(str).str.contains(b, regex=False)]
    if so == "Seguem":
        mae = mae[mae.decisao == "liberar"]
    elif so == "Fora do lote":
        mae = mae[mae.decisao != "liberar"]
    st.dataframe(pd.DataFrame({
        "Lote": mae.lote_remessa, "Título": mae.titulo_id, "Fornecedor": mae.razao_social,
        "NF digitada": mae.numero_nf_digitado, "NF normalizada": mae.nf_normalizada, "Parcela": mae.parcela,
        "Valor": mae.valor, "Valor da duplicata": mae.valor_duplicata, "Vencimento": mae.vencimento,
        "Forma": mae.forma_pagamento, "Destino": mae.destino_pagamento,
        "Decisão": mae.decisao.map({"liberar": "✓ Segue", "retirar": "✕ Fora do lote", "acionar": "? Acionar"}),
        "Regras": mae.regras_violadas, "Aprovação no lote": mae.aprovacao.map(
            {"PS03": "Diretora (PS03)", "aprovador": "Aprovador", "": "Analista"}),
    }), hide_index=True, use_container_width=True, height=460,
        column_config={"Valor": st.column_config.NumberColumn(format="R$ %.2f"),
                       "Valor da duplicata": st.column_config.NumberColumn(format="R$ %.2f")})
    st.caption(f"{len(mae)} de {len(vis)} títulos")

# ---------- Lote final
with aba_lote:
    aprov = seguem.aprovacao.value_counts()
    st.markdown(f"""<div class="kpis">
      <div class="kpi destaque"><div class="rotulo">Vai ao banco</div><div class="valor">{len(seguem)}</div>
        <div class="sub">{brl(seguem.valor.sum())}</div></div>
      <div class="kpi"><div class="rotulo">Voltaram ao lote após decisão</div>
        <div class="valor">{seguem.titulo_id.isin(voltam).sum()}</div><div class="sub">aprovados por uma pessoa ou pelo agente</div></div>
      <div class="kpi"><div class="rotulo">Aprovação do aprovador</div><div class="valor">{aprov.get('aprovador', 0)}</div>
        <div class="sub">acima de R$ 5 mil</div></div>
      <div class="kpi"><div class="rotulo">Aprovação da diretora</div><div class="valor">{aprov.get('PS03', 0)}</div>
        <div class="sub">acima de R$ 50 mil</div></div></div>""", unsafe_allow_html=True)
    if len(pendentes):
        st.warning(f"{len(pendentes)} caso(s) ainda sem decisão ficam fora deste lote até alguém decidir.")
    # Aplica o efeito da decisão: reversão → conta anterior; correção → valor da duplicata
    acao_por_titulo = {t.strip(): (c.acao, c.efetiva) for c in cs[cs.volta].itertuples() for t in c.titulos.split(",")}
    ajustado = seguem.copy()
    obs = []
    for i, t in ajustado.iterrows():
        acao, efe = acao_por_titulo.get(t.titulo_id, (None, None))
        nota = ""
        if efe and efe["decisao"] == "aprovar" and acao == "reverter_alteracao_cadastro" and t.destino_anterior:
            ajustado.at[i, "destino_pagamento"] = t.destino_anterior
            nota = f"conta revertida para a anterior (era {t.destino_pagamento})"
        elif (efe and efe["decisao"] == "aprovar" and acao == "corrigir_lancamento"
              and pd.notna(t.valor_duplicata) and "valor_diferente_duplicata" in t.regras_violadas):
            ajustado.at[i, "valor"] = float(t.valor_duplicata)
            nota = f"valor corrigido para o da duplicata (era {brl(t.valor)})"
        elif efe:
            nota = "liberado por decisão"
        obs.append(nota)
    final = pd.DataFrame({
        "Lote": ajustado.lote_remessa, "Título": ajustado.titulo_id, "Fornecedor": ajustado.razao_social,
        "Valor": ajustado.valor, "Vencimento": ajustado.vencimento, "Destino": ajustado.destino_pagamento,
        "Aprovação": ajustado.aprovacao.map({"PS03": "Diretora (PS03)", "aprovador": "Aprovador", "": "Analista"}),
        "Observação": obs,
    }).sort_values("Observação", ascending=False)
    st.dataframe(final, hide_index=True, use_container_width=True, height=420,
                 column_config={"Valor": st.column_config.NumberColumn(format="R$ %.2f")})
    st.markdown(f'<div class="secao">Total a enviar ao banco: {brl(final.Valor.sum())}</div>',
                unsafe_allow_html=True)
    st.download_button("Baixar planilha do lote (CSV)", final.to_csv(index=False).encode("utf-8-sig"),
                       file_name=f"lote_final_{'fila' if escolha.startswith('Fila') else escolha}.csv",
                       mime="text/csv")
    st.markdown('<div class="nota">Correções de valor e de conta aprovadas ainda precisam ser feitas no ERP '
                '(dados fictícios do evento: aqui não há integração real com o banco).</div>',
                unsafe_allow_html=True)
