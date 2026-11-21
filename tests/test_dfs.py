# [IA] Claude – sugestão de casos de teste do DFS e adaptação ao retorno (d, f, p, classif, tem_ciclo); resultados esperados conferidos à mão pelo grupo
from src.graphs.algorithms import dfs


# [IA] Claude – sugestão de caso de teste (quatro tipos de arco)
def test_dfs_quatro_tipos_de_arco():
    g = {
        "A": [("B", 1), ("D", 1), ("F", 1)],
        "B": [("C", 1)],
        "C": [("A", 1), ("D", 1)],
        "D": [],
        "F": [("D", 1)],
        "E": [("D", 1)],  # inalcançável a partir de A
    }
    d, f, p, classif, tem_ciclo = dfs(g, "A")

    # [IA] ChatGPT (Codex) – adaptação das consultas à identidade individual de cada arco.
    assert classif[("A", "B", 0)] == "arvore"
    assert classif[("B", "C", 0)] == "arvore"
    assert classif[("C", "D", 1)] == "arvore"
    assert classif[("A", "F", 2)] == "arvore"
    assert classif[("C", "A", 0)] == "retorno"
    assert classif[("A", "D", 1)] == "avanco"
    assert classif[("F", "D", 0)] == "cruzamento"
    assert ("E", "D", 0) not in classif  # E nunca é visitado
    assert "E" not in d
    assert tem_ciclo is True


# [IA] Claude – sugestão de caso de teste (cadeia longa, sem RecursionError)
def test_dfs_cadeia_longa_com_retorno():
    n = 20000  # maior que o limite de recursão padrão do Python (1000)
    g = {i: [(i + 1, 1)] for i in range(n - 1)}
    g[n - 1] = [(0, 1)]  # fecha o ciclo
    d, f, p, classif, tem_ciclo = dfs(g, 0)

    # [IA] ChatGPT (Codex) – adaptação à chave com índice do arco na adjacência.
    assert classif[(n - 1, 0, 0)] == "retorno"
    assert sum(1 for t in classif.values() if t == "arvore") == n - 1
    assert tem_ciclo is True


# [IA] ChatGPT (Codex) – sugestão de teste com arcos paralelos de pesos diferentes
def test_dfs_preserva_classificacao_de_arcos_paralelos():
    grafo = {
        "A": [("B", 1), ("B", 2)],
        "B": [],
    }

    _, _, _, classif, tem_ciclo = dfs(grafo, "A")
    tipos = list(classif.values())

    assert len(tipos) == 2
    assert tipos.count("arvore") == 1
    assert tipos.count("avanco") == 1
    # [IA] ChatGPT (Codex) – confere qual ocorrência recebe cada classificação.
    assert classif == {("A", "B", 0): "arvore", ("A", "B", 1): "avanco"}
    assert tem_ciclo is False


# [IA] ChatGPT (Codex) – sugestão de teste com laços paralelos de mesmo peso
def test_dfs_preserva_lacos_paralelos_de_mesmo_peso():
    grafo = {
        "A": [("A", 1), ("A", 1), ("B", 1)],
        "B": [],
    }

    _, _, _, classif, tem_ciclo = dfs(grafo, "A")
    tipos = list(classif.values())

    assert len(tipos) == 3
    assert tipos.count("retorno") == 2
    assert tipos.count("arvore") == 1
    # [IA] ChatGPT (Codex) – confere identidades distintas para laços de mesmo peso.
    assert classif == {
        ("A", "A", 0): "retorno",
        ("A", "A", 1): "retorno",
        ("A", "B", 2): "arvore",
    }
    assert tem_ciclo is True
