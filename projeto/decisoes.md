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

### [10:47] Camada 1 rodando ponta a ponta (v1-demo)
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

### [11:23] Camada 1.1: título × duplicata, fornecedor errado, beneficiário do boleto, ação por caso
- **Decisão:** o coletor junta NF (raiz do CNPJ + número) e duplicata (parcela). Entram 4 regras novas: `valor_diferente_duplicata`, `nf_de_outro_fornecedor`, `sem_nf_no_portal` e `boleto_beneficiario_diferente`. Cada exceção recebe uma ação proposta de `ferramentas.csv`: duplicidade → `cancelar_titulo`; troca bancária → `reverter_alteracao_cadastro`; valor ou fornecedor errado → `corrigir_lancamento`; boleto → `contatar_fornecedor`. Os títulos são agrupados por caso (fornecedor + regra) e há 1 acionamento por caso, com a PS03 no lugar da PS01 quando o caso passa de R$ 50 mil. O painel mostra 1 card por caso.
- **Resultado:** na fila inteira, **49 retidos** (R$ 483.642,28) em **21 casos**, sendo que só **13 precisam de uma pessoa**; os outros 8 ficam dentro da alçada do analista. No lote `RM20261103-MER`, **7 retidos** (os 6 de antes + TP431754, o boleto golpe) em 6 casos, com 3 acionamentos. Bate exatamente com a previsão da verificação das 11:10. pytest 21/21 (inclui um teste de integração na fila real com os 6 furos) e eval 10/10.
- **Descartei:** conferir `confirmacao_como` (sem efeito nos dados de hoje), reprocessar a cada tique, IA real (camada 2) e botões de aprovação (camada 3).
- **IA errou?**
  1. O dev escreveu `abs(valor − duplicata) > 0,10`. Em ponto flutuante, 1000,10 − 1000,00 = 0,1000000000000227, e uma diferença de exatamente 10 centavos, que a política aceita, seria barrada. Um teste novo pegou o erro; a correção foi arredondar a diferença para centavos.
  2. Os casos 01 e 05 do eval falharam depois da mudança, porque foram escritos sem as colunas da NF. O guardião acertou ao acionar quem não tem NF no portal; a entrada dos casos foi atualizada para o formato novo.
- **Ainda é gabarito do dev, não do Mateus.** O /testes precisa confirmar.

### [11:57] /testes, rodada 1 da IA: leitura de e-mails com o Jev (AI Proxy)
- **Decisão:** a IA é o **Jev** do AI Proxy do evento (`/v1/systemone`), e não o Claude, porque o token liberado é do proxy, no formato OpenAI. Ele responde 3 perguntas sobre o texto: pede troca de conta?, tenta dar ordem ao agente? e tipo. Banco, conta e CNPJ citados ficam com o código. A saída é validada contra um schema, com até 2 tentativas; se falhar, vai para uma pessoa. Confiança abaixo de 0,7 → revisão. Prompt em `src/leitor_email.py` (`ler_email_v1`).
- **Gabarito:** `eval/gabarito_emails.csv`, com 30 e-mails (25 da base e 5 inventados e marcados), **confirmado pelo Mateus**. Ponto 1 (a 2ª via falsa da Pigmentos é `cobranca`: quem pega é o código) e ponto 2 (o falso cartório não instrui o agente) aceitos. O ponto 3 (INV004) é verificado com um par no cadastro: confirmada → segue; sem confirmação → retida.
- **Resultado (4 repetições sem cache):**

  | Pergunta | Acerto |
  |---|---|
  | pede troca de conta | 30/30 nas 4 |
  | tenta instruir o agente | 30/30 nas 4 (inclui a injeção disfarçada e a em inglês) |
  | tipo | 29 ou 30/30: só o falso cartório (EM570998) oscila entre `phishing` e `cobranca` |
  | e-mails 100% certos | 97–100% |

  O EM570998 tem confiança de ~0,4 em todas as rodadas, então **sempre vai para revisão humana**. O erro da IA nunca vira decisão.
  Custo: US$ 0,0008 por rodada de 30 e-mails.
