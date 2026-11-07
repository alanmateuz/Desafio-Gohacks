# 04 · Submissão (até 16h30 · código congelado às 15h30)

## Nome do projeto (até 80)
GoGuardian · o agente que confere cada pagamento antes do lote ir ao banco

## Qual problema você resolveu? (até 600)
No contas a pagar do case, a fila (876 títulos, R$ 10,2 mi entre 03 e 13/11, dados fictícios do evento) chega por 6 canais, é digitada à mão no ERP e vai ao banco em lotes às 10h e 14h. O tesoureiro assina sem conferir título por título. Nessa fila havia golpe de troca de conta (Embalarte, R$ 194 mil indo para o golpista), boleto falso, pagamento em dobro, zero a mais e título no fornecedor errado: cerca de R$ 466 mil sairiam indevidamente. Conferir à mão leva ~8 min por título (estimativa), então ninguém confere.

## Qual é a sua solução? (até 800)
O GoGuardian é um agente que confere 100% dos títulos antes do envio ao banco.
1) Junta fila, títulos, fornecedores, NF-e, duplicatas, DDA, alterações de cadastro e caixa de e-mail numa planilha mãe.
2) Regras em código: troca de conta sem confirmação, boleto de outro CNPJ, duplicidade (NF + parcela), valor diferente da duplicata, fornecedor errado e fracionamento de alçada.
3) Sozinho, tira do lote o que está errado, resolve o que cabe na alçada do analista (ex.: cancela o duplicado) e avisa a pessoa certa: uma mensagem por pessoa, com motivo e ação proposta.
4) No painel, quem tem a alçada decide só as exceções: aprovar, liberar com motivo, manter fora ou anotar.
5) Sai o lote final já corrigido (conta antiga, valor certo), com CSV.

## Como você usou a IA? (até 800)
No produto: o Jev (AI Proxy do evento) lê os 246 e-mails e responde 3 perguntas: assunto, pede troca de conta? e tenta dar ordem ao robô? A saída é JSON validado por schema, com 2 tentativas; confiança abaixo de 0,7 vai para uma pessoa. A IA nunca libera pagamento: só reforça uma regra que o código já disparou. Custo: US$ 0,0059.
Na construção: Claude Code com agentes de produto, dev e avaliador. Conferi com gabaritos meus (26 casos de regras e 30 e-mails): regras de 85% para 100%, e-mails 97–100%.
O que corrigi: os testes do próprio agente davam 5/5 e deixavam R$ 166 mil passar; a Embalarte voltava ao lote na conta do golpista; o falso cartório oscilava, e não ajustei o prompt ao teste (o código pega pelo domínio). Tudo em decisoes.md.

## Qual o resultado ou impacto esperado? (até 500)
Na fila do evento, R$ 483 mil ficaram fora do lote (49 títulos em 21 casos) de R$ 10,2 mi conferidos; cerca de R$ 466 mil teriam saído indevidamente. 100% dos títulos conferidos, contra 0 hoje. 15 avisos para pessoas em vez de um por título; o resto o agente resolve sozinho. Conferência de ~8 min para ~30 s por título (estimativa). Próximo passo: conectar direto ao ERP e às fontes para a pessoa só aprovar.

## Envio
- Link do GitHub: https://github.com/alanmateuz/Desafio-Gohacks (público, confere 200)
- Slides em PDF: exportar do Canva ("Pitch GoHacks", 9 slides) e subir na plataforma — o Mateus faz o upload
- App publicado: não (roda local, `streamlit run app.py`)
- Vídeo: opcional, se der tempo de gravar os 30 s do plano B
- Outros materiais: opcional, `eval/antes_depois.csv`
- Declaração: o Mateus marca
