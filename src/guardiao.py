"""Roda o guardião sobre a planilha mãe. Uso: python src/guardiao.py [lote]"""
import sys

import pandas as pd

from coletor import montar_planilha_mae
from solucao import resolver


def conferir(mae: pd.DataFrame) -> pd.DataFrame:
    saidas = [resolver(t) for t in mae.to_dict("records")]
    out = mae.copy()
    out["decisao"] = [s["decisao"] for s in saidas]
    out["regras_violadas"] = [", ".join(s["regras_violadas"]) for s in saidas]
    out["acao"] = [s["acao"] or "" for s in saidas]
    out["acionar"] = [s["acionar"] or "" for s in saidas]
    out["caso_id"] = [s["caso_id"] or "" for s in saidas]
    out["motivo"] = [s["motivo"] for s in saidas]
    return out


def casos(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa as exceções por caso (fornecedor + regra principal): 1 acionamento por caso."""
    exc = df[df.decisao != "liberar"]
    g = exc.groupby("caso_id").agg(
        fornecedor=("razao_social", "first"), regra=("regras_violadas", "first"),
        acao=("acao", "first"), acionar=("acionar", lambda s: next((x for x in s if x), "")),
        titulos=("titulo_id", lambda s: ", ".join(s)), qtd=("titulo_id", "count"),
        valor=("valor", "sum"), motivo=("motivo", "first"))
    # aprovação dupla acima de R$ 50 mil vai para a diretora (PS03) no lugar da coordenadora
    g.loc[(g.acionar == "PS01") & (g.valor > 50000), "acionar"] = "PS03"
    return g.reset_index().sort_values("valor", ascending=False)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    df = conferir(montar_planilha_mae())
    if len(sys.argv) > 1:
        df = df[df.lote_remessa == sys.argv[1]]
    print(f"{len(df)} títulos · R$ {df.valor.sum():,.2f}")
    for decisao, g in df.groupby("decisao"):
        print(f"  {decisao:8} {len(g):4} títulos · R$ {g.valor.sum():,.2f}")
    print("\nPor regra:")
    for regra, g in df[df.regras_violadas != ""].groupby("regras_violadas"):
        print(f"  {regra}: {len(g)} · R$ {g.valor.sum():,.2f}")
    c = casos(df)
    print(f"\nCasos: {len(c)} · acionamentos de pessoa: {(c.acionar != '').sum()}")
    cols = ["caso_id", "qtd", "valor", "acao", "acionar", "titulos"]
    print(c[cols].to_string(index=False, max_colwidth=60))


if __name__ == "__main__":
    main()
