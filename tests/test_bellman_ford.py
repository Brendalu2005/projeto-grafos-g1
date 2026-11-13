# [IA] Claude – sugestão dos casos de teste; valores esperados calculados à mão
import math

from src.graphs.algorithms import bellman_ford


def peso(grafo, u, v):
    for vizinho, p in grafo[u]:
        if vizinho == v:
            return p
    raise AssertionError(f"{u} -> {v} não é aresta do grafo")


def test_pesos_negativos_sem_ciclo():
    grafo = {
        "S": [("E", 8), ("A", 10)],
        "A": [("C", 2)],
        "B": [("A", 1)],
        "C": [("B", -2)],
        "D": [("A", -4), ("C", -1)],
        "E": [("D", 1)],
    }
    dist, pred, ciclo = bellman_ford(grafo, "S")

    assert ciclo is None
    assert dist == {"S": ..., "A": ..., "B": ..., "C": ..., "D": ..., "E": ...}
    assert pred["A"] == ...


def test_ciclo_negativo_detectado():
    grafo = {
        "S": [("A", 1)],
        "A": [("B", 1)],
        "B": [("C", -3)],
        "C": [("A", 1), ("D", 2)],
        "D": [],
    }
    dist, pred, ciclo = bellman_ford(grafo, "S")

    assert ciclo is not None
    assert ciclo[0] == ciclo[-1]
    # D é alcançável a partir do ciclo, mas não faz parte dele
    assert set(ciclo) == {"A", "B", "C"}
    custo = sum(peso(grafo, u, v) for u, v in zip(ciclo, ciclo[1:]))
    assert custo == ...