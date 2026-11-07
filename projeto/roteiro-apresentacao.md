# Roteiro de apresentação · GoGuardian (5 min)

> **Pitch não é apresentação, é narrativa.** É uma história com começo, meio e fim, com emoção e evidência, e termina num chamado à decisão.
> **Regra de ouro:** se algo tiver que ser cortado, corte texto, nunca a demo.

**Esqueleto SOAR:**
- **S** (Situação): o Marcos assina R$ 10,2 mi sem olhar.
- **O** (Obstáculos): a IA errou, e eu peguei.
- **A** (Ações): código confere, IA lê, você decide.
- **R** (Resultados): R$ 483 mil fora do lote.

**Antes de subir:**
- Apague `dados/decisoes_humanas.json` e `dados/outbox_slack.jsonl`.
- Deixe o painel aberto no lote **Meridiano 03/11 10:00**.
- Deixe o vídeo de 30 s aberto numa aba (plano B).
- Tenha água por perto e respire.

---

## 0:00 · Abertura (15 s) · slide 1 "GoGuardian"
*Conceito: elevator pitch em 1 frase. Se não couber, a ideia ainda está grande.*

> "Para o tesoureiro que assina R$ 10,2 milhões sem conferir, construí o GoGuardian: um agente que confere cada pagamento antes de o lote ir ao banco. Com ele, golpe, pagamento em dobro e zero a mais ficam fora do lote, e só as exceções chegam a uma pessoa."

## 0:15 · Dor (35 s) · slide 2 "Marcos assina R$ 10,2 mi sem olhar" · **S**
*Conceito: quem sofre e qual é o custo. Emoção + evidência.*

> "Este é o Marcos, tesoureiro. Na segunda, às 10h, o lote vai ao banco. Ele assina 876 títulos, R$ 10,2 milhões, sem conferir nenhum, porque conferir leva uns 8 minutos por título. Nessa fila tinha golpe de troca de conta, boleto falso, pagamento em dobro e zero a mais: cerca de R$ 466 mil sairiam errado."

## 0:50 · Visão 360 (30 s) · slide 3 "Onde o dinheiro escapa"
*Conceito: mostre a área inteira e a frente que você provou.*

> "Hoje funciona assim: chega por 6 canais, o analista digita no ERP, o tesoureiro assina e o dinheiro sai às 10h e às 14h. O problema está aqui (aponte o card rosa): ninguém confere antes de assinar. A área tem outras frentes, como duplicidades já pagas. Eu provei esta: o lote antes de sair."

## 1:20 · O agente (50 s) · slide 4 "Código confere. IA lê. Você decide." · **A**
*Conceito: o que ele faz sozinho. Fale do que a IA faz no fluxo e do passo que ela acelera; evite como foi treinada, detalhes de implementação e buzzwords.*

> "O GoGuardian confere 100% dos títulos. O código checa duplicidade, conta trocada, nota, alçada. A IA tem um papel pequeno e vigiado: lê os e-mails e marca troca de conta, golpe e quem tenta dar ordem ao robô. Ela nunca libera pagamento, só reforça uma regra. Sozinho, ele tira do lote o que está errado, resolve o que cabe na alçada e avisa a pessoa certa. O humano só decide as exceções. Deixa eu mostrar na prática."

## 2:10 · Demo (80 s) · slide 5 "Demo ao vivo" → painel · ⭐ a estrela
*Conceito: mostre, não descreva. Abra no caso, não no login. Mostre dois casos: um que o agente resolve sozinho e um que ele passa para uma pessoa.*

1. **(10 s)** Painel já no lote: "Este lote vai ao banco às 10h. O agente já conferiu tudo. **Antes: ~8 min por título. Depois: 30 s.** É uma estimativa."
2. **(20 s) Caso A, Maciez, R$ 4.750:** "Título em dobro, mesma nota e parcela. Dentro da alçada, ele cancela sozinho e registra. Ninguém precisou olhar."
3. **(35 s) Caso B, Embalarte, R$ 194 mil** (no seletor, escolha **Fila inteira**; no lote das 10h ela aparece só com 2 títulos, R$ 3,1 mil):
   - "A conta foi trocada por e-mail, de um domínio parecido. E olha isso: uma 'Obs. para o robô' tentando mandar no agente. Ele não obedece. Tirou do lote e avisou a Helena, a diretora, porque passa de R$ 50 mil."
   - Clique em **Liberar mesmo assim** e mostre que exige confirmação e motivo.
