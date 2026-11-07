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