- **Descartei:** reescrever a pergunta só para acertar o EM570998. Com 30 casos, seria decorar o teste (overfitting). No lugar, a regra em código "remetente com domínio fora do cadastro" pega esse e-mail sempre, junto com os outros 4 domínios falsos.
- **IA errou?**
  1. O Jev oscila no falso cartório → percebi rodando 4 vezes → a confiança baixa já manda para revisão, e o código vai pegar pelo domínio.
  2. O dev (agente) errou o cache: com `--sem-cache`, o arquivo era regravado só com a última leitura → percebi porque uma leitura que devia vir do cache chamou o Jev de novo → corrigido para sempre carregar o cache antes de gravar.
  3. A primeira chamada ao Jev deu 403 (o Cloudflare bloqueia o User-Agent padrão do Python) → corrigido com um User-Agent próprio.

### [12:08] /testes, rodada 2: IA ligada às regras (camada 2) e gabarito de 26 casos
- **Decisão:** a caixa de e-mail é ligada ao fornecedor pelo código (endereço ou domínio do cadastro, nome ou CNPJ citado; domínio parecido → `dominio_parecido`; nome sem domínio do cadastro → `remetente_fora_do_cadastro`). A leitura do Jev **só reforça** uma regra que já disparou (`pedido_troca_por_email_suspeito`, `boleto_de_email_fora_do_cadastro`) e gera **alertas da caixa** (phishing → PS08 jurídico; tentativa de instruir o agente → PS01), sem reter título limpo.
- **Alçada (mudança no gabarito, por causa dos dados):** nenhum dos 876 títulos da fila tem aprovação, e isso é o normal: 2.669 de 2.760 aprovações em `aprovacoes.csv` são "em lote" no dia do pagamento. Reter acima de R$ 5 mil sem aprovação seguraria 533 títulos legítimos. Por isso a alçada virou **roteamento** (514 títulos para o aprovador e 19 para a diretora PS03 no lote) e só **fracionamento** retém (0 casos na fila; a regra é testada no eval).
- **Resultado:** gabarito de 26 casos (21 confirmados + par INV004 + 3 de evidência da IA): **antes 22/26 (85%) → depois 26/26 (100%)**. Na fila inteira continuam **49 retidos**: a IA não mudou nenhuma decisão, só acrescentou evidência a 26 títulos (Embalarte e Pigmentos) e 2 alertas da caixa. Acionamentos: 15 (13 casos de título + 2 alertas). Leitura dos 246 e-mails: US$ 0,0059, 0 falhas depois da nova tentativa. pytest 25/25, incluindo o teste de segurança "a IA nunca libera o que as regras seguraram".
- **Tabela antes → depois:** `eval/antes_depois.csv` (para "Outros materiais" da submissão).
- **Descartei:** a IA escrevendo o motivo com o chat (`latest`). O motivo continua montado pelo código a partir dos fatos, sem risco de inventar; o chat pode reescrever no painel depois, se houver tempo.
- **IA errou?**
  1. Na 1ª leitura dos 246 e-mails, 1 falhou (EM570938, falha passageira no proxy compartilhado) → foi para revisão, não liberou nada → na nova tentativa leu certo (confiança 0,96).
  2. O agente havia proposto a alçada como "reter sem aprovação" → os dados mostraram que a aprovação é em lote no dia → corrigido para roteamento, com o Mateus avisado.

### [12:38] Painel com a identidade Gogroup (camada 3 incluída)
- **Decisão:** painel Streamlit com tema próprio, seguindo o brandbook: azul `#2659a5` como protagonista, Poppins, pílulas, blocos de cantos arredondados (color blocking azul + limão com texto escuro) e logo oficial recortado do brandbook (`assets/`). Telas, na ordem da tarefa: visão do lote (próximo envio, "precisa da sua decisão", 4 números), **Exceções** (1 card por caso, com evidência do e-mail e os botões da ação proposta / "Liberar mesmo assim" / desfazer), **Caixa de e-mail** (246 leituras da IA, suspeitos pelo código, revisão), **Planilha mãe** (busca e filtros) e **Lote final** (o que vai ao banco, aprovação necessária e CSV). As decisões ficam em `dados/decisoes_humanas.json` (`src/decisoes_humanas.py`).
- **Por quê:** o Mateus pediu o sistema num painel com a identidade Gogroup, minimalista e profissional, usando as skills de UI/UX (estado sempre com texto + ícone, um botão principal por card, valores em R$ com lote e período, estados vazio, simulado e falha).
- **Descartei:** reescrever em HTML/JS separado (mais bonito, porém sem tempo antes de congelar o código às 15h30).
- **IA errou?** Ao testar o painel, o agente percebeu que, depois de "Aprovar reversão da conta", os títulos da Embalarte voltavam ao lote **com o destino ainda na conta do golpista** (905). Corrigido: o coletor guarda `destino_anterior` (774/7166/9517944-5) e o lote final usa a conta anterior e o valor da duplicata nas correções. Há um teste novo para isso (`test_reversao_paga_na_conta_anterior`). pytest 26/26.

