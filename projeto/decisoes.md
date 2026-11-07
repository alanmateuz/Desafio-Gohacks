# Log de decisões

Todo agente (e o Mateus) acrescenta aqui. Nunca apague. É a matéria-prima do relatório.

<!-- Formato:
### [HH:MM] Título
- **Decisão:**
- **Por quê:**
- **Descartei:**
- **IA errou?** o que sugeriu → como verifiquei → como corrigi
-->

### [09:46] Triagem — desafio escolhido: Pagamentos
- **Decisão:** Desafio 2 (Pagamentos). Plano B: Desafio 1 (Atendimento ao Cliente).
- **Por quê:** escolha do Mateus. Pagamentos tem regras checáveis no código (duplicidade, "zero a mais", dado cadastrado errado), fáceis de provar com pytest e eval, e um momento de ação claro: barrar antes de o dinheiro sair, com aprovação humana só nas exceções. Ponto de atenção: deixar explícito na demo onde está a autonomia do agente e o papel da IA (além das regras).
- **Descartei:** Transportes (tende a virar painel/análise e depende de dados de concorrência e performance por CEP difíceis de simular até 16h30). Atendimento ficou como plano B (agente recomendou como 1ª opção por Modelagem e Conceito).
- **IA errou?** não se aplica nesta etapa. Notas da tabela de triagem são avaliação do agente, ainda `[HIPÓTESE]` até a descoberta com o mentor.

### [10:15] Mudança de rota: desafio fictício com base de dados do evento
- **Decisão:** o desafio de Pagamentos passa a ser um cenário simulado (Gogroup fictício, 02/11 a 09/11/2026) com as bases enviadas pela organização, baixadas em `dados/`. O que faltar será inventado e marcado como `[HIPÓTESE]`.
- **Por quê:** a organização mudou o formato. As perguntas de descoberta para o mentor ficam como apoio, mas a fonte principal passa a ser `dados/parametros.md` e `dados/dicionario_de_dados.md`.
- **Descartei:** —
- **IA errou?** —

### [10:40] Problema definido
- **Decisão:** problema: "O volume de pagamentos é tão grande que o processo vira manual e impossível de revisar, abrindo espaço para golpes e perda de dinheiro." Usuário-chave: Marcos Teles, tesoureiro, que assina o lote. A prova de conceito é um "guardião do lote", que confere cada título antes do fechamento.
- **Por quê:** as dores 1 (troca bancária fraudulenta, score 100) e 2 (duplicidade, score 92) são as maiores em R$ e acontecem no mesmo momento (título na fila antes do fechamento), junto com as 3 vias e a alçada.
- **Descartei:** para a prova de conceito, ficaram fora a triagem de e-mails, a conciliação de extrato e a auditoria de login. Viram próximos passos da visão 360°.
- **IA errou?** O agente escreveu a frase do problema; o Mateus reescreveu com as próprias palavras, mais focadas em volume e golpe.

### [11:00] Desenho da solução: Guardião do lote com painel
- **Decisão:** a solução junta as fontes espalhadas (ERP, Compras, NF-e, DDA, bancos, e-mail) numa **planilha mãe**. As regras em código conferem cada título, o que está limpo vai para a **planilha final do lote** que o Marcos assina, e as exceções saem do lote e vão para a pessoa certa. Tudo acontece num **painel** (planilha mãe, exceções, lote final), e outras telas serão pensadas depois.
- **Por quê:** era a ideia do Mateus. O agente propôs que a IA só leia e-mails e boletos e escreva o motivo, enquanto a decisão de liberar fica com o código ou a pessoa (código para regra, IA para linguagem, humano para a palavra final).
- **Descartei:** "automatizar lançamentos" no sentido de lançar títulos a partir do XML. O Mateus esclareceu que quis dizer coletar das fontes e montar a planilha final. Descartei também a IA decidindo sozinha.
- **IA errou?** O agente entendeu "lançamentos" como lançar títulos no ERP. O Mateus corrigiu: era a coleta das plataformas até a planilha final.

### [11:45] Camada 1 rodando ponta a ponta (v1-demo)
- **Decisão:** coletor → planilha mãe → 2 regras em código (troca bancária sem confirmação, duplicidade por NF normalizada + fornecedor + parcela) → resolver → painel Streamlit (planilha mãe, exceções, lote final). Motivo escrito em modo simulado, sem IA.
- **Resultado:** fila inteira com 876 títulos e R$ 10.206.764,09. Seguem 838 (R$ 9.907.060,39); retidos 38 (R$ 299.703,70), sendo 25 por troca bancária (R$ 194.440,08, todos da Embalarte) e 13 por duplicidade (R$ 105.263,62). No lote `RM20261103-MER` (192 títulos), 6 foram retidos, entre eles os 2 da Embalarte e o TP430006 da Maciez; o TP429834 seguiu. pytest 6/6, eval 5/5.
- **Descartei:** por enquanto, 3 vias, alçada e IA real (ficam para a camada 2).
- **IA errou?** Na análise inicial, o agente contou 67 "grupos com mesmo fornecedor e valor" como possíveis duplicidades. Ao comparar NF normalizada **e parcela**, sobraram 13, porque parcelas legítimas têm o mesmo valor. Ainda falta conferir os 13 no gabarito.
