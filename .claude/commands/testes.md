---
description: 5. Teste e validação — gabarito, pytest, eval, erros por causa
---
Use o agente **avaliador**. Leia `projeto/01-problema.md` (critérios de aceite) e `projeto/02-solucao.md`.

1. Liste as regras de negócio e **peça a confirmação do gabarito**. Não invente expectativa.
2. Escreva/atualize `tests/test_regras.py` para as regras determinísticas.
3. Escreva/atualize `eval/casos.json` com pelo menos os 3 casos de borda:
   dado faltando, texto estranho, tentativa de burlar a regra.
4. Rode `pytest -q` e `python eval/run.py`. Mostre os vermelhos agrupados por causa
   e onde está cada causa (prompt, código, schema, dado).
5. Não altere teste só para passar.
6. Registre em `projeto/decisoes.md`: rodada N, taxa antes → depois, o que a IA errou.
7. Lembre de exportar a tabela antes → depois para "Outros materiais" da submissão.

Foco opcional: $ARGUMENTS
