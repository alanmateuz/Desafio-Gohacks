"""Coletor: junta as bases espalhadas de dados/ numa PLANILHA MÃE (uma linha por título da fila)."""
from datetime import datetime
from pathlib import Path

import pandas as pd

from regras import chave_duplicidade, normalizar_nf, troca_bancaria_sem_confirmacao

DADOS = Path(__file__).resolve().parent.parent / "dados"
REFERENCIA = datetime(2026, 11, 2, 8, 0)  # parametros.md: segunda 02/11/2026 08:00


def _ler(nome: str) -> pd.DataFrame:
    return pd.read_csv(DADOS / nome, dtype=str, keep_default_na=False)


def montar_planilha_mae(referencia: datetime = REFERENCIA) -> pd.DataFrame:
    agenda = _ler("agenda_remessa.csv")
    titulos = _ler("contas_a_pagar.csv")
    fornecedores = _ler("fornecedores.csv")
    alteracoes = _ler("alteracoes_cadastro.csv")

    # Detalhes do título no ERP (NF digitada, parcela, lançador)
    cols = ["titulo_id", "numero_nf_digitado", "parcela", "oc_id", "lancado_por", "data_lancamento"]
    mae = agenda.merge(titulos[cols], on="titulo_id", how="left")
    mae = mae.merge(fornecedores[["fornecedor_id", "razao_social", "categoria"]],
                    on="fornecedor_id", how="left")
    mae["valor"] = mae["valor"].astype(float)
    mae["nf_normalizada"] = mae["numero_nf_digitado"].map(normalizar_nf)

    # Troca bancária recente sem confirmação, por fornecedor
    por_fornecedor = alteracoes.to_dict("records")
    trocas = {}
    for fid in mae["fornecedor_id"].unique():
        alts = [a for a in por_fornecedor if a["fornecedor_id"] == fid]
        trocas[fid] = troca_bancaria_sem_confirmacao(alts, referencia)
    mae["troca_bancaria_suspeita"] = mae["fornecedor_id"].map(trocas)

    # Duplicidade contra todos os títulos não cancelados do ERP
    vivos = titulos[titulos["status"] != "cancelado"].copy()
    vivos["chave"] = [chave_duplicidade(f, n, p) for f, n, p in
                      zip(vivos.fornecedor_id, vivos.numero_nf_digitado, vivos.parcela)]
    vivos = vivos[vivos["chave"].notna()].sort_values(["data_lancamento", "titulo_id"])
    duplicado_de = {}
    for _, grupo in vivos.groupby("chave"):
        if len(grupo) < 2:
            continue
        pagos = grupo[grupo["status"] == "pago"]
        # o que já foi pago é o original; se nenhum foi pago, o primeiro lançado é o original
        original = pagos.iloc[0] if len(pagos) else grupo.iloc[0]
        for _, t in grupo.iterrows():
            if t["titulo_id"] != original["titulo_id"] and t["status"] == "agendado":
                rotulo = original["titulo_id"] + (" (já pago)" if original["status"] == "pago" else "")
                duplicado_de[t["titulo_id"]] = rotulo
    mae["duplicado_de"] = mae["titulo_id"].map(duplicado_de).fillna("")
    return _juntar_nf(mae, titulos, fornecedores)


def _so_digitos(texto: str) -> str:
    return "".join(c for c in str(texto or "") if c.isdigit())


def _juntar_nf(mae: pd.DataFrame, titulos: pd.DataFrame, fornecedores: pd.DataFrame) -> pd.DataFrame:
    """3 vias: acha a NF no portal (raiz do CNPJ + número) e a duplicata da parcela."""
    nfs = _ler("notas_fiscais.csv")
    dups = _ler("nf_duplicatas.csv")
    nfs["raiz"] = nfs["cnpj_emitente"].map(lambda c: _so_digitos(c)[:8])
    nfs["nf_norm"] = nfs["numero_nf"].map(normalizar_nf)
    nfs = nfs.drop_duplicates(["raiz", "nf_norm"])
    dups["valor"] = dups["valor"].astype(float)
    valor_dup = {(c, n): v for c, n, v in zip(dups.chave_acesso, dups.n_dup, dups.valor)}

    raiz_forn = {f: _so_digitos(c)[:8] for f, c in zip(fornecedores.fornecedor_id, fornecedores.cnpj)}
    forn_por_raiz = {r: f for f, r in raiz_forn.items()}
    nf_por_chave = {(r, n): row for r, n, row in zip(nfs.raiz, nfs.nf_norm, nfs.to_dict("records"))}
    nfs_por_numero = nfs.groupby("nf_norm")

    extra = titulos.set_index("titulo_id")[["cnpj_beneficiario_boleto"]]
    mae = mae.join(extra, on="titulo_id")
    mae["raiz_fornecedor"] = mae["fornecedor_id"].map(raiz_forn)

    chaves, vdups, cnpjs, outros = [], [], [], []
    for t in mae.to_dict("records"):
        n_dup = str(t["parcela"]).split("/")[0].zfill(3)
        nf = nf_por_chave.get((t["raiz_fornecedor"], t["nf_normalizada"])) if t["nf_normalizada"] else None
        outro = ""
        if nf is None and t["nf_normalizada"] and t["nf_normalizada"] in nfs_por_numero.groups:
            # NF com esse número existe para outra raiz e com o mesmo valor na parcela → fornecedor errado
            for cand in nfs_por_numero.get_group(t["nf_normalizada"]).to_dict("records"):
                v = valor_dup.get((cand["chave_acesso"], n_dup))
                if v is not None and abs(v - t["valor"]) <= 0.10:
                    outro = forn_por_raiz.get(cand["raiz"], cand["razao_social_emitente"])
                    break
        chaves.append(nf["chave_acesso"] if nf else "")
        vdups.append(valor_dup.get((nf["chave_acesso"], n_dup)) if nf else None)
        cnpjs.append(nf["cnpj_emitente"] if nf else "")
        outros.append(outro)
    mae["chave_nf"], mae["valor_duplicata"] = chaves, vdups
    mae["cnpj_emitente_nf"], mae["nf_outro_fornecedor"] = cnpjs, outros
    mae["raiz_beneficiario_boleto"] = mae["cnpj_beneficiario_boleto"].map(lambda c: _so_digitos(c)[:8])
    return mae


if __name__ == "__main__":
    df = montar_planilha_mae()
    print(df.head().to_string())
    print(f"\n{len(df)} títulos na fila · R$ {df.valor.sum():,.2f}")
