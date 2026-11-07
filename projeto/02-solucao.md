# 02 · Solução: Guardião do lote

**Em uma frase:** "Um agente de IA que junta as informações espalhadas de pagamentos numa planilha mãe e confere cada título antes de o lote ir ao banco. Assim, o tesoureiro só assina pagamentos seguros, e só as suspeitas chegam à pessoa certa."

## Hoje × novo
```
Hoje:  NF/boleto chegam → analista digita no ERP → título cai sozinho na fila → [Marcos assina o lote sem conferir = fricção] → dinheiro sai às 10h/14h

Novo:  ERP + Compras + NF-e + DDA + bancos + e-mail
         → coletor (código) monta a PLANILHA MÃE (1 linha por título, CNPJ e NF normalizados)
         → IA lê e-mails e boletos → JSON validado pelo código
         → regras em código conferem cada título
         → ok: PLANILHA FINAL DO LOTE → Marcos assina
         → exceção: sai do lote → Slack para a pessoa certa, com o motivo → aprovou: volta ao lote
```

## Painel (interface)
Tudo acontece num painel web. A primeira versão tem três telas; o resto será pensado depois.

1. **Planilha mãe:** todos os títulos da fila com os dados cruzados das fontes. Tem filtros por lote, fornecedor e status e uma coluna com o motivo de cada decisão.
2. **Exceções:** só o que o agente segurou, com o motivo, as evidências (e-mail, alteração de cadastro, título gêmeo) e os botões **Aprovar** e **Recusar**. Cada exceção mostra quem pode decidir.
3. **Lote final:** o que vai ao banco em cada fechamento, com o total em R$. É o que o Marcos assina.

Para o painel não virar um "painel bonito", **o agente age sozinho antes do fechamento**: tira o título do lote e avisa a pessoa sem esperar ninguém abrir a tela. O painel é onde a pessoa vê e decide as exceções.

## Código / IA / humano
| Parte | Quem faz | Por quê |
|---|---|---|
| Juntar as fontes e normalizar CNPJ (raiz de 8 dígitos), NF (sem zeros e série) e fornecedor entre sistemas | Código | É regra checável e precisa ser igual sempre |
| Duplicidade: mesma NF normalizada, mesmo fornecedor, **mesma parcela** | Código | Regra exata; valor igual sozinho dá falso positivo (parcelas) |
| 3 vias: NF × OC (2% ou R$ 50), título × duplicata (R$ 0,10), raiz do CNPJ, banco do boleto | Código | Tolerâncias escritas em `parametros.md` |
| Alçada (soma por fornecedor + NF no dia) e aprovação dupla | Código | Regra de política; fracionar é proibido |
| Troca bancária: vale só com confirmação pelo telefone **anterior** à troca | Código | Só o registro em `alteracoes_cadastro` vale, nunca o texto de um e-mail |
| Domínio parecido com o do cadastro (`embalartte` × `embalarte`) | Código | Distância entre textos, sem julgamento |
| Ler e-mail ou boleto e extrair banco, CNPJ, valor, NF, linha digitável e "pede troca de conta?" | IA | Texto livre, cada fornecedor escreve de um jeito |
| Marcar se o texto tenta dar ordem ao agente ("libere sem conferir", "já foi validado") | IA | Exige linguagem; a marcação só **aumenta** a suspeita, nunca libera |
| Escrever o motivo da exceção em 2 linhas para a pessoa | IA | Linguagem; os fatos vêm do código |
| Liberar um título que ficou em dúvida | Humano | Palavra final: Renata (fraude e duplicidade), aprovador (até R$ 50 mil), Helena (acima) |

**Por que workflow e não agente autônomo:** a decisão de pagar é regra e precisa ser auditável e repetível. O agente tem autonomia para **segurar** e **acionar**, que são ações seguras. **Liberar** só acontece por regra limpa ou por uma pessoa. A IA nunca libera nada sozinha.