### [13:02] Revisão visual do painel (feedback do Mateus)
- **Feedback:** "precisa de uma revisão visual; as informações monetárias devem ter mais destaque; muitas coisas cortadas ou mal feitas". Ele mandou 2 telas de referência de sistemas de gestão financeira e pediu **sem menu lateral**.
- **Decisão:** barra superior (logo, pílula, status da IA); cabeçalho com o lote e o seletor; **4 KPIs no estilo das referências** (bloco de ícone colorido + **R$ em destaque**: vai ao banco, protegido, precisa de decisão, pessoas acionadas); **navegação por pílulas** (Exceções · Lote final · Caixa de e-mail · Planilha mãe · Resumo da fila), uma seção por vez; cada seção num painel branco com **tabela compacta**, valores alinhados à direita e selos com texto e ícone. Nada cortado: tabelas HTML com quebra de linha; larguras definidas na planilha mãe.
- **Descartei:** menu lateral (o Mateus não quis) e a rolagem de uma página só.
- **IA errou?** A 1ª versão tinha cortes (título quebrando, colunas truncadas) e R$ pequenos → corrigido com o feedback do Mateus e conferido no navegador em 1366 px.

### [13:12] Ações sobre as suspeitas ("CRUD") para o app ser autônomo
- **Pedido do Mateus:** poder agir sobre suspeitas e casos (por exemplo, tirar da contagem final), como um CRUD.
- **Decisão:**
  - **criar:** retirar qualquer título do lote, com motivo (aba Lote final);
  - **ler:** a aba Exceções lista os casos do agente e as retiradas manuais;
  - **atualizar:** aprovar a ação, liberar mesmo assim, **manter fora do lote**, nota e responsável;
  - **excluir:** desfazer uma decisão, **desfazer uma ação automática do agente** (o caso volta para uma pessoa) e devolver o título ao lote.

  Tudo grava quem e quando em `dados/decisoes_humanas.json` (`src/decisoes_humanas.py`). O agente continua resolvendo sozinho o que está dentro da alçada do analista, mas qualquer ação dele pode ser revertida no painel. Os testes de unidade passaram (pytest 28/28).
- **IA errou?** Os horários dos registros [11:45], [12:20], [12:50], [13:20], [14:10] e [14:45] foram **estimados pelo agente e estavam adiantados**. Foram corrigidos para os horários reais dos commits (10:47, 11:23, 11:57, 12:08, 12:38 e 13:02). O conteúdo não mudou.
- **Teste no navegador (13:23):** retirada manual pelo Lote final → 2 títulos selecionados (TP426904 e TP432060; o 2º entrou sem querer pelo Enter do campo de busca) → "Vai ao banco" caiu de R$ 2.206.452,95 para R$ 2.193.073,65 (−R$ 13.379,30, exato) e "Protegido" subiu para R$ 48.410,74 → os 2 apareceram em Exceções › Retiradas manuais → "Devolver ao lote" devolveu o TP426904. Ciclo completo ok. Ajustes: o botão "Retirar do lote" cortava em ~800 px e virou "Retirar"; o campo agora mostra quantos títulos estão selecionados (só um aparecia); o título do lote não quebra mais de linha.

### [13:30] Retirar títulos a partir da Caixa de e-mail + confirmação para liberar fraude
- **Pedido do Mateus:** o "Retirar títulos do lote" deve ficar na Caixa de e-mail, com um atalho em cada linha: clicou no e-mail, o formulário já vem preenchido.
- **Decisão:** a tabela de e-mails tem seleção por linha. Ao clicar, o código sugere os títulos daquele fornecedor que ainda seguem no lote (só os da NF citada no e-mail, se houver) e preenche o motivo com o e-mail, o remetente e o assunto. Se o título da NF já está fora do lote, avisa "nada a retirar". O formulário saiu do Lote final, que agora tem um atalho em texto.
- **IA errou?** Durante o teste no navegador, um clique do agente caiu em "Liberar mesmo assim" no caso da **Pigmentos (boleto falso)**, às 13:27: o golpe voltou ao lote com 1 clique. A decisão de teste foi apagada e, por ser uma ação crítica (skill de UX), **liberar um caso de fraude agora exige confirmação e um motivo escrito**. Também corrigidos: data dos e-mails em formato americano (10/13 → 13/10), seletor de lote cortado ("Banco Meridiano · 0") e rótulos dos KPIs quebrando em tela estreita.