4. **(15 s) Aba Equipe:** "Ninguém precisa ficar olhando a tela: cada pessoa recebe uma mensagem só, com os casos dela." Mostre a conversa da Helena (a Embalarte) ou a da Renata (7 casos).

*Plano B: se travar, abra o vídeo de 30 s e narre por cima.*

## 3:30 · Como fez (30 s) · slide 6 "A IA errou. O sistema pegou." · **O**
*Conceito: onde a IA errou e como você corrigiu. É aqui que se ganha Modelagem.*

> "A IA errou, e eu peguei. Os testes que o próprio agente escreveu davam 5 de 5 e não pegavam nada. Montei meu gabarito de 26 casos e apareceram R$ 166 mil passando: fui de 85% para 100%. Num falso cartório a IA ficou em dúvida, e eu não mexi no prompt para passar no teste: a dúvida vai para uma pessoa. E a Embalarte voltava ao lote na conta do golpista: corrigi e escrevi um teste."

## 4:00 · Impacto (20 s) · slide 7 "O número que fica" · **R**
*Conceito: o número que fica, sempre com a premissa.*

> "R$ 483 mil ficaram fora do lote, de R$ 10,2 milhões conferidos. Desses, R$ 466 mil sairiam errado. 100% dos títulos conferidos, contra zero hoje, e 15 avisos em vez de um por título. Premissa: dados fictícios do evento, fila de 3 a 13 de novembro."

## 4:20 · Próximos passos (20 s) · slide 8
*Conceito: mostre como seria com os dados reais (Adaptabilidade).*

> "Hoje ele confere. O próximo passo é ele fazer o trabalho e a pessoa só aprovar: conectar direto ao ERP, à NF-e, ao DDA e ao e-mail; lançar o título sozinho, sem digitação; aprovar com um clique; e escalar para outras marcas."

## 4:40 · Fechamento (20 s) · slide 9 "O que muda e como chegar lá"
*Conceito: chamado à decisão. Repita o elevator pitch.*

> "Para o Marcos, some assinar sem conferir. Para começar, preciso só de acesso de leitura às fontes, e na segunda eu já rodaria no próximo lote, só segurando e avisando. Para o tesoureiro que assina R$ 10 milhões sem olhar, o GoGuardian confere tudo, e ele só aprova as exceções. Obrigado."

---

## Sabatina (5 min)
*Regras: diga "Boa pergunta…" e respire 2 s. Responda só o que foi perguntado. Se não souber: "não cheguei lá ainda, mas o próximo passo seria…". Nunca contradiga; redirecione.*

| Se perguntarem… | Responda |
|---|---|
| E quando a IA erra? | "Ela nunca libera nada, só reforça uma regra. Se a resposta vem estranha ou com baixa confiança, vai para uma pessoa com o motivo." |
| O que você fez e o que a IA fez? | "Eu defini as regras, o gabarito e as decisões. A IA escreveu código, e eu peguei os erros dela. Está tudo no decisoes.md." |
| O que falta para funcionar de verdade? | "Acesso de leitura ao ERP, NF-e, DDA e e-mail, e calibrar as regras com os dados reais." |
| Lançar no ERP não é arriscado? | "Exige acesso de escrita, por isso começa só lendo e segurando. Lançar vem depois, com aprovação." |
| Como medir o sucesso? | "R$ que seriam indevidos e ficaram fora do lote, % de títulos conferidos e quantos alarmes falsos chegam a uma pessoa." |
| E os R$ 466 mil × R$ 483 mil? | "483 mil ficaram fora do lote; desses, 466 mil sairiam errado. O resto é o que o agente segurou para conferir." |

## Cola rápida dos números
876 títulos · R$ 10,2 mi · R$ 483 mil fora · R$ 466 mil indevidos · 49 títulos em 21 casos · 15 avisos · 85% → 100% em 26 casos · e-mails 97–100% · US$ 0,0059 · Embalarte R$ 194 mil · Maciez R$ 4.750 · ~8 min → 30 s (estimativa)
