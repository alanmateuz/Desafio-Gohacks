"""Eval da leitura de e-mails (IA). Uso: python eval/run_emails.py [--sem-cache]

Compara a leitura do Jev com eval/gabarito_emails.csv (confirmado pelo Mateus)
e mostra acertos por pergunta, erros por causa e o custo da rodada."""
import csv
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))
from leitor_email import ler_email  # noqa: E402

SIM = {"sim": True, "não": False}


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    usar_cache = "--sem-cache" not in sys.argv
    base = {}
    with open(RAIZ / "dados" / "comunicacoes_fornecedores.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            base[r["comunicacao_id"]] = r
    with open(RAIZ / "eval" / "gabarito_emails.csv", encoding="utf-8") as f:
        casos = list(csv.DictReader(f))

    acertos, erros, custo, revisar, causas = Counter(), [], 0.0, 0, Counter()
    for c in casos:
        texto = c["texto_inventado"] if c["origem"] == "inventado" else base[c["id"]]["texto"]
        lido = ler_email(c["remetente"], c["assunto"], texto, usar_cache=usar_cache)
        custo += lido.get("custo_usd", 0.0)
        if "erro" in lido:
            erros.append((c["id"], "falha_leitura", lido["erro"], "", lido.get("fonte")))
            causas["falha_leitura"] += 1
            continue
        revisar += bool(lido["revisar"])
        esperado = {"pede_troca_bancaria": SIM[c["pede_troca_bancaria"]],
                    "tenta_instruir_agente": SIM[c["tenta_instruir_agente"]], "tipo": c["tipo"]}
        for q, v in esperado.items():
            if lido[q] == v:
                acertos[q] += 1
            else:
                erros.append((c["id"], q, lido[q], v, f"conf {lido['confianca']}"))
                causas[q] += 1

    n = len(casos)
    tudo_certo = n - len({e[0] for e in erros})
    print(f"Casos: {n} ({sum(c['origem'] == 'inventado' for c in casos)} inventados)")
    for q in ("pede_troca_bancaria", "tenta_instruir_agente", "tipo"):
        print(f"  {q:24} {acertos[q]:2}/{n} ({acertos[q] / n:.0%})")
    print(f"  e-mails 100% certos      {tudo_certo:2}/{n} ({tudo_certo / n:.0%})")
    print(f"  mandados para revisão    {revisar} (confiança < 0,7)")
    if erros:
        print("\nErros:")
        for id_, q, obtido, esperado, extra in erros:
            print(f"  {id_:8} {q:22} obteve {obtido!s:22} esperado {esperado!s:22} {extra}")
        print("Erros por pergunta: " + ", ".join(f"{k}={v}" for k, v in causas.most_common()))
    print(f"\n💲 jev · rodada US$ {custo:.7f} (leituras em cache não custam)")


if __name__ == "__main__":
    main()
