def adicionar_vertice(grafo, v):
    if v not in grafo:
        grafo[v] = []


def adicionar_arco(grafo, origem, destino, peso):
    adicionar_vertice(grafo, origem)
    adicionar_vertice(grafo, destino)
    grafo[origem].append((destino, peso))


def arcos(grafo):
    lista = []
    for origem in grafo:
        for destino, peso in grafo[origem]:
            lista.append((origem, destino, peso))
    return lista