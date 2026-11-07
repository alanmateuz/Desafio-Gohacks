# 03 · Pitch

Uso o mesmo roteiro de 5 min no pré-júri (5 de pitch + 5 de perguntas) e na final (5 + 5 de sabatina).
Os slides vão em PDF: são 8, fundo branco, brandbook Gogroup (azul `#2659a5`, limão, rosa, Poppins, 3 bolinhas limão e logo embaixo à direita).
**Se faltar tempo, corto texto, nunca a demo.**

Estrutura SOAR: **S**ituação (slides 1–3) → **O**bstáculos (slide 6) → **A**ções (slides 4–5) → **R**esultados (slides 7–8).

## Elevator (1 frase)
> Para o tesoureiro que assina R$ 10,2 mi sem conferir, construí o **GoGuardian**, um agente que confere cada título antes de o lote ir ao banco. Com ele, golpe, pagamento em dobro e zero a mais ficam fora do lote, e só as exceções chegam a uma pessoa.

## Os 8 slides: o que falar, animação e GIF
| # | Tempo | Slide (Canva) | Fala-chave | Animação / GIF |
|---|---|---|---|---|
| 1 | 0:00–0:15 | **GoGuardian**: pílula "Desafio 2 · Pagamentos" + bloco azul com o elevator | Elevator em 1 frase | Bloco azul entra com **Pan** (da direita); título com **Rise**. Nada mais: abertura limpa. |
| 2 | 0:15–0:50 | **Marcos assina R$ 10,2 mi sem olhar**: card com "876 títulos · 0 conferidos" | "O Marcos é tesoureiro. Ele assina 876 títulos sem conferir nenhum. Nessa fila, cerca de R$ 466 mil sairiam errado: golpe na conta, pagamento em dobro, zero a mais." | "876" com **Pop**; a linha dos R$ 466 mil entra **depois do clique** (Fade). Contador subindo: o Canva não tem nativo, então seria um GIF de 2 s (opcional). |
| 3 | 0:50–1:20 | **Onde o dinheiro escapa**: Chega → Digita → **Assina** (rosa) → Paga | "Hoje funciona assim: chega por 6 canais, o analista digita, o tesoureiro assina sem conferir e o dinheiro sai às 10h e 14h. O problema está aqui." (aponte o card rosa) | Cards entram **da esquerda para a direita** (Rise em sequência); o card rosa por último, com **Pop**; a pílula "O GoGuardian entra aqui" desce com **Drift**. |
| 4 | 1:20–2:10 | **Código confere. IA lê. Você decide.**: 3 blocos (azul / limão / branco) | "O GoGuardian é um agente que confere cada título antes de o lote sair. O **código** confere duplicidade, 3 vias, troca de conta e alçada. A **IA** lê e-mails e boletos e explica o motivo, mas **nunca libera pagamento**. O **humano** decide só as exceções. Sozinho, ele retira do lote e avisa a pessoa certa. Deixa eu mostrar na prática." | Os 3 blocos entram **um por clique** (Rise), na ordem da fala. |
| 5 | 2:10–3:30 | **Demo ao vivo**: Caso A (branco) e Caso B (rosa) | Ver roteiro da demo abaixo | **Aqui entra o GIF/vídeo:** gravação de 30 s do painel (plano B), linkada no botão ▶ ou numa aba aberta. Pílula "ao vivo" com **Breathe**. |
| 6 | 3:30–4:00 | **A IA errou. O sistema pegou.**: 85% → 100% + card azul com 3 erros | "Montei um gabarito de 26 casos. A 1ª rodada acertou 85% (22/26). Corrigi e cheguei a 100%. E a IA errou de verdade: arredondou R$ 0,10, deixou a conta do golpista no lote final, liberou um boleto falso num clique. Cada erro virou regra ou teste." | "85%" aparece primeiro e "100%" no clique (**Pop**); os 3 erros entram **um por clique** (Fade). |
| 7 | 4:00–4:20 | **O número que fica**: **R$ 483 mil** + card limão "15" | "R$ 483 mil fora do lote: 49 títulos em 21 casos, de R$ 10,2 mi conferidos. 15 pessoas avisadas, não uma por título. E a IA custou US$ 0,0059 para ler 246 e-mails." Diga a premissa: dados fictícios, fila de 03 a 13/11. | "R$ 483 mil" com **Stomp** (impacto); card do 15 com Pop; pílulas com Fade. |
| 8 | 4:20–5:00 | **O que muda e como chegar lá**: 01 / 02 / 03 + faixa azul | "Para o Marcos, some assinar sem conferir. Primeira dependência: acesso de leitura a ERP, NF-e, DDA e e-mail. Na segunda, eu rodaria no próximo lote só segurando e avisando. Com os dados reais, calibro as regras, e serve para outras marcas trocando a config." **Feche repetindo o elevator.** | Cards 01→02→03 por clique (Rise); faixa "Obrigado" com Fade no fim. |

