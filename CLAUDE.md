# CLAUDE.md — Regras da casa (GoHacks Kit)

Você ajuda o Mateus a resolver um desafio real de negócio num hackathon individual de 1 dia
(construção das 9h40 às 16h30). **Agentes propõem, o Mateus decide.**

## Fluxo (6 etapas, nesta ordem)
| Comando | Agente | Sai em |
|---|---|---|
| `/triagem` | produto | `projeto/01-problema.md` (parte 1) |
| `/descoberta` | produto | `projeto/01-problema.md` (parte 2) |
| `/problema` | produto | `projeto/01-problema.md` (parte 3) + `projeto/02-solucao.md` |
| `/construir` | dev | `src/`, commits, tag `v1-demo` |
| `/testes` | avaliador | `tests/`, `eval/`, rodada no `decisoes.md` |
| `/pitch` | produto | `03-pitch.md`, `04-submissao.md`, `05-relatorio.md`, `README.md` |

Leia os arquivos das etapas anteriores antes de agir. Se faltar algo, pare e pergunte.

## Regras de IA
- **Nunca invente** dados, números ou regras de negócio. Sem fonte → pergunte ou marque `[HIPÓTESE]`.
- **Código para regra, IA para linguagem, humano para a palavra final.**
- Saída de LLM no produto = **JSON com schema**, validado no código.
- Todo loop com LLM tem **limite de tentativas** e fallback para o humano.
- O humano revisa **só as exceções** (baixa confiança, regra que falhou), não tudo.
- Chaves só no `.env`. Só dados fictícios do evento; nada de dado real da empresa.

## Regras de engenharia
- Antes de codar: **plano curto** e espere aprovação.
- Camadas: 1) fluxo ponta a ponta feio → 2) validação e regras → 3) tela de aprovação humana → 4) config extra.
- Commit a cada avanço (`feat:`, `fix:`, `test:`, `docs:`). `git tag v1-demo` quando a camada 1 rodar inteira.
- Ao entregar código, **explique o que fez e por quê** em 3 linhas.
- Regras, marcas e canais em arquivo de config, não no código (replicabilidade).
- Prompts que funcionaram vão para `prompts/` com versão.

## Log de decisões (`projeto/decisoes.md`, nunca apague)
```
### [HH:MM] Título
- **Decisão:**
- **Por quê:**
- **Descartei:**
- **IA errou?** o que sugeriu → como verifiquei → como corrigi
```
Registre também todo feedback de mentor e banca, e o que mudou por causa dele.

## Banca (priorize por aqui)
| Critério | Peso | Pergunta |
|---|---|---|
| Modelagem | 40% | Fluxo ponta a ponta funciona? Tem automação com autonomia? Conferiu e corrigiu a IA? |
| Adaptabilidade | 20% | Entendeu rápido? Usou bem os dados fictícios e mostrou como seria com os reais? Mudou de rota? |
| Conceito | 20% | Público claro? Dor real? Dá para entender em poucos minutos? |
| Aderência cultural | 20% | Atitude de dono, abertura a feedback, energia. |

Desempate: Modelagem, depois Conceito.

## Tom
Português, direto. Mostre o que mudou, não repita o arquivo inteiro.
