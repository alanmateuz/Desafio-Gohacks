"""Ponto de entrada da solução. O eval/run.py chama resolver(entrada) para cada caso.

Stub de exemplo para o eval rodar ponta a ponta. Substitua no dia:
camada 1 = fluxo feio que funciona; depois validação, aprovação humana e config.
"""
from regras import tem_termo_proibido, validar_saida


def resolver(entrada: dict) -> dict:
    texto = entrada.get("texto", "")

    # 1. Código para regra: o que é checável não depende da IA.
    if not texto.strip():
        return {"decisao": "revisar", "motivo": "entrada sem texto"}
    if tem_termo_proibido(texto):
        return {"decisao": "revisar", "motivo": "termo proibido"}

    # 2. IA para linguagem: aqui entraria a chamada ao modelo, pedindo JSON com schema.
    saida = {"decisao": "aprovar", "motivo": "sem problemas encontrados"}

    # 3. Confere a saída da IA; se vier inválida, vai para o humano.
    if validar_saida(saida):
        return {"decisao": "revisar", "motivo": "saída da IA inválida"}
    return saida
