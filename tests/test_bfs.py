# [IA] Claude – sugestão de casos de teste para BFS; resultados conferidos com a lógica do algoritmo
import math

from src.graphs.algorithms import bfs


def test_bfs_encontra_caminho_com_menor_numero_de_passos():
	grafo = {
		"S": [("A", 50), ("B", 1)],
		"A": [("T", 4), ("X", -10)],
		"B": [("C", 1), ("X", 0)],
		"C": [("T", 1)],
		"T": [],
		"X": [],
	}

	distancias, predecessores = bfs(grafo, "S")

	assert distancias == {
		"S": 0,
		"A": 1,
		"B": 1,
		"C": 2,
		"T": 2,
		"X": 2,
	}
	assert predecessores == {
		"S": None,
		"A": "S",
		"B": "S",
		"C": "B",
		"T": "A",
		"X": "A",
	}


def test_bfs_respeita_direcao_e_mantem_nos_inalcancaveis():
	grafo = {
		"S": [("A", 1)],
		"A": [],
		"VOLTA": [("S", 1)],
		"ISOLADO": [],
	}

	distancias, predecessores = bfs(grafo, "S")

	assert distancias == {
		"S": 0,
		"A": 1,
		"VOLTA": math.inf,
		"ISOLADO": math.inf,
	}
	assert predecessores["VOLTA"] is None
	assert predecessores["ISOLADO"] is None


def test_bfs_inclui_vizinho_sem_chave_explicita_no_grafo():
	grafo = {"S": [("ALVO", 1)]}

	distancias, predecessores = bfs(grafo, "S")

	assert distancias == {"S": 0, "ALVO": 1}
	assert predecessores == {"S": None, "ALVO": "S"}
