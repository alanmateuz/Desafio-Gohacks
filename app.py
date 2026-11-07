"""Painel do guardião do lote (camada 1, feio de propósito). Rode: streamlit run app.py"""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from coletor import montar_planilha_mae  # noqa: E402
from guardiao import conferir  # noqa: E402

st.set_page_config(page_title="Guardião do lote", layout="wide")
st.title("Guardião do lote")
st.caption("Gogroup (fictício) · referência 02/11/2026 08:00 · camada 1: troca bancária e duplicidade")


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
        "nf_normalizada", "parcela", "valor", "vencimento", "forma_pagamento",
        "destino_pagamento", "decisao", "regras_violadas", "acionar", "motivo"]

with aba_mae:
    st.dataframe(vis[COLS], use_container_width=True, hide_index=True)

with aba_exc:
    if retidos.empty:
        st.success("Nenhuma exceção neste lote.")
    for _, t in retidos.iterrows():
        with st.container(border=True):
            st.markdown(f"**{t.titulo_id} · {t.razao_social} · R$ {t.valor:,.2f}** · vence {t.vencimento}")
            st.write(t.motivo)
            st.caption(f"Regras: {t.regras_violadas} · acionar: {t.acionar} · destino: {t.destino_pagamento}")

with aba_lote:
    st.write(f"O que vai ao banco: **{len(seguem)} títulos · R$ {seguem.valor.sum():,.2f}**")
    st.dataframe(seguem[["lote_remessa", "titulo_id", "razao_social", "valor", "vencimento",
                         "destino_pagamento"]], use_container_width=True, hide_index=True)
