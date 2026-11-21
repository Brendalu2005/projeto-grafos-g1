# [IA] ChatGPT (Codex) – testes das convenções de métricas aprovadas pela equipe.
from copy import deepcopy

import pytest

from src.graphs.metricas_dataset import calcular_metricas_dataset


def test_metricas_do_exemplo_com_paralelos_laco_e_peso_negativo():
    grafo = {
        "A": [("B", -1), ("B", 1), ("A", 0)],
        "B": [],
        "C": [("B", 2)],
    }
    original = deepcopy(grafo)

    resultado = calcular_metricas_dataset(grafo)

    assert resultado == {
        "vertices": 3,
        "arcos": 4,
        "lacos": 1,
        "pares_distintos": 3,
        "pares_distintos_sem_laco": 2,
        "densidade_pares_sem_laco": pytest.approx(1 / 3),
        "graus_entrada": {"A": 1, "B": 3, "C": 0},
        "graus_saida": {"A": 3, "B": 0, "C": 1},
        "resumo_entrada": {"minimo": 0, "maximo": 3, "media": pytest.approx(4 / 3)},
        "resumo_saida": {"minimo": 0, "maximo": 3, "media": pytest.approx(4 / 3)},
        "distribuicao_entrada": {0: 1, 1: 1, 3: 1},
        "distribuicao_saida": {0: 1, 1: 1, 3: 1},
        "vizinhos_distintos_entrada": {"A": 1, "B": 2, "C": 0},
        "vizinhos_distintos_saida": {"A": 2, "B": 0, "C": 1},
        "percentual_peso_negativo": 25,
    }
    assert sum(resultado["graus_entrada"].values()) == resultado["arcos"]
    assert sum(resultado["graus_saida"].values()) == resultado["arcos"]
    assert grafo == original


def test_metricas_do_grafo_vazio():
    assert calcular_metricas_dataset({}) == {
        "vertices": 0,
        "arcos": 0,
        "lacos": 0,
        "pares_distintos": 0,
        "pares_distintos_sem_laco": 0,
        "densidade_pares_sem_laco": 0,
        "graus_entrada": {},
        "graus_saida": {},
        "resumo_entrada": {"minimo": None, "maximo": None, "media": 0},
        "resumo_saida": {"minimo": None, "maximo": None, "media": 0},
        "distribuicao_entrada": {},
        "distribuicao_saida": {},
        "vizinhos_distintos_entrada": {},
        "vizinhos_distintos_saida": {},
        "percentual_peso_negativo": None,
    }
