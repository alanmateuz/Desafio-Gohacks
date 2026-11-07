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

### [10:51] Cadastro: agente pré-preenche, analista confere
- **Decisão:** responder ao "cadastro manual em vários sistemas" do desafio. O agente lê NF-e do portal + duplicata + OC e monta o título **pré-preenchido**; o analista confere e confirma, **sem digitar**. Lançamento 100% automático (sem confirmação humana) fica para fase futura (plano 360° / pitch).
- **Por quê:** os erros mais caros nascem na digitação (NF em formatos diferentes, "zero a mais", fornecedor errado). Pré-preencher ataca a causa; o guardião continua pegando o que escapar.
- **Regras:** fonte só NF-e do portal. Boleto por e-mail **não** gera título (vetor do golpe Embalarte, da 2ª via falsa da Pigmentos Aquarela e das injeções). Todo título criado passa pelo guardião como qualquer outro (quem cadastra não libera).
- **Prioridade:** camada opcional, só se as camadas 1 a 3 estiverem prontas até ~14h; senão entra no pitch com tela mockada. `ferramentas.csv` **não tem** ferramenta de criar título (só `corrigir_lancamento` e `agendar_titulo`), então na demo a confirmação gera um rascunho `[HIPÓTESE]`, não um lançamento real no ERP.
- **Descartei:** boleto por e-mail como fonte de pré-preenchimento.
- **IA errou?** —

### [11:10] Verificação da camada 1 (avaliador): 13 duplicidades e 25 Embalarte certos, mas ~R$ 166 mil passam
- **Como verifiquei:** rodei `guardiao.py` com as bases do Drive (resultado idêntico ao do dev: 876 títulos, 38 retidos, pytest 6/6, eval 5/5) e cruzei a fila com `nf_duplicatas.csv`, `notas_fiscais.csv`, `dda_boletos.csv`, `alteracoes_cadastro.csv`, `comunicacoes_fornecedores.csv` e `usuarios_sistema.csv`.
- **O que está certo:**
  - **13 duplicidades: todas reais.** Mesmo padrão: um título TED lançado do XML do portal + um boleto lançado do e-mail por outra pessoa, NF digitada diferente, mesma parcela, uma só NF no portal. Nenhum refaturamento; em nenhum o original já estava pago. A regra mantém o TED e retira o boleto (correto). Em 3 pares o boleto tem R$ 3,50–4,50 a mais que a duplicata (TP432119, TP430389, TP432847): manter o TED paga o valor certo.
  - **25 Embalarte: todos TED para 905/0001/4471203-9.** Nenhum boleto, nenhum falso positivo.
  - **Trocas bancárias:** as 4 confirmadas (Cartonart, Polyfilm, Evoluir, Magnetec) usaram o telefone de antes da troca, e nenhum desses telefones mudou. Sem falso negativo por TED/pix.
  - **`normalizar_nf`** cobre todos os formatos da fila; não há duplicidade com fornecedor_id diferente.
- **O que passa sem ser visto (falsos negativos):**

  | Furo | Títulos | R$ | Regra que pega |
  |---|---|---|---|
  | **"Zero a mais"** (valor 10× a duplicata) | TP431459 (lote 05/11), TP431775 (06/11), TP431536 (09/11) | **132.232,50 a mais** | título × duplicata (R$ 0,10) |
  | **Fornecedor errado** (nome parecido) | TP431946 lançado na Cartonart, NF é da Gráfica Cartonar (FP6799); TP432337 lançado na Polyfilm, NF é da Polifilm (FP3302) | 22.250,50 para a empresa errada | raiz do CNPJ da NF × fornecedor |
  | **Boleto golpe (2ª via falsa)** | TP431754 Pigmentos Aquarela, **lote `RM20261103-MER`, sai 03/11 10h**. E-mail de `cobranca.pigmentosaquarela@outlook.com` (29/10); CNPJ do beneficiário 61.525.615/0001-26 ≠ 20.623.234 do fornecedor. Banco 368 = banco do cadastro, então só o CNPJ pega | 11.740,00 | CNPJ do beneficiário do boleto |
  | "Zero a menos" (valor ÷10) | TP431634, TP433092, TP432245, TP432623, TP432136 | paga a menos; o resto atrasa | título × duplicata → `corrigir_lancamento` |

- **Padrão:** os 8 erros de vírgula **e** os 2 de fornecedor errado foram lançados pelo **usuario_07** (Gabriel Antunes, analista júnior), o mesmo que trocou a conta da Embalarte sem confirmação. Ele lançou 94 títulos da fila → caso para `abrir_incidente` e `propor_correcao_processo`.
- **Problemas de ação (afetam o placar):**
  - Duplicidade usa `retirar_do_lote`, que devolve o título para `aberto`, e ele pode voltar a outro lote. O certo é `cancelar_titulo` (analista até R$ 5 mil; acima, `solicitar_aprovacao`).
  - Embalarte: retirar os 25 custa **~R$ 24,3 mil** de atraso (multa 2% + juros 7 dias + R$ 800 × 25), porque a dívida é legítima. Melhor: `reverter_alteracao_cadastro` (aprovação dupla) e pagar no prazo na conta antiga 774/7166/9517944-5.
  - O código aciona PS01 **por título** (25 acionamentos para um caso só). O certo é 1 acionamento por fornecedor/caso.
  - A regra de troca confia só em `confirmacao_registrada = sim`. Não confere em `confirmacao_como` se o telefone era o anterior à troca e se não mudou há < 30 dias. Sem efeito nos dados de hoje, mas fica abaixo da política.
  - Há 21 pares duplicados ainda em `aberto` (R$ 162,8 mil, as próximas parcelas dessas mesmas NFs). O guardião precisa rodar de novo a cada tique.
- **Para o 360° / pitch (fora da prova de conceito):**
  - 55 grupos de duplicidade **já pagos** (~R$ 407,7 mil, a confirmar): recuperação com o controller (PS09).
  - Trocas de e-mail sem confirmação (ex.: FP9180 → `contasareceber@gmail.com`) preparam o próximo golpe por boleto.
- **IA errou?**
  1. O `contexto.md` dizia "~500 títulos do usuario_02 depois do desligamento" → em `contas_a_pagar.csv` são **7**, e **nenhum na fila**. A dor 7 cai; o padrão de risco real é o usuario_07.
  2. O plano da camada 1 deixou título × duplicata e raiz do CNPJ para a camada 2 como "menos prioritários" → é ali que está a maior perda não vista (R$ 132 mil, mais que as 13 duplicidades juntas).
  3. O eval 5/5 foi escrito pelo próprio agente dev, sem gabarito → passa, mas não cobre nenhum dos 6 furos. 100% no eval ≠ seguro.
  4. A análise inicial chamou Cartonart e Polyfilm só de "trocas legítimas para comparar" → são também os fornecedores que recebem os títulos lançados no fornecedor errado.
- **Decisão (Mateus):** trazer 3 regras para a camada 1 (título × duplicata, raiz do CNPJ da NF, CNPJ do beneficiário do boleto) e corrigir as ações (cancelar duplicidade, 1 acionamento por caso). Implementação com o outro Claude; especificação no `contexto.md`.
