# [IA] Claude – sugestão de casos de teste (resultados esperados conferidos à mão pelo grupo)
from src.graphs.algorithms import dfs


def test_dfs_quatro_tipos_de_arco():
    g = {
        "A": [("B", 1), ("D", 1), ("F", 1)],
        "B": [("C", 1)],
        "C": [("A", 1), ("D", 1)],
        "D": [],
        "F": [("D", 1)],
        "E": [("D", 1)],  # inalcançável a partir de A
    }
    classif, tem_ciclo = dfs(g, "A")  # adaptar ao retorno real

    assert classif[("A", "B")] == "arvore"
    assert classif[("B", "C")] == "arvore"
    assert classif[("C", "D")] == "arvore"
    assert classif[("A", "F")] == "arvore"
    assert classif[("C", "A")] == "retorno"
    assert classif[("A", "D")] == "avanco"
    assert classif[("F", "D")] == "cruzamento"
    assert ("E", "D") not in classif  # E nunca é visitado
    assert tem_ciclo is True


def test_dfs_cadeia_longa_com_retorno():
    n = 20000  # maior que o limite de recursão padrão do Python (1000)
    g = {i: [(i + 1, 1)] for i in range(n - 1)}
    g[n - 1] = [(0, 1)]  # fecha o ciclo
    classif, tem_ciclo = dfs(g, 0)  # adaptar ao retorno real

    assert classif[(n - 1, 0)] == "retorno"
    assert sum(1 for t in classif.values() if t == "arvore") == n - 1
    assert tem_ciclo is True