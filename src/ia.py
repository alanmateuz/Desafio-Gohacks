"""Camada de IA. Camada 1 = MODO SIMULADO: o motivo é montado a partir dos fatos do código.
Na camada 2 entra a API do Claude (chave no .env), com saída JSON validada e limite de tentativas.
"""
NOMES = {
    "troca_bancaria_sem_confirmacao": "Conta bancária trocada sem confirmação",
    "duplicidade": "Possível pagamento em duplicidade",
    "boleto_beneficiario_diferente": "Boleto com beneficiário diferente do fornecedor",
    "nf_de_outro_fornecedor": "Título lançado no fornecedor errado",
    "sem_nf_no_portal": "NF não encontrada no portal",
    "valor_diferente_duplicata": "Valor diferente da duplicata",
    "fracionamento_alcada": "Valor dividido para caber na alçada",
    "pedido_troca_por_email_suspeito": "Evidência",
    "boleto_de_email_fora_do_cadastro": "Evidência",
}


def escrever_motivo(titulo: dict, violacoes: list[dict]) -> str:
    partes = [f"{NOMES.get(v['regra'], v['regra'])}: {v['fato']}." for v in violacoes]
    return " ".join(partes)
