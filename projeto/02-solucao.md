# 02 · Solução

**Em uma frase:** "Um agente de IA que [ação], para que [resultado]."

## Hoje × novo
```
Hoje:  [passo 1] → [passo 2] → [passo 3 = fricção] → [passo 4]
Novo:  entrada → código valida → IA [faz o quê] → código confere → ok: segue | exceção: humano (com motivo)
```

## Código / IA / humano
| Parte | Quem faz | Por quê |
|---|---|---|
| | Código | é regra checável |
| | IA | exige linguagem ou julgamento |
| | Humano | só exceção / palavra final |

**Por que workflow e não agente autônomo (ou o contrário):** ___

## Contrato de dados
Entrada:
```json
{}
```
Saída (schema que o código valida):
```json
{}
```
Limite de tentativas: ___ · Fallback: vai para o humano com o motivo.

## Quanto a IA economiza
Passo substituído: ___ · Antes: ___ min · Depois: ___ min · Volume: ___ /semana

## Replicabilidade
Trocar de marca/canal = trocar o arquivo `config/___`.

## Riscos
| Risco | Mitigação |
|---|---|
| IA inventa dado | código confere contra a entrada |
| JSON inválido / API fora | retry com limite + modo simulado + humano |
| Dados de clientes (LGPD) | só o necessário vai ao modelo, anonimizado |
| Custo | tokens × chamadas × volume = ___ |

## Stack
Backend: ___ · IA: ___ · Interface: ___ · Deploy: ___