### [13:47] Painel no layout do wireframe do Mateus
- **Pedido:** seguir um wireframe com o lote como título e seletor à esquerda, "GoGuardian / Gogroup" à direita, 4 cartões de números iguais, abas sublinhadas (Exceções · Caixa de e-mail · Planilha mãe · Lote final) e bastante respiro. Usar como guia, não copiar.
- **Decisão:**
  - **Cabeçalho:** o título **é** o seletor de lote, com a seta ao lado; à direita, o nome do produto "GoGuardian", o logo oficial da Gogroup e o status da IA. Saiu a barra superior.
  - **KPIs:** rótulo e ícone pequeno em cima, **valor em R$ grande** embaixo, alinhados à esquerda.
  - **Navegação:** abas sublinhadas, com a ativa em azul; a aba "Resumo da fila" saiu.
  - **Botões dos casos:** em 4 colunas iguais.
  - **Espaçamento** maior entre os blocos.
- **Observação:** o wireframe escreve "GoGroup"; pelo brandbook o certo é **Gogroup**, por isso foi usado o logo oficial.

### [14:10] Skill checkout-form-ux: só o que muda a experiência
- **Pedido do Mateus:** aplicar a skill `checkout-form-ux` apenas no que importa, para adiantar o pitch.
- **Aplicado:**
  1. **Cor com significado:** o KPI "Protegido" passou de vermelho para verde, e o vermelho ficou só para fraude e erro.
  2. **Total consolidado antes de confirmar:** na retirada, aparece "Sai do lote: R$ X · o envio cai de R$ A para R$ B"; ao liberar uma fraude, aparece "R$ X vão para a conta Z".
  3. **Formulário de retirada em coluna única**, com aviso embaixo do campo quando falta o motivo e botão que diz quantos títulos vão sair.
  4. **Data real** com dia da semana no título do lote ("ter, 03/11").
  5. **Botões com altura mínima de 44 px**, a área mínima de toque.
- **Descartado (não se aplica ou tem pouco ganho aqui):** campo de cartão, checkout como convidado, meios de pagamento, troca de listas suspensas por botões de opção.
- **IA errou?** No teste, o primeiro item da lista de títulos é "selecionar todos", e o Enter marcou os 185 títulos. Nada saiu, porque o motivo é obrigatório e o resumo mostrou "o envio cai para R$ 0,00". O caso ficou como argumento de por que o total antes de confirmar importa.

### [15:04] Avisos para a equipe (Slack) e chat no painel
- **Decisão:** `src/notificador.py` manda 1 mensagem por pessoa (Renata, Helena, Lívia, aprovador) só com os casos que esperam a decisão dela; o que o agente resolve na alçada do analista não vai. Não repete: só caso novo ou com valor mudado. Envio automático quando o painel carrega (`config/equipe.json`, `envio_automatico`) e botão "Avisar a equipe". Nova aba **Equipe** mostra o histórico como chat, uma conversa por pessoa.
- **Por quê:** o pedido do Mateus foi "ninguém precisa ficar lendo a tela direto". O aviso chega na pessoa certa, com motivo e ação, e o painel vira o lugar de decidir.
- **Como:** 3 modos pelo `.env`: Slack DM (`SLACK_BOT_TOKEN` + `SLACK_ID_<pessoa>`), webhook (`SLACK_WEBHOOK_URL`) ou simulado (grava em `dados/outbox_slack.jsonl`). Texto montado em código, a IA não escreve na mensagem. 2 tentativas por envio; se falhar, fica "falhou" e volta no próximo aviso. Pessoas e textos de ação no config, não no código.
- **Descartei:** botões "Aprovar" dentro do Slack (exige servidor público para receber o clique), que ficou como próximo passo do slide 8. Também descartei o patch que outro Claude montou numa cópia remota do repositório, porque não chegou aqui (sem push). Refiz localmente, com o chat que ele não tinha.
- **IA errou?** O alerta de phishing saiu com fornecedor "—" no chat. Vi no navegador e troquei para "Caixa de e-mail · remetentes desconhecidos". Os motivos vêm das regras com valor no formato americano (R$ 90,873.80), o que é anterior a esta mudança e fica anotado para corrigir.
- **Resultado:** 15 avisos em 4 mensagens (bate com os 15 acionamentos), 4 testes novos, 32/32 passando.
