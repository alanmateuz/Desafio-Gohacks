"""Camada de IA. Camada 1 = MODO SIMULADO: o motivo é montado a partir dos fatos do código.
Na camada 2 entra a API do Claude (chave no .env), com saída JSON validada e limite de tentativas.
"""
NOMES = {
    "troca_bancaria_sem_confirmacao": "Conta bancária trocada sem confirmação",
    "duplicidade": "Possível pagamento em duplicidade",
}


def escrever_motivo(titulo: dict, violacoes: list[dict]) -> str:
    partes = [f"{NOMES.get(v['regra'], v['regra'])}: {v['fato']}." for v in violacoes]
    return " ".join(partes)
