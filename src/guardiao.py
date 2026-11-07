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
    out["acionar"] = [s["acionar"] or "" for s in saidas]
    out["motivo"] = [s["motivo"] for s in saidas]
    return out


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
    print("\nExceções:")
    cols = ["titulo_id", "razao_social", "valor", "regras_violadas", "motivo"]
    print(df[df.decisao != "liberar"][cols].to_string(index=False, max_colwidth=90))


if __name__ == "__main__":
    main()