**Regra das animações:** use no máximo 1 tipo por slide e sempre **por clique**, nunca automática, para a fala mandar no ritmo. No Canva, selecione o elemento → **Animar** → escolha o efeito e marque "ao clicar".

## Roteiro da demo (80 s)
Antes de subir: apague `dados/decisoes_humanas.json`, abra o painel já no lote **Meridiano 03/11 10:00** e deixe o vídeo de 30 s aberto numa aba.

1. **(10 s) Abro no caso, não no login.** "Este é o lote que vai ao banco às 10h. O agente já conferiu tudo."
2. **(20 s) Caso A, que ele resolve sozinho:** Maciez, R$ 4.750 (TP430006), título em dobro (mesma NF e parcela). "Dentro da alçada, ele cancela sozinho e registra. Ninguém precisou olhar."
3. **(40 s) Caso B, que ele passa para uma pessoa:** Embalarte, 25 títulos, R$ 194 mil.
   - A conta foi trocada por e-mail de um domínio parecido (`embalartte`), e o e-mail ainda trazia uma "Obs. para o robô" tentando instruir o agente.
   - Os títulos saem do lote e a Renata é avisada com o motivo.
   - Clico em **Liberar mesmo assim** e mostro que ele exige confirmação e motivo.
4. **(10 s) Lote final:** a conta do golpista não aparece, o pagamento vai para a conta antiga e o total bate.

Antes ~8 min por título, depois 30 s: **é estimativa, diga isso em voz alta.**

## Roteiro de 90 s
"O Marcos assina R$ 10,2 mi em 876 títulos sem conferir nenhum. O GoGuardian é um agente que confere cada título antes do lote ir ao banco: o código confere as regras, a IA lê e-mails e boletos e o humano só decide as exceções. Testei em 26 casos e fui de 85% para 100%. Na fila do evento, R$ 483 mil ficaram fora do lote, com 15 avisos em vez de um por título. O próximo passo é acesso de leitura ao ERP e rodar no próximo lote só segurando e avisando."

## Sabatina
Regras: "Boa pergunta…" (2 s) · responda só o que foi perguntado · "não cheguei lá ainda, mas o próximo passo seria…" · nunca contradiga, redirecione.

| Pergunta | Minha resposta (curta) |
|---|---|
| Como funciona tecnicamente? | Python. As regras ficam em código, e a IA (Jev, pelo AI Proxy) só lê e-mails e responde em JSON com schema validado. Painel em Streamlit. |
| Quem usaria na prática? | O tesoureiro, que assina o lote, e o analista de contas a pagar, que recebe só as exceções. |
| O que falta para funcionar? | Acesso de leitura a ERP, NF-e, DDA e e-mail, e calibrar as regras com os dados reais. |
| Como medir o sucesso? | R$ retido que era indevido, % de títulos conferidos (hoje 0%) e quantos alarmes falsos chegam a uma pessoa. |
| E quando a IA erra? | Ela nunca libera um pagamento, só reforça uma regra. Se a confiança é baixa ou o JSON não valida, o caso vai para uma pessoa com o motivo. |
| O que você fez e o que a IA fez? | Eu defini as regras, o gabarito de 26 casos e as decisões. A IA escreveu código e eu peguei os erros dela: arredondamento, conta do golpista no lote, boleto falso liberado. Está no `decisoes.md`. |