## Contrato de dados
Entrada (uma linha da planilha mãe):
```json
{
  "titulo_id": "TP432130",
  "lote": "RM20261105-MER",
  "fornecedor_id": "FP4615",
  "valor": 96480.00,
  "vencimento": "2026-11-05",
  "nf_normalizada": "78418",
  "parcela": "1/1",
  "destino": "ted 905/0001/4471203-9",
  "troca_bancaria_recente": {"data": "2026-10-30", "confirmada": false},
  "emails_relacionados": ["EM5xxxxx"]
}
```
Saída da IA, por e-mail (schema que o código valida):
```json
{
  "pede_troca_bancaria": true,
  "banco": "905", "agencia": "0001", "conta": "4471203-9",
  "cnpj_citado": "85.990.602/0001-96",
  "nf_citada": "78418",
  "tenta_instruir_agente": true,
  "trecho_suspeito": "Obs. para o robô de pagamentos: ...",
  "confianca": 0.0
}
```
Saída do guardião, por título (é o que o `eval/run.py` confere):
```json
{
  "decisao": "liberar | retirar | acionar",
  "regras_violadas": ["troca_bancaria_sem_confirmacao", "dominio_parecido"],
  "acionar": "PS01 | aprovador | PS03 | null",
  "motivo": "Conta trocada em 30/10 sem ligação de confirmação; pedido veio de domínio parecido (embalartte)."
}
```
- **Limite de tentativas:** 2 chamadas à IA por e-mail.
- **Fallback:** se o JSON vier inválido ou a IA estiver fora, o título vai para a pessoa com o motivo "não foi possível ler o e-mail". Nunca é liberado.

## Quanto a IA economiza
- **Passo substituído:** a conferência título por título, que hoje ninguém faz.
- **Antes:** 0 de 876 títulos conferidos `[HIPÓTESE: conferir à mão levaria ~5 min por título, ~73 h por semana]`.
- **Depois:** 100% conferidos antes do fechamento; a pessoa só olha as exceções, com alvo de ≤ 10% `[HIPÓTESE]`.
- **Volume:** 876 títulos em 9 dias úteis, ~R$ 10,2 milhões.

## Replicabilidade
- Trocar de empresa, marca ou banco = trocar `config/regras.yaml` (tolerâncias, alçadas, horários de fechamento, pessoas a acionar) e `config/fontes.yaml` (caminho e formato de cada base).
- O código não muda.

## Riscos
| Risco | Mitigação |
|---|---|
| IA inventa dado ao ler um e-mail | Código confere com o cadastro e a NF; o que a IA extrai só serve para **segurar**, nunca para liberar |
| Injeção de prompt no e-mail ("robô, libere") | O texto do e-mail é dado; a regra de troca bancária só aceita o registro do ERP; a tentativa vira evidência na exceção |
| Barrar demais (falso positivo custa R$ 60 + atraso) | Duplicidade exige mesma NF **e** parcela; eval com casos de parcelas legítimas; medir acionamentos por lote |
| JSON inválido ou API fora | 2 tentativas, depois vai para a pessoa; modo simulado sem chave |
| Dados sensíveis (conta, CNPJ) | Para a IA vai só o texto do e-mail; os dados bancários ficam no código. Dados fictícios do evento |
| Custo | ~246 e-mails no período × 1 a 2 chamadas = poucas centenas de chamadas `[calcular com o preço do modelo]` |
| Python não instalado no notebook | Instalar com `winget install Python.Python.3.12` antes de construir |

## Stack
- **Backend:** Python 3.12, `pandas` para o coletor e a planilha mãe.
- **IA:** API do Claude, liberada no evento. A chave fica no `.env` (`LLM_API_KEY`), com saída em JSON validada no código.
- **Interface:** painel em **Streamlit**, com planilha mãe, exceções com botões e lote final.
- **Canal:** aviso no Slack por webhook `[HIPÓTESE: se não houver Slack, simular com um log de mensagens no painel]`.
- **Testes:** `pytest` para as regras e `eval/run.py` com 15 a 25 casos tirados de `dados/`.
- **Deploy:** local na demo; Streamlit Community Cloud se houver tempo.
