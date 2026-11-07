# GoHacks Kit

Kit para o GoHacks: 6 etapas, 3 agentes, 6 documentos. **Agentes propõem, você decide.**

## Fluxo no dia
```
/triagem <cole os desafios>     → escolha 1 (até 10h)
/descoberta                     → perguntas para o mentor
/descoberta <cole as anotações> → fato × hipótese, o que invalida a ideia
/problema                       → 1 problema · 1 usuário · 1 hipótese → aprova → solução → aprova
/construir                      → camada 1, 2, 3, 4 (aprova cada plano; commit a cada avanço)
/testes                         → gabarito → pytest + eval → taxa e erros por causa
/pitch                          → submissão, 8 slides, roteiros, relatório, README
```

| Agente | Etapas |
|---|---|
| produto | triagem, descoberta, problema e solução, pitch |
| dev | construção em camadas |
| avaliador | testes (aponta o erro, nunca corrige) |

## Começando no notebook do evento
```bash
git clone <url-deste-repo> meu-projeto
cd meu-projeto
cp .env.example .env
pip install pytest
python eval/run.py
pytest -q
claude
```
O `eval/run.py` deve mostrar **3/4 (75%)**: o stub falha de propósito no caso de texto estranho,
para você ver como uma falha aparece. É o primeiro "erro da IA" que o eval pega.

## Estrutura
```
CLAUDE.md            regras da casa (lida por todo agente)
.claude/agents/      produto, dev, avaliador
.claude/commands/    triagem, descoberta, problema, construir, testes, pitch
projeto/             01-problema · 02-solucao · 03-pitch · 04-submissao · 05-relatorio · decisoes
prompts/             prompts que funcionaram, com versão
eval/                casos.json (gabarito) + run.py (taxa de acerto) + promptfoo/ (opcional)
src/                 solucao.py (resolver) + regras.py (código para regra)
tests/               pytest das regras
CHECKLIST.md         checklist do dia, para o celular
```

## Dois tipos de teste
- **pytest** testa o código: regra determinística, passa ou falha.
- **eval** mede a IA: taxa de acerto num conjunto de casos com gabarito, e falhas agrupadas por causa.

## Regras de ouro
1. Agentes propõem, você decide.
2. Código para regra, IA para linguagem, humano para a palavra final.
3. Gabarito antes do código; meça depois de cada camada.
4. Commit a cada avanço; `git tag v1-demo` quando a camada 1 rodar inteira.
5. Código congelado às 15h30; submissão até 16h30.
