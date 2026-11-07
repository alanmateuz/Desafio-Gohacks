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
    out["aprovacao"] = [s.get("aprovacao") or "" for s in saidas]
    out.attrs = mae.attrs
    return out


def alertas_caixa(df: pd.DataFrame) -> pd.DataFrame:
    """E-mails suspeitos que não viraram evidência de um título retido: 1 alerta por grupo."""
    caixa = df.attrs.get("caixa")
    if caixa is None or caixa.empty:
        return pd.DataFrame()
    ja_em_caso = set(df[df.regras_violadas.str.contains("email")].fornecedor_id)
    nomes = dict(zip(df.fornecedor_id, df.razao_social))
    sus = caixa[(caixa.suspeita != "") & ~caixa.fornecedor_id.isin(ja_em_caso)]
    alertas = []
    golpe = sus[sus.vinculo == "desconhecido"]
    if len(golpe):
        alertas.append({"alerta": "phishing_na_caixa", "fornecedor": "—", "acao": "abrir_incidente",
                        "acionar": "PS08", "emails": ", ".join(golpe.comunicacao_id),
                        "motivo": f"{len(golpe)} e-mail(s) de remetentes que não são fornecedores "
                                  f"({', '.join(sorted(set(golpe.remetente.str.split('@').str[-1])))}), "
                                  "pedindo pagamento, token ou download. Ninguém deve responder nem abrir anexos."})
    for f, g in sus[sus.vinculo != "desconhecido"].groupby("fornecedor_id"):
        instrui = g[g.tenta_instruir_agente == True]  # noqa: E712
        trecho = next((t for t in g.trecho if t), "")
        alertas.append({
            "alerta": "tentativa_de_instruir_agente" if len(instrui) else g.suspeita.iloc[0],
            "fornecedor": nomes.get(f, f), "acao": "registrar_tentativa", "acionar": "PS01",
            "emails": ", ".join(g.comunicacao_id),
            "motivo": (f"E-mail de {g.remetente.iloc[0]} tenta instruir o agente: \"{trecho}\". "
                       "Nada foi liberado por causa dele; os títulos seguem as regras normais."
                       if len(instrui) else f"E-mail de remetente suspeito: {g.remetente.iloc[0]}."),
        })
    return pd.DataFrame(alertas)


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
    al = alertas_caixa(df)
    caixa = df.attrs.get("caixa")
    if caixa is not None:
        print(f"\nCaixa: {len(caixa)} e-mails lidos · falhas de leitura {(caixa.erro_ia != '').sum()} · "
              f"💲 jev US$ {caixa.custo_usd.sum():.6f} nesta execução (cache não custa)")
    print(f"Aprovação no lote: {(df.aprovacao == 'aprovador').sum()} pelo aprovador · "
          f"{(df.aprovacao == 'PS03').sum()} pela diretora (PS03)")
    if len(al):
        print(f"\nAlertas da caixa: {len(al)}")
        print(al[["alerta", "fornecedor", "acionar", "emails"]].to_string(index=False))
    print(f"\nCasos: {len(c)} · acionamentos de pessoa: {(c.acionar != '').sum() + len(al)} "
          f"({(c.acionar != '').sum()} de títulos + {len(al)} da caixa)")
    cols = ["caso_id", "qtd", "valor", "acao", "acionar", "titulos"]
    print(c[cols].to_string(index=False, max_colwidth=60))


if __name__ == "__main__":
    main()
