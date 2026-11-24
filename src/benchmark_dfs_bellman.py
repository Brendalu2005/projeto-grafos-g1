"""Mede DFS e Bellman-Ford pelo procedimento comum da Parte 2.

Execute na raiz: python -m src.benchmark_dfs_bellman
"""

# [IA] ChatGPT (Codex) – integração das medições solicitadas por André;
# usa os algoritmos existentes, sem modificar sua implementação.
import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

# [IA] ChatGPT (Codex) – reutiliza a mesma coleta de ambiente do executor BFS/Dijkstra.
from src.benchmark import ambiente_atual, criar_recortes, medir_algoritmo, selecionar_fontes
from src.graphs.algorithms import bellman_ford, bfs, dfs
from src.graphs.io import carregar_dataset


# [IA] ChatGPT (Codex) – complemento sem repetir configurações nem sobrescrever a base. !andre!
def executar_benchmark(caminho_csv, caminho_saida, fontes_bellman_completo=1, complementar_de=None):
    if complementar_de is not None:
        fontes_bellman_completo = 3
    if fontes_bellman_completo not in (1, 3):
        raise ValueError("Use uma ou três fontes de Bellman-Ford no grafo completo.")
    caminho_csv = Path(caminho_csv)
    caminho_saida = Path(caminho_saida)
    if caminho_saida.exists():
        raise ValueError(f"A saída já existe: {caminho_saida}. Use outro caminho em --out.")
    grafo = carregar_dataset(caminho_csv)
    recortes = criar_recortes(grafo, semente=42)
    fontes = selecionar_fontes(recortes)
    relatorio = {
        "arquivo_entrada": caminho_csv.as_posix(),
        "sha256_entrada": hashlib.sha256(caminho_csv.read_bytes()).hexdigest(),
        "ambiente": ambiente_atual(),
        "inicio_utc": datetime.now(timezone.utc).isoformat(),
        "semente": 42,
        "regra_recorte": "prefixos de 10%, 50% e 100% das ocorrências embaralhadas uma vez; PESO preservado",
        "regra_fontes": "no recorte de 10%, grau de saída >= 3; ordem por grau decrescente e nome crescente; posições 0, n // 4, n // 2",
        "fontes": fontes,
        "alcance_inclui_fonte": False,
        "intervalo_medido": "somente a chamada do algoritmo; busca completa por fonte",
        "fontes_bellman_por_percentual": {
            "10": fontes, "50": fontes, "100": fontes[:fontes_bellman_completo],
        },
        "configuracoes_esperadas": 15 + fontes_bellman_completo,
        "completo": False,
        "medicoes": [],
    }
    if complementar_de is not None:
        base = Path(complementar_de)
        anterior = json.loads(base.read_text(encoding="utf-8"))
        for campo in ("sha256_entrada", "ambiente", "semente", "fontes", "regra_recorte", "regra_fontes"):
            if anterior[campo] != relatorio[campo]:
                raise ValueError(f"A base difere da execução atual: {campo}.")
        esperadas = {(a, p, f) for a in ("DFS", "BELLMAN_FORD")
                     for p in (10, 50, 100) for f in fontes}
        chaves = [(m["algoritmo"], m["percentual"], m["fonte"]) for m in anterior["medicoes"]]
        faltantes = esperadas - set(chaves)
        if len(chaves) != len(set(chaves)) or set(chaves) - esperadas:
            raise ValueError("Configurações duplicadas ou inesperadas na base.")
        if not faltantes or any(a != "BELLMAN_FORD" or p != 100 for a, p, _ in faltantes):
            raise ValueError("A base deve ter somente Bellman-Ford em 100% pendente.")
        relatorio["medicoes"] = anterior["medicoes"]
        relatorio["complementacao"] = {
            "arquivo_base": base.as_posix(),
            "sha256_base": hashlib.sha256(base.read_bytes()).hexdigest(),
            "inicio_base_utc": anterior["inicio_utc"],
            "fim_base_utc": anterior.get("fim_utc"),
            "regra": "preservar medições anteriores e completar somente Bellman-Ford em 100%",
        }
    concluidas = {(m["algoritmo"], m["percentual"], m["fonte"]) for m in relatorio["medicoes"]}
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    for nome, algoritmo in (("DFS", dfs), ("BELLMAN_FORD", bellman_ford)):
        for recorte in recortes:
            grafo_recorte = recorte["grafo"]
            fontes_medicao = fontes
            if nome == "BELLMAN_FORD" and recorte["percentual"] == 100:
                fontes_medicao = fontes[:fontes_bellman_completo]
            for fonte in fontes_medicao:
                if (nome, recorte["percentual"], fonte) in concluidas:
                    continue
                # Preparação e alcance ficam fora do intervalo medido.
                distancias, _ = bfs(grafo_recorte, fonte)
                alcance = sum(v != fonte and d != math.inf for v, d in distancias.items())
                print(f"Iniciando {nome} | {recorte['percentual']}% | {fonte}", flush=True)
                medicao = medir_algoritmo(algoritmo, grafo_recorte, fonte, repeticoes=5)
                medicao.update({
                    "algoritmo": nome, "tarefa": "busca_completa_por_fonte",
                    "fonte": fonte, "percentual": recorte["percentual"],
                    "vertices": recorte["vertices"], "arcos": recorte["arcos"],
                    "grau_saida_fonte": len(grafo_recorte[fonte]),
                    "outros_usuarios_alcancados": alcance,
                    "versao_pesos": "PESO", "deslocamento": 0, "semente": 42,
                })
                relatorio["medicoes"].append(medicao)
                relatorio["completo"] = len(relatorio["medicoes"]) == relatorio["configuracoes_esperadas"]
                if relatorio["completo"]:
                    relatorio["fim_utc"] = datetime.now(timezone.utc).isoformat()
                caminho_saida.write_text(
                    json.dumps(relatorio, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8"
                )
                print(f"Concluído {nome} | {recorte['percentual']}% | {fonte} | média {medicao['media']:.6f} s", flush=True)
    return relatorio


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default="data/dataset_parte2/processed/wikiRfA_tratado.csv")
    parser.add_argument("--out", default="out/parte2/benchmark_dfs_bellman.json")
    parser.add_argument("--fontes-bellman-completo", type=int, choices=[1, 3], default=1,
                        help="quantidade de fontes de Bellman-Ford em 100%%; padrão 1")
    # [IA] ChatGPT (Codex) – opção para concluir as duas fontes restantes. !andre!
    parser.add_argument("--complementar", metavar="JSON_BASE",
                        help="preservar a base e completar somente Bellman-Ford em 100%%")
    args = parser.parse_args()
    executar_benchmark(args.dataset, args.out, args.fontes_bellman_completo, args.complementar)


if __name__ == "__main__":
    main()
