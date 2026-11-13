from src.graphs.algorithms import dijkstra
import math
import pytest

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
