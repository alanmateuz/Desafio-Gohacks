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
    return mae


if __name__ == "__main__":
    df = montar_planilha_mae()
    print(df.head().to_string())
    print(f"\n{len(df)} títulos na fila · R$ {df.valor.sum():,.2f}")
