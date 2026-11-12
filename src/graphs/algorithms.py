import math
from collections import deque

# Bellman-Ford (Vinícius)
def belman_ford(grafo, origem):

    distancia = {}

    for vertice in grafo:
        if (vertice.value == origem):
            distancia[vertice.value] == 0
        else:
            distancia[vertice.value] = math.inf

    num_vertices = 6 # ex 

    for i in range (num_vertices - 1):
        #ex
        vertice_inicial = origem

# BFS (Clarissa Lopes)
def bfs(grafo, origem):
    distancias = {vertice: math.inf for vertice in grafo}
    predecessores = {vertice: None for vertice in grafo}

    for vizinhos in grafo.values():
        for vizinho, _ in vizinhos:
            distancias.setdefault(vizinho, math.inf)
            predecessores.setdefault(vizinho, None)

    distancias.setdefault(origem, math.inf)
    predecessores.setdefault(origem, None)
    distancias[origem] = 0
    fila = deque([origem])

    while fila:
        atual = fila.popleft()

        for vizinho, _ in grafo.get(atual, []):
            if distancias[vizinho] == math.inf:
                distancias[vizinho] = distancias[atual] + 1
                predecessores[vizinho] = atual
                fila.append(vizinho)

    return distancias, predecessores

#DFS (André Avelino)
def dfs(grafo):
    d, f, p = {}, {}, {}
    arestas = {"arvore": [], "retorno": [], "avanco": [], "cruzamento": []}
    tempo = 0

    def visita(u):
        nonlocal tempo
        tempo += 1
        d[u] = tempo

        for v, _ in grafo[u]:
            if v not in d:
                p[v] = u
                arestas["arvore"].append((u, v))
                visita(v)
            elif v not in f: 
                arestas["retorno"].append((u, v))
            elif d[u] < d[v]:
                arestas["avanco"].append((u, v))
            else:  
                arestas["cruzamento"].append((u, v))

        tempo += 1
        f[u] = tempo
    for v in grafo:
        if v not in d:
            p[v] = None
            visita(v)

    return d, f, p, arestas, len(arestas["retorno"]) > 0