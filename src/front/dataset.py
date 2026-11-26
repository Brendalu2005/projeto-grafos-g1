"""Dados da visualização; reutiliza os algoritmos existentes, sem gravar resultados."""

# [IA] ChatGPT (Codex) – recorte visual e integração HTTP da Parte 2.
from collections import Counter
from functools import lru_cache
from pathlib import Path
from random import Random

from src.graphs.algorithms import dijkstra
from src.graphs.io import carregar_dataset
from src.solve import (CASOS_BELLMAN, FONTES_DATASET, PARES_DATASET,
                       resultado_bellman_dataset, resultado_busca_dataset,
                       resultado_par_dataset, transformar_pesos_dataset)

CSV = Path(__file__).resolve().parents[2] / "data/dataset_parte2/processed/wikiRfA_tratado.csv"


@lru_cache(maxsize=1)
def carregar(caminho, modificacao, tamanho):
    # A chave inclui a assinatura do arquivo: um CSV atualizado invalida o cache.
    return carregar_dataset(caminho)


def grafo_completo():
    info = CSV.stat()
    return carregar(str(CSV), info.st_mtime_ns, info.st_size)


def recortar(grafo, limite_vertices=500, limite_arcos=20000):
    graus = Counter({u: len(vizinhos) for u, vizinhos in grafo.items()})
    for vizinhos in grafo.values():
        for destino, _ in vizinhos:
            graus[destino] += 1
    obrigatorios = set(FONTES_DATASET)
    for origem, destino in PARES_DATASET:
        obrigatorios.update((origem, destino))
    for caso in CASOS_BELLMAN.values():
        obrigatorios.update(caso["usuarios"])
    usuarios = obrigatorios.intersection(grafo)
    for usuario in sorted(grafo, key=lambda u: (-graus[u], u)):
        if len(usuarios) >= limite_vertices:
            break
        usuarios.add(usuario)
    # O índice da adjacência identifica cada ocorrência, inclusive paralelos.
    arcos = [(u, v, peso, indice) for u in sorted(usuarios)
             for indice, (v, peso) in enumerate(grafo[u]) if v in usuarios]
    if len(arcos) > limite_arcos:
        arcos = Random(42).sample(arcos, limite_arcos)
    return {
        "nos": [{"id": u, "grau": graus[u]} for u in sorted(usuarios)],
        "arcos": arcos,
        "vertices_total": len(grafo),
        "arcos_total": sum(map(len, grafo.values())),
        "semente": 42,
        "regra": "Até 500 usuários: fontes e pares dos testes, mais os maiores graus totais; "
                 "até 20.000 ocorrências entre eles, amostradas com semente 42. "
                 "O recorte privilegia usuários conectados e não representa toda a rede.",
    }


def conexoes(usuario):
    """Todas as ocorrências incidentes, inclusive as que não estão no recorte."""
    grafo = grafo_completo()
    if usuario not in grafo:
        raise ValueError("Usuário não encontrado no dataset.")
    arcos = [(u, v, peso, i) for u, vizinhos in grafo.items()
             for i, (v, peso) in enumerate(vizinhos) if u == usuario or v == usuario]
    entradas = sum(v == usuario for u, v, peso, i in arcos)
    saidas = sum(u == usuario for u, v, peso, i in arcos)
    vizinhos = sorted({v if u == usuario else u for u, v, peso, i in arcos})
    return {"usuario": usuario, "vizinhos": vizinhos, "arcos": arcos,
            "entradas": entradas, "saidas": saidas,
            "lacos": sum(u == v for u, v, peso, i in arcos)}


def arcos_caminho(grafo, caminho):
    # O predecessor do Dijkstra identifica o nó, não a ocorrência paralela.
    # Entre os dois nós, o menor PESO corresponde ao custo do caminho retornado.
    return [[u, v, min(p for destino, p in grafo[u] if destino == v)]
            for u, v in zip(caminho, caminho[1:])]


def executar(algoritmo):
    if algoritmo not in ("BFS", "DFS", "DIJKSTRA", "BELLMAN_FORD"):
        raise ValueError("Algoritmo desconhecido.")
    grafo = grafo_completo()
    visiveis = {n["id"] for n in recortar(grafo)["nos"]}
    casos = []
    if algoritmo in ("BFS", "DFS"):
        for fonte in FONTES_DATASET:
            resultado = resultado_busca_dataset(grafo, fonte, algoritmo)
            visitados = (set(u for u, d in resultado["distancias"].items() if d is not None)
                         if algoritmo == "BFS" else set(resultado["ordem_descoberta"]))
            arcos = [[u, v, next(p for destino, p in grafo[u] if destino == v)]
                     for v, u in resultado["predecessores"].items()
                     if u in visiveis and v in visiveis]
            resumo = {"outros_usuarios_alcancados": resultado["outros_usuarios_alcancados"]}
            if algoritmo == "BFS":
                resumo["maior_distancia_em_arcos"] = resultado["maior_distancia_finita"]
            else:
                resumo["classificacao_arcos"] = resultado["classificacao_arcos"]
                resumo["tem_ciclo"] = resultado["tem_ciclo"]
            casos.append({"titulo": fonte, "fonte": fonte, "nos": sorted(visitados & visiveis),
                          "arcos": arcos, "resumo": resumo})
            if algoritmo == "BFS":
                casos[-1]["resultado_bfs"] = resultado
        nota = "Busca no grafo completo, em três fontes. Pesos ignorados. " \
               "Destacam-se os usuários alcançados e os arcos da árvore com ambos os extremos no recorte."
    elif algoritmo == "DIJKSTRA":
        transformado = transformar_pesos_dataset(grafo, 1)
        buscas = {}
        for origem, destino in PARES_DATASET:
            if origem not in buscas:
                buscas[origem] = dijkstra(transformado, origem)
            resultado = resultado_par_dataset(*buscas[origem], origem, destino)
            casos.append({"titulo": f"{origem} → {destino}", "fonte": origem,
                          "nos": resultado["caminho"],
                          "arcos": arcos_caminho(grafo, resultado["caminho"]),
                          "resumo": resultado})
        nota = "Cinco pares no grafo completo. Novo peso = PESO + 1 (mínimo original −1, " \
               "transformado 0). O PESO original é preservado. Cada arco acrescenta 1 ao custo; " \
               "isso pode mudar a preferência entre caminhos de comprimentos diferentes."
    else:
        for nome in CASOS_BELLMAN:
            resultado = resultado_bellman_dataset(str(CSV), nome)
            resumo = {k: resultado[k] for k in ("status", "tem_ciclo_negativo")}
            if resultado["tem_ciclo_negativo"]:
                resumo.update(ciclo=resultado["ciclo"], custo_ciclo=resultado["custo_ciclo"])
            else:
                resumo["distancias_em_PESO"] = resultado["distancias"]
            casos.append({"titulo": nome.replace("_", " "), "fonte": resultado["fonte"],
                          "nos": resultado["usuarios"],
                          "arcos": [[a["origem"], a["destino"], a["PESO"]] for a in resultado["arcos"]],
                          "resumo": resumo})
        nota = "Dois subgrafos induzidos pelos usuários dos casos já definidos no projeto, " \
               "com arcos reais e PESO original: negativo sem ciclo e ciclo negativo. " \
               "Com ciclo negativo alcançável, não há custo mínimo finito. Não é execução no grafo completo."
    return {"algoritmo": algoritmo, "nota": nota, "casos": casos}
