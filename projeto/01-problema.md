# 01 · Problema

## Parte 1 — Triagem (`/triagem`, até 20 min)

| # | Desafio | Dor aparente | Impacto | Agêntico | Viável até 16h30? | Replicável? |
|---|---|---|---|---|---|---|
| 1 | Atendimento ao Cliente | Milhares de contatos/mês (WhatsApp, e-mail, Reclame Aqui) tratados à mão; cada um passa por vários sistemas; há avaria falsa | alto | alto | sim | sim |
| 2 | Pagamentos | Volume alto sem conferência individual; cadastro manual repetido gera duplicidade e valor errado; dado espalhado entre sistemas e bancos | alto | médio-alto | sim | sim |
| 3 | Transportes | Várias transportadoras em portais diferentes; prazo do site precisa vender sem quebrar SLA; visão por CEP e concorrência montada à mão | alto | médio | arriscado | parcial |

> Fonte: página de desafios do evento. Notas de impacto/agêntico/viabilidade são avaliação do agente produto, sem número da empresa ainda → `[HIPÓTESE]` até a descoberta com o mentor.

**Recomendados:**
1. **Atendimento** — melhor encaixe em Modelagem (40%): o agente age nos sistemas (consulta pedido, portal da transportadora, abre troca/reenvio), decide sozinho os casos simples e "levanta a mão" nos suspeitos (avaria falsa). Dor fácil de entender em 1 min (Conceito) e mora no WhatsApp, como a página pede. Divisão código/IA/humano é natural: regra de elegibilidade no código, IA lê a mensagem, humano só vê exceção.
2. **Pagamentos** — muito forte em "código para regra": duplicidade e "zero a mais" são checagens determinísticas, fáceis de testar com pytest e eval; o momento de ação é claro (barrar antes de o dinheiro sair) e a aprovação humana por exceção é óbvia. Risco: o papel da IA é menor (ler boleto/NF, explicar o motivo do bloqueio), então é preciso deixar claro na demo onde está a autonomia.

Transportes ficou fora: tende a virar painel/análise (o que a página diz que **não** é agente) e depende de dados de concorrência e performance por CEP difíceis de simular até 16h30.
**Escolhido:** Pagamentos · **Motivo:** escolha do Mateus; regras checáveis (duplicidade, valor fora do padrão) dão base forte de código + testes, e o ponto de ação é claro: barrar antes de o dinheiro sair · **Plano B:** Atendimento ao Cliente

## Parte 2 — Descoberta (`/descoberta`)

**As 3 perguntas da dor**
1. Qual é a parte mais frustrante disso hoje?
2. Como vocês contornam isso hoje?
3. Se pudessem mudar uma coisa, o que mudariam?

**Perguntas extras (máx. 12)**
- Pessoas: quem faz, quantas pessoas, quem sofre com o resultado?
- Processo: passo a passo de hoje, ferramentas, onde trava?
- Volume e custo: quantas vezes, quanto tempo cada, % de retrabalho, quanto custa?
- Dados: de onde vêm, tem um exemplo agora?
- Sucesso: o que é "bom o suficiente"? Qual número mover?
- Restrições: o que não pode dar errado? Dado sensível?
- Replicabilidade: outras marcas/áreas têm o mesmo problema?

**Anotações**
| Tema | Fato | Número | Fonte |
|---|---|---|---|
| | | | mentor / base / site |

**Hipóteses:** `[HIPÓTESE]` ___
**O que poderia invalidar a ideia:** ___
**Em aberto:** ___

## Parte 3 — Definição (`/problema`)

**Mapa de dores** — `score = (Agêntico×0,4 + Conceito×0,3 + Dados×0,3) × 20` · viabilidade < 3 elimina

| # | Dor | Agêntico | Conceito | Dados | Viabilidade | Impacto × Esforço | Score |
|---|---|---|---|---|---|---|---|
| 1 | | | | | | alto/baixo | |
| 2 | | | | | | | |
| 3 | | | | | | | |

**Em uma linha:** 1 problema: ___ · 1 usuário-chave: ___ · 1 hipótese: ___

**Problema com número:** "[persona] perde [tempo] por [período] fazendo [tarefa], e [N%] volta por [motivo]."

**Menor experimento que valida a hipótese:** ___

**Métrica**
| Métrica | Hoje | Alvo |
|---|---|---|
| Processo | | |
| Negócio | | |

**Escopo:** Dentro: ___ · Fora (vira "próximos passos"): ___

**Critérios de aceite** (cada um vira teste ou caso de eval)
- [ ] Dado ___, o sistema ___.
- [ ] Nenhuma saída aprovada viola ___.
- [ ] O humano vê só as exceções, com o motivo.

**MVP pronto quando:** problema definido · fluxo funcional · demonstrável · resultado mensurável.
