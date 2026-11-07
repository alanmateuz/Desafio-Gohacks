"""Painel do guardião do lote (camada 1, feio de propósito). Rode: streamlit run app.py"""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from coletor import montar_planilha_mae  # noqa: E402
from guardiao import casos, conferir  # noqa: E402

st.set_page_config(page_title="Guardião do lote", layout="wide")
st.title("Guardião do lote")
st.caption("Gogroup (fictício) · referência 02/11/2026 08:00 · camada 1.1: 6 regras, ação por caso")


@st.cache_data
def carregar():
    return conferir(montar_planilha_mae())


df = carregar()
lotes = ["todos"] + sorted(df.lote_remessa.unique())
lote = st.selectbox("Lote de remessa", lotes, index=lotes.index("RM20261103-MER"))
vis = df if lote == "todos" else df[df.lote_remessa == lote]

seguem, retidos = vis[vis.decisao == "liberar"], vis[vis.decisao != "liberar"]
c1, c2, c3 = st.columns(3)
c1.metric("Títulos conferidos", f"{len(vis)}", f"R$ {vis.valor.sum():,.2f}", delta_color="off")
c2.metric("Seguem no lote", f"{len(seguem)}", f"R$ {seguem.valor.sum():,.2f}", delta_color="off")
c3.metric("Retidos (exceções)", f"{len(retidos)}", f"R$ {retidos.valor.sum():,.2f}", delta_color="off")

aba_mae, aba_exc, aba_lote = st.tabs(["Planilha mãe", "Exceções", "Lote final"])
COLS = ["lote_remessa", "titulo_id", "razao_social", "categoria", "numero_nf_digitado",
        "nf_normalizada", "parcela", "valor", "valor_duplicata", "vencimento", "forma_pagamento",
        "destino_pagamento", "decisao", "regras_violadas", "acao", "acionar", "caso_id", "motivo"]
ACOES = {
    "reverter_alteracao_cadastro": "Reverter a conta para a anterior (aprovação dupla)",
    "cancelar_titulo": "Cancelar o título duplicado",
    "corrigir_lancamento": "Corrigir o lançamento",
    "contatar_fornecedor": "Confirmar o boleto com o fornecedor pelo canal do cadastro",
    "retirar_do_lote": "Retirar do lote",
}

with aba_mae:
    st.dataframe(vis[COLS], use_container_width=True, hide_index=True)

with aba_exc:
    cs = casos(vis)
    if cs.empty:
        st.success("Nenhuma exceção neste lote.")
    else:
        st.write(f"**{len(cs)} casos** · {(cs.acionar != '').sum()} precisam de uma pessoa; "
                 "o resto o agente resolve dentro da alçada do analista.")
    for _, c in cs.iterrows():
        with st.container(border=True):
            quem = c.acionar or "agente (dentro da alçada)"
            st.markdown(f"**{c.fornecedor}** · {c.qtd} título(s) · **R$ {c.valor:,.2f}**")
            st.write(c.motivo)
            st.caption(f"Ação proposta: {ACOES.get(c.acao, c.acao)} · quem decide: {quem} · "
                       f"regras: {c.regra} · títulos: {c.titulos}")

with aba_lote:
    st.write(f"O que vai ao banco: **{len(seguem)} títulos · R$ {seguem.valor.sum():,.2f}**")
    st.dataframe(seguem[["lote_remessa", "titulo_id", "razao_social", "valor", "vencimento",
                         "destino_pagamento"]], use_container_width=True, hide_index=True)
