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
