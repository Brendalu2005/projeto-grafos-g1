from src.graphs.algorithms import dijkstra
import math
import pytest

# [IA] ChatGPT – sugestão de testes para algoritmo de dijkstra
@pytest.fixture
# parte 1
def grafo():
    return {
        "A": [("B", 4), ("C", 1)],
        "C": [("B", 2)],
        "B": [("D", 1)],
    }

def test_distancias_do_exemplo(grafo):
    dist, proc = dijkstra(grafo, "A")
    assert dist == {"A": 0, "B": 3, "C": 1, "D": 4}
    assert proc == {"A": None, "B": "C", "C": "A", "D": "B"}

def test_peso_negativo_levanta_erro():
    with pytest.raises(ValueError):
        dijkstra({"A": [("B", -1)]}, "A")

def test_origem_inexistente_levanta_erro(grafo):
    with pytest.raises(ValueError):
        dijkstra(grafo, "Z")

def test_grafo_vazio_levanta_erro():
    with pytest.raises(ValueError):
        dijkstra({}, "A")

def test_no_inalcancavel_fica_infinito(grafo):
    dist, _ = dijkstra(grafo, "C")
    assert dist["A"] == math.inf


# [IA] ChatGPT (Codex) – sugestão de teste de revisão com arestas de peso zero
def test_arestas_de_peso_zero():
    grafo = {
        "S": [("A", 0), ("B", 5)],
        "A": [("B", 0)],
        "B": [("T", 2)],
        "T": [],
    }

    dist, proc = dijkstra(grafo, "S")

    assert dist == {"S": 0, "A": 0, "B": 0, "T": 2}
    assert proc == {"S": None, "A": "S", "B": "A", "T": "B"}


# [IA] ChatGPT (Codex) – sugestão de teste de revisão com peso negativo inalcançável
def test_peso_negativo_inalcancavel_levanta_erro():
    grafo = {
        "S": [("A", 1)],
        "A": [],
        "X": [("Y", -1)],
        "Y": [],
    }

    with pytest.raises(ValueError, match="negativ"):
        dijkstra(grafo, "S")
