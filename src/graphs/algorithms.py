import math
from collections import deque
# imports do dikjstra abaixo (Brenda)
import heapq #fila de prioridade 
#heappush adiciona(mantem menor pronto pra sair), heappop remove e devolve o menor elemento
import math #math.inf valor infinito ou float("inf")
from itertools import count #itertools.count() quando há distâncias iguais, compara com o campo seguinte da tupla
from collections import defaultdict #dicionáro cria valor padrão ao acessar chave nova (opcional)

# Bellman-Ford (Vinícius)
def bellman_ford(grafo, origem):

    # Distancia de cada vértice da origem
    distancia = {}
    # Vértice que procede cada vértice no melhor caminho até agora
    proc = {}

    num_vertices = len(grafo)

    if origem not in grafo:
        raise ValueError('O vértice de origem não está no grafo')

    for vertice in grafo:

        proc[vertice] = None

        if vertice == origem:
            distancia[vertice] = 0
        else:
            distancia[vertice] = math.inf

    ciclo = None

    # Referência: grafo = {'S': [('E', 8), ('A', 10)]}

    # Execução do bellmna-ford em si
    for i in range (num_vertices - 1):

        vertice_atual = origem

        for vertice_atual in grafo:

            for vertice_destino, peso in grafo[vertice_atual]:

                # Se a distancia de S->S (0) + 8 < distancia de S->E (infinito) (VERDADEIRO)
                # Peso 8 mais leve que infinito
                if distancia[vertice_atual] + peso < distancia[vertice_destino]:
                    
                    distancia[vertice_destino] = distancia[vertice_atual] + peso
                    proc[vertice_destino] = vertice_atual

    # Verificação de ciclo negativo
    
    for vertice_atual in grafo:

        for vertice_destino, peso in grafo[vertice_atual]:

            # Se distancia de A->B + (-4) < distancia de A->C + (1)
            if distancia[vertice_atual] + peso < distancia[vertice_destino]:
                
                proc[vertice_destino] = vertice_atual

                atual = vertice_destino

                for i in range (num_vertices):
                    atual = proc[atual]

                ciclo = [atual]
                vertice_anterior = proc[atual]

                while vertice_anterior != atual:

                    ciclo.append(vertice_anterior)
                    vertice_anterior = proc[vertice_anterior]

                ciclo.append(atual) #  adiçãodo primeiro vértice pra fechar

                ciclo.reverse()

                return distancia, proc, ciclo

    return distancia, proc, ciclo

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
def dfs(grafo, origem, cobrir_todos=False):
    d, f, p = {}, {}, {}
    classif = {}
    tempo = 0

    def explora(raiz):
        nonlocal tempo
        tempo += 1
        d[raiz] = tempo
        p[raiz] = None
        pilha = [[raiz, 0]]

        while pilha:
            topo = pilha[-1]
            u, i = topo
            vizinhos = grafo.get(u, [])

            if i < len(vizinhos):
                topo[1] += 1
                v = vizinhos[i][0]

                if v not in d:
                    classif[(u, v)] = "arvore"
                    tempo += 1
                    d[v] = tempo
                    p[v] = u
                    pilha.append([v, 0])
                elif v not in f:
                    classif[(u, v)] = "retorno"
                elif d[u] < d[v]:
                    classif[(u, v)] = "avanco"
                else:
                    classif[(u, v)] = "cruzamento"
            else:
                tempo += 1
                f[u] = tempo
                pilha.pop()

    explora(origem)
    if cobrir_todos:
        for v in grafo:
            if v not in d:
                explora(v)

    tem_ciclo = "retorno" in classif.values()
    return d, f, p, classif, tem_ciclo

# Dijkstra (Brenda)
def dijkstra(grafo, origem):
    nos = set()
    dist = {}
    proc = {}

    for no, vizinhos in grafo.items():
        nos.add(no)
        for vizinho, peso in vizinhos:
            if peso < 0:
                raise ValueError("Dijkstra não funciona para pesos negativos")
            nos.add(vizinho)

    if origem not in nos:
        raise ValueError("Origem fora do grafo")

    for no in nos:
        dist[no] = math.inf 
        proc[no] = None 
    dist[origem] = 0 

    desempate = count() 
    fila_prioridade = [] 
    heapq.heappush(fila_prioridade, (dist[origem], next(desempate), origem))

    while fila_prioridade:
        distancia_atual, _, no_atual = heapq.heappop(fila_prioridade) 

        if distancia_atual > dist[no_atual]:
            continue

        for vizinho, peso in grafo.get(no_atual, []):
            nova_distancia = dist[no_atual] + peso
            if nova_distancia < dist[vizinho]: 
                dist[vizinho] = nova_distancia 
                proc[vizinho] = no_atual 
                heapq.heappush(fila_prioridade, (nova_distancia, next(desempate), vizinho)) 

    return dist, proc

# função de reconstrução de caminho que pode ser utilizada para dikjstra e bellman-ford (Brenda)
def reconstruir_caminho(dist, proc, destino):
    if dist[destino] == math.inf:
        return "sem caminho"

    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = proc[atual]

    caminho.reverse()
    return caminho

