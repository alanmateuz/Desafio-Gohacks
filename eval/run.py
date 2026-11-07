"""Mede a taxa de acerto da solução num conjunto de casos com gabarito.

Uso:  python eval/run.py            (usa eval/casos.json)
      python eval/run.py outro.json

Para cada caso: chama resolver(entrada) de src/solucao.py, confere a saída com as
checagens do caso (código puro, sem IA) e no fim mostra a taxa e as falhas por causa.

Checagens disponíveis (use só as que fizerem sentido no caso):
  esperado              {"campo": "valor"}       o campo precisa ter exatamente esse valor
  campos_obrigatorios   ["campo", ...]           o campo existe e não está vazio
  max_caracteres        {"campo": 60}            limite de tamanho
  deve_conter           {"campo": ["termo"]}     o termo aparece
  nao_deve_conter       {"campo": ["termo"]}     o termo não aparece
"""
import json
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from solucao import resolver  # noqa: E402


def texto(valor) -> str:
    return json.dumps(valor, ensure_ascii=False) if isinstance(valor, (dict, list)) else str(valor or "")


def checar(checagens: dict, saida: dict) -> list[str]:
    erros = []
    for campo, valor in checagens.get("esperado", {}).items():
        if saida.get(campo) != valor:
            erros.append(f"errou_{campo}:{saida.get(campo)}")
    for campo in checagens.get("campos_obrigatorios", []):
        if not saida.get(campo):
            erros.append(f"campo_faltando:{campo}")
    for campo, limite in checagens.get("max_caracteres", {}).items():
        if len(texto(saida.get(campo))) > limite:
            erros.append(f"limite_excedido:{campo}")
    for campo, termos in checagens.get("deve_conter", {}).items():
        for termo in termos:
            if termo.lower() not in texto(saida.get(campo)).lower():
                erros.append(f"faltou_termo:{campo}:{termo}")
    for campo, termos in checagens.get("nao_deve_conter", {}).items():
        for termo in termos:
            if termo.lower() in texto(saida.get(campo)).lower():
                erros.append(f"termo_proibido:{campo}:{termo}")
    return erros


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    arquivo = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "eval" / "casos.json"
    casos = json.loads(arquivo.read_text(encoding="utf-8"))["casos"]

    acertos, causas = 0, Counter()
    for caso in casos:
        try:
            erros = checar(caso.get("checagens", {}), resolver(caso["entrada"]))
        except Exception as e:  # erro da solução conta como falha, não derruba a avaliação
            erros = [f"excecao:{type(e).__name__}"]
        if erros:
            print(f"FALHOU {caso['id']}: {', '.join(erros)}")
            causas.update(e.split(":")[0] for e in erros)
        else:
            print(f"ok     {caso['id']}")
            acertos += 1

    print(f"\nTaxa de acerto: {acertos}/{len(casos)} ({acertos / len(casos):.0%})")
    if causas:
        print("Falhas por causa:")
        for causa, n in causas.most_common():
            print(f"  - {causa}: {n}")


if __name__ == "__main__":
    main()
